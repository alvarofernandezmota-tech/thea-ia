"""
User Service - Manage Telegram users in database
100% conversational, no commands
"""

import logging
from typing import Optional, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class UserService:
    """Service for managing users"""
    
    def __init__(self):
        """Initialize user service"""
        pass
    
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
            # Mock user object for testing
            user = {
                'id': 1,
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
            
            logger.info(f"✅ User created: {username} ({telegram_id})")
            return user
            
        except Exception as e:
            logger.error(f"❌ Error creating user: {e}")
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
            # Mock - returns None for now
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting user: {e}")
            return None
    
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
                logger.error(f"❌ User not found: {telegram_id}")
                return False
            
            logger.info(f"✅ Preferences updated for user {telegram_id}: {preferences}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating preferences: {e}")
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
                logger.error(f"❌ User not found: {telegram_id}")
                return False
            
            logger.info(f"✅ User deactivated: {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error deactivating user: {e}")
            return False
    
    def close(self):
        """Close database session"""
        pass
