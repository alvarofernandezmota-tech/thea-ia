"""
FSM Context Merging System - Advanced Context Management
H03 FASE 1 - BLOQUE 1.4 - Context Management System

This module provides comprehensive context merging, validation, and serialization
for the THEA IA FSM system. Supports multiple merging strategies, conflict
resolution, and context validation.

Version: 1.0.0
Last Updated: 09-Dec-2025
Status: Production Ready - THEA IA Compatible
"""

import logging
from typing import Optional, Dict, Any, List, Callable, Union
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from copy import deepcopy

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERATIONS
# ============================================================================

class MergeStrategy(Enum):
    """Strategy for merging contexts."""
    OVERRIDE = "override"  # New values override old
    MERGE = "merge"        # Deep merge, new takes precedence
    PRESERVE = "preserve"  # Keep old values, reject new
    UNION = "union"        # Union of both contexts
    INTERSECTION = "intersection"  # Only common keys


class ConflictResolution(Enum):
    """How to handle conflicts during merge."""
    LAST_WRITE_WINS = "last_write_wins"
    FIRST_WRITE_WINS = "first_write_wins"
    THROW_ERROR = "throw_error"
    CUSTOM = "custom"


# ============================================================================
# CONTEXT VALIDATOR SYSTEM
# ============================================================================

