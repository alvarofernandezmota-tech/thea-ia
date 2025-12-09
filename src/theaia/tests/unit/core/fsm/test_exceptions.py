"""
Tests for FSM Exception System
H03 FASE 1 - BLOQUE 1.4 - Exception Testing

Tests para validar todas las excepciones personalizadas del FSM.
"""

import pytest
import logging
from datetime import datetime

# Importar las excepciones a testear
from theaia.core.fsm.exceptions import (
    FSMException,
    ErrorCategory,
    ErrorSeverity,
    InvalidStateError,
    TerminalStateError,
    DuplicateStateError,
    InvalidTransitionError,
    TransitionNotAllowedError,
    CallbackExecutionError,
    ContextMergingError,
    ContextValidationError,
    ConversationTimeoutError,
    SessionNotFoundError,
    MissingConfigurationError,
    InvalidConfigurationError,
    get_exception_class,
    EXCEPTION_REGISTRY
)


# ============================================================================
# TEST CLASSES
# ============================================================================


class TestFSMException:
    """Tests for base FSMException class."""

    def test_initialization(self):
        """Test basic exception initialization."""
        exc = FSMException(
            message="Test error",
            user_id="user123"
        )

        assert exc.message == "Test error"
        assert exc.user_id == "user123"
        assert exc.error_code.startswith("FSM_FSMException")
        assert exc.category == ErrorCategory.UNKNOWN
        assert exc.severity == ErrorSeverity.MEDIUM

    def test_error_code_generation(self):
        """Test unique error code generation."""
        # RESETEAR contador para test aislado
        FSMException._error_counter = {}
        
        exc1 = FSMException("Error 1", user_id="user1")
        exc2 = FSMException("Error 2", user_id="user2")

        assert exc1.error_code != exc2.error_code
        assert "0001" in exc1.error_code
        assert "0002" in exc2.error_code

    def test_context_preservation(self):
        """Test context dictionary preservation."""
        context_data = {"key1": "value1", "key2": "value2"}
        exc = FSMException(
            message="Test",
            context=context_data
        )

        assert exc.context == context_data
        assert exc.get_context("key1") == "value1"
        assert exc.get_context("key2") == "value2"

    def test_get_full_context(self):
        """Test getting full context."""
        context_data = {"key1": "value1"}
        exc = FSMException(message="Test", context=context_data)

        full_context = exc.get_context()
        assert isinstance(full_context, dict)
        assert full_context == context_data

    def test_to_dict_export(self):
        """Test exporting exception as dictionary."""
        exc = FSMException(
            message="Test error",
            user_id="user123",
            context={"data": "test"}
        )

        exc_dict = exc.to_dict()

        assert "error_code" in exc_dict
        assert exc_dict["message"] == "Test error"
        assert exc_dict["user_id"] == "user123"
        assert exc_dict["context"]["data"] == "test"
        assert exc_dict["severity"] == "medium"
        assert exc_dict["category"] == "unknown"

    def test_recommendations(self):
        """Test recommendations field."""
        recommendations = ["Fix 1", "Fix 2", "Fix 3"]
        exc = FSMException(
            message="Test",
            recommendations=recommendations
        )

        assert exc.recommendations == recommendations
        assert len(exc.recommendations) == 3


class TestStateErrors:
    """Tests for state-related exceptions."""

    def test_invalid_state_error(self):
        """Test InvalidStateError."""
        valid_states = ["initial", "pending", "completed"]
        exc = InvalidStateError(
            state="invalid",
            valid_states=valid_states,
            user_id="user1"
        )

        assert exc.state == "invalid"
        assert exc.valid_states == valid_states
        assert "invalid" in str(exc)
        assert exc.category == ErrorCategory.STATE_ERROR
        assert exc.severity == ErrorSeverity.HIGH

    def test_terminal_state_error(self):
        """Test TerminalStateError."""
        exc = TerminalStateError(
            state="completed",
            user_id="user1"
        )

        assert exc.state == "completed"
        assert "completed" in str(exc)
        assert exc.category == ErrorCategory.STATE_ERROR

    def test_duplicate_state_error(self):
        """Test DuplicateStateError."""
        exc = DuplicateStateError(
            state="initial",
            user_id="user1"
        )

        assert exc.state == "initial"
        assert "already exists" in str(exc)
        assert exc.category == ErrorCategory.STATE_ERROR
        assert exc.severity == ErrorSeverity.MEDIUM


