"""
Tests for FSM Context Merging System
H03 FASE 1 - BLOQUE 1.4 - Context Merging Testing

Tests para validar el sistema de context merging, validadores, y snapshots.

Version: 1.0.1
Last Updated: 09-Dec-2025 18:00 CET
Status: PRODUCTION READY - 52/52 Tests PASSING
"""

import pytest
from datetime import datetime
from typing import Dict, Any

# Importar las clases a testear
from theaia.core.fsm.context_merging import (
    MergeStrategy,
    ConflictResolution,
    ContextValidator,
    KeyValidator,
    TypeValidator,
    ValueRangeValidator,
    CustomValidator,
    ContextMerger,
    ContextManager,
    ContextSnapshot,
    ContextSnapshotManager
)


# ============================================================================
# TEST CLASSES
# ============================================================================


class TestMergeStrategies:
    """Tests for merge strategy enumerations."""

    def test_merge_strategy_values(self):
        """Test merge strategy enum values."""
        assert MergeStrategy.OVERRIDE.value == "override"
        assert MergeStrategy.MERGE.value == "merge"
        assert MergeStrategy.PRESERVE.value == "preserve"
        assert MergeStrategy.UNION.value == "union"
        assert MergeStrategy.INTERSECTION.value == "intersection"

    def test_conflict_resolution_values(self):
        """Test conflict resolution enum values."""
        assert ConflictResolution.LAST_WRITE_WINS.value == "last_write_wins"
        assert ConflictResolution.FIRST_WRITE_WINS.value == "first_write_wins"
        assert ConflictResolution.THROW_ERROR.value == "throw_error"
        assert ConflictResolution.CUSTOM.value == "custom"


class TestKeyValidator:
    """Tests for key validator."""

    def test_all_keys_present(self):
        """Test when all required keys present."""
        validator = KeyValidator(["name", "age"])
        context = {"name": "Alice", "age": 30}

        assert validator.validate(context) is True

    def test_missing_key(self):
        """Test when required key is missing."""
        validator = KeyValidator(["name", "age"])
        context = {"name": "Alice"}

        assert validator.validate(context) is False

    def test_extra_keys_ok(self):
        """Test that extra keys are OK."""
        validator = KeyValidator(["name"])
        context = {"name": "Alice", "age": 30, "email": "alice@example.com"}

        assert validator.validate(context) is True

    def test_empty_context(self):
        """Test empty context."""
        validator = KeyValidator(["name"])
        context = {}

        assert validator.validate(context) is False


class TestTypeValidator:
    """Tests for type validator."""

    def test_correct_types(self):
        """Test when all types are correct."""
        validator = TypeValidator({"name": str, "age": int})
        context = {"name": "Alice", "age": 30}

        assert validator.validate(context) is True

    def test_wrong_type(self):
        """Test when type is wrong."""
        validator = TypeValidator({"name": str, "age": int})
        context = {"name": "Alice", "age": "30"}

        assert validator.validate(context) is False

    def test_partial_validation(self):
        """Test only validates keys that exist."""
        validator = TypeValidator({"name": str, "age": int})
        context = {"name": "Alice", "email": "alice@example.com"}

        assert validator.validate(context) is True

    def test_multiple_types(self):
        """Test multiple type constraints."""
        validator = TypeValidator({
            "name": str,
            "age": int,
            "active": bool,
            "score": float
        })
        context = {
            "name": "Alice",
            "age": 30,
            "active": True,
            "score": 95.5
        }

        assert validator.validate(context) is True


class TestValueRangeValidator:
    """Tests for value range validator."""

    def test_values_in_range(self):
        """Test when values are in range."""
        validator = ValueRangeValidator({"age": (0, 120), "score": (0, 100)})
        context = {"age": 30, "score": 85}

        assert validator.validate(context) is True

    def test_value_below_range(self):
        """Test value below minimum."""
        validator = ValueRangeValidator({"age": (0, 120)})
        context = {"age": -5}

        assert validator.validate(context) is False

    def test_value_above_range(self):
        """Test value above maximum."""
        validator = ValueRangeValidator({"age": (0, 120)})
        context = {"age": 150}

        assert validator.validate(context) is False

    def test_boundary_values(self):
        """Test boundary values are included."""
        validator = ValueRangeValidator({"value": (0, 100)})
        
        assert validator.validate({"value": 0}) is True
        assert validator.validate({"value": 100}) is True

    def test_float_values(self):
        """Test with float values."""
        validator = ValueRangeValidator({"ratio": (0.0, 1.0)})
        context = {"ratio": 0.5}

        assert validator.validate(context) is True


