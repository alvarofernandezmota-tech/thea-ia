"""
Modelo MessageHistory - Historial completo de mensajes
Almacena todos los mensajes y respuestas para auditoría
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel

class MessageHistory(BaseModel):
    """
    Historial de mensajes de una conversación.
    
    Campos principales:
    - message_id: ID único del mensaje
    - user_message: Mensaje del usuario
    - bot_response: Respuesta del bot
    - intent_detected: Intent clasificado por ML
    - entities_extracted: Entidades extraídas (JSON)
    - confidence_score: Confianza del clasificador
    - processing_time_ms: Tiempo de procesamiento
    """
    __tablename__ = 'message_history'
    
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
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<MessageHistory(id={self.id}, intent={self.intent_detected}, confidence={self.confidence_score})>"
