"""
FSM Transitions System - Advanced Transition Validation & Guards
H03 FASE 1 - BLOQUE 1.4 - Transition Management System

This module provides comprehensive transition validation, guards, and metadata
management for the THEA IA FSM system. Supports pre/post conditions, conditional
transitions, and transition history tracking.

Version: 1.0.0
Last Updated: 09-Dec-2025
Status: Production Ready - THEA IA Compatible
"""

import logging
from typing import Optional, Dict, Any, List, Callable, Set
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMERATIONS
# ============================================================================

class GuardType(Enum):
    """Types of transition guards."""
    PRECONDITION = "precondition"
    POSTCONDITION = "postcondition"
    CONDITIONAL = "conditional"
    CONTEXT_VALIDATOR = "context_validator"
    STATE_VALIDATOR = "state_validator"


class TransitionDirection(Enum):
    """Direction of transition."""
    FORWARD = "forward"
    BACKWARD = "backward"
    LATERAL = "lateral"


# ============================================================================
# TRANSITION GUARD SYSTEM
# ============================================================================

class TransitionGuard(ABC):
    """
    Base class for all transition guards.
    
    A guard is a validation mechanism that can prevent or allow transitions
    based on specific conditions. Guards can be preconditions (checked before
    transition) or postconditions (checked after transition).
    """
    
    def __init__(
        self,
        name: str,
        guard_type: GuardType = GuardType.PRECONDITION,
        priority: int = 0,
        required: bool = True
    ):
        """
        Initialize a transition guard.
        
        Args:
            name: Guard identifier
            guard_type: Type of guard (precondition/postcondition/etc)
            priority: Execution priority (higher = earlier)
            required: If True, guard failure blocks transition
        """
        self.name = name
        self.guard_type = guard_type
        self.priority = priority
        self.required = required
        self.enabled = True
        
    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """
        Evaluate if the guard condition is met.
        
        Args:
            context: Current FSM context
            
        Returns:
            True if guard passes, False otherwise
        """
        pass
    
    def __call__(self, context: Dict[str, Any]) -> bool:
        """Make guard callable."""
        if not self.enabled:
            return True
        return self.evaluate(context)
    
    def disable(self):
        """Disable this guard."""
        self.enabled = False
    
    def enable(self):
        """Enable this guard."""
        self.enabled = True


# ============================================================================
# SPECIFIC GUARD IMPLEMENTATIONS
# ============================================================================

class PreconditionGuard(TransitionGuard):
    """
    Guard that validates preconditions before transition.
    
    Preconditions must be satisfied before a transition can occur.
    """
    
    def __init__(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool]
    ):
        """
        Initialize precondition guard.
        
        Args:
            name: Guard name
            condition: Callable that evaluates precondition
        """
        super().__init__(
            name=name,
            guard_type=GuardType.PRECONDITION,
            required=True
        )
        self.condition = condition
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate precondition."""
        try:
            return self.condition(context)
        except Exception as e:
            logger.error("Precondition guard {} failed: {}".format(
                self.name, str(e)
            ))
            return False


class PostconditionGuard(TransitionGuard):
    """
    Guard that validates postconditions after transition.
    
    Postconditions verify that the transition had the desired effect.
    """
    
    def __init__(
        self,
        name: str,
        condition: Callable[[Dict[str, Any]], bool]
    ):
        """
        Initialize postcondition guard.
        
        Args:
            name: Guard name
            condition: Callable that evaluates postcondition
        """
        super().__init__(
            name=name,
            guard_type=GuardType.POSTCONDITION,
            required=False
        )
        self.condition = condition
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate postcondition."""
        try:
            return self.condition(context)
        except Exception as e:
            logger.warning("Postcondition guard {} failed: {}".format(
                self.name, str(e)
            ))
            return False


class ConditionalGuard(TransitionGuard):
    """
    Guard based on conditional logic.
    
    Supports complex conditions with multiple branches.
    """
    
    def __init__(
        self,
        name: str,
        conditions: List[Callable[[Dict[str, Any]], bool]],
        logic: str = "AND"
    ):
        """
        Initialize conditional guard.
        
        Args:
            name: Guard name
            conditions: List of condition functions
            logic: "AND" (all must pass) or "OR" (any can pass)
        """
        super().__init__(
            name=name,
            guard_type=GuardType.CONDITIONAL
        )
        self.conditions = conditions
        self.logic = logic.upper()
        
        if self.logic not in ["AND", "OR"]:
            raise ValueError("Logic must be 'AND' or 'OR'")
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate conditional with AND/OR logic."""
        if not self.conditions:
            return True
        
        results = [cond(context) for cond in self.conditions]
        
        if self.logic == "AND":
            return all(results)
        else:  # OR
            return any(results)


class ContextHasKeyGuard(TransitionGuard):
    """Guard that checks if context has a specific key."""
    
    def __init__(self, key: str, required: bool = True):
        """
        Initialize context key guard.
        
        Args:
            key: Context key to check
            required: If True, key must exist; if False, key must not exist
        """
        super().__init__(
            name="context_has_key_{}".format(key),
            guard_type=GuardType.CONTEXT_VALIDATOR
        )
        self.key = key
        self.required = required
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Check if key exists in context."""
        has_key = self.key in context
        
        if self.required:
            return has_key
        else:
            return not has_key


