"""
Tests for Nested States System

Author: Álvaro Fernández Mota
Date: 10 December 2025
Version: 1.0.0
"""

import pytest
from src.theaia.core.fsm.nested_states import (
    NestedState,
    NestedStateMachine,
    HistoryType
)


class TestNestedState:
    """Tests for NestedState class"""
    
    def test_create_simple_state(self):
        """Test creating a simple state without parent"""
        state = NestedState("idle")
        
        assert state.name == "idle"
        assert state.parent is None
        assert len(state.children) == 0
        assert state.history_type == HistoryType.NONE
    
    def test_create_state_with_parent(self):
        """Test creating state with parent relationship"""
        parent = NestedState("event_management")
        child = NestedState("creating_event", parent=parent)
        
        assert child.parent == parent
        assert child in parent.children
    
    def test_create_state_empty_name_raises(self):
        """Test that empty state name raises ValueError"""
        with pytest.raises(ValueError, match="State name must be a non-empty string"):
            NestedState("")
    
    def test_create_state_with_metadata(self):
        """Test creating state with metadata"""
        state = NestedState("idle", metadata={"priority": "high"})
        
        assert state.metadata["priority"] == "high"
    
    def test_add_child_manually(self):
        """Test manually adding child to parent"""
        parent = NestedState("root")
        child = NestedState("child")
        
        parent.add_child(child)
        
        assert child.parent == parent
        assert child in parent.children
    
    def test_add_child_with_different_parent_raises(self):
        """Test that adding child with different parent raises error"""
        parent1 = NestedState("parent1")
        parent2 = NestedState("parent2")
        child = NestedState("child", parent=parent1)
        
        with pytest.raises(ValueError, match="already has parent"):
            parent2.add_child(child)
    
    def test_remove_child(self):
        """Test removing child from parent"""
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        parent.remove_child(child)
        
        assert child.parent is None
        assert child not in parent.children
    
    def test_get_hierarchy_single_level(self):
        """Test hierarchy for single-level state"""
        state = NestedState("idle")
        
        assert state.get_hierarchy() == ["idle"]
    
    def test_get_hierarchy_multi_level(self):
        """Test hierarchy for multi-level nested states"""
        root = NestedState("event_management")
        creating = NestedState("creating_event", parent=root)
        gathering = NestedState("gathering_title", parent=creating)
        
        hierarchy = gathering.get_hierarchy()
        
        assert hierarchy == ["event_management", "creating_event", "gathering_title"]
    
    def test_get_depth_root_state(self):
        """Test depth for root state"""
        state = NestedState("root")
        
        assert state.get_depth() == 0
    
    def test_get_depth_nested_state(self):
        """Test depth for nested state"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        assert root.get_depth() == 0
        assert child.get_depth() == 1
        assert grandchild.get_depth() == 2
    
    def test_is_child_of_direct_parent(self):
        """Test is_child_of for direct parent"""
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        assert child.is_child_of("parent")
    
    def test_is_child_of_grandparent(self):
        """Test is_child_of for grandparent"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        assert grandchild.is_child_of("root")
        assert grandchild.is_child_of("child")
    
    def test_is_child_of_not_parent(self):
        """Test is_child_of for non-parent state"""
        parent1 = NestedState("parent1")
        parent2 = NestedState("parent2")
        child = NestedState("child", parent=parent1)
        
        assert not child.is_child_of("parent2")
    
    def test_get_root_from_root(self):
        """Test get_root from root state"""
        root = NestedState("root")
        
        assert root.get_root() == root
    
    def test_get_root_from_nested(self):
        """Test get_root from nested state"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        assert grandchild.get_root() == root
    
    def test_get_all_descendants_no_children(self):
        """Test get_all_descendants for state with no children"""
        state = NestedState("state")
        
        assert len(state.get_all_descendants()) == 0
    
    def test_get_all_descendants_with_children(self):
        """Test get_all_descendants for state with children"""
        root = NestedState("root")
        child1 = NestedState("child1", parent=root)
        child2 = NestedState("child2", parent=root)
        grandchild = NestedState("grandchild", parent=child1)
        
        descendants = root.get_all_descendants()
        
        assert len(descendants) == 3
        assert child1 in descendants
        assert child2 in descendants
        assert grandchild in descendants
    
    def test_state_hashable(self):
        """Test that NestedState is hashable"""
        state1 = NestedState("state")
        state2 = NestedState("state")
        
        state_set = {state1, state2}
        
        # Should only have one element due to same name
        assert len(state_set) == 1
    
    def test_state_equality(self):
        """Test state equality based on name"""
        state1 = NestedState("state")
        state2 = NestedState("state")
        state3 = NestedState("other")
        
        assert state1 == state2
        assert state1 != state3
    
    def test_state_repr(self):
        """Test state string representation"""
        root = NestedState("root")
        child = NestedState("child", parent=root)
        
        repr_str = repr(child)
        
        assert "NestedState" in repr_str
        assert "root" in repr_str
        assert "child" in repr_str


class TestNestedStateHistory:
    """Tests for state history functionality"""
    
    def test_save_shallow_history(self):
        """Test saving shallow history"""
        parent = NestedState("parent", history_type=HistoryType.SHALLOW)
        
        parent.save_history("child1", ["parent", "child1"])
        
        assert parent.last_child_state == "child1"
    
    def test_save_deep_history(self):
        """Test saving deep history"""
        parent = NestedState("parent", history_type=HistoryType.DEEP)
        
        hierarchy = ["root", "parent", "child", "grandchild"]
        parent.save_history("grandchild", hierarchy)
        
        assert parent.saved_hierarchy == hierarchy
    
    def test_get_history_state_shallow(self):
        """Test getting history state for shallow history"""
        parent = NestedState("parent", history_type=HistoryType.SHALLOW)
        parent.save_history("child1", ["parent", "child1"])
        
        assert parent.get_history_state() == "child1"
    
    def test_get_history_state_deep(self):
        """Test getting history state for deep history"""
        parent = NestedState("parent", history_type=HistoryType.DEEP)
        hierarchy = ["root", "parent", "child", "grandchild"]
        parent.save_history("grandchild", hierarchy)
        
        assert parent.get_history_state() == "grandchild"
    
    def test_get_history_state_no_history(self):
        """Test getting history state when no history exists"""
        parent = NestedState("parent", history_type=HistoryType.NONE)
        
        assert parent.get_history_state() is None


class TestNestedStateMachine:
    """Tests for NestedStateMachine class"""
    
    def test_create_state_machine(self):
        """Test creating a nested state machine"""
        fsm = NestedStateMachine(user_id="user123")
        
        assert fsm.user_id == "user123"
        assert fsm.current_state is not None
        assert fsm.current_state.name == "initial"
    
    def test_create_state_machine_custom_initial(self):
        """Test creating FSM with custom initial state"""
        fsm = NestedStateMachine(user_id="user123", initial_state="idle")
        
        assert fsm.current_state.name == "idle"
    
    def test_register_nested_state(self):
        """Test registering a nested state"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("event_management")
        
        fsm.register_nested_state(state)
        
        assert "event_management" in fsm.states
        assert fsm.states["event_management"] == state
    
    def test_register_duplicate_state_raises(self):
        """Test that registering duplicate state raises error"""
        fsm = NestedStateMachine(user_id="user123")
        state1 = NestedState("duplicate")
        state2 = NestedState("duplicate")
        
        fsm.register_nested_state(state1)
        
        with pytest.raises(ValueError, match="already registered"):
            fsm.register_nested_state(state2)
    
    def test_register_state_hierarchy(self):
        """Test registering entire state hierarchy"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("event_management")
        creating = NestedState("creating_event", parent=root)
        gathering = NestedState("gathering_title", parent=creating)
        
        fsm.register_state_hierarchy(root)
        
        assert "event_management" in fsm.states
        assert "creating_event" in fsm.states
        assert "gathering_title" in fsm.states
    
    def test_transition_to_registered_state(self):
        """Test transitioning to a registered state"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("idle")
        fsm.register_nested_state(state)
        
        result = fsm.transition_to("idle")
        
        assert result is True
        assert fsm.current_state.name == "idle"
    
    def test_transition_to_unregistered_state_raises(self):
        """Test that transitioning to unregistered state raises error"""
        fsm = NestedStateMachine(user_id="user123")
        
        with pytest.raises(ValueError, match="not registered"):
            fsm.transition_to("nonexistent")
    
    def test_transition_records_history(self):
        """Test that transitions are recorded in history"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("idle")
        fsm.register_nested_state(state)
        
        fsm.transition_to("idle")
        
        assert "idle" in fsm.history
    
    def test_get_current_hierarchy_initial(self):
        """Test getting hierarchy for initial state"""
        fsm = NestedStateMachine(user_id="user123")
        
        assert fsm.get_current_hierarchy() == ["initial"]
    
    def test_get_current_hierarchy_nested(self):
        """Test getting hierarchy for nested state"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("event_management")
        creating = NestedState("creating_event", parent=root)
        gathering = NestedState("gathering_title", parent=creating)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("gathering_title")
        
        hierarchy = fsm.get_current_hierarchy()
        
        assert hierarchy == ["event_management", "creating_event", "gathering_title"]
    
    def test_get_current_state_name(self):
        """Test getting current state name"""
        fsm = NestedStateMachine(user_id="user123")
        
        assert fsm.get_current_state_name() == "initial"
    
    def test_get_current_depth(self):
        """Test getting current state depth"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root")
        child = NestedState("child", parent=root)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("child")
        
        assert fsm.get_current_depth() == 1
    
    def test_is_in_state_exact_match(self):
        """Test is_in_state with exact match"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("idle")
        fsm.register_nested_state(state)
        fsm.transition_to("idle")
        
        assert fsm.is_in_state("idle")
    
    def test_is_in_state_parent_match(self):
        """Test is_in_state with parent match"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("event_management")
        child = NestedState("creating_event", parent=root)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("creating_event")
        
        assert fsm.is_in_state("event_management", include_descendants=True)
    
    def test_is_in_state_no_descendants(self):
        """Test is_in_state without descendant matching"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("event_management")
        child = NestedState("creating_event", parent=root)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("creating_event")
        
        assert not fsm.is_in_state("event_management", include_descendants=False)