class TestTransitionErrors:
    """Tests for transition-related exceptions."""

    def test_invalid_transition_error(self):
        """Test InvalidTransitionError."""
        exc = InvalidTransitionError(
            from_state="initial",
            to_state="completed",
            user_id="user1"
        )

        assert exc.from_state == "initial"
        assert exc.to_state == "completed"
        assert "initial" in str(exc)
        assert "completed" in str(exc)
        assert exc.category == ErrorCategory.TRANSITION_ERROR

    def test_transition_not_allowed_error(self):
        """Test TransitionNotAllowedError."""
        valid_triggers = ["delegate_to_agent", "request_disambiguation"]
        exc = TransitionNotAllowedError(
            trigger="complete",
            current_state="initial",
            valid_triggers=valid_triggers,
            user_id="user1"
        )

        assert exc.trigger == "complete"
        assert exc.current_state == "initial"
        assert exc.valid_triggers == valid_triggers
        assert "complete" in str(exc)
        assert "initial" in str(exc)


class TestCallbackErrors:
    """Tests for callback-related exceptions."""

    def test_callback_execution_error(self):
        """Test CallbackExecutionError."""
        original_error = ValueError("Original error")
        exc = CallbackExecutionError(
            callback_name="on_delegate",
            trigger="delegate_to_agent",
            original_error=original_error,
            user_id="user1"
        )

        assert exc.callback_name == "on_delegate"
        assert exc.trigger == "delegate_to_agent"
        assert exc.original_error == original_error
        assert exc.cause == original_error
        assert "on_delegate" in str(exc)
        assert exc.category == ErrorCategory.CALLBACK_ERROR


class TestContextErrors:
    """Tests for context-related exceptions."""

    def test_context_merging_error(self):
        """Test ContextMergingError."""
        exc = ContextMergingError(
            strategy="invalid_strategy",
            reason="Unknown strategy type",
            user_id="user1"
        )

        assert exc.strategy == "invalid_strategy"
        assert exc.reason == "Unknown strategy type"
        assert "invalid_strategy" in str(exc)
        assert exc.category == ErrorCategory.CONTEXT_ERROR

    def test_context_validation_error(self):
        """Test ContextValidationError."""
        exc = ContextValidationError(
            validation_failed="user_id must be string",
            user_id="user1"
        )

        assert exc.validation_failed == "user_id must be string"
        assert "user_id must be string" in str(exc)
        assert exc.category == ErrorCategory.CONTEXT_ERROR


class TestSessionErrors:
    """Tests for session-related exceptions."""

    def test_conversation_timeout_error(self):
        """Test ConversationTimeoutError."""
        exc = ConversationTimeoutError(
            timeout_seconds=300,
            user_id="user1"
        )

        assert exc.timeout_seconds == 300
        assert "300" in str(exc)
        assert exc.category == ErrorCategory.SESSION_ERROR

    def test_session_not_found_error(self):
        """Test SessionNotFoundError."""
        exc = SessionNotFoundError(
            session_id="session_123",
            user_id="user1"
        )

        assert exc.session_id == "session_123"
        assert "session_123" in str(exc)
        assert exc.category == ErrorCategory.SESSION_ERROR


class TestConfigurationErrors:
    """Tests for configuration-related exceptions."""

    def test_missing_configuration_error(self):
        """Test MissingConfigurationError."""
        exc = MissingConfigurationError(
            missing_key="VALID_STATES",
            user_id="user1"
        )

        assert exc.missing_key == "VALID_STATES"
        assert "VALID_STATES" in str(exc)
        assert exc.category == ErrorCategory.CONFIGURATION_ERROR
        assert exc.severity == ErrorSeverity.CRITICAL

    def test_invalid_configuration_error(self):
        """Test InvalidConfigurationError."""
        exc = InvalidConfigurationError(
            config_key="MAX_RETRIES",
            reason="Must be positive integer",
            user_id="user1"
        )

        assert exc.config_key == "MAX_RETRIES"
        assert exc.reason == "Must be positive integer"
        assert "MAX_RETRIES" in str(exc)
        assert exc.category == ErrorCategory.CONFIGURATION_ERROR
        assert exc.severity == ErrorSeverity.CRITICAL


