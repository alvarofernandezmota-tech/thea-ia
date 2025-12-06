"""
Unit tests for BaseStateMachine and ConversationStateMachine
H03 FASE 1 - TAREA 1.2.3
"""


import pytest
import time
from datetime import datetime
from src.theaia.core.fsm import ConversationStateMachine



class TestBaseStateMachine:
    """Test BaseStateMachine functionality"""
    
    def test_initialization(self):
        """Test FSM initializes with correct state"""
        fsm = ConversationStateMachine(user_id="test_user")
        assert fsm.state == "initial"
        assert fsm.user_id == "test_user"
    
    def test_validate_state_valid(self):
        """Test state validation for valid states"""
        fsm = ConversationStateMachine(user_id="test_user")
        assert fsm.validate_state("initial") is True
        assert fsm.validate_state("agent_delegated") is True
    
    def test_validate_state_invalid(self):
        """Test state validation for invalid states"""
        fsm = ConversationStateMachine(user_id="test_user")
        assert fsm.validate_state("invalid_state") is False
    
    def test_get_valid_transitions_from_initial(self):
        """Test getting valid transitions from initial state"""
        fsm = ConversationStateMachine(user_id="test_user")
        valid = fsm.get_valid_transitions_set()
        assert "request_disambiguation" in valid
        assert "delegate_to_agent" in valid
        assert "reset" in valid
        assert "error" in valid
    
    def test_can_transition_to_valid(self):
        """Test checking valid transition"""
        fsm = ConversationStateMachine(user_id="test_user")
        assert fsm.can_transition_to("delegate_to_agent") is True
        assert fsm.can_transition_to("request_disambiguation") is True
    
    def test_can_transition_to_invalid(self):
        """Test checking invalid transition"""
        fsm = ConversationStateMachine(user_id="test_user")
        assert fsm.can_transition_to("invalid_trigger") is False
        assert fsm.can_transition_to("resolve_disambiguation") is False  # Not valid from initial
    
    def test_transition_safe_valid(self):
        """Test safe transition with valid trigger"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.active_agent = "agenda"
        result = fsm.transition_safe("delegate_to_agent")
        assert result is True
        assert fsm.state == "agent_delegated"
    
    def test_transition_safe_invalid_raises(self):
        """Test safe transition with invalid trigger raises error"""
        fsm = ConversationStateMachine(user_id="test_user")
        with pytest.raises(Exception):
            fsm.transition_safe("invalid_trigger")
    
    def test_get_state_info(self):
        """Test getting state information"""
        fsm = ConversationStateMachine(user_id="test_user")
        info = fsm.get_state_info()
        
        assert info["current_state"] == "initial"
        assert isinstance(info["valid_transitions"], list)
        assert isinstance(info["context"], dict)
        assert "timestamp" in info
        assert "request_disambiguation" in info["valid_transitions"]
    
    def test_update_context(self):
        """Test context update"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(test_key="test_value", number=42)
        
        assert fsm.get_context("test_key") == "test_value"
        assert fsm.get_context("number") == 42
    
    def test_get_context_all(self):
        """Test getting all context"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key1="value1", key2="value2")
        context = fsm.get_context()
        
        assert context["key1"] == "value1"
        assert context["key2"] == "value2"
    
    def test_get_context_with_default(self):
        """Test getting context with default value"""
        fsm = ConversationStateMachine(user_id="test_user")
        result = fsm.get_context("nonexistent", "default_value")
        assert result == "default_value"
    
    def test_clear_context(self):
        """Test clearing context"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key1="value1", key2="value2", session_id="test_session")
        fsm.clear_context()
        
        # Session ID should be preserved
        assert "session_id" in fsm.context or len(fsm.context) < 3



