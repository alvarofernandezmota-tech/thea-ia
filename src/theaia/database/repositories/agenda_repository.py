"""
Agenda Repository - Database operations for agenda/events
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models.event import Event
from ..models.user import User
from .base_repository import BaseRepository


class AgendaRepository(BaseRepository[Event]):
    """Repository for Event/Agenda operations with multi-tenant support"""
    
    def __init__(self, db_session: Session):
        super().__init__(Event, db_session)
    
    def create_event(
        self,
        user_id: int,
        title: str,
        description: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        location: Optional[str] = None,
        reminder_time: Optional[datetime] = None,
    ) -> Event:
        """Create a new event for user"""
        event = Event(
            user_id=user_id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            reminder_time=reminder_time,
        )
        self.db_session.add(event)
        self.db_session.commit()
        self.db_session.refresh(event)
        return event
    
    def get_event_by_id(self, event_id: int, user_id: int) -> Optional[Event]:
        """Get event by ID (with multi-tenant check)"""
        return self.db_session.query(Event).filter(
            and_(
                Event.id == event_id,
                Event.user_id == user_id
            )
        ).first()
    
    def get_user_events(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Event]:
        """Get all events for user with optional date filtering"""
        query = self.db_session.query(Event).filter(Event.user_id == user_id)
        
        if start_date:
            query = query.filter(Event.start_time >= start_date)
        
        if end_date:
            query = query.filter(Event.start_time <= end_date)
        
        return query.order_by(Event.start_time.asc()).limit(limit).all()
    
    def update_event(
        self,
        event_id: int,
        user_id: int,
        **kwargs
    ) -> Optional[Event]:
        """Update event fields (with multi-tenant check)"""
        event = self.get_event_by_id(event_id, user_id)
        
        if not event:
            return None
        
        for key, value in kwargs.items():
            if hasattr(event, key) and value is not None:
                setattr(event, key, value)
        
        self.db_session.commit()
        self.db_session.refresh(event)
        return event
    
    def delete_event(self, event_id: int, user_id: int) -> bool:
        """Delete event (with multi-tenant check)"""
        event = self.get_event_by_id(event_id, user_id)
        
        if not event:
            return False
        
        self.db_session.delete(event)
        self.db_session.commit()
        return True
    
    def search_events(
        self,
        user_id: int,
        search_term: str,
        limit: int = 50
    ) -> List[Event]:
        """Search events by title or description"""
        search_pattern = f"%{search_term}%"
        
        return self.db_session.query(Event).filter(
            and_(
                Event.user_id == user_id,
                or_(
                    Event.title.ilike(search_pattern),
                    Event.description.ilike(search_pattern)
                )
            )
        ).order_by(Event.start_time.desc()).limit(limit).all()
    
    def get_upcoming_events(
        self,
        user_id: int,
        from_date: Optional[datetime] = None,
        limit: int = 10
    ) -> List[Event]:
        """Get upcoming events for user"""
        if not from_date:
            from_date = datetime.utcnow()
        
        return self.db_session.query(Event).filter(
            and_(
                Event.user_id == user_id,
                Event.start_time >= from_date
            )
        ).order_by(Event.start_time.asc()).limit(limit).all()
    
    def get_events_with_reminders(
        self,
        user_id: int,
        check_time: Optional[datetime] = None
    ) -> List[Event]:
        """Get events that have reminder_time set and upcoming"""
        if not check_time:
            check_time = datetime.utcnow()
        
        return self.db_session.query(Event).filter(
            and_(
                Event.user_id == user_id,
                Event.reminder_time.isnot(None),
                Event.reminder_time <= check_time,
                Event.start_time >= check_time
            )
        ).order_by(Event.reminder_time.asc()).all()