class ContextValueGuard(TransitionGuard):
    """Guard that checks context value."""
    
    def __init__(
        self,
        key: str,
        expected_value: Any
    ):
        """
        Initialize context value guard.
        
        Args:
            key: Context key
            expected_value: Expected value
        """
        super().__init__(
            name="context_value_{}".format(key),
            guard_type=GuardType.CONTEXT_VALIDATOR
        )
        self.key = key
        self.expected_value = expected_value
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Check if context value matches expected."""
        if self.key not in context:
            return False
        return context[self.key] == self.expected_value


# ============================================================================
# TRANSITION METADATA
# ============================================================================

@dataclass
class TransitionMetadata:
    """Metadata for a transition."""
    
    from_state: str
    to_state: str
    trigger: str
    created_at: datetime = field(default_factory=datetime.now)
    description: str = ""
    direction: TransitionDirection = TransitionDirection.FORWARD
    guards: List[TransitionGuard] = field(default_factory=list)
    callbacks: List[Callable] = field(default_factory=list)
    priority: int = 0
    reversible: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Export metadata as dictionary."""
        return {
            "from_state": self.from_state,
            "to_state": self.to_state,
            "trigger": self.trigger,
            "created_at": self.created_at.isoformat(),
            "description": self.description,
            "direction": self.direction.value,
            "guards_count": len(self.guards),
            "callbacks_count": len(self.callbacks),
            "priority": self.priority,
            "reversible": self.reversible
        }


# ============================================================================
# TRANSITION HISTORY
# ============================================================================

@dataclass
class TransitionRecord:
    """Record of a single transition execution."""
    
    from_state: str
    to_state: str
    trigger: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    success: bool = True
    error: Optional[str] = None
    user_id: Optional[str] = None
    context_snapshot: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export record as dictionary."""
        return {
            "from_state": self.from_state,
            "to_state": self.to_state,
            "trigger": self.trigger,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "success": self.success,
            "error": self.error,
            "user_id": self.user_id
        }


class TransitionHistory:
    """
    Maintains history of all transitions in a session.
    
    Provides query capabilities and analytics on transition patterns.
    """
    
    def __init__(self, max_records: int = 1000):
        """
        Initialize transition history.
        
        Args:
            max_records: Maximum records to keep (FIFO)
        """
        self.max_records = max_records
        self.records: List[TransitionRecord] = []
    
    def record_transition(
        self,
        from_state: str,
        to_state: str,
        trigger: str,
        duration_ms: float = 0.0,
        success: bool = True,
        error: Optional[str] = None,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> TransitionRecord:
        """Record a transition."""
        record = TransitionRecord(
            from_state=from_state,
            to_state=to_state,
            trigger=trigger,
            duration_ms=duration_ms,
            success=success,
            error=error,
            user_id=user_id,
            context_snapshot=context or {}
        )
        
        self.records.append(record)
        
        # Maintain max size (FIFO)
        if len(self.records) > self.max_records:
            self.records.pop(0)
        
        return record
    
    def get_last_transition(self) -> Optional[TransitionRecord]:
        """Get the most recent transition."""
        return self.records[-1] if self.records else None
    
    def get_transitions_by_state(
        self,
        state: str
    ) -> List[TransitionRecord]:
        """Get all transitions from a specific state."""
        return [r for r in self.records if r.from_state == state]
    
    def get_transitions_by_trigger(
        self,
        trigger: str
    ) -> List[TransitionRecord]:
        """Get all transitions using a specific trigger."""
        return [r for r in self.records if r.trigger == trigger]
    
    def get_failed_transitions(self) -> List[TransitionRecord]:
        """Get all failed transitions."""
        return [r for r in self.records if not r.success]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about transitions."""
        if not self.records:
            return {
                "total_transitions": 0,
                "successful": 0,
                "failed": 0,
                "average_duration_ms": 0.0
            }
        
        successful = len([r for r in self.records if r.success])
        failed = len([r for r in self.records if not r.success])
        avg_duration = sum(r.duration_ms for r in self.records) / len(self.records)
        
        return {
            "total_transitions": len(self.records),
            "successful": successful,
            "failed": failed,
            "success_rate": successful / len(self.records),
            "average_duration_ms": avg_duration
        }
    
    def clear(self):
        """Clear all history."""
        self.records.clear()


# ============================================================================
# TRANSITION VALIDATOR
# ============================================================================