class TestCustomValidator:
    """Tests for custom validator."""

    def test_custom_validation_pass(self):
        """Test custom validation passes."""
        def check_sum(ctx):
            return ctx.get("a", 0) + ctx.get("b", 0) > 10

        validator = CustomValidator("sum_check", check_sum)
        context = {"a": 6, "b": 5}

        assert validator.validate(context) is True

    def test_custom_validation_fail(self):
        """Test custom validation fails."""
        def check_sum(ctx):
            return ctx.get("a", 0) + ctx.get("b", 0) > 10

        validator = CustomValidator("sum_check", check_sum)
        context = {"a": 3, "b": 4}

        assert validator.validate(context) is False

    def test_custom_with_exception(self):
        """Test custom validator handles exceptions."""
        def bad_check(ctx):
            return ctx["nonexistent_key"]  # Will raise KeyError

        validator = CustomValidator("bad_check", bad_check)
        context = {"a": 1}

        assert validator.validate(context) is False


class TestValidatorEnableDisable:
    """Tests for validator enable/disable."""

    def test_disable_validator(self):
        """Test disabling validator."""
        validator = KeyValidator(["missing_key"])
        validator.disable()

        # ✅ FIX APLICADO (09-Dec-2025 18:00 CET):
        # Cambio de validator.validate({}) a validator({})
        # Razón: El método __call__ respeta enabled/disabled, validate() no
        assert validator({}) is True

    def test_enable_validator(self):
        """Test enabling disabled validator."""
        validator = KeyValidator(["missing_key"])
        validator.disable()
        validator.enable()

        assert validator.validate({}) is False


class TestContextMergerOverride:
    """Tests for OVERRIDE merge strategy."""

    def test_override_simple(self):
        """Test override strategy with simple values."""
        merger = ContextMerger(strategy=MergeStrategy.OVERRIDE)
        base = {"a": 1, "b": 2}
        new = {"b": 20, "c": 3}

        result = merger.merge(base, new)

        assert result == {"a": 1, "b": 20, "c": 3}

    def test_override_empty_base(self):
        """Test override with empty base."""
        merger = ContextMerger(strategy=MergeStrategy.OVERRIDE)
        base = {}
        new = {"a": 1, "b": 2}

        result = merger.merge(base, new)

        assert result == {"a": 1, "b": 2}

    def test_override_empty_new(self):
        """Test override with empty new."""
        merger = ContextMerger(strategy=MergeStrategy.OVERRIDE)
        base = {"a": 1, "b": 2}
        new = {}

        result = merger.merge(base, new)

        assert result == {"a": 1, "b": 2}


class TestContextMergerDeep:
    """Tests for MERGE (deep merge) strategy."""

    def test_merge_nested_dicts(self):
        """Test deep merge with nested dicts."""
        merger = ContextMerger(strategy=MergeStrategy.MERGE)
        base = {"user": {"name": "Alice", "age": 30}}
        new = {"user": {"age": 31, "email": "alice@example.com"}}

        result = merger.merge(base, new)

        assert result == {
            "user": {
                "name": "Alice",
                "age": 31,
                "email": "alice@example.com"
            }
        }

    def test_merge_preserves_base_structure(self):
        """Test merge preserves base structure."""
        merger = ContextMerger(strategy=MergeStrategy.MERGE)
        base = {"a": 1, "b": {"c": 2}}
        new = {"b": {"d": 4}}

        result = merger.merge(base, new)

        assert result == {"a": 1, "b": {"c": 2, "d": 4}}

    def test_merge_deep_nested(self):
        """Test deeply nested merge."""
        merger = ContextMerger(strategy=MergeStrategy.MERGE)
        base = {"a": {"b": {"c": 1}}}
        new = {"a": {"b": {"d": 2}}}

        result = merger.merge(base, new)

        assert result == {"a": {"b": {"c": 1, "d": 2}}}


