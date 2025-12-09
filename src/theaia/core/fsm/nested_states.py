"""
Nested States System for FSM
Allows hierarchical state organization with parent-child relationships.

Author: Álvaro Fernández Mota
Date: 10 December 2025 (Updated)
Version: 2.0.0
"""

from typing import Optional, List, Dict, Set, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class HistoryType(Enum):
    """Types of history restoration"""
    NONE = "none"
    SHALLOW = "shallow"  # Restore last direct child
    DEEP = "deep"        # Restore entire hierarchy


@dataclass
class NestedState:
    """
    Represents a state that can have parent and children states.
    
    Attributes:
        name: Unique identifier for the state
        parent: Parent state (None for root states)
        children: Set of child states
        metadata: Custom data attached to state
        entry_callback: Function called on state entry
        exit_callback: Function called on state exit
        history_type: Type of history to maintain
    """
    name: str
    parent: Optional['NestedState'] = None
    children: Set['NestedState'] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    entry_callback: Optional[Callable] = None
    exit_callback: Optional[Callable] = None
    history_type: HistoryType = HistoryType.NONE
    
    # History tracking
    last_child_state: Optional[str] = None
    saved_hierarchy: Optional[List[str]] = None
    
    def __post_init__(self):
        """Validate state after initialization"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("State name must be a non-empty string")
        
        # Automatically register with parent if provided
        if self.parent is not None:
            self.parent.children.add(self)
    
    def add_child(self, child: 'NestedState') -> None:
        """
        Add a child state to this state.
        
        Args:
            child: The child state to add
            
        Raises:
            ValueError: If child already has a different parent
        """
        if child.parent is not None and child.parent != self:
            raise ValueError(f"State '{child.name}' already has parent '{child.parent.name}'")
        
        child.parent = self
        self.children.add(child)
    
    def remove_child(self, child: 'NestedState') -> None:
        """
        Remove a child state from this state.
        
        Args:
            child: The child state to remove
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None
    
    def get_hierarchy(self) -> List[str]:
        """
        Get the full hierarchy path from root to this state.
        
        Returns:
            List of state names from root to current state
        """
        hierarchy = []
        current = self
        
        while current is not None:
            hierarchy.insert(0, current.name)
            current = current.parent
        
        return hierarchy
    
    def get_depth(self) -> int:
        """
        Get the depth of this state in the hierarchy.
        
        Returns:
            Depth level (0 for root states)
        """
        depth = 0
        current = self.parent
        
        while current is not None:
            depth += 1
            current = current.parent
        
        return depth
    
    def is_child_of(self, state_name: str) -> bool:
        """
        Check if this state is a child (or grandchild, etc.) of a given state.
        
        Args:
            state_name: Name of potential parent state
            
        Returns:
            True if this state is a descendant of the given state
        """
        current = self.parent
        
        while current is not None:
            if current.name == state_name:
                return True
            current = current.parent
        
        return False
    
    def get_root(self) -> 'NestedState':
        """
        Get the root state of this hierarchy.
        
        Returns:
            The root state
        """
        current = self
        
        while current.parent is not None:
            current = current.parent
        
        return current
    
    def get_all_descendants(self) -> List['NestedState']:
        """
        Get all descendant states recursively.
        
        Returns:
            List of all descendant states
        """
        descendants = []
        
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        
        return descendants
    
    def save_history(self, state_name: str, hierarchy: List[str]) -> None:
        """
        Save history for this state.
        
        Args:
            state_name: Name of the state to save
            hierarchy: Full hierarchy path to save
        """
        if self.history_type == HistoryType.SHALLOW:
            self.last_child_state = state_name
        elif self.history_type == HistoryType.DEEP:
            self.saved_hierarchy = hierarchy.copy()
    
    def get_history_state(self) -> Optional[str]:
        """
        Get the saved history state.
        
        Returns:
            Saved state name or None if no history
        """
        if self.history_type == HistoryType.SHALLOW:
            return self.last_child_state
        elif self.history_type == HistoryType.DEEP and self.saved_hierarchy:
            return self.saved_hierarchy[-1]
        return None
    
    def __hash__(self):
        """Make state hashable based on name"""
        return hash(self.name)
    
    def __eq__(self, other):
        """States are equal if they have the same name"""
        if not isinstance(other, NestedState):
            return False
        return self.name == other.name
    
    def __repr__(self):
        """String representation of the state"""
        hierarchy = " -> ".join(self.get_hierarchy())
        return f"NestedState({hierarchy})"


