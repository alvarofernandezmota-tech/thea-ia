"""
Modelo Note - Notas y apuntes del usuario
Almacena notas, ideas, listas, con categorías y tags
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel

class Note(BaseModel):
    """
    Nota del usuario.
    
    Campos principales:
    - title: Título de la nota
    - content: Contenido (texto largo)
    - category: Categoría (general, work, personal, etc)
    - tags: Lista de etiquetas
    - priority: Prioridad (1=baja, 2=media, 3=alta)
    - is_pinned: Si está fijada
    - reminder_datetime: Recordatorio asociado (opcional)
    """
    __tablename__ = 'notes'
    
    # Relación con usuario
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Contenido
    title = Column(String(500))
    content = Column(Text, nullable=False)
    
    # Organización
    category = Column(String(100), default='general', index=True)
    tags = Column(ARRAY(Text), default=[])
    
    # Prioridad y estado
    priority = Column(Integer, default=1)
    is_pinned = Column(Boolean, default=False, index=True)
    
    # Recordatorio opcional
    reminder_datetime = Column(DateTime(timezone=True))
    
    # Metadatos adicionales
    extra_data = Column(JSONB, default={})

    
    # Relaciones
    user = relationship("User", back_populates="notes")
    
    def __repr__(self):
        return f"<Note(id={self.id}, title={self.title}, category={self.category})>"
