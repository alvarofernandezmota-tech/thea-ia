"""
Modelo Event - Eventos de la agenda
Almacena citas, eventos (sin recordatorios - manejados por ReminderAgent)

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025 (H03 PHASE 1)
Hito: H03 - EventAgent + Multi-tenant
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel


class Event(BaseModel):
    """
    Evento de la agenda.
    
    Campos principales:
    - title: Título del evento
    - description: Descripción detallada
    - start_datetime: Fecha/hora inicio
    - end_datetime: Fecha/hora fin (opcional)
    - location: Ubicación del evento
    - participants: Lista de participantes (JSONB)
    - event_type: Tipo (personal, work, medical, etc)
    - status: Estado (pending, completed, cancelled)
    - recurrence_rule: Regla de recurrencia (formato RRULE)
    - external_id: ID externo (Google Calendar, etc)
    - tenant_id: Multi-tenant isolation
    
    NOTE: Recordatorios manejados por ReminderAgent (tabla separada)
    NOTE: Búsquedas manejadas por QueryAgent (no duplicar lógica aquí)
    """
    __tablename__ = 'events'
    
    # Relación con usuario (manejado por Core)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Multi-tenant
    tenant_id = Column(String(50), nullable=False, index=True, default='default')
    
    # Información del evento
    title = Column(String(500), nullable=False)
    description = Column(Text)
    
    # Fechas
    start_datetime = Column(DateTime(timezone=True), nullable=False, index=True)
    end_datetime = Column(DateTime(timezone=True))
    
    # Detalles
    location = Column(String(500))
    participants = Column(JSONB, default=list)  # Lista de participantes ["Juan", "María"]
    event_type = Column(String(50), default='personal')
    status = Column(String(20), default='pending', index=True)
    
    # Recurrencia
    recurrence_rule = Column(String(200))
    
    # Sincronización externa
    external_id = Column(String(255))
    
    # Metadatos adicionales
    extra_data = Column(JSONB, default=dict)
    
    # Relaciones
    user = relationship("User", back_populates="events")
    # NOTE: NO relationship con Reminder (manejado por ReminderAgent)
    
    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title}, start={self.start_datetime}, tenant={self.tenant_id})>"