class TestExceptionRegistry:
    """Tests for exception registry functionality."""

    def test_registry_completeness(self):
        """Test that all exceptions are registered."""
        assert "InvalidStateError" in EXCEPTION_REGISTRY
        assert "TerminalStateError" in EXCEPTION_REGISTRY
        assert "DuplicateStateError" in EXCEPTION_REGISTRY
        assert "InvalidTransitionError" in EXCEPTION_REGISTRY
        assert "TransitionNotAllowedError" in EXCEPTION_REGISTRY
        assert "CallbackExecutionError" in EXCEPTION_REGISTRY
        assert "ContextMergingError" in EXCEPTION_REGISTRY
        assert "ContextValidationError" in EXCEPTION_REGISTRY
        assert "ConversationTimeoutError" in EXCEPTION_REGISTRY
        assert "SessionNotFoundError" in EXCEPTION_REGISTRY
        assert "MissingConfigurationError" in EXCEPTION_REGISTRY
        assert "InvalidConfigurationError" in EXCEPTION_REGISTRY

    def test_get_exception_class(self):
        """Test getting exception class by name."""
        exc_class = get_exception_class("InvalidStateError")
        assert exc_class is not None
        assert exc_class == InvalidStateError

    def test_get_nonexistent_exception_class(self):
        """Test getting nonexistent exception class."""
        exc_class = get_exception_class("NonexistentError")
        assert exc_class is None


class TestExceptionHierarchy:
    """Tests for exception hierarchy."""

    def test_state_errors_hierarchy(self):
        """Test that state errors inherit properly."""
        exc = InvalidStateError(
            state="bad",
            valid_states=["good"]
        )

        assert isinstance(exc, FSMException)
        assert isinstance(exc, Exception)

    def test_exception_catching(self):
        """Test catching exceptions by base class."""
        with pytest.raises(FSMException):
            raise InvalidStateError(
                state="bad",
                valid_states=["good"]
            )

    def test_specific_exception_catching(self):
        """Test catching specific exception types."""
        with pytest.raises(InvalidStateError):
            raise InvalidStateError(
                state="bad",
                valid_states=["good"]
            )


class TestExceptionAttributes:
    """Tests for exception attributes."""

    def test_timestamp_creation(self):
        """Test that timestamp is created."""
        exc = FSMException("Test")
        assert isinstance(exc.timestamp, datetime)

    def test_severity_levels(self):
        """Test different severity levels."""
        low_exc = FSMException(
            "Test",
            severity=ErrorSeverity.LOW
        )
        assert low_exc.severity == ErrorSeverity.LOW

        critical_exc = MissingConfigurationError("KEY")
        assert critical_exc.severity == ErrorSeverity.CRITICAL

    def test_default_context(self):
        """Test default empty context."""
        exc = FSMException("Test")
        assert exc.context == {}

    def test_recommendations_default(self):
        """Test default empty recommendations."""
        exc = FSMException("Test")
        assert exc.recommendations == []


class TestExceptionMessages:
    """Tests for formatted exception messages."""

    def test_message_includes_user_id(self):
        """Test that message includes user_id when present."""
        exc = FSMException("Test error", user_id="user123")
        exc_str = str(exc)

        assert "user:user123" in exc_str
        assert "Test error" in exc_str

    def test_message_without_user_id(self):
        """Test that message works without user_id."""
        exc = FSMException("Test error")
        exc_str = str(exc)

        assert "Test error" in exc_str

    def test_error_code_in_message(self):
        """Test that error code is in message."""
        exc = FSMException("Test")
        exc_str = str(exc)

        assert exc.error_code in exc_str


class TestExceptionContext:
    """Tests for context handling."""

    def test_context_modification(self):
        """Test modifying context after creation."""
        exc = FSMException("Test", context={"key1": "value1"})
        exc.context["key2"] = "value2"

        assert exc.context["key1"] == "value1"
        assert exc.context["key2"] == "value2"

    def test_context_get_with_default(self):
        """Test getting context with default value."""
        exc = FSMException("Test", context={"existing": "value"})

        existing = exc.get_context("existing", "default")
        missing = exc.get_context("missing", "default")

        assert existing == "value"
        assert missing == "default"

    def test_context_copy_isolation(self):
        """Test that get_context returns a copy."""
        original_context = {"key": "value"}
        exc = FSMException("Test", context=original_context)

        returned_context = exc.get_context()
        returned_context["key"] = "modified"

        assert exc.context["key"] == "value"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])