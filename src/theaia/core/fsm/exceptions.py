"""
FSM Custom Exceptions - Centralized Error Handling
H03 FASE 1 - BLOQUE 1.4 - Core FSM Exception System

This module provides comprehensive exception handling for the THEA IA FSM.
All state machine errors inherit from FSMException and include context
information for debugging and error recovery.

Version: 1.2.0
Last Updated: 09-Dec-2025
Status: Production Ready - THEA IA Compatible
"""

import logging
from typing import Optional, Dict, Any, List, Type
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ErrorCategory(Enum):
    """Error categorization for systematic handling."""
    STATE_ERROR = "state_error"
    TRANSITION_ERROR = "transition_error"
    CALLBACK_ERROR = "callback_error"
    CONTEXT_ERROR = "context_error"
    SESSION_ERROR = "session_error"
    CONFIGURATION_ERROR = "configuration_error"
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Error severity levels for prioritization."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# BASE EXCEPTION
# ============================================================================

class FSMException(Exception):
    """
    Base exception for all FSM errors.

    Provides foundation for all FSM-related exceptions with centralized
    error tracking, context preservation, and user ID association.
    """

    ERROR_CODE_PREFIX = "FSM"
    CATEGORY = ErrorCategory.UNKNOWN
    SEVERITY = ErrorSeverity.MEDIUM
    _error_counter = {}

    def __init__(
        self,
        message: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        category: Optional[ErrorCategory] = None,
        severity: Optional[ErrorSeverity] = None,
        cause: Optional[Exception] = None,
        recommendations: Optional[List[str]] = None
    ):
        """Initialize FSM exception."""
        self.message = message
        self.user_id = user_id
        self.context = context or {}
        self.category = category or self.CATEGORY
        self.severity = severity or self.SEVERITY
        self.cause = cause
        self.recommendations = recommendations or []
        self.timestamp = datetime.now()
        self.error_code = error_code or self._generate_error_code()

        self._log_exception()
        super().__init__(self._format_message())

    def _generate_error_code(self) -> str:
        """Generate unique error code."""
        class_name = self.__class__.__name__
        if class_name not in self._error_counter:
            self._error_counter[class_name] = 0

        self._error_counter[class_name] += 1
        code_num = self._error_counter[class_name]

        return "{}_{}_{:04d}".format(self.ERROR_CODE_PREFIX, class_name, code_num)

    def _format_message(self) -> str:
        """Format comprehensive error message."""
        parts = []
        parts.append("[{}] [{}]".format(self.error_code, self.category.value))

        if self.user_id:
            parts.append("[user:{}]".format(self.user_id))

        parts.append(self.message)

        return " ".join(parts)

    def _log_exception(self):
        """Log exception based on severity."""
        log_message = (
            "FSM Exception: {} | Category: {} | Severity: {} | User: {} | Message: {}"
        ).format(
            self.error_code,
            self.category.value,
            self.severity.value,
            self.user_id,
            self.message
        )

        if self.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif self.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif self.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        if self.recommendations:
            logger.info("Recommendations: {}".format("; ".join(self.recommendations)))

    def to_dict(self) -> Dict[str, Any]:
        """Export exception as dictionary for APIs."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "user_id": self.user_id,
            "context": self.context.copy(),
            "timestamp": self.timestamp.isoformat(),
            "recommendations": self.recommendations
        }

    def get_context(self, key: str = None, default: Any = None) -> Any:
        """Get context value or entire context."""
        if key is None:
            return self.context.copy()
        return self.context.get(key, default)


# ============================================================================
# STATE-RELATED EXCEPTIONS
# ============================================================================

class StateError(FSMException):
    """Base class for state-related errors."""
    CATEGORY = ErrorCategory.STATE_ERROR
    SEVERITY = ErrorSeverity.HIGH


class InvalidStateError(StateError):
    """Raised when attempting to use an invalid state."""

    def __init__(
        self,
        state: str,
        valid_states: List[str],
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize invalid state error."""
        self.state = state
        self.valid_states = valid_states

        message = (
            "Invalid state '{}'. Valid states: {}"
        ).format(state, ", ".join(valid_states))

        recommendations = [
            "Use one of the valid states",
            "Check state name for typos",
            "Ensure state is properly registered"
        ]

        error_context = context or {}
        error_context.update({
            "invalid_state": state,
            "valid_states": valid_states
        })

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.STATE_ERROR,
            severity=ErrorSeverity.HIGH,
            recommendations=recommendations
        )


