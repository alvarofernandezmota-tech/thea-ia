"""
Schemas para AgendaAgent
Exporta todos los schemas Pydantic
"""

from .event_schema import (
    EventBase,
    EventCreate,
    EventUpdate,
    EventResponse,
    EventListResponse
)

__all__ = [
    "EventBase",
    "EventCreate",
    "EventUpdate",
    "EventResponse",
    "EventListResponse"
]
