"""
FSM Custom Exceptions - Centralized error handling
H03 FASE 1 - BLOQUE 1.2 - TAREA 1.2.2
"""

from typing import Optional


class FSMException(Exception):
    """Base exception for all FSM errors"""
    
    def __init__(self, message: str, user_id: Optional[str] = None, context: Optional[dict] = None):
        self.message = message
        self.user_id = user_id
        self.context = context or {}
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.user_id:
            return f"[{self.user_id}] {self.message}"
        return self.message


class InvalidTransitionError(FSMException):
    """Raised when attempting invalid state transition"""
    
    def __init__(self, from_state: str, to_state: str, user_id: Optional[str] = None):
        self.from_state = from_state
        self.to_state = to_state
        message = f"Invalid transition: {from_state} → {to_state}"
        super().__init__(message, user_id)


class InvalidStateError(FSMException):
    """Raised when attempting to use invalid state"""
    
    def __init__(self, state: str, valid_states: list, user_id: Optional[str] = None):
        self.state = state
        self.valid_states = valid_states
        message = f"Invalid state '{state}'. Valid states: {', '.join(valid_states)}"
        super().__init__(message, user_id)


class TerminalStateError(FSMException):
    """Raised when attempting transition from terminal state"""
    
    def __init__(self, state: str, user_id: Optional[str] = None):
        self.state = state
        message = f"Cannot transition from terminal state '{state}'"
        super().__init__(message, user_id)


class TransitionNotAllowedError(FSMException):
    """Raised when trigger is not available in current state"""
    
    def __init__(self, trigger: str, current_state: str, user_id: Optional[str] = None):
        self.trigger = trigger
        self.current_state = current_state
        message = f"Trigger '{trigger}' not allowed from state '{current_state}'"
        super().__init__(message, user_id)


class CallbackExecutionError(FSMException):
    """Raised when callback execution fails"""
    
    def __init__(self, callback_name: str, trigger: str, original_error: Exception, user_id: Optional[str] = None):
        self.callback_name = callback_name
        self.trigger = trigger
        self.original_error = original_error
        message = f"Callback '{callback_name}' failed during '{trigger}': {str(original_error)}"
        super().__init__(message, user_id)


class ContextMergingError(FSMException):
    """Raised when context merging fails"""
    
    def __init__(self, strategy: str, reason: str, user_id: Optional[str] = None):
        self.strategy = strategy
        self.reason = reason
        message = f"Context merging failed with strategy '{strategy}': {reason}"
        super().__init__(message, user_id)


class ConversationTimeoutError(FSMException):
    """Raised when conversation times out"""
    
    def __init__(self, timeout_seconds: int, user_id: Optional[str] = None):
        self.timeout_seconds = timeout_seconds
        message = f"Conversation timeout after {timeout_seconds} seconds"
        super().__init__(message, user_id)
