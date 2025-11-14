"""
Modelo User - Usuario del sistema THEA IA
Almacena información de usuarios de Telegram y sus preferencias
VERSIÓN CORREGIDA H02 - Multi-tenant UNIQUE constraint
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel


class User(BaseModel):
    """
    Usuario de THEA IA.
    
    Campos principales:
    - telegram_id: ID único de Telegram (unique per tenant)
    - username: Username de Telegram
    - first_name, last_name: Nombre del usuario
    - language_code: Idioma preferido (es, en, etc)
    - timezone: Zona horaria del usuario
    - is_active: Si el usuario está activo
    - preferences: Configuraciones personalizadas (JSONB)
    """
    __tablename__ = 'users'
    
    # Campos Telegram
    telegram_id = Column(BigInteger, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    # Configuración
    language_code = Column(String(10), default='es')
    timezone = Column(String(50), default='UTC')
    is_active = Column(Boolean, default=True, index=True)
    
    # Preferencias personalizadas (JSON)
    preferences = Column(JSONB, default={})
    
    # Relaciones
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    
    # Multi-tenant constraint: telegram_id único POR tenant
    __table_args__ = (
        UniqueConstraint('tenant_id', 'telegram_id', name='uq_user_tenant_telegram'),
        {'extend_existing': True}
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"