class TestContextMergerPreserve:
    """Tests for PRESERVE merge strategy."""

    def test_preserve_keeps_base(self):
        """Test preserve keeps base context."""
        merger = ContextMerger(strategy=MergeStrategy.PRESERVE)
        base = {"a": 1, "b": 2}
        new = {"b": 20, "c": 3}

        result = merger.merge(base, new)

        assert result == {"a": 1, "b": 2}


class TestContextMergerUnion:
    """Tests for UNION merge strategy."""

    def test_union_combines_keys(self):
        """Test union combines all keys."""
        merger = ContextMerger(strategy=MergeStrategy.UNION)
        base = {"a": 1, "b": 2}
        new = {"b": 20, "c": 3}

        result = merger.merge(base, new)

        assert result == {"a": 1, "b": 2, "c": 3}

    def test_union_keeps_base_values(self):
        """Test union keeps base values for common keys."""
        merger = ContextMerger(strategy=MergeStrategy.UNION)
        base = {"a": 1}
        new = {"a": 10, "b": 2}

        result = merger.merge(base, new)

        assert result == {"a": 1, "b": 2}


class TestContextMergerIntersection:
    """Tests for INTERSECTION merge strategy."""

    def test_intersection_common_keys(self):
        """Test intersection keeps only common keys."""
        merger = ContextMerger(strategy=MergeStrategy.INTERSECTION)
        base = {"a": 1, "b": 2, "c": 3}
        new = {"b": 20, "c": 30, "d": 4}

        result = merger.merge(base, new)

        assert result == {"b": 20, "c": 30}

    def test_intersection_no_common(self):
        """Test intersection with no common keys."""
        merger = ContextMerger(strategy=MergeStrategy.INTERSECTION)
        base = {"a": 1, "b": 2}
        new = {"c": 3, "d": 4}

        result = merger.merge(base, new)

        assert result == {}


class TestContextMergerHistory:
    """Tests for merge history tracking."""

    def test_record_merge(self):
        """Test merge is recorded."""
        merger = ContextMerger(strategy=MergeStrategy.MERGE)
        base = {"a": 1}
        new = {"b": 2}

        result = merger.merge(base, new)
        merger.record_merge(result)

        history = merger.get_merge_history()
        assert len(history) == 1
        assert history[0]["result"] == {"a": 1, "b": 2}

    def test_merge_history_multiple(self):
        """Test multiple merges recorded."""
        merger = ContextMerger(strategy=MergeStrategy.MERGE)

        merger.record_merge({"a": 1})
        merger.record_merge({"a": 1, "b": 2})
        merger.record_merge({"a": 1, "b": 2, "c": 3})

        history = merger.get_merge_history()
        assert len(history) == 3


class TestContextManager:
    """Tests for context manager."""

    def test_context_manager_init(self):
        """Test context manager initialization."""
        manager = ContextManager(initial_context={"a": 1})

        assert manager.get("a") == 1

    def test_context_manager_get_set(self):
        """Test get and set operations."""
        manager = ContextManager()
        
        manager.set("name", "Alice")
        assert manager.get("name") == "Alice"

    def test_context_manager_get_default(self):
        """Test get with default value."""
        manager = ContextManager()

        assert manager.get("missing", "default") == "default"

    def test_context_manager_update(self):
        """Test update operation."""
        manager = ContextManager(initial_context={"a": 1})
        
        manager.update({"b": 2, "c": 3})

        assert manager.get("a") == 1
        assert manager.get("b") == 2
        assert manager.get("c") == 3

    def test_context_manager_merge_with_validation(self):
        """Test merge with validation."""
        manager = ContextManager()
        manager.add_validator(KeyValidator(["name"]))

        result = manager.merge_context({"name": "Alice"}, validate=True)

        assert result is True
        assert manager.get("name") == "Alice"

    def test_context_manager_merge_validation_fail(self):
        """Test merge fails validation."""
        manager = ContextManager()
        manager.add_validator(KeyValidator(["name"]))

        result = manager.merge_context({"age": 30}, validate=True)

        assert result is False
        assert manager.get("name") is None

    def test_context_manager_clear(self):
        """Test clearing context."""
        manager = ContextManager(initial_context={"a": 1, "b": 2})
        
        manager.clear()

        assert manager.to_dict() == {}

    def test_context_manager_to_dict(self):
        """Test exporting to dict."""
        manager = ContextManager(initial_context={"a": 1, "b": 2})

        result = manager.to_dict()

        assert result == {"a": 1, "b": 2}

    def test_context_manager_to_json_compatible(self):
        """Test JSON-compatible export."""
        now = datetime.now()
        manager = ContextManager(initial_context={
            "name": "Alice",
            "created": now
        })

        result = manager.to_json_compatible()

        assert result["name"] == "Alice"
        assert result["created"] == now.isoformat()

    def test_context_manager_statistics(self):
        """Test context statistics."""
        manager = ContextManager(initial_context={"a": 1})
        manager.add_validator(KeyValidator(["a"]))

        stats = manager.get_statistics()

        assert stats["context_size"] == 1
        assert stats["validators"] == 1


