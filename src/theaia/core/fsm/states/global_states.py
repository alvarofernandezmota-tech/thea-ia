# src/theaia/core/fsm/states/global_states.py

from enum import Enum
from typing import Dict, Any, List

class GlobalState(Enum):
    """Estados globales del sistema Thea IA 2.0"""
    
    INITIAL = "initial"
    AWAITING_DISAMBIGUATION = "awaiting_disambiguation"
    AGENT_DELEGATED = "agent_delegated" 
    SESSION_TIMEOUT = "session_timeout"
    ERROR_STATE = "error_state"
    COMPLETED = "completed"

class StateDescriptions:
    """Descripciones de cada estado global"""
    
    DESCRIPTIONS = {
        GlobalState.INITIAL: {
            "description": "Estado inicial de cualquier conversación",
            "entry_conditions": ["Nueva conversación", "Reset desde cualquier estado"],
            "exit_conditions": ["Intent claro detectado", "Ambigüedad detectada"],
            "allowed_actions": ["detect_intent", "request_disambiguation", "delegate_to_agent"]
        },
        
        GlobalState.AWAITING_DISAMBIGUATION: {
            "description": "Esperando aclaración del usuario",
            "entry_conditions": ["Múltiples intents detectados", "Intent ambiguo"],
            "exit_conditions": ["Usuario elige opción", "Timeout", "Error"],
            "allowed_actions": ["parse_user_choice", "resolve_disambiguation", "timeout"]
        },
        
        GlobalState.AGENT_DELEGATED: {
            "description": "Conversación derivada a agente específico",
            "entry_conditions": ["Intent claro", "Desambiguación resuelta"],
            "exit_conditions": ["Tarea completada", "Nueva conversación", "Error"],
            "allowed_actions": ["process_with_agent", "complete_conversation", "reset"]
        },
        
        GlobalState.SESSION_TIMEOUT: {
            "description": "Sesión expirada por inactividad",
            "entry_conditions": ["Timeout desde cualquier estado"],
            "exit_conditions": ["Usuario retoma conversación"],
            "allowed_actions": ["reset", "log_timeout"]
        },
        
        GlobalState.ERROR_STATE: {
            "description": "Estado de error recuperable",
            "entry_conditions": ["Error en procesamiento", "Estado inválido"],
            "exit_conditions": ["Error resuelto", "Reset manual"],
            "allowed_actions": ["handle_error", "reset", "log_error"]
        },
        
        GlobalState.COMPLETED: {
            "description": "Conversación completada exitosamente",
            "entry_conditions": ["Tarea finalizada por agente"],
            "exit_conditions": ["Nueva conversación iniciada"],
            "allowed_actions": ["reset", "log_completion"]
        }
    }

class StateValidation:
    """Validación de transiciones"""
    
    VALID_TRANSITIONS = {
        GlobalState.INITIAL: [
            GlobalState.AWAITING_DISAMBIGUATION,
            GlobalState.AGENT_DELEGATED,
            GlobalState.ERROR_STATE,
            GlobalState.SESSION_TIMEOUT
        ],
        
        GlobalState.AWAITING_DISAMBIGUATION: [
            GlobalState.AGENT_DELEGATED,
            GlobalState.ERROR_STATE,
            GlobalState.SESSION_TIMEOUT,
            GlobalState.INITIAL
        ],
        
        GlobalState.AGENT_DELEGATED: [
            GlobalState.COMPLETED,
            GlobalState.INITIAL,
            GlobalState.ERROR_STATE,
            GlobalState.SESSION_TIMEOUT
        ],
        
        GlobalState.SESSION_TIMEOUT: [
            GlobalState.INITIAL
        ],
        
        GlobalState.ERROR_STATE: [
            GlobalState.INITIAL,
            GlobalState.SESSION_TIMEOUT
        ],
        
        GlobalState.COMPLETED: [
            GlobalState.INITIAL
        ]
    }
    
    @classmethod
    def is_valid_transition(cls, from_state: GlobalState, to_state: GlobalState) -> bool:
        """Valida si una transición es permitida"""
        return to_state in cls.VALID_TRANSITIONS.get(from_state, [])
    
    @classmethod
    def get_valid_next_states(cls, current_state: GlobalState) -> List[GlobalState]:
        """Obtiene estados válidos desde el estado actual"""
        return cls.VALID_TRANSITIONS.get(current_state, [])

class AgentStates:
    """Estados relacionados con agentes específicos"""
    
    AGENT_MAPPING = {
        "notas": "NoteAgent",
        "agenda": "AgendaAgent", 
        "recordatorio": "ReminderAgent",
        "event": "EventAgent",
        "help": "HelpAgent",
        "query": "QueryAgent",
        "scheduler": "SchedulerAgent",
        "fallback": "FallbackAgent"
    }
    
    @classmethod
    def get_agent_class(cls, intent: str) -> str:
        """Obtiene clase de agente para un intent"""
        return cls.AGENT_MAPPING.get(intent, "FallbackAgent")

# Exportaciones
__all__ = [
    'GlobalState',
    'StateDescriptions', 
    'StateValidation',
    'AgentStates'
]