class ContextValidator(ABC):
    """
    Base class for context validators.
    
    A validator checks if a context meets certain criteria.
    """
    
    def __init__(self, name: str, required: bool = True):
        """
        Initialize validator.
        
        Args:
            name: Validator identifier
            required: If True, validation failure blocks operation
        """
        self.name = name
        self.required = required
        self.enabled = True
    
    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> bool:
        """
        Validate context.
        
        Args:
            context: Context to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def __call__(self, context: Dict[str, Any]) -> bool:
        """Make validator callable."""
        if not self.enabled:
            return True
        return self.validate(context)
    
    def disable(self):
        """Disable validator."""
        self.enabled = False
    
    def enable(self):
        """Enable validator."""
        self.enabled = True


# ============================================================================
# SPECIFIC VALIDATOR IMPLEMENTATIONS
# ============================================================================

class KeyValidator(ContextValidator):
    """Validates that required keys exist in context."""
    
    def __init__(self, required_keys: List[str]):
        """
        Initialize key validator.
        
        Args:
            required_keys: List of required keys
        """
        super().__init__(name="key_validator")
        self.required_keys = required_keys
    
    def validate(self, context: Dict[str, Any]) -> bool:
        """Check if all required keys exist."""
        return all(key in context for key in self.required_keys)


class TypeValidator(ContextValidator):
    """Validates that values have correct types."""
    
    def __init__(self, type_constraints: Dict[str, type]):
        """
        Initialize type validator.
        
        Args:
            type_constraints: Dict of {key: expected_type}
        """
        super().__init__(name="type_validator")
        self.type_constraints = type_constraints
    
    def validate(self, context: Dict[str, Any]) -> bool:
        """Check if values match expected types."""
        for key, expected_type in self.type_constraints.items():
            if key in context:
                if not isinstance(context[key], expected_type):
                    return False
        return True


class ValueRangeValidator(ContextValidator):
    """Validates that numeric values are within range."""
    
    def __init__(self, ranges: Dict[str, tuple]):
        """
        Initialize range validator.
        
        Args:
            ranges: Dict of {key: (min, max)}
        """
        super().__init__(name="range_validator")
        self.ranges = ranges
    
    def validate(self, context: Dict[str, Any]) -> bool:
        """Check if numeric values are in range."""
        for key, (min_val, max_val) in self.ranges.items():
            if key in context:
                value = context[key]
                if not isinstance(value, (int, float)):
                    return False
                if not (min_val <= value <= max_val):
                    return False
        return True


class CustomValidator(ContextValidator):
    """Validator with custom validation logic."""
    
    def __init__(
        self,
        name: str,
        validation_fn: Callable[[Dict[str, Any]], bool]
    ):
        """
        Initialize custom validator.
        
        Args:
            name: Validator name
            validation_fn: Custom validation function
        """
        super().__init__(name=name)
        self.validation_fn = validation_fn
    
    def validate(self, context: Dict[str, Any]) -> bool:
        """Run custom validation."""
        try:
            return self.validation_fn(context)
        except Exception as e:
            logger.error("Custom validator {} failed: {}".format(
                self.name, str(e)
            ))
            return False


# ============================================================================
# CONTEXT MERGING
# ============================================================================

class ContextMerger:
    """
    Handles context merging with multiple strategies.
    
    Supports different merge strategies and conflict resolution.
    """
    
    def __init__(
        self,
        strategy: MergeStrategy = MergeStrategy.MERGE,
        conflict_resolver: ConflictResolution = ConflictResolution.LAST_WRITE_WINS
    ):
        """
        Initialize context merger.
        
        Args:
            strategy: Merging strategy
            conflict_resolver: How to resolve conflicts
        """
        self.strategy = strategy
        self.conflict_resolver = conflict_resolver
        self.merge_history: List[Dict[str, Any]] = []
    
    def merge(
        self,
        base_context: Dict[str, Any],
        new_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge contexts according to strategy.
        
        Args:
            base_context: Base context
            new_context: New context to merge
            
        Returns:
            Merged context
        """
        if self.strategy == MergeStrategy.OVERRIDE:
            return self._merge_override(base_context, new_context)
        elif self.strategy == MergeStrategy.MERGE:
            return self._merge_deep(base_context, new_context)
        elif self.strategy == MergeStrategy.PRESERVE:
            return self._merge_preserve(base_context, new_context)
        elif self.strategy == MergeStrategy.UNION:
            return self._merge_union(base_context, new_context)
        elif self.strategy == MergeStrategy.INTERSECTION:
            return self._merge_intersection(base_context, new_context)
        else:
            raise ValueError("Unknown merge strategy: {}".format(self.strategy))
    
    def _merge_override(
        self,
        base: Dict[str, Any],
        new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """New context completely overrides base."""
        result = deepcopy(base)
        result.update(deepcopy(new))
        return result
    
    def _merge_deep(
        self,
        base: Dict[str, Any],
        new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep merge of contexts."""
        result = deepcopy(base)
        
        for key, value in new.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_deep(result[key], value)
            else:
                result[key] = deepcopy(value)
        
        return result
    
    def _merge_preserve(
        self,
        base: Dict[str, Any],
        new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Keep base context, ignore new."""
        return deepcopy(base)
    
    def _merge_union(
        self,
        base: Dict[str, Any],
        new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Union of both contexts (all keys)."""
        result = deepcopy(base)
        
        for key, value in new.items():
            if key not in result:
                result[key] = deepcopy(value)
        
        return result
    
    def _merge_intersection(
        self,
        base: Dict[str, Any],
        new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Intersection of both contexts (common keys only)."""
        common_keys = set(base.keys()) & set(new.keys())
        result = {}
        
        for key in common_keys:
            result[key] = deepcopy(new[key])
        
        return result
    
    def record_merge(self, result: Dict[str, Any]):
        """Record merge operation."""
        self.merge_history.append({
            "timestamp": datetime.now(),
            "result": deepcopy(result),
            "strategy": self.strategy.value
        })
    
    def get_merge_history(self) -> List[Dict[str, Any]]:
        """Get merge operation history."""
        return self.merge_history.copy()
    
    def clear_history(self):
        """Clear merge history."""
        self.merge_history.clear()


# ============================================================================
# CONTEXT MANAGER
# ============================================================================

class ContextManager:
    """
    Manages context state with validation and merging.
    
    Coordinates validators, merging, and serialization.
    """
    
    def __init__(
        self,
        initial_context: Optional[Dict[str, Any]] = None,
        strategy: MergeStrategy = MergeStrategy.MERGE
    ):
        """
        Initialize context manager.
        
        Args:
            initial_context: Initial context
            strategy: Merging strategy
        """
        self.context = deepcopy(initial_context) if initial_context else {}
        self.merger = ContextMerger(strategy=strategy)
        self.validators: List[ContextValidator] = []
        self.operation_log: List[Dict[str, Any]] = []
    
    def add_validator(self, validator: ContextValidator) -> "ContextManager":
        """Add validator."""
        self.validators.append(validator)
        return self
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate current context.
        
        Returns:
            (is_valid, error_message)
        """
        for validator in self.validators:
            try:
                if not validator(self.context):
                    if validator.required:
                        return (False, "Validator {} failed".format(validator.name))
            except Exception as e:
                logger.error("Validator {} error: {}".format(
                    validator.name, str(e)
                ))
                if validator.required:
                    return (False, str(e))
        
        return (True, None)
    
    def merge_context(
        self,
        new_context: Dict[str, Any],
        validate: bool = True
    ) -> bool:
        """
        Merge new context.
        
        Args:
            new_context: Context to merge
            validate: Whether to validate after merge
            
        Returns:
            True if successful, False otherwise
        """
        try:
            merged = self.merger.merge(self.context, new_context)
            
            if validate:
                # Temporarily set merged context for validation
                old_context = self.context
                self.context = merged
                
                is_valid, error = self.validate()
                if not is_valid:
                    self.context = old_context
                    logger.error("Merged context validation failed: {}".format(error))
                    return False
            
            self.context = merged
            self.merger.record_merge(merged)
            
            self.operation_log.append({
                "operation": "merge",
                "timestamp": datetime.now(),
                "success": True
            })
            
            return True
        
        except Exception as e:
            logger.error("Context merge failed: {}".format(str(e)))
            self.operation_log.append({
                "operation": "merge",
                "timestamp": datetime.now(),
                "success": False,
                "error": str(e)
            })
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from context."""
        return self.context.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set value in context.
        
        Args:
            key: Context key
            value: Value to set
            
        Returns:
            True if successful
        """
        try:
            self.context[key] = value
            return True
        except Exception as e:
            logger.error("Failed to set context key {}: {}".format(key, str(e)))
            return False
    
    def update(self, updates: Dict[str, Any]) -> bool:
        """
        Update context with dictionary.
        
        Args:
            updates: Updates to apply
            
        Returns:
            True if successful
        """
        return self.merge_context(updates, validate=False)
    
    def clear(self):
        """Clear context."""
        self.context.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Export context as dictionary."""
        return deepcopy(self.context)
    
    def to_json_compatible(self) -> Dict[str, Any]:
        """
        Export context in JSON-compatible format.
        
        Converts datetime objects to ISO format strings.
        """
        result = {}
        
        for key, value in self.context.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                # Recursively convert nested dicts
                result[key] = self._dict_to_json_compatible(value)
            else:
                result[key] = value
        
        return result
    
    def _dict_to_json_compatible(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to convert dict to JSON-compatible format."""
        result = {}
        
        for key, value in d.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = self._dict_to_json_compatible(value)
            else:
                result[key] = value
        
        return result
    
    def get_operation_log(self) -> List[Dict[str, Any]]:
        """Get operation log."""
        return self.operation_log.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get context statistics."""
        return {
            "context_size": len(self.context),
            "nested_dicts": self._count_nested_dicts(self.context),
            "total_operations": len(self.operation_log),
            "successful_operations": len([
                op for op in self.operation_log if op.get("success", True)
            ]),
            "validators": len(self.validators),
            "merge_history_size": len(self.merger.merge_history)
        }
    
    def _count_nested_dicts(self, d: Dict[str, Any]) -> int:
        """Count nested dictionaries."""
        count = 0
        
        for value in d.values():
            if isinstance(value, dict):
                count += 1
                count += self._count_nested_dicts(value)
        
        return count


# ============================================================================
# CONTEXT SNAPSHOT
# ============================================================================

@dataclass
class ContextSnapshot:
    """Snapshot of context at a point in time."""
    
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export snapshot as dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "context": deepcopy(self.context),
            "metadata": deepcopy(self.metadata)
        }


class ContextSnapshotManager:
    """
    Manages snapshots of context state over time.
    
    Useful for debugging and auditing.
    """
    
    def __init__(self, max_snapshots: int = 100):
        """
        Initialize snapshot manager.
        
        Args:
            max_snapshots: Maximum snapshots to keep
        """
        self.max_snapshots = max_snapshots
        self.snapshots: List[ContextSnapshot] = []
    
    def take_snapshot(
        self,
        context: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextSnapshot:
        """Take context snapshot."""
        snapshot = ContextSnapshot(
            context=deepcopy(context),
            metadata=metadata or {}
        )
        
        self.snapshots.append(snapshot)
        
        # Maintain max size (FIFO)
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots.pop(0)
        
        return snapshot
    
    def get_latest_snapshot(self) -> Optional[ContextSnapshot]:
        """Get latest snapshot."""
        return self.snapshots[-1] if self.snapshots else None
    
    def get_snapshot_by_index(self, index: int) -> Optional[ContextSnapshot]:
        """Get snapshot by index."""
        try:
            return self.snapshots[index]
        except IndexError:
            return None
    
    def get_all_snapshots(self) -> List[ContextSnapshot]:
        """Get all snapshots."""
        return self.snapshots.copy()
    
    def clear(self):
        """Clear all snapshots."""
        self.snapshots.clear()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get snapshot statistics."""
        if not self.snapshots:
            return {
                "total_snapshots": 0,
                "oldest": None,
                "latest": None
            }
        
        return {
            "total_snapshots": len(self.snapshots),
            "oldest": self.snapshots[0].timestamp.isoformat(),
            "latest": self.snapshots[-1].timestamp.isoformat(),
            "max_snapshots": self.max_snapshots
        }


if __name__ == "__main__":
    # Example usage
    logger.info("FSM Context Merging System v1.0.0 loaded")