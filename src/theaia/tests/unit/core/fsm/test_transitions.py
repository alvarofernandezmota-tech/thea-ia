"""
Tests for FSM Transitions System - CORRECTED VERSION
H03 FASE 1 - BLOQUE 1.4 - Transition Testing

Tests para validar el sistema de transiciones, guards, y validadores.
"""

import pytest
from datetime import datetime
from typing import Dict, Any

# Importar las clases a testear
from theaia.core.fsm.transitions import (
    GuardType,
    TransitionDirection,
    TransitionGuard,
    PreconditionGuard,
    PostconditionGuard,
    ConditionalGuard,
    ContextHasKeyGuard,
    ContextValueGuard,
    TransitionMetadata,
    TransitionRecord,
    TransitionHistory,
    TransitionValidator,
    TransitionBuilder
)


# ============================================================================
# TEST CLASSES
# ============================================================================


class TestGuardTypes:
    """Tests for guard type enumerations."""

    def test_guard_type_values(self):
        """Test guard type enum values."""
        assert GuardType.PRECONDITION.value == "precondition"
        assert GuardType.POSTCONDITION.value == "postcondition"
        assert GuardType.CONDITIONAL.value == "conditional"
        assert GuardType.CONTEXT_VALIDATOR.value == "context_validator"
        assert GuardType.STATE_VALIDATOR.value == "state_validator"

    def test_transition_direction_values(self):
        """Test transition direction enum values."""
        assert TransitionDirection.FORWARD.value == "forward"
        assert TransitionDirection.BACKWARD.value == "backward"
        assert TransitionDirection.LATERAL.value == "lateral"


class TestPreconditionGuard:
    """Tests for precondition guards."""

    def test_precondition_pass(self):
        """Test precondition that passes."""
        def check_user_id(context):
            return "user_id" in context

        guard = PreconditionGuard("check_user", check_user_id)
        context = {"user_id": "user123"}

        assert guard.evaluate(context) is True

    def test_precondition_fail(self):
        """Test precondition that fails."""
        def check_user_id(context):
            return "user_id" in context

        guard = PreconditionGuard("check_user", check_user_id)
        context = {}

        assert guard.evaluate(context) is False

    def test_precondition_callable(self):
        """Test precondition as callable."""
        guard = PreconditionGuard(
            "check",
            lambda ctx: ctx.get("status") == "ready"
        )
        context = {"status": "ready"}

        assert guard(context) is True

    def test_precondition_guard_type(self):
        """Test precondition is correct guard type."""
        guard = PreconditionGuard("test", lambda ctx: True)
        assert guard.guard_type == GuardType.PRECONDITION
        assert guard.required is True


class TestPostconditionGuard:
    """Tests for postcondition guards."""

    def test_postcondition_pass(self):
        """Test postcondition that passes."""
        def verify_state(context):
            return context.get("state") == "completed"

        guard = PostconditionGuard("verify", verify_state)
        context = {"state": "completed"}

        assert guard.evaluate(context) is True

    def test_postcondition_fail(self):
        """Test postcondition that fails."""
        def verify_state(context):
            return context.get("state") == "completed"

        guard = PostconditionGuard("verify", verify_state)
        context = {"state": "pending"}

        assert guard.evaluate(context) is False

    def test_postcondition_guard_type(self):
        """Test postcondition is correct guard type."""
        guard = PostconditionGuard("test", lambda ctx: True)
        assert guard.guard_type == GuardType.POSTCONDITION
        assert guard.required is False


