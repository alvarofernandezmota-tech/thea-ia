"""
Base Model para todos los modelos de la base de datos.
Incluye campos comunes: id, tenant_id, created_at, updated_at

IMPORTANTE: created_at y updated_at son timezone-aware (UTC).
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    """
    Modelo base del que heredan todos los modelos.
    
    Campos comunes:
    - id: Primary key autoincremental
    - tenant_id: Identificador de tenant para multi-tenancy
    - created_at: Timestamp de creación (timezone-aware UTC)
    - updated_at: Timestamp de última actualización (timezone-aware UTC)
    
    NOTA CRÍTICA:
    - DateTime(timezone=True) almacena TIMESTAMPTZ en PostgreSQL
    - lambda: datetime.now(timezone.utc) garantiza timezone-aware
    - Evita comparaciones naive vs aware datetime
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, default='default', index=True)
    
    # ✅ TIMEZONE-AWARE: DateTime(timezone=True) + lambda datetime.now(timezone.utc)
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    def to_dict(self):
        """Convierte el modelo a diccionario."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, tenant_id={self.tenant_id})>"