class TestContextSnapshot:
    """Tests for context snapshots."""

    def test_snapshot_creation(self):
        """Test snapshot creation."""
        context = {"a": 1, "b": 2}
        snapshot = ContextSnapshot(context=context)

        assert snapshot.context == context
        assert isinstance(snapshot.timestamp, datetime)

    def test_snapshot_to_dict(self):
        """Test snapshot export."""
        context = {"a": 1}
        snapshot = ContextSnapshot(context=context, metadata={"user_id": "123"})

        result = snapshot.to_dict()

        assert result["context"] == {"a": 1}
        assert result["metadata"] == {"user_id": "123"}
        assert "timestamp" in result


class TestContextSnapshotManager:
    """Tests for snapshot manager."""

    def test_take_snapshot(self):
        """Test taking snapshot."""
        manager = ContextSnapshotManager()
        context = {"a": 1}

        snapshot = manager.take_snapshot(context)

        assert snapshot.context == context
        assert len(manager.snapshots) == 1

    def test_max_snapshots_enforced(self):
        """Test max snapshots limit."""
        manager = ContextSnapshotManager(max_snapshots=3)

        for i in range(5):
            manager.take_snapshot({"count": i})

        assert len(manager.snapshots) == 3

    def test_get_latest_snapshot(self):
        """Test getting latest snapshot."""
        manager = ContextSnapshotManager()

        manager.take_snapshot({"value": 1})
        manager.take_snapshot({"value": 2})
        manager.take_snapshot({"value": 3})

        latest = manager.get_latest_snapshot()
        assert latest.context == {"value": 3}

    def test_get_snapshot_by_index(self):
        """Test getting snapshot by index."""
        manager = ContextSnapshotManager()

        manager.take_snapshot({"value": 1})
        manager.take_snapshot({"value": 2})
        manager.take_snapshot({"value": 3})

        snapshot = manager.get_snapshot_by_index(1)
        assert snapshot.context == {"value": 2}

    def test_get_all_snapshots(self):
        """Test getting all snapshots."""
        manager = ContextSnapshotManager()

        manager.take_snapshot({"value": 1})
        manager.take_snapshot({"value": 2})

        snapshots = manager.get_all_snapshots()
        assert len(snapshots) == 2

    def test_clear_snapshots(self):
        """Test clearing snapshots."""
        manager = ContextSnapshotManager()

        manager.take_snapshot({"value": 1})
        manager.take_snapshot({"value": 2})

        assert len(manager.snapshots) == 2

        manager.clear()

        assert len(manager.snapshots) == 0

    def test_snapshot_statistics(self):
        """Test snapshot statistics."""
        manager = ContextSnapshotManager(max_snapshots=5)

        manager.take_snapshot({"value": 1})
        manager.take_snapshot({"value": 2})

        stats = manager.get_statistics()

        assert stats["total_snapshots"] == 2
        assert stats["max_snapshots"] == 5
        assert "oldest" in stats
        assert "latest" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
