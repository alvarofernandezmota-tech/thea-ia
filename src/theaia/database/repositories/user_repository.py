"""
User Repository para THEA IA
Gestión de usuarios de Telegram con multi-tenant

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer
"""

from typing import Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.user import User


class UserRepository(BaseRepository[User]):
    """
    Repository para operaciones CRUD de usuarios.
    
    Extiende BaseRepository con métodos específicos para usuarios:
    - get_by_telegram_id(): Buscar usuario por Telegram ID
    - get_or_create_from_telegram(): Crear usuario desde datos Telegram
    - update_preferences(): Actualizar preferencias usuario
    - get_active_users(): Obtener usuarios activos
    
    Example:
        async with get_db() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_telegram_id(123456, "default")
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa UserRepository.
        
        Args:
            session: AsyncSession de SQLAlchemy
        """
        super().__init__(User, session)
    
    async def get_by_telegram_id(
        self, 
        telegram_id: int, 
        tenant_id: str
    ) -> Optional[User]:
        """
        Busca un usuario por su Telegram ID.
        
        Args:
            telegram_id: ID único de Telegram
            tenant_id: ID del tenant
        
        Returns:
            Usuario encontrado o None
        
        Example:
            user = await user_repo.get_by_telegram_id(123456789, "default")
            if user:
                print(f"Usuario encontrado: {user.username}")
        """
        stmt = select(User).where(
            User.telegram_id == telegram_id,
            User.tenant_id == tenant_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_or_create_from_telegram(
        self,
        telegram_data: Dict[str, Any],
        tenant_id: str
    ) -> tuple[User, bool]:
        """
        Obtiene un usuario existente o lo crea desde datos de Telegram.
        
        Este método es el punto de entrada principal cuando un usuario
        interactúa con el bot por primera vez.
        
        Args:
            telegram_data: Dict con datos de Telegram:
                - id: int (telegram_id)
                - username: str (opcional)
                - first_name: str (opcional)
                - last_name: str (opcional)
                - language_code: str (opcional)
            tenant_id: ID del tenant
        
        Returns:
            Tuple (User, created: bool)
            - User: Usuario encontrado o creado
            - created: True si fue creado, False si ya existía
        
        Example:
            telegram_data = {
                "id": 123456789,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "language_code": "es"
            }
            user, created = await user_repo.get_or_create_from_telegram(
                telegram_data, "default"
            )
            if created:
                print("Nuevo usuario registrado")
        """
        telegram_id = telegram_data.get("id")
        if not telegram_id:
            raise ValueError("telegram_data must contain 'id' field")
        
        # Intentar obtener usuario existente
        user = await self.get_by_telegram_id(telegram_id, tenant_id)
        
        if user:
            # Usuario existe, actualizar datos si cambiaron
            updated = False
            if telegram_data.get("username") and telegram_data["username"] != user.username:
                user.username = telegram_data["username"]
                updated = True
            if telegram_data.get("first_name") and telegram_data["first_name"] != user.first_name:
                user.first_name = telegram_data["first_name"]
                updated = True
            if telegram_data.get("last_name") and telegram_data["last_name"] != user.last_name:
                user.last_name = telegram_data["last_name"]
                updated = True
            
            if updated:
                await self.session.flush()
                await self.session.refresh(user)
            
            return user, False
        
        # Usuario no existe, crear nuevo
        user = await self.create(
            tenant_id=tenant_id,
            telegram_id=telegram_id,
            username=telegram_data.get("username"),
            first_name=telegram_data.get("first_name"),
            last_name=telegram_data.get("last_name"),
            language_code=telegram_data.get("language_code", "es"),
            is_active=True
        )
        
        return user, True
    
    async def update_preferences(
        self,
        user_id: int,
        tenant_id: str,
        preferences: Dict[str, Any]
    ) -> Optional[User]:
        """
        Actualiza las preferencias del usuario (JSONB).
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            preferences: Dict con preferencias a actualizar
        
        Returns:
            Usuario actualizado o None
        
        Example:
            preferences = {
                "notifications_enabled": True,
                "reminder_advance_minutes": 15,
                "timezone": "Europe/Madrid"
            }
            user = await user_repo.update_preferences(1, "default", preferences)
        """
        user = await self.get_by_id(user_id, tenant_id)
        if not user:
            return None
        
        # Merge preferences (mantener las existentes)
        current_prefs = user.preferences or {}
        current_prefs.update(preferences)
        user.preferences = current_prefs
        
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def get_active_users(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[User]:
        """
        Obtiene todos los usuarios activos.
        
        Args:
            tenant_id: ID del tenant
            skip: Número de registros a saltar
            limit: Máximo de registros a retornar
        
        Returns:
            Lista de usuarios activos
        
        Example:
            active_users = await user_repo.get_active_users("default")
            print(f"Usuarios activos: {len(active_users)}")
        """
        return await self.get_all(
            tenant_id=tenant_id,
            skip=skip,
            limit=limit,
            filters={"is_active": True}
        )
    
    async def deactivate_user(
        self,
        user_id: int,
        tenant_id: str
    ) -> Optional[User]:
        """
        Desactiva un usuario (soft deactivate).
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Usuario desactivado o None
        
        Example:
            user = await user_repo.deactivate_user(1, "default")
        """
        return await self.update(
            entity_id=user_id,
            tenant_id=tenant_id,
            is_active=False
        )
    
    async def activate_user(
        self,
        user_id: int,
        tenant_id: str
    ) -> Optional[User]:
        """
        Activa un usuario.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Usuario activado o None
        
        Example:
            user = await user_repo.activate_user(1, "default")
        """
        return await self.update(
            entity_id=user_id,
            tenant_id=tenant_id,
            is_active=True
        )
    
    async def count_active_users(self, tenant_id: str) -> int:
        """
        Cuenta usuarios activos del tenant.
        
        Args:
            tenant_id: ID del tenant
        
        Returns:
            Número de usuarios activos
        
        Example:
            count = await user_repo.count_active_users("default")
        """
        return await self.count(
            tenant_id=tenant_id,
            filters={"is_active": True}
        )
