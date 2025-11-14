"""
Modelo MessageHistory - Historial completo de mensajes
Almacena todos los mensajes y respuestas para auditoría
VERSIÓN CORREGIDA H02 - Con user_id para auditoría directa
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel


class MessageHistory(BaseModel):
    """
    Historial de mensajes de una conversación.
    
    Campos principales:
    - user_id: Usuario dueño del mensaje (para auditoría directa)
    - conversation_id: Conversación a la que pertenece
    - message_id: ID único del mensaje
    - user_message: Mensaje del usuario
    - bot_response: Respuesta del bot
    - intent_detected: Intent clasificado por ML
    - entities_extracted: Entidades extraídas (JSON)
    - confidence_score: Confianza del clasificador
    - processing_time_ms: Tiempo de procesamiento
    
    Nota: user_id es redundante con conversation.user_id pero mejora:
    - Auditoría directa (queries sin JOIN)
    - Performance en analytics
    - Compliance GDPR (borrado de datos)
    - Multi-tenant security
    """
    __tablename__ = 'message_history'
    
    # Relación con usuario (para auditoría directa)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Relación con conversación
    conversation_id = Column(Integer, ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Identificación
    message_id = Column(String(255), nullable=False, index=True)
    
    # Contenido
    user_message = Column(Text)
    bot_response = Column(Text)
    
    # ML/NLP
    intent_detected = Column(String(100), index=True)
    entities_extracted = Column(JSONB, default={})
    confidence_score = Column(Float)
    
    # Métricas
    processing_time_ms = Column(Integer)
    
    # Relaciones
    user = relationship("User", backref="messages")
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<MessageHistory(id={self.id}, user_id={self.user_id}, intent={self.intent_detected})>"