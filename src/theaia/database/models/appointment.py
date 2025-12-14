"""
Appointment Model - Database model for appointments
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel


class Appointment(BaseModel):
    """Appointment model for storing user appointments."""
    
    __tablename__ = "appointments"
    
    # Foreign key to User
    user_id = Column(String, ForeignKey('users.telegram_id'), nullable=False, index=True)
    
    # Appointment details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    
    # Status: scheduled, cancelled, completed
    status = Column(String(20), nullable=False, default="scheduled", index=True)
    
    # Cancellation details
    cancellation_reason = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="appointments")
    
    def __repr__(self):
        return f"<Appointment(id={self.id}, title='{self.title}', start={self.start_time}, status='{self.status}')>"
