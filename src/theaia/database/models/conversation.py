"""
Modelo Conversation - Sesiones de conversación FSM
Almacena el estado actual y contexto de cada conversación
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel

class Conversation(BaseModel):
    """
    Sesión de conversación con el usuario.
    
    Campos principales:
    - session_id: ID único de la sesión
    - current_state: Estado actual del FSM
    - context_data: Contexto de la conversación (JSON)
    - last_message_id: ID del último mensaje
    - is_active: Si la conversación está activa
    - started_at: Inicio de la conversación
    - last_activity: Última actividad
    """
    __tablename__ = 'conversations'
    
    # Relación con usuario
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Sesión
    session_id = Column(String(255), nullable=False, unique=True, index=True)
    
    # Estado FSM
    current_state = Column(String(50), nullable=False, index=True)
    
    # Contexto
    context_data = Column(JSONB, default={})
    
    # Último mensaje
    last_message_id = Column(String(255))
    
    # Estado y actividad
    is_active = Column(Boolean, default=True, index=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    last_activity = Column(DateTime(timezone=True), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="conversations")
    messages = relationship("MessageHistory", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, session_id={self.session_id}, state={self.current_state})>"
