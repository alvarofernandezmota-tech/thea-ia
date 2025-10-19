"""
Estados base del sistema conversacional de Thea IA.
Estos estados son comunes a todos los agentes.
"""

from enum import Enum

class ConversationState(str, Enum):
    """Estados principales de cualquier conversación."""
    
    # Estados generales
    IDLE = "idle"
    ACTIVE = "active"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    AWAITING_CANCELLATION = "awaiting_cancellation"
    TASK_COMPLETED = "task_completed"
    ERROR = "error"
    
    # Estados de recopilación de información
    GATHERING_INFO = "gathering_info"
    VALIDATING_INPUT = "validating_input"
    
    # Estados de finalización
    SUCCESS = "success"
    CANCELLED = "cancelled"
