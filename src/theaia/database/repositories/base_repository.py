"""
Base Repository Pattern para THEA IA
Proporciona CRUD genérico con multi-tenant support

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer
"""

from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from src.theaia.database.models.base import BaseModel

# Type variable para el modelo genérico
ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Repository base genérico con CRUD operations.
    
    Todos los repositories heredan de esta clase para operaciones comunes.
    Implementa automáticamente:
    - Multi-tenant isolation (tenant_id)
    - CRUD operations (create, read, update, delete)
    - Pagination (skip, limit)
    - Filtering básico
    
    Example:
        class UserRepository(BaseRepository[User]):
            def __init__(self, session: AsyncSession):
                super().__init__(User, session)
    """
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
        Inicializa el repository.
        
        Args:
            model: Modelo SQLAlchemy (User, Event, etc.)
            session: AsyncSession de SQLAlchemy
        """
        self.model = model
        self.session = session
    
    async def create(self, **kwargs) -> ModelType:
        """
        Crea una nueva entidad en la base de datos.
        
        Args:
            **kwargs: Campos del modelo (debe incluir tenant_id)
        
        Returns:
            Entidad creada con id asignado
        
        Raises:
            ValueError: Si falta tenant_id
        
        Example:
            user = await user_repo.create(
                tenant_id="default",
                telegram_id=123456,
                username="test_user"
            )
        """
        if 'tenant_id' not in kwargs:
            raise ValueError(f"{self.model.__name__} requires tenant_id")
        
        entity = self.model(**kwargs)
        self.session.add(entity)
        await self.session.flush()  # Asigna ID sin commit
        await self.session.refresh(entity)  # Carga relaciones
        return entity
    
    async def get_by_id(
        self, 
        entity_id: int, 
        tenant_id: str
    ) -> Optional[ModelType]:
        """
        Obtiene una entidad por ID con tenant isolation.
        
        Args:
            entity_id: ID de la entidad
            tenant_id: ID del tenant (multi-tenant)
        
        Returns:
            Entidad encontrada o None
        
        Example:
            user = await user_repo.get_by_id(1, "default")
        """
        stmt = select(self.model).where(
            self.model.id == entity_id,
            self.model.tenant_id == tenant_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Obtiene todas las entidades con paginación y filtros.
        
        Args:
            tenant_id: ID del tenant
            skip: Número de registros a saltar (pagination)
            limit: Máximo de registros a retornar
            filters: Filtros adicionales {campo: valor}
        
        Returns:
            Lista de entidades
        
        Example:
            users = await user_repo.get_all(
                tenant_id="default",
                skip=0,
                limit=10,
                filters={"is_active": True}
            )
        """
        stmt = select(self.model).where(self.model.tenant_id == tenant_id)
        
        # Aplicar filtros adicionales
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def update(
        self, 
        entity_id: int, 
        tenant_id: str, 
        **kwargs
    ) -> Optional[ModelType]:
        """
        Actualiza una entidad existente.
        
        Args:
            entity_id: ID de la entidad
            tenant_id: ID del tenant
            **kwargs: Campos a actualizar
        
        Returns:
            Entidad actualizada o None si no existe
        
        Example:
            updated_user = await user_repo.update(
                entity_id=1,
                tenant_id="default",
                username="new_username"
            )
        """
        entity = await self.get_by_id(entity_id, tenant_id)
        if not entity:
            return None
        
        for field, value in kwargs.items():
            if hasattr(entity, field):
                setattr(entity, field, value)
        
        await self.session.flush()
        await self.session.refresh(entity)
        return entity
    
    async def delete(self, entity_id: int, tenant_id: str) -> bool:
        """
        Elimina una entidad (hard delete).
        
        Args:
            entity_id: ID de la entidad
            tenant_id: ID del tenant
        
        Returns:
            True si se eliminó, False si no existía
        
        Example:
            deleted = await user_repo.delete(1, "default")
        """
        stmt = delete(self.model).where(
            self.model.id == entity_id,
            self.model.tenant_id == tenant_id
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0
    
    async def count(
        self, 
        tenant_id: str, 
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Cuenta entidades con filtros opcionales.
        
        Args:
            tenant_id: ID del tenant
            filters: Filtros adicionales {campo: valor}
        
        Returns:
            Número de entidades que cumplen los filtros
        
        Example:
            active_users = await user_repo.count(
                tenant_id="default",
                filters={"is_active": True}
            )
        """
        stmt = select(func.count()).select_from(self.model).where(
            self.model.tenant_id == tenant_id
        )
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
        
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def exists(self, entity_id: int, tenant_id: str) -> bool:
        """
        Verifica si una entidad existe.
        
        Args:
            entity_id: ID de la entidad
            tenant_id: ID del tenant
        
        Returns:
            True si existe, False si no
        
        Example:
            if await user_repo.exists(1, "default"):
                print("User exists")
        """
        entity = await self.get_by_id(entity_id, tenant_id)
        return entity is not None
