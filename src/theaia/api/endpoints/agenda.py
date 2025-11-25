"""
Agenda Agent API Endpoints
REST API para AgendaAgent - CRUD de eventos

Responsable: Álvaro Fernández Mota (CEO THEA-IA)
Fecha: 21 Noviembre 2025
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session

from src.theaia.database.models.event import Event
from src.theaia.database.models.user import User
from src.theaia.database.session import get_db

# Router instance
router = APIRouter(
    prefix="/agents/agenda",
    tags=["agenda"],
    responses={404: {"description": "Not found"}},
)

# ==================== ENDPOINTS ====================

@router.post("/create-event")
async def create_event(
    user_id: int,
    tenant_id: str,
    title: str,
    start_datetime: str,
    end_datetime: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Create a new event for user
    
    Parameters:
    - user_id: User ID
    - tenant_id: Tenant ID (multi-tenant)
    - title: Event title
    - start_datetime: Start datetime (ISO format: 2025-11-22T10:00:00)
    - end_datetime: End datetime (optional)
    - location: Event location (optional)
    
    Returns:
    - Created event with ID
    """
    try:
        # Verify user exists
        user = db.query(User).filter_by(id=user_id, tenant_id=tenant_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Parse datetime
        try:
            start_dt = datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
            if not start_dt.tzinfo:
                start_dt = start_dt.replace(tzinfo=timezone.utc)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format: 2025-11-22T10:00:00Z")
        
        # Create event
        event = Event(
            title=title,
            start_datetime=start_dt,
            user_id=user_id,
            tenant_id=tenant_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        if location:
            event.location = location
        if end_datetime:
            try:
                end_dt = datetime.fromisoformat(end_datetime.replace('Z', '+00:00'))
                if not end_dt.tzinfo:
                    end_dt = end_dt.replace(tzinfo=timezone.utc)
                event.end_datetime = end_dt
            except ValueError:
                pass  # Ignore invalid end_datetime
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        return {
            "status": "success",
            "event_id": event.id,
            "title": event.title,
            "start_datetime": event.start_datetime.isoformat(),
            "user_id": user_id,
            "tenant_id": tenant_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")


@router.get("/events")
async def list_events(
    user_id: int,
    tenant_id: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    List events for user
    
    Parameters:
    - user_id: User ID
    - tenant_id: Tenant ID
    - start_date: Optional filter start date (ISO format)
    - end_date: Optional filter end date (ISO format)
    
    Returns:
    - List of user's events
    """
    try:
        # Verify user exists
        user = db.query(User).filter_by(id=user_id, tenant_id=tenant_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Query events
        query = db.query(Event).filter_by(user_id=user_id, tenant_id=tenant_id)
        
        # Filter by date range if provided
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                if not start_dt.tzinfo:
                    start_dt = start_dt.replace(tzinfo=timezone.utc)
                query = query.filter(Event.start_datetime >= start_dt)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                if not end_dt.tzinfo:
                    end_dt = end_dt.replace(tzinfo=timezone.utc)
                query = query.filter(Event.start_datetime <= end_dt)
            except ValueError:
                pass
        
        events = query.order_by(Event.start_datetime).all()
        
        return {
            "status": "success",
            "count": len(events),
            "events": [
                {
                    "id": e.id,
                    "title": e.title,
                    "start_datetime": e.start_datetime.isoformat(),
                    "location": e.location or None,
                    "user_id": e.user_id,
                    "tenant_id": e.tenant_id
                }
                for e in events
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing events: {str(e)}")


@router.get("/event/{event_id}")
async def get_event(
    event_id: int,
    user_id: int,
    tenant_id: str,
    db: Session = Depends(get_db)
):
    """
    Get specific event details
    
    Parameters:
    - event_id: Event ID
    - user_id: User ID (for authorization)
    - tenant_id: Tenant ID
    
    Returns:
    - Event details
    """
    try:
        event = db.query(Event).filter_by(
            id=event_id,
            user_id=user_id,
            tenant_id=tenant_id
        ).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "status": "success",
            "event": {
                "id": event.id,
                "title": event.title,
                "start_datetime": event.start_datetime.isoformat(),
                "location": event.location or None,
                "user_id": event.user_id,
                "tenant_id": event.tenant_id,
                "created_at": event.created_at.isoformat()
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving event: {str(e)}")


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AgendaAgent API",
        "version": "1.0.0"
    }