class NestedStateMachine:
    """
    State machine with support for nested/hierarchical states.
    
    Features:
    - Hierarchical state organization
    - State history (shallow and deep)
    - Entry/exit callbacks
    - Transition guards
    - Context inheritance
    """
    
    def __init__(self, user_id: str, initial_state: str = "initial"):
        """
        Initialize the nested state machine.
        
        Args:
            user_id: Unique identifier for the user/session
            initial_state: Name of the initial state
        """
        self.user_id = user_id
        self.states: Dict[str, NestedState] = {}
        self.guards: Dict[str, Callable] = {}
        self.context: Dict[str, Any] = {}
        self.history: List[str] = []
        
        # Create and register initial state
        initial = NestedState(initial_state)
        self.register_nested_state(initial)
        self.current_state = initial
    
    def register_nested_state(self, state: NestedState) -> None:
        """
        Register a state in the state machine.
        
        Args:
            state: The state to register
            
        Raises:
            ValueError: If state name is already registered
        """
        if state.name in self.states:
            raise ValueError(f"State '{state.name}' is already registered")
        
        self.states[state.name] = state
    
    def register_state_hierarchy(self, root_state: NestedState) -> None:
        """
        Register a complete state hierarchy.
        
        Args:
            root_state: The root state of the hierarchy
        """
        # Register root
        if root_state.name not in self.states:
            self.register_nested_state(root_state)
        
        # Register all descendants
        for descendant in root_state.get_all_descendants():
            if descendant.name not in self.states:
                self.register_nested_state(descendant)
    
    def add_guard(self, from_state: str, to_state: str, guard: Callable) -> None:
        """
        Add a guard condition for a transition.
        
        Args:
            from_state: Source state name
            to_state: Target state name
            guard: Function that returns True if transition is allowed
        """
        key = f"{from_state}->{to_state}"
        self.guards[key] = guard
    
    def transition_to(self, state_name: str) -> bool:
        """
        Transition to a new state.
        
        Args:
            state_name: Name of the target state
            
        Returns:
            True if transition succeeded, False otherwise
            
        Raises:
            ValueError: If target state is not registered
        """
        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' is not registered")
        
        target_state = self.states[state_name]
        
        # Check guard conditions
        guard_key = f"{self.current_state.name}->{state_name}"
        if guard_key in self.guards:
            try:
                if not self.guards[guard_key](self, self.context):
                    logger.warning(f"Guard blocked transition from {self.current_state.name} to {state_name}")
                    return False
            except Exception as e:
                logger.error(f"Guard error: {e}")
                return False
        
        # Save history in parent states
        current_hierarchy = self.current_state.get_hierarchy()
        
        # Find common ancestor and save history
        for i, state_name_in_path in enumerate(current_hierarchy[:-1]):
            state = self.states[state_name_in_path]
            if state.history_type != HistoryType.NONE:
                # Save the child state that we're leaving
                if i + 1 < len(current_hierarchy):
                    child_state = current_hierarchy[i + 1]
                    state.save_history(child_state, current_hierarchy)
        
        # Execute exit callback
        if self.current_state.exit_callback:
            try:
                self.current_state.exit_callback(self, self.context)
            except Exception as e:
                logger.error(f"Exit callback error: {e}")
        
        # Perform transition
        old_state = self.current_state
        self.current_state = target_state
        self.history.append(state_name)
        
        logger.info(f"Transitioned from {old_state.name} to {state_name}")
        
        # Execute entry callback
        if self.current_state.entry_callback:
            try:
                self.current_state.entry_callback(self, self.context)
            except Exception as e:
                logger.error(f"Entry callback error: {e}")
        
        return True
    
    def restore_from_history(self, state_name: str) -> bool:
        """
        Restore to a previously saved history state.
        
        Args:
            state_name: Name of the state with saved history
            
        Returns:
            True if restoration succeeded, False otherwise
        """
        if state_name not in self.states:
            logger.warning(f"State '{state_name}' not found")
            return False
        
        state = self.states[state_name]
        history_state = state.get_history_state()
        
        if history_state is None:
            logger.warning(f"No history found for state '{state_name}'")
            return False
        
        # Transition to the saved history state
        return self.transition_to(history_state)
    
    def get_current_hierarchy(self) -> List[str]:
        """
        Get the current state hierarchy.
        
        Returns:
            List of state names from root to current
        """
        return self.current_state.get_hierarchy()
    
    def get_current_state_name(self) -> str:
        """
        Get the name of the current state.
        
        Returns:
            Current state name
        """
        return self.current_state.name
    
    def get_current_depth(self) -> int:
        """
        Get the depth of the current state.
        
        Returns:
            Depth level of current state
        """
        return self.current_state.get_depth()
    
    def is_in_state(self, state_name: str, include_descendants: bool = False) -> bool:
        """
        Check if currently in a specific state.
        
        Args:
            state_name: Name of the state to check
            include_descendants: If True, also check if in any descendant state
            
        Returns:
            True if in the specified state
        """
        if self.current_state.name == state_name:
            return True
        
        if include_descendants:
            return self.current_state.is_child_of(state_name)
        
        return False
    
    def update_context(self, **kwargs) -> None:
        """
        Update the context dictionary.
        
        Args:
            **kwargs: Key-value pairs to add to context
        """
        self.context.update(kwargs)
    
    def clear_context(self) -> None:
        """Clear all context data"""
        self.context.clear()
    
    def get_inherited_context(self, key: str, default: Any = None) -> Any:
        """
        Get a context value with inheritance from parent states.
        
        Args:
            key: Context key to retrieve
            default: Default value if key not found
            
        Returns:
            Context value or default
        """
        # Check FSM context first
        if key in self.context:
            return self.context[key]
        
        # Check parent state metadata
        current = self.current_state
        while current is not None:
            if key in current.metadata:
                return current.metadata[key]
            current = current.parent
        
        return default
    
    def get_state_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about current state.
        
        Returns:
            Dictionary with state information
        """
        return {
            "user_id": self.user_id,
            "current_state": self.current_state.name,
            "hierarchy": self.get_current_hierarchy(),
            "depth": self.get_current_depth(),
            "context": self.context.copy(),
            "history": self.history.copy(),
            "registered_states": len(self.states)
        }
    
    def reset(self) -> None:
        """Reset state machine to initial state"""
        initial_state = self.states.get("initial")
        if initial_state:
            self.current_state = initial_state
        self.context.clear()
        self.history.clear()
    
    def __repr__(self):
        """String representation"""
        return f"NestedStateMachine(user={self.user_id}, state={self.current_state.name})"
