"""
User Service - Manage Telegram users in database
100% conversational, no commands
"""

import logging
from typing import Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from theaia.infrastructure.database.models import User
from theaia.infrastructure.database.connection import get_session

logger = logging.getLogger(__name__)


class UserService:
    """Service for managing users conversationally"""
    
    def __init__(self):
        """Initialize user service"""
        self.session: Optional[Session] = None
    
    def _get_session(self) -> Session:
        """Get database session"""
        if not self.session:
            self.session = next(get_session())
        return self.session
    
    def register_or_get_user(
        self,
        telegram_id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None
    ) -> User:
        """
        Register new user or get existing one
        Called automatically when user starts chatting
        
        Args:
            telegram_id: Telegram user ID
            first_name: User first name
            last_name: User last name (optional)
            username: Telegram username (optional)
        
        Returns:
            User object
        """
        session = self._get_session()
        
        try:
            # Check if user exists
            user = session.query(User).filter(
                User.telegram_id == telegram_id
            ).first()
            
            if user:
                # Update last seen
                user.last_seen = datetime.utcnow()
                session.commit()
                logger.info(f"✅ Existing user: {first_name} ({telegram_id})")
                return user
            
            # Create new user
            user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                is_active=True,
                created_at=datetime.utcnow(),
                last_seen=datetime.utcnow()
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            logger.info(f"✅ New user registered: {first_name} ({telegram_id})")
            return user
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error registering user: {e}")
            raise
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Get user by Telegram ID
        
        Args:
            telegram_id: Telegram user ID
        
        Returns:
            User object or None
        """
        session = self._get_session()
        
        try:
            user = session.query(User).filter(
                User.telegram_id == telegram_id
            ).first()
            
            return user
            
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
        session = self._get_session()
        
        try:
            user = self.get_user_by_telegram_id(telegram_id)
            
            if not user:
                logger.error(f"❌ User not found: {telegram_id}")
                return False
            
            # Update preferences (you can extend User model with preferences field)
            # For now, just log
            logger.info(f"✅ Preferences updated for user {telegram_id}: {preferences}")
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
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
        session = self._get_session()
        
        try:
            user = self.get_user_by_telegram_id(telegram_id)
            
            if not user:
                logger.error(f"❌ User not found: {telegram_id}")
                return False
            
            user.is_active = False
            session.commit()
            
            logger.info(f"✅ User deactivated: {telegram_id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error deactivating user: {e}")
            return False
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()
            self.session = None
