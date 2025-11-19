"""
Base Repository Pattern para THEA IA
Proporciona CRUD genérico con multi-tenant support

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025 | Actualizado: 19 Nov 2025 (FASE 8)
Hito: H02 - Database Layer + Advanced Persistence
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
    Repository base genérico con CRUD operations y multi-tenant isolation.
    
    Todos los repositories heredan de esta clase para operaciones comunes.
    Implementa automáticamente:
    - Multi-tenant isolation (tenant_id obligatorio en casi todos los métodos)
    - CRUD operations (create, read, update, delete)
    - Pagination (skip, limit)
    - Filtering básico (dict-based filters)
    - Count y exists utilities
    
    Generic Type:
        ModelType: Tipo del modelo SQLAlchemy (User, Event, Note, etc.)
    
    Multi-tenant Strategy:
        - tenant_id es OBLIGATORIO en create()
        - tenant_id filtra automáticamente en get_by_id(), get_all(), etc.
        - Un mismo ID puede existir en múltiples tenants
    
    Example:
        class UserRepository(BaseRepository[User]):
            def __init__(self, session: AsyncSession):
                super().__init__(User, session)
        
        # Uso
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            user = await user_repo.create(
                tenant_id="default",
                telegram_id=123456
            )
    """
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
        Inicializa el repository con modelo y sesión.
        
        Args:
            model: Clase del modelo SQLAlchemy (ej: User, Event)
            session: AsyncSession activa de SQLAlchemy
        
        Note:
            La sesión debe ser gestionada externamente (context manager).
            El repository NO hace commit/rollback.
        """
        self.model = model
        self.session = session
    
    async def create(self, **kwargs) -> ModelType:
        """
        Crea una nueva entidad en la base de datos.
        
        Args:
            **kwargs: Campos del modelo (tenant_id es OBLIGATORIO)
        
        Returns:
            Entidad creada con ID asignado y relaciones cargadas
        
        Raises:
            ValueError: Si falta tenant_id en kwargs
            SQLAlchemyError: Si hay error de base de datos
        
        Note:
            - Hace flush() pero NO commit()
            - Asigna ID automáticamente
            - Carga relaciones con refresh()
        
        Example:
            user = await user_repo.create(
                tenant_id="default",
                telegram_id=123456,
                username="john_doe"
            )
            print(f"Usuario creado con ID: {user.id}")
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
        tenant_id: Optional[str] = None
    ) -> Optional[ModelType]:
        """
        Obtiene una entidad por ID con tenant isolation opcional.
        
        Args:
            entity_id: ID interno de la entidad
            tenant_id: ID del tenant (opcional para compatibilidad tests)
        
        Returns:
            Entidad encontrada o None si no existe
        
        Note:
            Si tenant_id no se proporciona, se obtiene sin filtro de tenant.
            Esto es útil para métodos internos como update_last_activity().
            En producción, SIEMPRE pasar tenant_id explícitamente.
        
        Security Warning:
            No pasar tenant_id puede causar data leaks en multi-tenant.
            Solo usar sin tenant_id en métodos internos seguros.
        
        Example:
            # Con tenant_id (RECOMENDADO en producción)
            user = await user_repo.get_by_id(1, "default")
            
            # Sin tenant_id (solo para métodos internos)
            user = await user_repo.get_by_id(1)
        """
        if tenant_id:
            stmt = select(self.model).where(
                self.model.id == entity_id,
                self.model.tenant_id == tenant_id
            )
        else:
            # Sin filtro tenant (usar con precaución)
            stmt = select(self.model).where(
                self.model.id == entity_id
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
        Obtiene entidades con paginación, filtros y tenant isolation.
        
        Args:
            tenant_id: ID del tenant (OBLIGATORIO)
            skip: Número de registros a saltar (offset)
            limit: Máximo de registros a retornar (default 100)
            filters: Filtros adicionales como dict {campo: valor}
        
        Returns:
            Lista de entidades que cumplen los filtros
        
        Note:
            Los filtros se aplican con igualdad exacta (==).
            Para filtros más complejos, crear métodos específicos.
        
        Example:
            # Todos los usuarios activos (paginado)
            users = await user_repo.get_all(
                tenant_id="default",
                skip=0,
                limit=50,
                filters={"is_active": True}
            )
            
            # Segunda página
            more_users = await user_repo.get_all(
                tenant_id="default",
                skip=50,
                limit=50,
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
        Actualiza campos de una entidad existente.
        
        Args:
            entity_id: ID de la entidad
            tenant_id: ID del tenant
            **kwargs: Campos a actualizar {campo: nuevo_valor}
        
        Returns:
            Entidad actualizada o None si no existe
        
        Note:
            - Solo actualiza campos que existan en el modelo
            - Hace flush() pero NO commit()
            - Refresca la entidad después de actualizar
        
        Example:
            updated_user = await user_repo.update(
                entity_id=1,
                tenant_id="default",
                username="new_username",
                is_active=False
            )
            if updated_user:
                print(f"Usuario actualizado: {updated_user.username}")
        """
        entity = await self.get_by_id(entity_id, tenant_id)
        if not entity:
            return None
        
        # Actualizar solo campos válidos
        for field, value in kwargs.items():
            if hasattr(entity, field):
                setattr(entity, field, value)
        
        await self.session.flush()
        await self.session.refresh(entity)
        return entity
    
    async def delete(self, entity_id: int, tenant_id: str) -> bool:
        """
        Elimina una entidad permanentemente (hard delete).
        
        Args:
            entity_id: ID de la entidad
            tenant_id: ID del tenant
        
        Returns:
            True si se eliminó, False si no existía
        
        Warning:
            Esta operación es IRREVERSIBLE. Para soft delete,
            usar update(is_active=False) en su lugar.
        
        Example:
            deleted = await user_repo.delete(1, "default")
            if deleted:
                print("✅ Usuario eliminado")
            else:
                print("❌ Usuario no encontrado")
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
        Cuenta entidades que cumplen filtros opcionales.
        
        Args:
            tenant_id: ID del tenant
            filters: Filtros adicionales {campo: valor}
        
        Returns:
            Número de entidades (int)
        
        Example:
            # Contar usuarios activos
            active_count = await user_repo.count(
                tenant_id="default",
                filters={"is_active": True}
            )
            print(f"Usuarios activos: {active_count}")
            
            # Contar todos los usuarios
            total_count = await user_repo.count(tenant_id="default")
            print(f"Total usuarios: {total_count}")
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
        Verifica si una entidad existe (método de utilidad).
        
        Args:
            entity_id: ID de la entidad
            tenant_id: ID del tenant
        
        Returns:
            True si existe, False si no
        
        Note:
            Internamente usa get_by_id() y verifica si es None.
        
        Example:
            if await user_repo.exists(1, "default"):
                print("✅ Usuario existe")
            else:
                print("❌ Usuario no encontrado")
        """
        entity = await self.get_by_id(entity_id, tenant_id)
        return entity is not None
