# src/theaia/core/fsm/__init__.py

"""
FSM (Finite State Machine) Module para Thea IA 2.0
"""

from .state_machine import BaseStateMachine, ConversationStateMachine
from .states.global_states import (
    GlobalState, 
    StateDescriptions, 
    StateValidation,
    AgentStates
)
from .transitions import TransitionConfig

__version__ = "2.0.0"

__all__ = [
    'BaseStateMachine', 
    'ConversationStateMachine',
    'GlobalState',
    'StateDescriptions',
    'StateValidation',
    'AgentStates',
    'TransitionConfig'
]

def create_conversation_fsm(user_id: str) -> ConversationStateMachine:
    """Factory para crear ConversationStateMachine"""
    return ConversationStateMachine(user_id)

def validate_state_transition(from_state: str, to_state: str) -> bool:
    """Valida transición de estado"""
    try:
        from_enum = GlobalState(from_state)
        to_enum = GlobalState(to_state)
        return StateValidation.is_valid_transition(from_enum, to_enum)
    except ValueError:
        return False

# Configuración por defecto
DEFAULT_CONFIG = {
    'session_timeout_minutes': 30,
    'disambiguation_timeout_minutes': 5,
    'max_disambiguation_retries': 3
}
