"""
Booking Service - Manage appointments conversationally
100% natural language, no commands
"""

import logging
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from theaia.infrastructure.database.models import Appointment, User
from theaia.infrastructure.database.connection import get_session

logger = logging.getLogger(__name__)


class BookingService:
    """Service for managing appointments conversationally"""
    
    def __init__(self):
        """Initialize booking service"""
        self.session: Optional[Session] = None
    
    def _get_session(self) -> Session:
        """Get database session"""
        if not self.session:
            self.session = next(get_session())
        return self.session
    
    def create_appointment(
        self,
        user_id: int,
        start_time: datetime,
        duration_minutes: int = 60,
        title: str = "Cita",
        description: Optional[str] = None
    ) -> Optional[Appointment]:
        """
        Create new appointment
        Called when user says: "Quiero una cita mañana a las 3"
        
        Args:
            user_id: User ID from database
            start_time: Start datetime
            duration_minutes: Duration in minutes (default 60)
            title: Appointment title
            description: Optional description
        
        Returns:
            Appointment object or None if error
        """
        session = self._get_session()
        
        try:
            # Calculate end time
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            # Check for conflicts
            if self.check_conflict(start_time, end_time):
                logger.warning(f"⚠️ Conflict detected for {start_time}")
                return None
            
            # Create appointment
            appointment = Appointment(
                user_id=user_id,
                start_time=start_time,
                end_time=end_time,
                title=title,
                description=description,
                status='scheduled',
                created_at=datetime.utcnow()
            )
            
            session.add(appointment)
            session.commit()
            session.refresh(appointment)
            
            logger.info(f"✅ Appointment created: ID={appointment.id}, {start_time}")
            return appointment
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error creating appointment: {e}")
            return None
    
    def get_user_appointments(
        self,
        user_id: int,
        include_past: bool = False
    ) -> List[Appointment]:
        """
        Get all appointments for a user
        Called when user says: "¿Qué citas tengo?"
        
        Args:
            user_id: User ID
            include_past: Include past appointments
        
        Returns:
            List of appointments
        """
        session = self._get_session()
        
        try:
            query = session.query(Appointment).filter(
                Appointment.user_id == user_id,
                Appointment.status != 'cancelled'
            )
            
            if not include_past:
                query = query.filter(
                    Appointment.start_time >= datetime.utcnow()
                )
            
            appointments = query.order_by(
                Appointment.start_time.asc()
            ).all()
            
            logger.info(f"✅ Found {len(appointments)} appointments for user {user_id}")
            return appointments
            
        except Exception as e:
            logger.error(f"❌ Error getting appointments: {e}")
            return []
    
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """
        Get specific appointment by ID
        
        Args:
            appointment_id: Appointment ID
        
        Returns:
            Appointment object or None
        """
        session = self._get_session()
        
        try:
            appointment = session.query(Appointment).filter(
                Appointment.id == appointment_id
            ).first()
            
            return appointment
            
        except Exception as e:
            logger.error(f"❌ Error getting appointment: {e}")
            return None
    
    def cancel_appointment(
        self,
        appointment_id: int,
        user_id: int
    ) -> bool:
        """
        Cancel appointment (soft delete)
        Called when user says: "Cancela mi cita de mañana"
        
        Args:
            appointment_id: Appointment ID
            user_id: User ID (for security check)
        
        Returns:
            True if cancelled successfully
        """
        session = self._get_session()
        
        try:
            appointment = session.query(Appointment).filter(
                Appointment.id == appointment_id,
                Appointment.user_id == user_id
            ).first()
            
            if not appointment:
                logger.error(f"❌ Appointment not found or not owned by user")
                return False
            
            if appointment.status == 'cancelled':
                logger.warning(f"⚠️ Appointment already cancelled")
                return False
            
            appointment.status = 'cancelled'
            appointment.updated_at = datetime.utcnow()
            session.commit()
            
            logger.info(f"✅ Appointment cancelled: ID={appointment_id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error cancelling appointment: {e}")
            return False
    
    def update_appointment(
        self,
        appointment_id: int,
        user_id: int,
        new_start_time: Optional[datetime] = None,
        new_duration: Optional[int] = None,
        new_title: Optional[str] = None
    ) -> Optional[Appointment]:
        """
        Update appointment details
        Called when user says: "Cambia mi cita a las 5"
        
        Args:
            appointment_id: Appointment ID
            user_id: User ID (for security)
            new_start_time: New start time
            new_duration: New duration in minutes
            new_title: New title
        
        Returns:
            Updated appointment or None
        """
        session = self._get_session()
        
        try:
            appointment = session.query(Appointment).filter(
                Appointment.id == appointment_id,
                Appointment.user_id == user_id
            ).first()
            
            if not appointment:
                logger.error(f"❌ Appointment not found")
                return None
            
            # Update start time
            if new_start_time:
                duration = (appointment.end_time - appointment.start_time).total_seconds() / 60
                new_end_time = new_start_time + timedelta(minutes=duration)
                
                # Check conflicts (excluding current appointment)
                if self.check_conflict(new_start_time, new_end_time, exclude_id=appointment_id):
                    logger.warning(f"⚠️ Conflict detected for new time")
                    return None
                
                appointment.start_time = new_start_time
                appointment.end_time = new_end_time
            
            # Update duration
            if new_duration:
                appointment.end_time = appointment.start_time + timedelta(minutes=new_duration)
            
            # Update title
            if new_title:
                appointment.title = new_title
            
            appointment.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(appointment)
            
            logger.info(f"✅ Appointment updated: ID={appointment_id}")
            return appointment
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error updating appointment: {e}")
            return None
    
    def check_conflict(
        self,
        start_time: datetime,
        end_time: datetime,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Check if there's a conflict with existing appointments
        
        Args:
            start_time: Proposed start time
            end_time: Proposed end time
            exclude_id: Exclude specific appointment (for updates)
        
        Returns:
            True if conflict exists, False otherwise
        """
        session = self._get_session()
        
        try:
            query = session.query(Appointment).filter(
                Appointment.status == 'scheduled',
                and_(
                    Appointment.start_time < end_time,
                    Appointment.end_time > start_time
                )
            )
            
            if exclude_id:
                query = query.filter(Appointment.id != exclude_id)
            
            conflicts = query.count()
            
            if conflicts > 0:
                logger.warning(f"⚠️ {conflicts} conflicts found")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error checking conflicts: {e}")
            return True  # Return True on error to be safe
    
    def find_appointment_by_description(
        self,
        user_id: int,
        description: str
    ) -> Optional[Appointment]:
        """
        Find appointment by natural language description
        Called when user says: "Cancela mi cita de mañana"
        
        Args:
            user_id: User ID
            description: Natural language description (e.g., "mañana", "el jueves")
        
        Returns:
            Best matching appointment or None
        """
        # This is a simplified version
        # In production, you'd use NLP to parse "mañana", "jueves", etc.
        
        appointments = self.get_user_appointments(user_id)
        
        # For now, just return the next scheduled appointment
        if appointments:
            return appointments[0]
        
        return None
    
    def get_appointments_for_date(
        self,
        date: datetime,
        user_id: Optional[int] = None
    ) -> List[Appointment]:
        """
        Get all appointments for a specific date
        
        Args:
            date: Date to check
            user_id: Optional user filter
        
        Returns:
            List of appointments
        """
        session = self._get_session()
        
        try:
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            query = session.query(Appointment).filter(
                Appointment.status == 'scheduled',
                Appointment.start_time >= start_of_day,
                Appointment.start_time < end_of_day
            )
            
            if user_id:
                query = query.filter(Appointment.user_id == user_id)
            
            appointments = query.order_by(
                Appointment.start_time.asc()
            ).all()
            
            return appointments
            
        except Exception as e:
            logger.error(f"❌ Error getting appointments for date: {e}")
            return []
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()
            self.session = None
