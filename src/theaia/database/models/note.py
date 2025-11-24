"""
Note Model — Modelo de nota con timezone-aware datetimes y relationship bidireccional
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.theaia.database.models.base import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, nullable=False, index=True)
    
    # ✨ ForeignKey hacia users.id
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    tags = Column(ARRAY(String), nullable=True, default=[])
    is_pinned = Column(Boolean, default=False, nullable=False)
    
    # ✨ timezone=True para datetime aware
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
    
    # ✨ CRÍTICO: Relationship bidireccional (faltaba esto!)
    user = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}', user_id={self.user_id})>"
