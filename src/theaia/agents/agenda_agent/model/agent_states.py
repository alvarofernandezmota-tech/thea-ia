"""
AgendaAgent State Definitions
Estados para FSM v2.0 del AgendaAgent

Responsable: Álvaro Fernández Mota (CEO THEA IA)
Fecha: 21 Noviembre 2025 (Actualizado 04 Dic 2025)
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
"""

from enum import Enum
from typing import List


class AgentState(str, Enum):
    """
    Estados del AgendaAgent FSM v2.0
    
    Estados principales:
    - IDLE: Estado inicial/reposo
    - AWAITING_*: Esperando información del usuario
    - PROCESSING: Procesando acción
    - COMPLETED: Acción completada
    - ERROR: Error en proceso
    """
    
    # Estado inicial/reposo
    IDLE = "idle"
    
    # Estados de espera de información
    AWAITING_EVENT_DETAILS = "awaiting_event_details"
    AWAITING_TIME = "awaiting_time"
    AWAITING_EVENT_SELECTION = "awaiting_event_selection"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    
    # Estados de procesamiento
    PROCESSING = "processing"
    
    # Estados finales
    COMPLETED = "completed"
    ERROR = "error"
    
    # Estados legacy (para compatibilidad con FSM v2.0)
    AWAITING_TITLE = "awaiting_title"
    AWAITING_DATE = "awaiting_date"
    AWAITING_LOCATION = "awaiting_location"
    EVENT_SAVED = "event_saved"
    LISTING_EVENTS = "listing_events"
    SELECTING_EVENT = "selecting_event"
    EDITING_FIELD = "editing_field"
    EVENT_UPDATED = "event_updated"
    DELETING_EVENT = "deleting_event"
    CONFIRMING_DELETE = "confirming_delete"
    EVENT_DELETED = "event_deleted"
    SEARCHING_EVENTS = "searching_events"
    CANCELLED = "cancelled"
    
    @classmethod
    def all_states(cls) -> List[str]:
        """
        Retorna todos los estados como lista.
        
        Returns:
            Lista de todos los estados
        """
        return [state.value for state in cls]
    
    @classmethod
    def creation_states(cls) -> List[str]:
        """
        Retorna estados del flujo de creación.
        
        Returns:
            Lista de estados de creación
        """
        return [
            cls.AWAITING_EVENT_DETAILS.value,
            cls.AWAITING_TIME.value,
            cls.PROCESSING.value,
            cls.COMPLETED.value
        ]
    
    @classmethod
    def edit_states(cls) -> List[str]:
        """
        Retorna estados del flujo de edición.
        
        Returns:
            Lista de estados de edición
        """
        return [
            cls.AWAITING_EVENT_SELECTION.value,
            cls.AWAITING_EVENT_DETAILS.value,
            cls.PROCESSING.value,
            cls.COMPLETED.value
        ]
    
    @classmethod
    def delete_states(cls) -> List[str]:
        """
        Retorna estados del flujo de eliminación.
        
        Returns:
            Lista de estados de eliminación
        """
        return [
            cls.AWAITING_EVENT_SELECTION.value,
            cls.AWAITING_CONFIRMATION.value,
            cls.PROCESSING.value,
            cls.COMPLETED.value
        ]


# Alias para compatibilidad con código legacy
AgendaStates = AgentState