class TestConditionalGuard:
    """Tests for conditional guards."""

    def test_conditional_and_all_pass(self):
        """Test conditional with AND when all pass."""
        conditions = [
            lambda ctx: "a" in ctx,
            lambda ctx: "b" in ctx,
            lambda ctx: ctx["a"] > 0
        ]
        guard = ConditionalGuard("and_test", conditions, logic="AND")
        context = {"a": 5, "b": 10}

        assert guard.evaluate(context) is True

    def test_conditional_and_one_fail(self):
        """Test conditional with AND when one fails."""
        conditions = [
            lambda ctx: "a" in ctx,
            lambda ctx: "b" in ctx,
            lambda ctx: ctx["a"] > 10
        ]
        guard = ConditionalGuard("and_test", conditions, logic="AND")
        context = {"a": 5, "b": 10}

        assert guard.evaluate(context) is False

    def test_conditional_or_one_pass(self):
        """Test conditional with OR when one passes."""
        conditions = [
            lambda ctx: "x" in ctx,
            lambda ctx: "a" in ctx,
            lambda ctx: "b" in ctx
        ]
        guard = ConditionalGuard("or_test", conditions, logic="OR")
        context = {"a": 5}

        assert guard.evaluate(context) is True

    def test_conditional_or_all_fail(self):
        """Test conditional with OR when all fail."""
        conditions = [
            lambda ctx: "x" in ctx,
            lambda ctx: "y" in ctx,
            lambda ctx: "z" in ctx
        ]
        guard = ConditionalGuard("or_test", conditions, logic="OR")
        context = {"a": 5}

        assert guard.evaluate(context) is False

    def test_conditional_invalid_logic(self):
        """Test conditional with invalid logic raises error."""
        with pytest.raises(ValueError):
            ConditionalGuard(
                "bad",
                [lambda ctx: True],
                logic="INVALID"
            )


class TestContextHasKeyGuard:
    """Tests for context key guards."""

    def test_key_exists_required(self):
        """Test key exists when required."""
        guard = ContextHasKeyGuard("user_id", required=True)
        context = {"user_id": "user123"}

        assert guard.evaluate(context) is True

    def test_key_missing_required(self):
        """Test key missing when required."""
        guard = ContextHasKeyGuard("user_id", required=True)
        context = {}

        assert guard.evaluate(context) is False

    def test_key_missing_not_required(self):
        """Test key missing when not required."""
        guard = ContextHasKeyGuard("user_id", required=False)
        context = {}

        assert guard.evaluate(context) is True

    def test_key_exists_not_required(self):
        """Test key exists when not required."""
        guard = ContextHasKeyGuard("user_id", required=False)
        context = {"user_id": "user123"}

        assert guard.evaluate(context) is False


class TestContextValueGuard:
    """Tests for context value guards."""

    def test_value_matches(self):
        """Test context value matches expected."""
        guard = ContextValueGuard("status", "ready")
        context = {"status": "ready"}

        assert guard.evaluate(context) is True

    def test_value_not_matches(self):
        """Test context value does not match."""
        guard = ContextValueGuard("status", "ready")
        context = {"status": "pending"}

        assert guard.evaluate(context) is False

    def test_key_missing(self):
        """Test key missing returns False."""
        guard = ContextValueGuard("status", "ready")
        context = {}

        assert guard.evaluate(context) is False

    def test_value_types_different(self):
        """Test different types don't match."""
        guard = ContextValueGuard("count", 5)
        context = {"count": "5"}

        assert guard.evaluate(context) is False


class TestGuardEnableDisable:
    """Tests for guard enable/disable functionality."""

    def test_guard_disable(self):
        """Test disabling a guard."""
        guard = PreconditionGuard(
            "test",
            lambda ctx: False
        )
        guard.disable()

        assert guard({"any": "context"}) is True

    def test_guard_enable(self):
        """Test enabling a disabled guard."""
        guard = PreconditionGuard(
            "test",
            lambda ctx: False
        )
        guard.disable()
        guard.enable()

        assert guard({}) is False


class TestTransitionMetadata:
    """Tests for transition metadata."""

    def test_metadata_initialization(self):
        """Test metadata initializes correctly."""
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start"
        )

        assert metadata.from_state == "initial"
        assert metadata.to_state == "processing"
        assert metadata.trigger == "start"
        assert metadata.guards == []
        assert metadata.callbacks == []

    def test_metadata_to_dict(self):
        """Test metadata export to dictionary."""
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start",
            description="Start processing"
        )
        result = metadata.to_dict()

        assert result["from_state"] == "initial"
        assert result["to_state"] == "processing"
        assert result["trigger"] == "start"
        assert result["description"] == "Start processing"
        assert "created_at" in result

    def test_metadata_with_guards(self):
        """Test metadata with guards."""
        guard = PreconditionGuard("test", lambda ctx: True)
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start",
            guards=[guard]
        )

        assert len(metadata.guards) == 1
        assert metadata.guards[0].name == "test"


