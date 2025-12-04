"""
Event Schemas - Validación y serialización
Schemas Pydantic para AgendaAgent

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025 (H03 PHASE 1)
Hito: H03 - AgendaAgent Schemas
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List


class EventBase(BaseModel):
    """
    Schema base para Event (campos comunes).
    
    Usado como base para EventCreate y EventUpdate.
    """
    title: str = Field(..., min_length=1, max_length=500, description="Título del evento")
    description: Optional[str] = Field(None, description="Descripción detallada")
    start_datetime: datetime = Field(..., description="Fecha/hora inicio (timezone-aware)")
    end_datetime: Optional[datetime] = Field(None, description="Fecha/hora fin (timezone-aware)")
    location: Optional[str] = Field(None, max_length=500, description="Ubicación del evento")
    participants: List[str] = Field(default_factory=list, description="Lista de participantes")
    event_type: str = Field(default="personal", max_length=50, description="Tipo de evento")
    status: str = Field(default="pending", max_length=20, description="Estado del evento")
    recurrence_rule: Optional[str] = Field(None, max_length=200, description="Regla de recurrencia (RRULE)")
    external_id: Optional[str] = Field(None, max_length=255, description="ID externo (Google Calendar, etc)")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Valida que status sea un valor permitido."""
        allowed = ['pending', 'completed', 'cancelled']
        if v not in allowed:
            raise ValueError(f"status debe ser uno de: {', '.join(allowed)}")
        return v
    
    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        """Valida que event_type sea un valor permitido."""
        allowed = ['personal', 'work', 'medical', 'social', 'other']
        if v not in allowed:
            raise ValueError(f"event_type debe ser uno de: {', '.join(allowed)}")
        return v
    
    @field_validator('end_datetime')
    @classmethod
    def validate_end_after_start(cls, v: Optional[datetime], info) -> Optional[datetime]:
        """Valida que end_datetime sea posterior a start_datetime."""
        if v is not None and 'start_datetime' in info.data:
            start = info.data['start_datetime']
            if v <= start:
                raise ValueError("end_datetime debe ser posterior a start_datetime")
        return v


class EventCreate(EventBase):
    """
    Schema para crear un evento.
    
    Incluye todos los campos de EventBase.
    user_id y tenant_id se agregan automáticamente desde el contexto.
    
    Example:
        event_data = EventCreate(
            title="Reunión con cliente",
            description="Presentación de propuesta",
            start_datetime=datetime(2025, 12, 5, 10, 0, tzinfo=timezone.utc),
            end_datetime=datetime(2025, 12, 5, 11, 0, tzinfo=timezone.utc),
            location="Oficina central",
            participants=["Juan Pérez", "María García"],
            event_type="work",
            status="pending"
        )
    """
    pass


class EventUpdate(BaseModel):
    """
    Schema para actualizar un evento.
    
    Todos los campos son opcionales (partial update).
    Solo se actualizan los campos proporcionados.
    
    Example:
        # Cambiar solo el título
        update_data = EventUpdate(title="Reunión CANCELADA")
        
        # Cambiar varios campos
        update_data = EventUpdate(
            status="completed",
            description="Reunión completada exitosamente"
        )
    """
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=500)
    participants: Optional[List[str]] = None
    event_type: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    recurrence_rule: Optional[str] = Field(None, max_length=200)
    external_id: Optional[str] = Field(None, max_length=255)
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Valida que status sea un valor permitido."""
        if v is not None:
            allowed = ['pending', 'completed', 'cancelled']
            if v not in allowed:
                raise ValueError(f"status debe ser uno de: {', '.join(allowed)}")
        return v
    
    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: Optional[str]) -> Optional[str]:
        """Valida que event_type sea un valor permitido."""
        if v is not None:
            allowed = ['personal', 'work', 'medical', 'social', 'other']
            if v not in allowed:
                raise ValueError(f"event_type debe ser uno de: {', '.join(allowed)}")
        return v


class EventResponse(EventBase):
    """
    Schema para respuesta de API con evento completo.
    
    Incluye todos los campos de EventBase + metadata (id, timestamps, tenant).
    
    Example:
        {
            "id": 1,
            "user_id": 5,
            "tenant_id": "default",
            "title": "Reunión con cliente",
            "description": "Presentación de propuesta",
            "start_datetime": "2025-12-05T10:00:00Z",
            "end_datetime": "2025-12-05T11:00:00Z",
            "location": "Oficina central",
            "participants": ["Juan Pérez", "María García"],
            "event_type": "work",
            "status": "pending",
            "created_at": "2025-12-04T16:00:00Z",
            "updated_at": "2025-12-04T16:00:00Z"
        }
    """
    id: int
    user_id: int
    tenant_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True  # Permite cargar desde objetos ORM
    }


class EventListResponse(BaseModel):
    """
    Schema para lista paginada de eventos.
    
    Example:
        {
            "events": [...],
            "total": 25,
            "page": 1,
            "page_size": 10,
            "total_pages": 3
        }
    """
    events: List[EventResponse]
    total: int
    page: int = 1
    page_size: int = 10
    total_pages: int
    
    model_config = {
        "from_attributes": True
    }