class TerminalStateError(StateError):
    """Raised when attempting transition from terminal state."""

    def __init__(
        self,
        state: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize terminal state error."""
        self.state = state

        message = "Cannot transition from terminal state '{}'".format(state)

        recommendations = [
            "Reset the state machine",
            "Create new session instead",
            "Check if '{}' should be terminal".format(state)
        ]

        error_context = context or {}
        error_context.update({"terminal_state": state})

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.STATE_ERROR,
            severity=ErrorSeverity.HIGH,
            recommendations=recommendations
        )


class DuplicateStateError(StateError):
    """Raised when attempting to register duplicate state."""

    def __init__(
        self,
        state: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize duplicate state error."""
        self.state = state

        message = "State '{}' already exists".format(state)

        recommendations = [
            "Use different name for new state",
            "Check if '{}' is registered".format(state),
            "Review state initialization"
        ]

        error_context = context or {}
        error_context.update({"duplicate_state": state})

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.STATE_ERROR,
            severity=ErrorSeverity.MEDIUM,
            recommendations=recommendations
        )


# ============================================================================
# TRANSITION-RELATED EXCEPTIONS
# ============================================================================

class TransitionError(FSMException):
    """Base class for transition-related errors."""
    CATEGORY = ErrorCategory.TRANSITION_ERROR
    SEVERITY = ErrorSeverity.HIGH


class InvalidTransitionError(TransitionError):
    """Raised when attempting invalid state transition."""

    def __init__(
        self,
        from_state: str,
        to_state: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize invalid transition error."""
        self.from_state = from_state
        self.to_state = to_state

        message = "Invalid transition: '{}' -> '{}'".format(from_state, to_state)

        recommendations = [
            "Check if transition is registered",
            "Verify both states exist",
            "Review transition config"
        ]

        error_context = context or {}
        error_context.update({
            "from_state": from_state,
            "to_state": to_state
        })

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.TRANSITION_ERROR,
            severity=ErrorSeverity.HIGH,
            recommendations=recommendations
        )


class TransitionNotAllowedError(TransitionError):
    """Raised when trigger is not available from current state."""

    def __init__(
        self,
        trigger: str,
        current_state: str,
        valid_triggers: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize transition not allowed error."""
        self.trigger = trigger
        self.current_state = current_state
        self.valid_triggers = valid_triggers or []

        valid_triggers_str = ", ".join(self.valid_triggers) if self.valid_triggers else "none"
        message = (
            "Trigger '{}' not allowed from '{}'. Valid: [{}]"
        ).format(trigger, current_state, valid_triggers_str)

        recommendations = [
            "Use valid trigger from current state",
            "Check current state",
            "Call get_valid_transitions_set()"
        ]

        error_context = context or {}
        error_context.update({
            "trigger": trigger,
            "current_state": current_state,
            "valid_triggers": self.valid_triggers
        })

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.TRANSITION_ERROR,
            severity=ErrorSeverity.MEDIUM,
            recommendations=recommendations
        )


# ============================================================================
# CALLBACK-RELATED EXCEPTIONS
# ============================================================================

class CallbackError(FSMException):
    """Base class for callback-related errors."""
    CATEGORY = ErrorCategory.CALLBACK_ERROR
    SEVERITY = ErrorSeverity.HIGH


class CallbackExecutionError(CallbackError):
    """Raised when callback execution fails."""

    def __init__(
        self,
        callback_name: str,
        trigger: str,
        original_error: Exception,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize callback execution error."""
        self.callback_name = callback_name
        self.trigger = trigger
        self.original_error = original_error

        message = (
            "Callback '{}' failed during '{}': {}"
        ).format(callback_name, trigger, type(original_error).__name__)

        recommendations = [
            "Check callback implementation",
            "Verify data available during trigger",
            "Handle exception in callback"
        ]

        error_context = context or {}
        error_context.update({
            "callback_name": callback_name,
            "trigger": trigger,
            "original_error_type": type(original_error).__name__
        })

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.CALLBACK_ERROR,
            severity=ErrorSeverity.HIGH,
            cause=original_error,
            recommendations=recommendations
        )


# ============================================================================
# CONTEXT-RELATED EXCEPTIONS
# ============================================================================

class ContextError(FSMException):
    """Base class for context-related errors."""
    CATEGORY = ErrorCategory.CONTEXT_ERROR
    SEVERITY = ErrorSeverity.MEDIUM


class ContextMergingError(ContextError):
    """Raised when context merging fails."""

    def __init__(
        self,
        strategy: str,
        reason: str,
        valid_strategies: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize context merging error."""
        self.strategy = strategy
        self.reason = reason
        self.valid_strategies = valid_strategies or ["merge", "replace"]

        message = (
            "Context merge failed with strategy '{}': {}"
        ).format(strategy, reason)

        recommendations = [
            "Use valid strategy",
            "Check context data types",
            "Ensure new_context is dict"
        ]

        error_context = context or {}
        error_context.update({
            "strategy": strategy,
            "reason": reason,
            "valid_strategies": self.valid_strategies
        })

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.CONTEXT_ERROR,
            severity=ErrorSeverity.MEDIUM,
            recommendations=recommendations
        )


