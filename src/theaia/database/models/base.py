"""
Base Model para todos los modelos de la base de datos.
Incluye campos comunes: id, tenant_id, created_at, updated_at
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    """
    Modelo base del que heredan todos los modelos.
    
    Campos comunes:
    - id: Primary key autoincremental
    - tenant_id: Identificador de tenant para multi-tenancy
    - created_at: Timestamp de creación
    - updated_at: Timestamp de última actualización
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, default='default', index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, tenant_id={self.tenant_id})>"
