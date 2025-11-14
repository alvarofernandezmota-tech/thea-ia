"""
Modelo Conversation - Sesiones de conversacion FSM
Almacena el estado actual y contexto de cada conversacion
VERSION CORREGIDA H02 - Con defaults para started_at y last_activity
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel


class Conversation(BaseModel):
    """
    Sesion de conversacion con el usuario.
    
    Campos principales:
    - session_id: ID unico de la sesion
    - current_state: Estado actual del FSM
    - context_data: Contexto de la conversacion (JSON)
    - last_message_id: ID del ultimo mensaje
    - is_active: Si la conversacion esta activa
    - started_at: Inicio de la conversacion (auto now)
    - last_activity: Ultima actividad (auto now)
    """
    __tablename__ = 'conversations'
    
    # Relacion con usuario
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Sesion
    session_id = Column(String(255), nullable=False, unique=True, index=True)
    
    # Estado FSM
    current_state = Column(String(50), nullable=False, index=True)
    
    # Contexto
    context_data = Column(JSONB, default={})
    
    # Ultimo mensaje
    last_message_id = Column(String(255))
    
    # Estado y actividad
    is_active = Column(Boolean, default=True, index=True)
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_activity = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="conversations")
    messages = relationship("MessageHistory", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, session_id={self.session_id}, state={self.current_state})>"