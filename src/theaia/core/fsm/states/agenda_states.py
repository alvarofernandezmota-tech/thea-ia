"""
Estados específicos del AgendaAgent.
"""

from enum import Enum

class AgendaState(str, Enum):
    """Estados del flujo de agendamiento."""
    
    # Estados de recopilación
    AWAITING_DATETIME = "awaiting_datetime"
    AWAITING_DESCRIPTION = "awaiting_description"
    AWAITING_ATTENDEES = "awaiting_attendees"
    AWAITING_LOCATION = "awaiting_location"
    
    # Estados de validación
    VALIDATING_DATETIME = "validating_datetime"
    CHECKING_CONFLICTS = "checking_conflicts"
    
    # Estados de confirmación
    READY_TO_SAVE = "ready_to_save"
    SAVING_EVENT = "saving_event"
    EVENT_SAVED = "event_saved"