class TestNestedStateMachineContext:
    """Tests for context management in nested FSM"""
    
    def test_update_context(self):
        """Test updating context"""
        fsm = NestedStateMachine(user_id="user123")
        
        fsm.update_context(title="Meeting", priority="high")
        
        assert fsm.context["title"] == "Meeting"
        assert fsm.context["priority"] == "high"
    
    def test_clear_context(self):
        """Test clearing context"""
        fsm = NestedStateMachine(user_id="user123")
        fsm.update_context(title="Meeting")
        
        fsm.clear_context()
        
        assert len(fsm.context) == 0
    
    def test_get_inherited_context_from_fsm(self):
        """Test getting context value from FSM context"""
        fsm = NestedStateMachine(user_id="user123")
        fsm.update_context(title="Meeting")
        
        assert fsm.get_inherited_context("title") == "Meeting"
    
    def test_get_inherited_context_from_parent_metadata(self):
        """Test getting context value from parent state metadata"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root", metadata={"default_duration": 60})
        child = NestedState("child", parent=root)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("child")
        
        assert fsm.get_inherited_context("default_duration") == 60
    
    def test_get_inherited_context_default(self):
        """Test getting context with default value"""
        fsm = NestedStateMachine(user_id="user123")
        
        assert fsm.get_inherited_context("nonexistent", default="default_value") == "default_value"


class TestNestedStateMachineCallbacks:
    """Tests for entry/exit callbacks"""
    
    def test_entry_callback_executed(self):
        """Test that entry callback is executed on transition"""
        fsm = NestedStateMachine(user_id="user123")
        callback_executed = []
        
        def on_enter(fsm_instance, context):
            callback_executed.append("entered")
        
        state = NestedState("idle", entry_callback=on_enter)
        fsm.register_nested_state(state)
        fsm.transition_to("idle")
        
        assert "entered" in callback_executed
    
    def test_exit_callback_executed(self):
        """Test that exit callback is executed on transition"""
        fsm = NestedStateMachine(user_id="user123")
        callback_executed = []
        
        def on_exit(fsm_instance, context):
            callback_executed.append("exited")
        
        state1 = NestedState("state1", exit_callback=on_exit)
        state2 = NestedState("state2")
        
        fsm.register_nested_state(state1)
        fsm.register_nested_state(state2)
        
        fsm.transition_to("state1")
        callback_executed.clear()
        fsm.transition_to("state2")
        
        assert "exited" in callback_executed
    
    def test_callback_receives_context(self):
        """Test that callbacks receive FSM and context"""
        fsm = NestedStateMachine(user_id="user123")
        fsm.update_context(test_value="hello")
        
        received_context = {}
        
        def on_enter(fsm_instance, context):
            received_context.update(context)
        
        state = NestedState("idle", entry_callback=on_enter)
        fsm.register_nested_state(state)
        fsm.transition_to("idle")
        
        assert received_context["test_value"] == "hello"
    
    def test_callback_error_handled(self):
        """Test that callback errors are handled gracefully"""
        fsm = NestedStateMachine(user_id="user123")
        
        def failing_callback(fsm_instance, context):
            raise RuntimeError("Callback failed")
        
        state = NestedState("idle", entry_callback=failing_callback)
        fsm.register_nested_state(state)
        
        # Should not raise, just log error
        result = fsm.transition_to("idle")
        
        assert result is True


class TestNestedStateMachineGuards:
    """Tests for transition guards"""
    
    def test_add_guard(self):
        """Test adding a guard"""
        fsm = NestedStateMachine(user_id="user123")
        
        def guard(fsm_instance, context):
            return True
        
        fsm.add_guard("initial", "idle", guard)
        
        assert "initial->idle" in fsm.guards
    
    def test_guard_allows_transition(self):
        """Test that guard can allow transition"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("idle")
        fsm.register_nested_state(state)
        
        def allow_guard(fsm_instance, context):
            return True
        
        fsm.add_guard("initial", "idle", allow_guard)
        
        result = fsm.transition_to("idle")
        
        assert result is True
        assert fsm.current_state.name == "idle"
    
    def test_guard_blocks_transition(self):
        """Test that guard can block transition"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("idle")
        fsm.register_nested_state(state)
        
        def block_guard(fsm_instance, context):
            return False
        
        fsm.add_guard("initial", "idle", block_guard)
        
        result = fsm.transition_to("idle")
        
        assert result is False
        assert fsm.current_state.name == "initial"
    
    def test_guard_checks_context(self):
        """Test that guard can check context"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("creating_event")
        fsm.register_nested_state(state)
        
        def context_guard(fsm_instance, context):
            return context.get("has_permission", False)
        
        fsm.add_guard("initial", "creating_event", context_guard)
        
        # Without permission
        result1 = fsm.transition_to("creating_event")
        assert result1 is False
        
        # With permission
        fsm.update_context(has_permission=True)
        result2 = fsm.transition_to("creating_event")
        assert result2 is True
    
    def test_guard_error_handled(self):
        """Test that guard errors block transition"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("idle")
        fsm.register_nested_state(state)
        
        def failing_guard(fsm_instance, context):
            raise RuntimeError("Guard failed")
        
        fsm.add_guard("initial", "idle", failing_guard)
        
        result = fsm.transition_to("idle")
        
        assert result is False


class TestNestedStateMachineHistory:
    """Tests for history restoration"""
    
    def test_save_state_history(self):
        """Test that history is saved on transition"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root", history_type=HistoryType.SHALLOW)
        child1 = NestedState("child1", parent=root)
        child2 = NestedState("child2", parent=root)
        
        fsm.register_state_hierarchy(root)
        fsm.transition_to("child1")
        fsm.transition_to("child2")
        
        # History should be saved in root
        assert root.last_child_state == "child1"
    
    def test_restore_from_shallow_history(self):
        """Test restoring from shallow history"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root", history_type=HistoryType.SHALLOW)
        child1 = NestedState("child1", parent=root)
        child2 = NestedState("child2", parent=root)
        
        fsm.register_state_hierarchy(root)
        
        # Navigate to child1, then child2, then back to root
        fsm.transition_to("child1")
        fsm.transition_to("child2")
        fsm.transition_to("root")
        
        # Restore should go back to child2
        result = fsm.restore_from_history("root")
        
        assert result is True
    
    def test_restore_from_deep_history(self):
        """Test restoring from deep history"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root", history_type=HistoryType.DEEP)
        child = NestedState("child", parent=root)
        grandchild = NestedState("grandchild", parent=child)
        
        fsm.register_state_hierarchy(root)
        
        fsm.transition_to("grandchild")
        fsm.transition_to("root")
        
        # Should restore full hierarchy
        result = fsm.restore_from_history("root")
        
        assert result is True
    
    def test_restore_no_history(self):
        """Test restoring when no history exists"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root", history_type=HistoryType.NONE)
        fsm.register_nested_state(root)
        
        result = fsm.restore_from_history("root")
        
        assert result is False


class TestNestedStateMachineUtilities:
    """Tests for utility methods"""
    
    def test_get_state_info(self):
        """Test getting comprehensive state info"""
        fsm = NestedStateMachine(user_id="user123")
        fsm.update_context(test="value")
        
        info = fsm.get_state_info()
        
        assert info["user_id"] == "user123"
        assert info["current_state"] == "initial"
        assert "context" in info
        assert "history" in info
        assert info["registered_states"] > 0
    
    def test_reset_state_machine(self):
        """Test resetting state machine"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("idle")
        fsm.register_nested_state(state)
        
        fsm.transition_to("idle")
        fsm.update_context(test="value")
        
        fsm.reset()
        
        assert fsm.current_state.name == "initial"
        assert len(fsm.context) == 0
        assert len(fsm.history) == 0
    
    def test_repr(self):
        """Test string representation"""
        fsm = NestedStateMachine(user_id="user123")
        
        repr_str = repr(fsm)
        
        assert "NestedStateMachine" in repr_str
        assert "user123" in repr_str
        assert "initial" in repr_str