class TestTransitionRecord:
    """Tests for transition records."""

    def test_record_initialization(self):
        """Test record initializes correctly."""
        record = TransitionRecord(
            from_state="initial",
            to_state="processing",
            trigger="start"
        )

        assert record.from_state == "initial"
        assert record.to_state == "processing"
        assert record.trigger == "start"
        assert record.success is True
        assert record.error is None

    def test_record_to_dict(self):
        """Test record export to dictionary."""
        record = TransitionRecord(
            from_state="initial",
            to_state="processing",
            trigger="start",
            duration_ms=123.45,
            user_id="user123"
        )
        result = record.to_dict()

        assert result["from_state"] == "initial"
        assert result["to_state"] == "processing"
        assert result["trigger"] == "start"
        assert result["duration_ms"] == 123.45
        assert result["user_id"] == "user123"
        assert result["success"] is True

    def test_record_with_error(self):
        """Test record with error."""
        record = TransitionRecord(
            from_state="initial",
            to_state="processing",
            trigger="start",
            success=False,
            error="Guard validation failed"
        )

        assert record.success is False
        assert record.error == "Guard validation failed"


class TestTransitionHistory:
    """Tests for transition history."""

    def test_history_initialization(self):
        """Test history initializes correctly."""
        history = TransitionHistory(max_records=100)

        assert history.max_records == 100
        assert len(history.records) == 0

    def test_record_transition(self):
        """Test recording a transition."""
        history = TransitionHistory()
        record = history.record_transition(
            from_state="initial",
            to_state="processing",
            trigger="start"
        )

        assert len(history.records) == 1
        assert history.records[0] == record

    def test_max_records_enforced(self):
        """Test max records limit is enforced."""
        history = TransitionHistory(max_records=3)

        for i in range(5):
            history.record_transition(
                from_state="s{}".format(i),
                to_state="s{}".format(i+1),
                trigger="next"
            )

        assert len(history.records) == 3

    def test_get_last_transition(self):
        """Test getting last transition."""
        history = TransitionHistory()
        history.record_transition("a", "b", "trigger1")
        history.record_transition("b", "c", "trigger2")

        last = history.get_last_transition()
        assert last.from_state == "b"
        assert last.to_state == "c"
        assert last.trigger == "trigger2"

    def test_get_transitions_by_state(self):
        """Test getting transitions by state."""
        history = TransitionHistory()
        history.record_transition("initial", "processing", "start")
        history.record_transition("initial", "failed", "error")
        history.record_transition("processing", "done", "complete")

        transitions = history.get_transitions_by_state("initial")
        assert len(transitions) == 2

    def test_get_transitions_by_trigger(self):
        """Test getting transitions by trigger."""
        history = TransitionHistory()
        history.record_transition("a", "b", "start")
        history.record_transition("b", "c", "continue")
        history.record_transition("c", "d", "start")

        transitions = history.get_transitions_by_trigger("start")
        assert len(transitions) == 2

    def test_get_failed_transitions(self):
        """Test getting failed transitions."""
        history = TransitionHistory()
        history.record_transition("a", "b", "ok", success=True)
        history.record_transition("b", "c", "fail", success=False)
        history.record_transition("c", "d", "ok", success=True)

        failed = history.get_failed_transitions()
        assert len(failed) == 1
        assert failed[0].trigger == "fail"

    def test_get_statistics(self):
        """Test getting history statistics."""
        history = TransitionHistory()
        history.record_transition("a", "b", "t1", duration_ms=100.0, success=True)
        history.record_transition("b", "c", "t2", duration_ms=200.0, success=True)
        history.record_transition("c", "d", "t3", duration_ms=50.0, success=False)

        stats = history.get_statistics()
        assert stats["total_transitions"] == 3
        assert stats["successful"] == 2
        assert stats["failed"] == 1
        assert stats["success_rate"] == pytest.approx(2.0/3.0)
        assert stats["average_duration_ms"] == pytest.approx(116.666666, rel=1e-5)

    def test_clear_history(self):
        """Test clearing history."""
        history = TransitionHistory()
        history.record_transition("a", "b", "t")
        history.record_transition("b", "c", "t")

        assert len(history.records) == 2
        history.clear()
        assert len(history.records) == 0