class TransitionValidator:
    """
    Validates transitions against configured guards and constraints.
    
    Manages all guards for a transition and determines if it's allowed.
    """
    
    def __init__(self, transition_metadata: TransitionMetadata):
        """
        Initialize validator for a transition.
        
        Args:
            transition_metadata: Transition metadata with guards
        """
        self.metadata = transition_metadata
        self.preconditions: List[TransitionGuard] = []
        self.postconditions: List[TransitionGuard] = []
        
        # Separate guards by type
        for guard in transition_metadata.guards:
            if guard.guard_type == GuardType.PRECONDITION:
                self.preconditions.append(guard)
            elif guard.guard_type == GuardType.POSTCONDITION:
                self.postconditions.append(guard)
    
    def validate_preconditions(
        self,
        context: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate all preconditions.
        
        Args:
            context: Current FSM context
            
        Returns:
            (is_valid, error_message)
        """
        # Sort by priority (higher first)
        sorted_guards = sorted(
            self.preconditions,
            key=lambda g: g.priority,
            reverse=True
        )
        
        for guard in sorted_guards:
            try:
                if not guard.evaluate(context):
                    if guard.required:
                        return (False, "Guard {} failed: {}".format(
                            guard.name, guard.guard_type.value
                        ))
            except Exception as e:
                logger.error("Guard {} error: {}".format(
                    guard.name, str(e)
                ))
                if guard.required:
                    return (False, str(e))
        
        return (True, None)
    
    def validate_postconditions(
        self,
        context: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate all postconditions.
        
        Args:
            context: Context after transition
            
        Returns:
            (is_valid, error_message)
        """
        sorted_guards = sorted(
            self.postconditions,
            key=lambda g: g.priority,
            reverse=True
        )
        
        for guard in sorted_guards:
            try:
                if not guard.evaluate(context):
                    if guard.required:
                        return (False, "Postcondition {} failed".format(
                            guard.name
                        ))
                    else:
                        logger.warning("Postcondition {} failed (non-blocking)".format(
                            guard.name
                        ))
            except Exception as e:
                logger.error("Postcondition {} error: {}".format(
                    guard.name, str(e)
                ))
        
        return (True, None)
    
    def validate_transition(
        self,
        context: Dict[str, Any]
    ) -> bool:
        """
        Validate complete transition (pre + post).
        
        Args:
            context: Current context
            
        Returns:
            True if transition is allowed
        """
        is_valid, error = self.validate_preconditions(context)
        if not is_valid:
            logger.warning("Transition validation failed: {}".format(error))
            return False
        
        return True
    
    def can_transition(self, context: Dict[str, Any]) -> bool:
        """Check if transition is possible."""
        return self.validate_transition(context)


# ============================================================================
# TRANSITION BUILDER
# ============================================================================

class TransitionBuilder:
    """
    Fluent builder for creating transitions with guards.
    
    Provides a clean API for building complex transitions.
    """
    
    def __init__(
        self,
        from_state: str,
        to_state: str,
        trigger: str
    ):
        """Initialize builder."""
        self.metadata = TransitionMetadata(
            from_state=from_state,
            to_state=to_state,
            trigger=trigger
        )
    
    def with_description(self, description: str) -> "TransitionBuilder":
        """Add description."""
        self.metadata.description = description
        return self
    
    def with_guard(self, guard: TransitionGuard) -> "TransitionBuilder":
        """Add a guard."""
        self.metadata.guards.append(guard)
        return self
    
    def with_precondition(
        self,
        name: str,
        condition: Callable
    ) -> "TransitionBuilder":
        """Add precondition guard."""
        guard = PreconditionGuard(name, condition)
        self.metadata.guards.append(guard)
        return self
    
    def with_postcondition(
        self,
        name: str,
        condition: Callable
    ) -> "TransitionBuilder":
        """Add postcondition guard."""
        guard = PostconditionGuard(name, condition)
        self.metadata.guards.append(guard)
        return self
    
    def with_callback(self, callback: Callable) -> "TransitionBuilder":
        """Add callback."""
        self.metadata.callbacks.append(callback)
        return self
    
    def with_priority(self, priority: int) -> "TransitionBuilder":
        """Set transition priority."""
        self.metadata.priority = priority
        return self
    
    def reversible(self, value: bool = True) -> "TransitionBuilder":
        """Mark as reversible."""
        self.metadata.reversible = value
        return self
    
    def build(self) -> TransitionMetadata:
        """Build the transition."""
        return self.metadata


# ============================================================================
# TRANSITION CONFIGURATION (For backward compatibility)
# ============================================================================

@dataclass
class TransitionConfig:
    """
    Configuration for a transition in the FSM.
    
    Provides metadata and configuration for transitions between states.
    Compatible with existing THEA IA conversation_manager.py
    """
    from_state: str
    to_state: str
    trigger: str
    description: Optional[str] = None
    guards: Optional[List] = None
    callbacks: Optional[List[Callable]] = None
    priority: int = 0
    reversible: bool = False
    
    def __post_init__(self):
        """Initialize defaults."""
        if self.guards is None:
            self.guards = []
        if self.callbacks is None:
            self.callbacks = []


if __name__ == "__main__":
    # Example usage
    logger.info("FSM Transitions System v1.0.0 loaded")