class TestNestedStateMachineTransitionValidation:
    """Tests for transition validation logic"""
    
    def test_transition_from_initial_allowed(self):
        """Test that transitions from initial state are always allowed"""
        fsm = NestedStateMachine(user_id="user123")
        state = NestedState("any_state")
        fsm.register_nested_state(state)
        
        result = fsm.transition_to("any_state")
        
        assert result is True
    
    def test_transition_to_child_allowed(self):
        """Test transition to child state"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        fsm.register_state_hierarchy(parent)
        fsm.transition_to("parent")
        
        result = fsm.transition_to("child")
        
        assert result is True
    
    def test_transition_to_parent_allowed(self):
        """Test transition to parent state"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent")
        child = NestedState("child", parent=parent)
        
        fsm.register_state_hierarchy(parent)
        fsm.transition_to("child")
        
        result = fsm.transition_to("parent")
        
        assert result is True
    
    def test_transition_between_siblings_allowed(self):
        """Test transition between sibling states"""
        fsm = NestedStateMachine(user_id="user123")
        
        parent = NestedState("parent")
        child1 = NestedState("child1", parent=parent)
        child2 = NestedState("child2", parent=parent)
        
        fsm.register_state_hierarchy(parent)
        fsm.transition_to("child1")
        
        result = fsm.transition_to("child2")
        
        assert result is True
    
    def test_transition_to_root_allowed(self):
        """Test transition to root state"""
        fsm = NestedStateMachine(user_id="user123")
        
        root = NestedState("root")
        other = NestedState("other")
        
        fsm.register_nested_state(root)
        fsm.register_nested_state(other)
        
        fsm.transition_to("other")
        
        result = fsm.transition_to("root")
        
        assert result is True
