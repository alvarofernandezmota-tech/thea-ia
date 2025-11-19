"""
User Repository para THEA IA
Gestión de usuarios de Telegram con multi-tenant

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025 | Actualizado: 19 Nov 2025 (FASE 8)
Hito: H02 - Database Layer + Advanced Persistence
"""

from typing import Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.user import User


class UserRepository(BaseRepository[User]):
    """
    Repository para operaciones CRUD de usuarios con multi-tenant.
    
    Extiende BaseRepository con métodos específicos para usuarios de Telegram:
    - get_by_telegram_id(): Buscar usuario por Telegram ID
    - get_or_create_from_telegram(): Crear usuario desde datos Telegram
    - get_or_create_telegram_user(): Alias compatible con tests
    - update_preferences(): Actualizar preferencias usuario (JSONB)
    - update_last_activity(): Actualizar timestamp última actividad
    - get_active_users(): Obtener usuarios activos paginados
    - deactivate_user() / activate_user(): Soft delete/restore
    - count_active_users(): Contar usuarios activos por tenant
    
    Multi-tenant:
        Todos los métodos requieren tenant_id para aislar datos.
        Un mismo telegram_id puede existir en múltiples tenants.
    
    Example:
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            user, created = await user_repo.get_or_create_from_telegram(
                {"id": 123456, "username": "john"}, 
                "default"
            )
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa UserRepository.
        
        Args:
            session: AsyncSession de SQLAlchemy activa
        """
        super().__init__(User, session)
    
    async def get_by_telegram_id(
        self, 
        telegram_id: int, 
        tenant_id: str
    ) -> Optional[User]:
        """
        Busca un usuario por su Telegram ID dentro de un tenant.
        
        Args:
            telegram_id: ID único de Telegram del usuario
            tenant_id: ID del tenant (aislamiento multi-tenant)
        
        Returns:
            Usuario encontrado o None si no existe
        
        Raises:
            SQLAlchemyError: Si hay error de base de datos
        
        Example:
            user = await user_repo.get_by_telegram_id(123456789, "tenant_001")
            if user:
                print(f"Usuario: {user.username}")
            else:
                print("Usuario no encontrado")
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
        Obtiene usuario existente o lo crea desde datos de Telegram.
        
        Este método es el punto de entrada principal cuando un usuario
        interactúa con el bot por primera vez. Si el usuario ya existe,
        actualiza sus datos si han cambiado en Telegram.
        
        Args:
            telegram_data: Dict con datos de Telegram API:
                - id: int (telegram_id) [REQUERIDO]
                - username: str (opcional, puede ser None)
                - first_name: str (opcional)
                - last_name: str (opcional)
                - language_code: str (opcional, default "es")
            tenant_id: ID del tenant para multi-tenant isolation
        
        Returns:
            Tuple (User, created: bool)
            - User: Instancia del usuario (encontrado o creado)
            - created: True si fue creado, False si ya existía
        
        Raises:
            ValueError: Si telegram_data no contiene campo 'id'
            SQLAlchemyError: Si hay error de base de datos
        
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
                print("✅ Nuevo usuario registrado")
            else:
                print("✅ Usuario existente actualizado")
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
    
    async def get_or_create_telegram_user(
        self,
        telegram_id: int,
        tenant_id: str,
        defaults: Optional[Dict[str, Any]] = None
    ) -> tuple[User, bool]:
        """
        Alias para get_or_create_from_telegram con firma compatible con tests.
        
        Este método existe para compatibilidad con la suite de tests que
        espera esta firma específica.
        
        Args:
            telegram_id: ID de Telegram del usuario
            tenant_id: ID del tenant
            defaults: Dict con datos adicionales del usuario (username, first_name, etc.)
        
        Returns:
            Tuple (User, created: bool)
        
        Example:
            user, created = await user_repo.get_or_create_telegram_user(
                123456789,
                "default",
                defaults={"username": "john", "first_name": "John"}
            )
        """
        telegram_data = {"id": telegram_id}
        if defaults:
            telegram_data.update(defaults)
        
        return await self.get_or_create_from_telegram(telegram_data, tenant_id)
    
    async def update_last_activity(
        self,
        user_id: int
    ) -> Optional[User]:
        """
        Actualiza la última actividad del usuario al momento actual (UTC).
        
        Este método se llama cada vez que un usuario interactúa con el bot
        para mantener un registro de actividad reciente.
        
        Args:
            user_id: ID interno del usuario (no telegram_id)
        
        Returns:
            Usuario actualizado o None si no existe
        
        Note:
            Este método NO requiere tenant_id porque get_by_id ya lo filtra.
        
        Example:
            user = await user_repo.update_last_activity(42)
            if user:
                print(f"Última actividad: {user.last_activity}")
        """
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        user.last_activity = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def update_preferences(
        self,
        user_id: int,
        tenant_id: str,
        preferences: Dict[str, Any]
    ) -> Optional[User]:
        """
        Actualiza las preferencias del usuario (campo JSONB).
        
        Las preferencias se hacen merge con las existentes (no se sobrescriben).
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            preferences: Dict con preferencias a actualizar/añadir
        
        Returns:
            Usuario actualizado o None si no existe
        
        Preferences típicas:
            - notifications_enabled: bool
            - reminder_advance_minutes: int
            - timezone: str (ej: "Europe/Madrid")
            - language: str (ej: "es", "en")
        
        Example:
            preferences = {
                "notifications_enabled": True,
                "reminder_advance_minutes": 15,
                "timezone": "Europe/Madrid"
            }
            user = await user_repo.update_preferences(1, "default", preferences)
            print(user.preferences)  # {'notifications_enabled': True, ...}
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
        Obtiene todos los usuarios activos del tenant (paginado).
        
        Args:
            tenant_id: ID del tenant
            skip: Número de registros a saltar (paginación)
            limit: Máximo de registros a retornar (default 100)
        
        Returns:
            Lista de usuarios activos (is_active=True)
        
        Example:
            # Primera página
            active_users = await user_repo.get_active_users("default", skip=0, limit=50)
            print(f"Usuarios activos: {len(active_users)}")
            
            # Segunda página
            more_users = await user_repo.get_active_users("default", skip=50, limit=50)
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
        Desactiva un usuario (soft delete).
        
        El usuario no se elimina de la base de datos, solo se marca
        como inactivo (is_active=False).
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Usuario desactivado o None si no existe
        
        Example:
            user = await user_repo.deactivate_user(1, "default")
            if user:
                print(f"Usuario {user.username} desactivado")
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
        Activa un usuario previamente desactivado.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Usuario activado o None si no existe
        
        Example:
            user = await user_repo.activate_user(1, "default")
            if user:
                print(f"Usuario {user.username} reactivado")
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
            Número de usuarios activos (is_active=True)
        
        Example:
            count = await user_repo.count_active_users("default")
            print(f"Total usuarios activos: {count}")
        """
        return await self.count(
            tenant_id=tenant_id,
            filters={"is_active": True}
        )