class TestTransitionValidator:
    """Tests for transition validator."""

    def test_validator_initialization(self):
        """Test validator initializes correctly."""
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start"
        )
        validator = TransitionValidator(metadata)

        assert validator.metadata == metadata
        assert len(validator.preconditions) == 0
        assert len(validator.postconditions) == 0

    def test_validator_with_preconditions(self):
        """Test validator separates preconditions."""
        guard = PreconditionGuard("pre", lambda ctx: True)
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start",
            guards=[guard]
        )
        validator = TransitionValidator(metadata)

        assert len(validator.preconditions) == 1

    def test_validate_preconditions_pass(self):
        """Test preconditions validation passes."""
        guard = PreconditionGuard(
            "check",
            lambda ctx: ctx.get("ready") is True
        )
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start",
            guards=[guard]
        )
        validator = TransitionValidator(metadata)

        is_valid, error = validator.validate_preconditions({"ready": True})
        assert is_valid is True
        assert error is None

    def test_validate_preconditions_fail(self):
        """Test preconditions validation fails."""
        guard = PreconditionGuard(
            "check",
            lambda ctx: ctx.get("ready") is True
        )
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start",
            guards=[guard]
        )
        validator = TransitionValidator(metadata)

        is_valid, error = validator.validate_preconditions({"ready": False})
        assert is_valid is False
        assert error is not None

    def test_can_transition(self):
        """Test can_transition method."""
        guard = PreconditionGuard(
            "check",
            lambda ctx: "user_id" in ctx
        )
        metadata = TransitionMetadata(
            from_state="initial",
            to_state="processing",
            trigger="start",
            guards=[guard]
        )
        validator = TransitionValidator(metadata)

        assert validator.can_transition({"user_id": "123"}) is True
        assert validator.can_transition({}) is False


class TestTransitionBuilder:
    """Tests for transition builder."""

    def test_builder_initialization(self):
        """Test builder initializes correctly."""
        builder = TransitionBuilder("initial", "processing", "start")

        assert builder.metadata.from_state == "initial"
        assert builder.metadata.to_state == "processing"
        assert builder.metadata.trigger == "start"

    def test_builder_with_description(self):
        """Test adding description."""
        builder = TransitionBuilder("a", "b", "t")
        builder.with_description("Start processing")
        metadata = builder.build()

        assert metadata.description == "Start processing"

    def test_builder_with_precondition(self):
        """Test adding precondition."""
        builder = TransitionBuilder("a", "b", "t")
        builder.with_precondition("check", lambda ctx: "user" in ctx)
        metadata = builder.build()

        assert len(metadata.guards) == 1
        assert metadata.guards[0].guard_type == GuardType.PRECONDITION

    def test_builder_with_postcondition(self):
        """Test adding postcondition."""
        builder = TransitionBuilder("a", "b", "t")
        builder.with_postcondition("verify", lambda ctx: ctx.get("state") == "b")
        metadata = builder.build()

        assert len(metadata.guards) == 1
        assert metadata.guards[0].guard_type == GuardType.POSTCONDITION

    def test_builder_fluent_chaining(self):
        """Test fluent API chaining."""
        metadata = (
            TransitionBuilder("a", "b", "trigger")
            .with_description("Test transition")
            .with_precondition("pre", lambda ctx: True)
            .with_postcondition("post", lambda ctx: True)
            .with_priority(10)
            .reversible(True)
            .build()
        )

        assert metadata.description == "Test transition"
        assert len(metadata.guards) == 2
        assert metadata.priority == 10
        assert metadata.reversible is True

    def test_builder_with_callback(self):
        """Test adding callback."""
        def my_callback():
            pass

        builder = TransitionBuilder("a", "b", "t")
        builder.with_callback(my_callback)
        metadata = builder.build()

        assert len(metadata.callbacks) == 1
        assert metadata.callbacks[0] == my_callback


if __name__ == "__main__":
    pytest.main([__file__, "-v"])