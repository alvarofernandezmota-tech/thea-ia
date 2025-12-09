"""
Nested States System for FSM
Allows hierarchical state organization with parent-child relationships.

Author: Álvaro Fernández Mota
Date: 09 December 2025
Version: 1.0.0
"""

from typing import Optional, List, Dict, Set, Any
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class NestedState:
    """
    Represents a state that can have parent and children states.
    
    Attributes:
        name: Unique identifier for this state
        parent: Reference to parent state (None if root)
        children: Set of child states
        metadata: Additional state metadata
    
    Example:
        >>> root = NestedState("event_management")
        >>> child = NestedState("creating_event", parent=root)
        >>> root.add_child(child)
        >>> child.get_hierarchy()
        ['event_management', 'creating_event']
    """
    name: str
    parent: Optional['NestedState'] = None
    children: Set['NestedState'] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate state name and setup"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("State name must be a non-empty string")
        
        # Auto-register with parent
        if self.parent:
            self.parent.add_child(self)
    
    def add_child(self, child: 'NestedState') -> None:
        """
        Add a child state to this state.
        
        Args:
            child: Child state to add
            
        Raises:
            ValueError: If child already has a different parent
        """
        if child.parent and child.parent != self:
            raise ValueError(
                f"Child '{child.name}' already has parent '{child.parent.name}'"
            )
        
        child.parent = self
        self.children.add(child)
        logger.debug(f"Added child '{child.name}' to parent '{self.name}'")
    
    def remove_child(self, child: 'NestedState') -> None:
        """Remove a child state from this state"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            logger.debug(f"Removed child '{child.name}' from parent '{self.name}'")
    
    def get_hierarchy(self) -> List[str]:
        """
        Get full hierarchy path from root to this state.
        
        Returns:
            List of state names from root to current
            
        Example:
            >>> state.get_hierarchy()
            ['event_management', 'creating_event', 'gathering_title']
        """
        hierarchy = []
        current = self
        
        while current:
            hierarchy.insert(0, current.name)
            current = current.parent
        
        return hierarchy
    
    def get_depth(self) -> int:
        """
        Get depth level in hierarchy (root = 0).
        
        Returns:
            Depth level (0-based)
        """
        return len(self.get_hierarchy()) - 1
    
    def is_child_of(self, potential_parent: str) -> bool:
        """
        Check if this state is a child/descendant of given parent.
        
        Args:
            potential_parent: Name of potential parent state
            
        Returns:
            True if this state is descendant of potential_parent
        """
        current = self.parent
        
        while current:
            if current.name == potential_parent:
                return True
            current = current.parent
        
        return False
    
    def get_root(self) -> 'NestedState':
        """
        Get root state of this hierarchy.
        
        Returns:
            Root state (topmost parent)
        """
        current = self
        
        while current.parent:
            current = current.parent
        
        return current
    
    def get_all_descendants(self) -> Set['NestedState']:
        """
        Get all descendant states (children, grandchildren, etc).
        
        Returns:
            Set of all descendant states
        """
        descendants = set()
        
        for child in self.children:
            descendants.add(child)
            descendants.update(child.get_all_descendants())
        
        return descendants
    
    def __hash__(self):
        """Make NestedState hashable for use in sets"""
        return hash(self.name)
    
    def __eq__(self, other):
        """Equality based on state name"""
        if not isinstance(other, NestedState):
            return False
        return self.name == other.name
    
    def __repr__(self):
        """String representation"""
        hierarchy = " > ".join(self.get_hierarchy())
        return f"NestedState({hierarchy})"


class NestedStateMachine:
    """
    State Machine with support for nested/hierarchical states.
    
    Features:
        - Parent-child state relationships
        - Context inheritance from parent states
        - Automatic transition validation through hierarchy
        - State entry/exit callbacks for each level
    
    Example:
        >>> fsm = NestedStateMachine(user_id="user123")
        >>> 
        >>> # Setup hierarchy
        >>> root = NestedState("event_management")
        >>> creating = NestedState("creating_event", parent=root)
        >>> gathering = NestedState("gathering_title", parent=creating)
        >>> 
        >>> fsm.register_nested_state(root)
        >>> fsm.register_nested_state(creating)
        >>> fsm.register_nested_state(gathering)
        >>> 
        >>> # Transition
        >>> fsm.transition_to("gathering_title")
        >>> fsm.get_current_hierarchy()
        ['event_management', 'creating_event', 'gathering_title']
    """
    
    def __init__(self, user_id: str, initial_state: str = "initial"):
        """
        Initialize nested state machine.
        
        Args:
            user_id: User identifier for this FSM instance
            initial_state: Initial state name (default: "initial")
        """
        self.user_id = user_id
        self.current_state: Optional[NestedState] = None
        self.states: Dict[str, NestedState] = {}
        self.context: Dict[str, Any] = {}
        self.history: List[str] = []
        
        # Create and set initial state
        initial = NestedState(initial_state)
        self.register_nested_state(initial)
        self.current_state = initial
        
        logger.info(f"NestedStateMachine initialized for user {user_id}")
    
    def register_nested_state(self, state: NestedState) -> None:
        """
        Register a nested state in the machine.
        
        Args:
            state: NestedState to register
            
        Raises:
            ValueError: If state name already exists
        """
        if state.name in self.states:
            raise ValueError(f"State '{state.name}' already registered")
        
        self.states[state.name] = state
        logger.debug(f"Registered nested state: {state.name}")
    
    def register_state_hierarchy(self, root: NestedState) -> None:
        """
        Register entire state hierarchy (root + all descendants).
        
        Args:
            root: Root state of hierarchy to register
        """
        # Register root
        self.register_nested_state(root)
        
        # Register all descendants
        for descendant in root.get_all_descendants():
            self.register_nested_state(descendant)
        
        logger.info(f"Registered hierarchy with root: {root.name}")
    
    def transition_to(self, target_state_name: str) -> bool:
        """
        Transition to target state (nested or flat).
        
        Args:
            target_state_name: Name of target state
            
        Returns:
            True if transition successful
            
        Raises:
            ValueError: If target state doesn't exist
        """
        if target_state_name not in self.states:
            raise ValueError(f"State '{target_state_name}' not registered")
        
        target_state = self.states[target_state_name]
        
        # Validate transition
        if not self._can_transition(target_state):
            logger.warning(
                f"Transition from {self.current_state.name} to "
                f"{target_state_name} not allowed"
            )
            return False
        
        # Execute transition
        old_state = self.current_state
        self.current_state = target_state
        
        # Record in history
        self.history.append(target_state_name)
        
        logger.info(
            f"Transitioned from {old_state.name} to {target_state_name} "
            f"(hierarchy: {' > '.join(target_state.get_hierarchy())})"
        )
        
        return True
    
    def _can_transition(self, target: NestedState) -> bool:
        """
        Check if transition to target state is allowed.
        
        Args:
            target: Target state
            
        Returns:
            True if transition is valid
        """
        # Always allow first transition from initial state
        if self.current_state.name == "initial":
            return True
        
        # Always allow transitions within same hierarchy
        if target.is_child_of(self.current_state.name):
            return True
        
        if self.current_state.is_child_of(target.name):
            return True
        
        # Allow transitions between siblings
        if target.parent == self.current_state.parent:
            return True
        
        # Allow transitions to root states (no parent)
        if target.parent is None or self.current_state.parent is None:
            return True
        
        return False
    
    def get_current_hierarchy(self) -> List[str]:
        """
        Get current state hierarchy path.
        
        Returns:
            List of state names from root to current
        """
        if not self.current_state:
            return []
        
        return self.current_state.get_hierarchy()
    
    def get_current_state_name(self) -> str:
        """
        Get current state name.
        
        Returns:
            Current state name
        """
        return self.current_state.name if self.current_state else "unknown"
    
    def get_current_depth(self) -> int:
        """
        Get current hierarchy depth.
        
        Returns:
            Depth level (0 = root)
        """
        return self.current_state.get_depth() if self.current_state else 0
    
    def is_in_state(self, state_name: str, include_descendants: bool = True) -> bool:
        """
        Check if currently in given state.
        
        Args:
            state_name: State name to check
            include_descendants: If True, also match if in child states
            
        Returns:
            True if in state (or descendant if include_descendants=True)
        """
        if not self.current_state:
            return False
        
        # Exact match
        if self.current_state.name == state_name:
            return True
        
        # Check if current is descendant of state_name
        if include_descendants:
            return self.current_state.is_child_of(state_name)
        
        return False
    
    def get_inherited_context(self, key: str, default: Any = None) -> Any:
        """
        Get context value, checking parent states if not found.
        
        Args:
            key: Context key to retrieve
            default: Default value if key not found
            
        Returns:
            Context value (from current or parent state)
        """
        # Check current state context
        if key in self.context:
            return self.context[key]
        
        # Check parent metadata
        current = self.current_state
        while current:
            if key in current.metadata:
                return current.metadata[key]
            current = current.parent
        
        return default
    
    def update_context(self, **kwargs) -> None:
        """
        Update context with new values.
        
        Args:
            **kwargs: Key-value pairs to update
        """
        self.context.update(kwargs)
        logger.debug(f"Updated context: {kwargs}")
    
    def clear_context(self) -> None:
        """Clear all context data"""
        self.context.clear()
        logger.debug("Context cleared")
    
    def get_state_info(self) -> Dict[str, Any]:
        """
        Get comprehensive state information.
        
        Returns:
            Dictionary with current state details
        """
        return {
            "user_id": self.user_id,
            "current_state": self.get_current_state_name(),
            "hierarchy": self.get_current_hierarchy(),
            "depth": self.get_current_depth(),
            "context": self.context.copy(),
            "history": self.history[-10:],  # Last 10 transitions
            "registered_states": len(self.states)
        }
    
    def reset(self) -> None:
        """Reset state machine to initial state"""
        if "initial" in self.states:
            self.current_state = self.states["initial"]
            self.context.clear()
            self.history.clear()
            logger.info(f"State machine reset for user {self.user_id}")
        else:
            logger.warning("Cannot reset: 'initial' state not registered")
    
    def __repr__(self):
        """String representation"""
        hierarchy = " > ".join(self.get_current_hierarchy())
        return f"NestedStateMachine(user={self.user_id}, state={hierarchy})"