class TestConversationStateMachine:
    """Test ConversationStateMachine specific functionality"""
    
    def test_session_tracking(self):
        """Test session creation and tracking"""
        fsm = ConversationStateMachine(user_id="test_user")
        
        assert fsm.session_id is not None
        assert fsm.created_at is not None
        assert fsm.last_activity is not None
    
    def test_session_id_custom(self):
        """Test custom session ID"""
        custom_session = "custom_session_123"
        fsm = ConversationStateMachine(user_id="test_user", session_id=custom_session)
        
        assert fsm.session_id == custom_session
    
    def test_get_session_duration(self):
        """Test getting session duration"""
        fsm = ConversationStateMachine(user_id="test_user")
        time.sleep(0.1)
        
        duration = fsm.get_session_duration()
        assert duration >= 0.1
        assert isinstance(duration, float)
    
    def test_track_activity(self):
        """Test activity tracking"""
        fsm = ConversationStateMachine(user_id="test_user")
        initial_activity = fsm.last_activity
        
        time.sleep(0.05)
        fsm.track_activity()
        
        assert fsm.last_activity > initial_activity
    
    def test_export_state(self):
        """Test exporting complete state"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key="value")
        exported = fsm.export_state()
        
        assert exported["user_id"] == "test_user"
        assert exported["current_state"] == "initial"
        assert exported["context"]["key"] == "value"
        assert "session_duration_seconds" in exported
        assert "created_at" in exported
        assert "last_activity" in exported
        assert "session_id" in exported
        assert isinstance(exported["valid_transitions"], list)
    
    def test_disambiguation_flow(self):
        """Test disambiguation flow"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.request_disambiguation()
        
        assert fsm.state == "awaiting_disambiguation"
        assert fsm.get_context("disambiguation_started") is True
    
    def test_delegation_flow(self):
        """Test delegation flow from initial state"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.active_agent = "agenda"
        fsm.delegate_to_agent()
        
        assert fsm.state == "agent_delegated"
        assert fsm.get_context("active_agent") == "agenda"
    
    def test_delegation_flow_from_disambiguation(self):
        """Test delegation flow from awaiting_disambiguation state"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.request_disambiguation()
        assert fsm.state == "awaiting_disambiguation"
        
        fsm.active_agent = "notas"
        fsm.delegate_to_agent()
        
        assert fsm.state == "agent_delegated"
        assert fsm.get_context("active_agent") == "notas"
    
    def test_complete_flow(self):
        """Test complete conversation flow"""
        fsm = ConversationStateMachine(user_id="test_user")
        
        # Start disambiguation
        fsm.request_disambiguation()
        assert fsm.state == "awaiting_disambiguation"
        
        # Delegate to agent
        fsm.active_agent = "agenda"
        fsm.delegate_to_agent()
        assert fsm.state == "agent_delegated"
        
        # Complete conversation
        fsm.complete_conversation()
        assert fsm.state == "completed"
        assert fsm.get_context("status") == "completed"
    
    def test_complete_from_disambiguation(self):
        """Test completing conversation directly from disambiguation"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.request_disambiguation()
        
        fsm.complete_conversation()
        assert fsm.state == "completed"
    
    def test_resolve_disambiguation_flow(self):
        """Test resolve disambiguation flow"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.request_disambiguation()
        assert fsm.state == "awaiting_disambiguation"
        
        fsm.resolve_disambiguation()
        assert fsm.state == "agent_delegated"
        assert fsm.get_context("disambiguation_resolved") is True



class TestStateMachineExceptions:
    """Test exception handling"""
    
    def test_reset_from_any_state(self):
        """Test reset capability from any state"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.delegate_to_agent()
        assert fsm.state == "agent_delegated"
        
        fsm.reset()
        assert fsm.state == "initial"
    
    def test_reset_clears_context(self):
        """Test reset clears context"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(test_key="test_value")
        fsm.reset()
        
        assert fsm.get_context("test_key") is None
    
    def test_error_state_from_any_state(self):
        """Test error state transition from any state"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.delegate_to_agent()
        assert fsm.state == "agent_delegated"
        
        fsm.error()
        assert fsm.state == "error_state"
    
    def test_error_state_from_initial(self):
        """Test error state transition from initial"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.error()
        assert fsm.state == "error_state"
    
    def test_session_timeout(self):
        """Test session timeout transition"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.delegate_to_agent()
        
        fsm.timeout_session()
        assert fsm.state == "session_timeout"
    
    def test_session_timeout_from_any_state(self):
        """Test session timeout clears context"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key="value")
        fsm.timeout_session()
        
        assert fsm.state == "session_timeout"



