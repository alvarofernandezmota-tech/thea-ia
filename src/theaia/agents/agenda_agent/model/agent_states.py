"""
AgendaAgent State Definitions
Estados para FSM v2.0 del AgendaAgent

Responsable: Álvaro Fernández Mota (CEO THEA IA)
Fecha: 21 Noviembre 2025
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
"""

from enum import Enum
from typing import List


class AgendaStates(str, Enum):
    """
    Estados del AgendaAgent FSM v2.0
    
    15 estados que manejan 6 flujos completos:
    - CREAR evento
    - LISTAR eventos
    - EDITAR evento
    - ELIMINAR evento
    - BUSCAR eventos
    - CANCELAR operación
    """
    
    # Estado inicial/reposo
    IDLE = "idle"
    
    # FLUJO 1: Crear evento
    AWAITING_TITLE = "awaiting_title"
    AWAITING_DATE = "awaiting_date"
    AWAITING_TIME = "awaiting_time"
    AWAITING_LOCATION = "awaiting_location"
    PROCESSING = "processing"
    EVENT_SAVED = "event_saved"
    
    # FLUJO 2: Listar eventos
    LISTING_EVENTS = "listing_events"
    
    # FLUJO 3: Editar evento
    SELECTING_EVENT = "selecting_event"
    EDITING_FIELD = "editing_field"
    EVENT_UPDATED = "event_updated"
    
    # FLUJO 4: Eliminar evento
    DELETING_EVENT = "deleting_event"
    CONFIRMING_DELETE = "confirming_delete"
    EVENT_DELETED = "event_deleted"
    
    # FLUJO 5: Buscar eventos
    SEARCHING_EVENTS = "searching_events"
    
    # FLUJO 6: Cancelar
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
            cls.AWAITING_TITLE.value,
            cls.AWAITING_DATE.value,
            cls.AWAITING_TIME.value,
            cls.AWAITING_LOCATION.value,
            cls.PROCESSING.value,
            cls.EVENT_SAVED.value
        ]
    
    @classmethod
    def edit_states(cls) -> List[str]:
        """
        Retorna estados del flujo de edición.
        
        Returns:
            Lista de estados de edición
        """
        return [
            cls.SELECTING_EVENT.value,
            cls.EDITING_FIELD.value,
            cls.PROCESSING.value,
            cls.EVENT_UPDATED.value
        ]
    
    @classmethod
    def delete_states(cls) -> List[str]:
        """
        Retorna estados del flujo de eliminación.
        
        Returns:
            Lista de estados de eliminación
        """
        return [
            cls.DELETING_EVENT.value,
            cls.CONFIRMING_DELETE.value,
            cls.EVENT_DELETED.value
        ]
