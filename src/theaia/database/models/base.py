"""
BaseModel - Modelo base para todas las entidades
Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025 (Actualizado: 19 Nov 2025)
Hito: H02 - Database Layer
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    Clase base abstracta para todos los modelos.
    
    Proporciona:
    - ID autoincremental
    - Tenant ID (multi-tenant obligatorio)
    - Timestamps automáticos (created_at, updated_at)
    
    Todos los modelos deben heredar de esta clase.
    """
    __abstract__ = True
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Multi-tenant (obligatorio en TODAS las tablas)
    tenant_id = Column(String(100), nullable=False, index=True)
    
    # ✅ FIX CRÍTICO: default Python con lambda funciona con async
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