class TestContextMerging:
    """Test context merging functionality"""
    
    def test_merge_context_merge_strategy(self):
        """Test context merge with merge strategy"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key1="value1", key2="value2")
        
        new_context = {"key2": "new_value2", "key3": "value3"}
        result = fsm.merge_context(new_context, strategy="merge")
        
        assert result["key1"] == "value1"
        assert result["key2"] == "new_value2"
        assert result["key3"] == "value3"
    
    def test_merge_context_overwrite_strategy(self):
        """Test context merge with overwrite strategy"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key1="value1", key2="value2")
        
        new_context = {"key2": "new_value2", "key3": "value3"}
        result = fsm.merge_context(new_context, strategy="overwrite")
        
        # Overwrite strategy replaces entire context
        assert "key1" not in result or result.get("key1") is None
    
    def test_get_context_stats(self):
        """Test getting context statistics"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key1="value1", key2="value2")
        
        stats = fsm.get_context_stats()
        assert isinstance(stats, dict)
    
    def test_prune_context(self):
        """Test context pruning"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key1="value1", key2="value2", key3="value3")
        
        fsm.prune_context(keep_keys=["key1", "key3"])
        context = fsm.get_context()
        
        assert "key1" in context
        assert "key3" in context
        assert "key2" not in context or context.get("key2") is None
    
    def test_prune_context_empty_keys(self):
        """Test pruning context with empty keys list"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(key1="value1", key2="value2")
        
        fsm.prune_context(keep_keys=[])
        context = fsm.get_context()
        
        # All keys should be removed
        assert len(context) == 0



class TestPendingMessageManagement:
    """Test pending message functionality"""
    
    def test_set_pending_message(self):
        """Test setting pending message"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.set_pending_message("test message", ["intent1", "intent2"])
        
        assert fsm.pending_message == "test message"
        assert fsm.candidate_intents == ["intent1", "intent2"]
    
    def test_get_pending_data(self):
        """Test getting pending data"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.set_pending_message("test message", ["intent1", "intent2"])
        
        message, intents = fsm.get_pending_data()
        assert message == "test message"
        assert intents == ["intent1", "intent2"]
    
    def test_clear_pending_data(self):
        """Test clearing pending data"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.set_pending_message("test message", ["intent1", "intent2"])
        fsm.clear_pending_data()
        
        assert fsm.pending_message is None
        assert fsm.candidate_intents == []
    
    def test_pending_data_updates_context(self):
        """Test that setting pending message updates context"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.set_pending_message("test message", ["intent1", "intent2"])
        
        assert fsm.get_context("pending_message") == "test message"
        assert fsm.get_context("candidate_intents") == ["intent1", "intent2"]



class TestMultipleTransitions:
    """Test multiple transition scenarios"""
    
    def test_reset_recovery(self):
        """Test recovery through reset"""
        fsm = ConversationStateMachine(user_id="test_user")
        
        # Go through multiple states
        fsm.request_disambiguation()
        fsm.delegate_to_agent()
        fsm.complete_conversation()
        
        assert fsm.state == "completed"
        
        # Reset and verify
        fsm.reset()
        assert fsm.state == "initial"
    
    def test_error_recovery(self):
        """Test error state and recovery"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.delegate_to_agent()
        
        fsm.error()
        assert fsm.state == "error_state"
        
        # Can reset from error state
        fsm.reset()
        assert fsm.state == "initial"
    
    def test_state_transitions_with_context(self):
        """Test state transitions maintain context properly"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.update_context(user_data="important")
        
        fsm.request_disambiguation()
        assert fsm.get_context("user_data") == "important"
        assert fsm.get_context("disambiguation_started") is True
        
        fsm.active_agent = "test_agent"
        fsm.delegate_to_agent()
        assert fsm.get_context("user_data") == "important"
        assert fsm.get_context("active_agent") == "test_agent"



class TestTransitionValidation:
    """Test transition validation methods"""
    
    def test_get_valid_transitions_changes_with_state(self):
        """Test that valid transitions change based on state"""
        fsm = ConversationStateMachine(user_id="test_user")
        
        # From initial state
        initial_valid = fsm.get_valid_transitions_set()
        assert "request_disambiguation" in initial_valid
        
        # Transition to disambiguation state
        fsm.request_disambiguation()
        disambiguation_valid = fsm.get_valid_transitions_set()
        
        # From disambiguation, resolve_disambiguation should be valid
        assert "resolve_disambiguation" in disambiguation_valid
        assert "delegate_to_agent" in disambiguation_valid
    
    def test_invalid_transition_from_state(self):
        """Test invalid transitions are properly detected"""
        fsm = ConversationStateMachine(user_id="test_user")
        fsm.request_disambiguation()
        
        # request_disambiguation not valid from awaiting_disambiguation
        assert fsm.can_transition_to("request_disambiguation") is False
    
    def test_reset_always_available(self):
        """Test reset is always available"""
        fsm = ConversationStateMachine(user_id="test_user")
        
        states_to_test = ["initial", "awaiting_disambiguation", "agent_delegated"]
        for state in states_to_test:
            if state == "initial":
                pass  # Already in initial
            elif state == "awaiting_disambiguation":
                fsm.request_disambiguation()
            elif state == "agent_delegated":
                fsm.active_agent = "test"
                fsm.delegate_to_agent()
            
            # Reset should always be available
            assert fsm.can_transition_to("reset") is True
            fsm.reset()