"""
Tests for Nested States System
Tests hierarchical state organization and transitions.

Author: Álvaro Fernández Mota
Date: 09 December 2025
"""

import pytest
from src.theaia.core.fsm.nested_states import NestedState, NestedStateMachine


class TestNestedState:
    """Test NestedState class"""
    
    def test_create_simple_state(self):
        """Test creating a simple state without parent"""
        state = NestedState("root")
        
        assert state.name == "root"
        assert state.parent is None
        assert len(state.children) == 0
        assert state.get_depth() == 0
    
    def test_create_state_with_parent(self):
        """Test creating state with parent"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        
        assert child.parent == root
        assert child in root.children
        assert child.get_depth() == 1
    
    def test_add_child_manually(self):
        """Test adding child after creation"""
        parent = NestedState("parent")
        child = NestedState("child")
        
        parent.add_child(child)
        
        assert child.parent == parent
        assert child in parent.children
    
    def test_remove_child(self):
        """Test removing child from parent"""
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        parent.remove_child(child)
        
        assert child.parent is None
        assert child not in parent.children
    
    def test_get_hierarchy_single_level(self):
        """Test hierarchy with single state"""
        state = NestedState("root")
        
        hierarchy = state.get_hierarchy()
        
        assert hierarchy == ["root"]
    
    def test_get_hierarchy_multi_level(self):
        """Test hierarchy with multiple levels"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        hierarchy = grandchild.get_hierarchy()
        
        assert hierarchy == ["root", "child", "grandchild"]
    
    def test_get_depth_levels(self):
        """Test depth calculation at different levels"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        assert root.get_depth() == 0
        assert child.get_depth() == 1
        assert grandchild.get_depth() == 2
    
    def test_is_child_of_direct_parent(self):
        """Test is_child_of with direct parent"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        
        assert child.is_child_of("root")
        assert not root.is_child_of("child")
    
    def test_is_child_of_grandparent(self):
        """Test is_child_of with grandparent"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        assert grandchild.is_child_of("root")
        assert grandchild.is_child_of("child")
        assert not root.is_child_of("grandchild")
    
    def test_is_child_of_not_related(self):
        """Test is_child_of with unrelated states"""
        state1 = NestedState("state1")
        state2 = NestedState("state2")
        
        assert not state1.is_child_of("state2")
        assert not state2.is_child_of("state1")
    
    def test_get_root(self):
        """Test getting root from any level"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        assert root.get_root() == root
        assert child.get_root() == root
        assert grandchild.get_root() == root
    
    def test_get_all_descendants(self):
        """Test getting all descendants"""
        root = NestedState("root")
        child1 = NestedState("child1", parent=root)
        child2 = NestedState("child2", parent=root)
        grandchild = NestedState("grandchild", parent=child1)
        
        descendants = root.get_all_descendants()
        
        assert len(descendants) == 3
        assert child1 in descendants
        assert child2 in descendants
        assert grandchild in descendants
    
    def test_state_equality(self):
        """Test state equality based on name"""
        state1 = NestedState("same_name")
        state2 = NestedState("same_name")
        state3 = NestedState("different")
        
        assert state1 == state2
        assert state1 != state3
    
    def test_state_hashable(self):
        """Test that states can be used in sets"""
        state1 = NestedState("state1")
        state2 = NestedState("state2")
        
        state_set = {state1, state2}
        
        assert len(state_set) == 2
        assert state1 in state_set
    
    def test_state_metadata(self):
        """Test state metadata storage"""
        state = NestedState("state", metadata={"key": "value"})
        
        assert state.metadata["key"] == "value"
        
        state.metadata["new_key"] = "new_value"
        assert state.metadata["new_key"] == "new_value"
    
    def test_invalid_state_name(self):
        """Test that empty state name raises error"""
        with pytest.raises(ValueError):
            NestedState("")
    
    def test_add_child_with_existing_parent_raises_error(self):
        """Test that adding child with different parent raises error"""
        parent1 = NestedState("parent1")
        parent2 = NestedState("parent2")
        child = NestedState("child", parent=parent1)
        
        with pytest.raises(ValueError):
            parent2.add_child(child)
    
    def test_repr(self):
        """Test string representation"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        
        assert "root > child" in repr(child)


class TestNestedStateMachine:
    """Test NestedStateMachine class"""
    
    def test_init_default(self):
        """Test initialization with default values"""
        fsm = NestedStateMachine(user_id="user123")
        
        assert fsm.user_id == "user123"
        assert fsm.get_current_state_name() == "initial"
        assert len(fsm.states) == 1
    
    def test_init_custom_initial(self):
        """Test initialization with custom initial state"""
        fsm = NestedStateMachine(user_id="user123", initial_state="start")
        
        assert fsm.get_current_state_name() == "start"
    
    def test_register_single_state(self):
        """Test registering single state"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("new_state")
        
        fsm.register_nested_state(state)
        
        assert "new_state" in fsm.states
        assert len(fsm.states) == 2  # initial + new_state
    
    def test_register_duplicate_state_raises_error(self):
        """Test that registering duplicate state raises error"""
        fsm = NestedStateMachine(user_id="user123")
        state1 = NestedState("duplicate")
        state2 = NestedState("duplicate")
        
        fsm.register_nested_state(state1)
        
        with pytest.raises(ValueError):
            fsm.register_nested_state(state2)
    
    def test_register_state_hierarchy(self):
        """Test registering entire hierarchy"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root")
        child1 = NestedState("child1", parent=root)
        child2 = NestedState("child2", parent=root)
        grandchild = NestedState("grandchild", parent=child1)
        
        fsm.register_state_hierarchy(root)
        
        assert len(fsm.states) == 5  # initial + 4 new states
        assert "root" in fsm.states
        assert "child1" in fsm.states
        assert "child2" in fsm.states
        assert "grandchild" in fsm.states
    
    def test_transition_to_registered_state(self):
        """Test transitioning to registered state"""
        fsm = NestedStateMachine(user_id="user123")
        target = NestedState("target")
        fsm.register_nested_state(target)
        
        result = fsm.transition_to("target")
        
        assert result is True
        assert fsm.get_current_state_name() == "target"
    
    def test_transition_to_unregistered_state_raises_error(self):
        """Test that transitioning to unregistered state raises error"""
        fsm = NestedStateMachine(user_id="user123")
        
        with pytest.raises(ValueError):
            fsm.transition_to("nonexistent")
    
    def test_transition_to_child_state(self):
        """Test transitioning from parent to child"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        fsm.register_nested_state(parent)
        fsm.register_nested_state(child)
        
        fsm.transition_to("parent")
        result = fsm.transition_to("child")
        
        assert result is True
        assert fsm.get_current_state_name() == "child"
    
    def test_transition_to_parent_state(self):
        """Test transitioning from child to parent"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        fsm.register_nested_state(parent)
        fsm.register_nested_state(child)
        
        fsm.transition_to("child")
        result = fsm.transition_to("parent")
        
        assert result is True
        assert fsm.get_current_state_name() == "parent"
    
    def test_transition_between_siblings(self):
        """Test transitioning between sibling states"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent")
        child1 = NestedState("child1", parent=parent)
        child2 = NestedState("child2", parent=parent)
        
        fsm.register_state_hierarchy(parent)
        
        fsm.transition_to("child1")
        result = fsm.transition_to("child2")
        
        assert result is True
        assert fsm.get_current_state_name() == "child2"
    
    def test_get_current_hierarchy(self):
        """Test getting current hierarchy"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("grandchild")
        
        hierarchy = fsm.get_current_hierarchy()
        
        assert hierarchy == ["root", "child", "grandchild"]
    
    def test_get_current_depth(self):
        """Test getting current depth"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root")
        child = NestedState("child", parent=root)
        
        fsm.register_state_hierarchy(root)
        
        fsm.transition_to("root")
        assert fsm.get_current_depth() == 0
        
        fsm.transition_to("child")
        assert fsm.get_current_depth() == 1
    
    def test_is_in_state_exact(self):
        """Test is_in_state with exact match"""
        fsm = NestedStateMachine(user_id="user123")
        
        state = NestedState("my_state")
        fsm.register_nested_state(state)
        fsm.transition_to("my_state")
        
        assert fsm.is_in_state("my_state")
        assert not fsm.is_in_state("other_state")
    
    def test_is_in_state_with_descendants(self):
        """Test is_in_state including descendants"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        fsm.register_state_hierarchy(parent)
        fsm.transition_to("child")
        
        # Child is in "parent" hierarchy
        assert fsm.is_in_state("parent", include_descendants=True)
        assert not fsm.is_in_state("parent", include_descendants=False)
    
    def test_update_context(self):
        """Test updating context"""
        fsm = NestedStateMachine(user_id="user123")
        
        fsm.update_context(key1="value1", key2="value2")
        
        assert fsm.context["key1"] == "value1"
        assert fsm.context["key2"] == "value2"
    
    def test_get_inherited_context_from_current(self):
        """Test getting context from current state"""
        fsm = NestedStateMachine(user_id="user123")
        fsm.update_context(key="value")
        
        result = fsm.get_inherited_context("key")
        
        assert result == "value"
    
    def test_get_inherited_context_from_parent(self):
        """Test getting context from parent state metadata"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent", metadata={"inherited_key": "parent_value"})
        child = NestedState("child", parent=parent)
        
        fsm.register_state_hierarchy(parent)
        fsm.transition_to("child")
        
        result = fsm.get_inherited_context("inherited_key")
        
        assert result == "parent_value"
    
    def test_get_inherited_context_default(self):
        """Test getting context with default value"""
        fsm = NestedStateMachine(user_id="user123")
        
        result = fsm.get_inherited_context("nonexistent", default="default_val")
        
        assert result == "default_val"
    
    def test_clear_context(self):
        """Test clearing context"""
        fsm = NestedStateMachine(user_id="user123")
        fsm.update_context(key="value")
        
        fsm.clear_context()
        
        assert len(fsm.context) == 0
    
    def test_get_state_info(self):
        """Test getting comprehensive state info"""
        fsm = NestedStateMachine(user_id="user123")
        fsm.update_context(test_key="test_value")
        
        info = fsm.get_state_info()
        
        assert info["user_id"] == "user123"
        assert info["current_state"] == "initial"
        assert "hierarchy" in info
        assert "depth" in info
        assert "context" in info
        assert info["context"]["test_key"] == "test_value"
    
    def test_reset(self):
        """Test resetting state machine"""
        fsm = NestedStateMachine(user_id="user123")
        
        state = NestedState("other")
        fsm.register_nested_state(state)
        fsm.transition_to("other")
        fsm.update_context(key="value")
        
        fsm.reset()
        
        assert fsm.get_current_state_name() == "initial"
        assert len(fsm.context) == 0
        assert len(fsm.history) == 0
    
    def test_history_tracking(self):
        """Test that transitions are tracked in history"""
        fsm = NestedStateMachine(user_id="user123")
        
        state1 = NestedState("state1")
        state2 = NestedState("state2")
        
        fsm.register_nested_state(state1)
        fsm.register_nested_state(state2)
        
        fsm.transition_to("state1")
        fsm.transition_to("state2")
        
        assert "state1" in fsm.history
        assert "state2" in fsm.history
    
    def test_repr(self):
        """Test string representation"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root")
        child = NestedState("child", parent=root)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("child")
        
        repr_str = repr(fsm)
        
        assert "user123" in repr_str
        assert "root" in repr_str
        assert "child" in repr_str
