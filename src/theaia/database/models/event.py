"""
Modelo Event - Eventos y recordatorios de la agenda
Almacena citas, recordatorios, eventos recurrentes
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel

class Event(BaseModel):
    """
    Evento/Recordatorio de la agenda.
    
    Campos principales:
    - title: Título del evento
    - description: Descripción detallada
    - start_datetime: Fecha/hora inicio
    - end_datetime: Fecha/hora fin (opcional)
    - location: Ubicación del evento
    - event_type: Tipo (personal, work, medical, etc)
    - status: Estado (active, cancelled, completed)
    - reminder_minutes: Minutos antes para recordatorio
    - recurrence_rule: Regla de recurrencia (formato RRULE)
    - external_id: ID externo (Google Calendar, etc)
    """
    __tablename__ = 'events'
    
    # Relación con usuario
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Información del evento
    title = Column(String(500), nullable=False)
    description = Column(Text)
    
    # Fechas
    start_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    end_datetime = Column(DateTime(timezone=True))
    
    # Detalles
    location = Column(String(500))
    event_type = Column(String(50), default='personal')
    status = Column(String(20), default='active', index=True)
    
    # Recordatorios
    reminder_minutes = Column(Integer, default=30)
    
    # Recurrencia
    recurrence_rule = Column(String(200))
    
    # Sincronización externa
    external_id = Column(String(255))
    
    # Metadatos adicionales
    extra_data = Column(JSONB, default={})

    
    # Relaciones
    user = relationship("User", back_populates="events")
    
    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title}, start={self.start_datetime})>"