class ContextValidationError(ContextError):
    """Raised when context validation fails."""

    def __init__(
        self,
        validation_failed: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize context validation error."""
        self.validation_failed = validation_failed

        message = "Context validation failed: {}".format(validation_failed)

        recommendations = [
            "Check data types and values",
            "Verify required fields present",
            "Validate before calling merge"
        ]

        error_context = context or {}
        error_context.update({"validation_failed": validation_failed})

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.CONTEXT_ERROR,
            severity=ErrorSeverity.MEDIUM,
            recommendations=recommendations
        )


# ============================================================================
# SESSION-RELATED EXCEPTIONS
# ============================================================================

class SessionError(FSMException):
    """Base class for session-related errors."""
    CATEGORY = ErrorCategory.SESSION_ERROR
    SEVERITY = ErrorSeverity.HIGH


class ConversationTimeoutError(SessionError):
    """Raised when conversation times out."""

    def __init__(
        self,
        timeout_seconds: int,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize conversation timeout error."""
        self.timeout_seconds = timeout_seconds

        message = "Conversation timeout after {} seconds".format(timeout_seconds)

        recommendations = [
            "Create new session",
            "Increase timeout if needed",
            "Check network connectivity"
        ]

        error_context = context or {}
        error_context.update({"timeout_seconds": timeout_seconds})

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.SESSION_ERROR,
            severity=ErrorSeverity.MEDIUM,
            recommendations=recommendations
        )


class SessionNotFoundError(SessionError):
    """Raised when session cannot be found."""

    def __init__(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize session not found error."""
        self.session_id = session_id

        message = "Session '{}' not found".format(session_id)

        recommendations = [
            "Verify session ID",
            "Create new session",
            "Check session storage"
        ]

        error_context = context or {}
        error_context.update({"session_id": session_id})

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.SESSION_ERROR,
            severity=ErrorSeverity.HIGH,
            recommendations=recommendations
        )


# ============================================================================
# CONFIGURATION-RELATED EXCEPTIONS
# ============================================================================

class ConfigurationError(FSMException):
    """Base class for configuration-related errors."""
    CATEGORY = ErrorCategory.CONFIGURATION_ERROR
    SEVERITY = ErrorSeverity.CRITICAL


class MissingConfigurationError(ConfigurationError):
    """Raised when required configuration is missing."""

    def __init__(
        self,
        missing_key: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize missing configuration error."""
        self.missing_key = missing_key

        message = "Missing configuration: '{}'".format(missing_key)

        recommendations = [
            "Define '{}'".format(missing_key),
            "Check class initialization",
            "Review configuration docs"
        ]

        error_context = context or {}
        error_context.update({"missing_key": missing_key})

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.CONFIGURATION_ERROR,
            severity=ErrorSeverity.CRITICAL,
            recommendations=recommendations
        )


class InvalidConfigurationError(ConfigurationError):
    """Raised when configuration is invalid."""

    def __init__(
        self,
        config_key: str,
        reason: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize invalid configuration error."""
        self.config_key = config_key
        self.reason = reason

        message = "Invalid config '{}': {}".format(config_key, reason)

        recommendations = [
            "Fix configuration",
            "Review validation rules",
            "Check format and types"
        ]

        error_context = context or {}
        error_context.update({
            "config_key": config_key,
            "reason": reason
        })

        super().__init__(
            message,
            user_id=user_id,
            context=error_context,
            category=ErrorCategory.CONFIGURATION_ERROR,
            severity=ErrorSeverity.CRITICAL,
            recommendations=recommendations
        )


# ============================================================================
# EXCEPTION REGISTRY
# ============================================================================

EXCEPTION_REGISTRY = {
    "InvalidStateError": InvalidStateError,
    "TerminalStateError": TerminalStateError,
    "DuplicateStateError": DuplicateStateError,
    "InvalidTransitionError": InvalidTransitionError,
    "TransitionNotAllowedError": TransitionNotAllowedError,
    "CallbackExecutionError": CallbackExecutionError,
    "ContextMergingError": ContextMergingError,
    "ContextValidationError": ContextValidationError,
    "ConversationTimeoutError": ConversationTimeoutError,
    "SessionNotFoundError": SessionNotFoundError,
    "MissingConfigurationError": MissingConfigurationError,
    "InvalidConfigurationError": InvalidConfigurationError,
}


def get_exception_class(exception_name: str) -> Optional[Type[FSMException]]:
    """Get exception class by name."""
    return EXCEPTION_REGISTRY.get(exception_name)