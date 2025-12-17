"""
User Service - Manage Telegram users in database
100% conversational, no commands

✅ FIX #3: get_or_create_user() busca ANTES de crear
✅ FIX #4: Added update_last_interaction() method
"""

import logging
from typing import Optional, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class UserService:
    """Service for managing users"""
    
    def __init__(self):
        """Initialize user service"""
        # Simple in-memory cache para usuarios (para prevenir duplicados en tests)
        self._user_cache: Dict[int, dict] = {}
    
    def create_user(
        self,
        telegram_id: int,
        username: str,
        timezone: str = "UTC",
        tenant_id: str = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        language_code: str = "es"
    ) -> dict:
        """
        Create a new user (Mock for tests)
        
        Args:
            telegram_id: Telegram user ID
            username: Telegram username
            timezone: User timezone
            tenant_id: Tenant ID (required)
            first_name: User first name (optional)
            last_name: User last name (optional)
            language_code: User language code
        
        Returns:
            User object/dict
        """
        try:
            # ✅ FIX: Verificar si ya existe
            if telegram_id in self._user_cache:
                logger.warning(f"⚠️ Usuario ya existe: {telegram_id}, retornando existente")
                return self._user_cache[telegram_id]
            
            # Mock user object for testing
            user = {
                'id': telegram_id,  # Usar telegram_id como ID para simplificar
                'telegram_id': telegram_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'language_code': language_code,
                'timezone': timezone,
                'is_active': True,
                'preferences': {},
                'tenant_id': tenant_id,
                'last_activity': datetime.utcnow(),
                'created_at': datetime.utcnow()
            }
            
            # ✅ Guardar en cache
            self._user_cache[telegram_id] = user
            
            logger.info(f"✅ Usuario creado: {username} ({telegram_id})")
            return user
            
        except Exception as e:
            logger.error(f"❌ Error creando usuario: {e}")
            raise
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[dict]:
        """
        Get user by Telegram ID
        
        Args:
            telegram_id: Telegram user ID
        
        Returns:
            User object or None
        """
        try:
            # ✅ FIX #3: Buscar en cache primero
            if telegram_id in self._user_cache:
                logger.debug(f"✅ Usuario encontrado en cache: {telegram_id}")
                return self._user_cache[telegram_id]
            
            logger.debug(f"❌ Usuario no encontrado: {telegram_id}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo usuario: {e}")
            return None
    
    def get_user(self, telegram_id: int) -> Optional[dict]:
        """
        Get user by Telegram ID (alias for get_user_by_telegram_id)
        
        Args:
            telegram_id: Telegram user ID
        
        Returns:
            User object or None
        """
        return self.get_user_by_telegram_id(telegram_id)
    
    def get_or_create_user(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        **kwargs
    ) -> dict:
        """
        Get existing user or create new one if doesn't exist.
        This is the key method that prevents duplicate users.
        
        ✅ FIX #3: BUSCA PRIMERO, luego crea SOLO si no existe
        
        Args:
            telegram_id: Telegram user ID
            username: Username (optional, will default to user_{telegram_id} if not provided)
            **kwargs: Additional arguments (first_name, last_name, timezone, etc.)
        
        Returns:
            User dict with id, telegram_id, username, etc.
        """
        try:
            # ✅ PASO 1: BUSCAR primero
            user = self.get_user(telegram_id)
            if user:
                logger.info(f"✅ Usuario ya existe: {telegram_id}, NO creando duplicado")
                return user
            
            # ✅ PASO 2: CREAR SOLO si no existe
            if not username:
                username = f"user_{telegram_id}"
            
            logger.info(f"✅ Creando nuevo usuario: {username} ({telegram_id})")
            return self.create_user(
                telegram_id=telegram_id,
                username=username,
                **kwargs
            )
            
        except Exception as e:
            logger.error(f"❌ Error en get_or_create_user: {e}")
            raise
    
    def update_last_interaction(self, telegram_id: int) -> bool:
        """
        Update last interaction timestamp for user.
        
        ✅ FIX #4: Added missing method for tracking user activity
        
        Args:
            telegram_id: Telegram user ID
        
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            user = self.get_user(telegram_id)
            
            if not user:
                logger.warning(f"⚠️ Usuario no encontrado para actualizar: {telegram_id}")
                return False
            
            # Update last_activity timestamp
            user['last_activity'] = datetime.utcnow()
            logger.debug(f"✅ Last interaction updated for user {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating last interaction: {e}")
            return False
    
    def update_user_preferences(
        self,
        telegram_id: int,
        preferences: Dict
    ) -> bool:
        """
        Update user preferences (timezone, language, etc.)
        
        Args:
            telegram_id: Telegram user ID
            preferences: Dict with preferences
        
        Returns:
            True if updated successfully
        """
        try:
            user = self.get_user_by_telegram_id(telegram_id)
            
            if not user:
                logger.error(f"❌ Usuario no encontrado: {telegram_id}")
                return False
            
            # Actualizar preferencias
            user['preferences'].update(preferences)
            logger.info(f"✅ Preferencias actualizadas para usuario {telegram_id}: {preferences}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error actualizando preferencias: {e}")
            return False
    
    def deactivate_user(self, telegram_id: int) -> bool:
        """
        Deactivate user (soft delete)
        
        Args:
            telegram_id: Telegram user ID
        
        Returns:
            True if deactivated successfully
        """
        try:
            user = self.get_user_by_telegram_id(telegram_id)
            
            if not user:
                logger.error(f"❌ Usuario no encontrado: {telegram_id}")
                return False
            
            user['is_active'] = False
            logger.info(f"✅ Usuario desactivado: {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error desactivando usuario: {e}")
            return False
    
    def close(self):
        """Close database session"""
        pass
