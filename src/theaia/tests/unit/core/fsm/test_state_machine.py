"""
Test Suite for EventAgent FSM State Machine
H03 FASE 1 - BLOQUE 1.4 - Tests

Comprehensive test coverage for:
- BaseStateMachine core functionality
- ConversationStateMachine workflows
- State transitions and validation
- Context management
- Session tracking
"""

import pytest
import logging
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.theaia.core.fsm.state_machine import BaseStateMachine, ConversationStateMachine


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestBaseStateMachine:
    """Tests for BaseStateMachine abstract base class."""
    
    class SimpleStateMachine(BaseStateMachine):
        """Simple concrete implementation for testing."""
        VALID_STATES = ["initial", "running", "stopped"]
        INITIAL_STATE = "initial"
    
    def test_initialization(self):
        """Test BaseStateMachine initialization."""
        machine = self.SimpleStateMachine(user_id="test_user")
        assert machine.user_id == "test_user"
        assert machine.state == "initial"
        assert machine.context == {}
        assert machine.machine is not None
    
    def test_invalid_user_id(self):
        """Test that empty user_id raises ValueError."""
        with pytest.raises(ValueError):
            self.SimpleStateMachine(user_id="")
        
        with pytest.raises(ValueError):
            self.SimpleStateMachine(user_id=None)


class TestConversationStateMachine:
    """Tests for ConversationStateMachine implementation."""
    
    def test_initialization_auto_session_id(self):
        """Test ConversationStateMachine with auto-generated session ID."""
        machine = ConversationStateMachine(user_id="user_123")
        
        assert machine.user_id == "user_123"
        assert machine.state == "initial"
        assert machine.session_id is not None
        assert len(machine.session_id) == 36
    
    def test_initialization_custom_session_id(self):
        """Test ConversationStateMachine with custom session ID."""
        custom_session = "custom_session_123"
        machine = ConversationStateMachine(
            user_id="user_123",
            session_id=custom_session
        )
        
        assert machine.session_id == custom_session
    
    def test_initial_state_transitions(self):
        """Test valid transitions from initial state."""
        machine = ConversationStateMachine(user_id="user_123")
        
        valid_transitions = machine.get_valid_transitions_set()
        assert "request_disambiguation" in valid_transitions
        assert "delegate_to_agent" in valid_transitions
        assert "reset" in valid_transitions
        assert "error" in valid_transitions
        assert "timeout_session" in valid_transitions
    
    def test_request_disambiguation_transition(self):
        """Test transition to awaiting_disambiguation state."""
        machine = ConversationStateMachine(user_id="user_123")
        machine.set_pending_message(
            "Create event",
            ["create_event", "search_events"]
        )
        
        assert machine.can_transition_to("request_disambiguation")
        machine.request_disambiguation()
        
        assert machine.state == "awaiting_disambiguation"
        assert machine.context.get("disambiguation_started") is True
    
    def test_delegate_to_agent_from_initial(self):
        """Test delegation from initial state."""
        machine = ConversationStateMachine(user_id="user_123")
        machine.active_agent = "AgendaAgent"
        
        assert machine.can_transition_to("delegate_to_agent")
        machine.delegate_to_agent()
        
        assert machine.state == "agent_delegated"
        assert machine.context.get("active_agent") == "AgendaAgent"
    
    def test_resolve_disambiguation_transition(self):
        """Test disambiguation resolution."""
        machine = ConversationStateMachine(user_id="user_123")
        
        machine.set_pending_message("Create", ["create_event"])
        machine.request_disambiguation()
        
        machine.active_agent = "AgendaAgent"
        assert machine.can_transition_to("resolve_disambiguation")
        machine.resolve_disambiguation()
        
        assert machine.state == "agent_delegated"
        assert machine.context.get("disambiguation_resolved") is True
    
    def test_complete_conversation(self):
        """Test conversation completion."""
        machine = ConversationStateMachine(user_id="user_123")
        machine.active_agent = "AgendaAgent"
        machine.delegate_to_agent()
        
        assert machine.can_transition_to("complete_conversation")
        machine.complete_conversation()
        
        assert machine.state == "completed"
        assert machine.context.get("status") == "completed"
    
    def test_reset_transition(self):
        """Test state machine reset."""
        machine = ConversationStateMachine(user_id="user_123")
        session_id = machine.session_id
        
        machine.active_agent = "AgendaAgent"
        machine.delegate_to_agent()
        machine.update_context(custom_key="custom_value")
        
        assert machine.state == "agent_delegated"
        
        machine.reset()
        
        assert machine.state == "initial"
        assert machine.active_agent is None
        assert machine.session_id == session_id
    
    def test_error_transition(self):
        """Test error state transition."""
        machine = ConversationStateMachine(user_id="user_123")
        machine.active_agent = "AgendaAgent"
        machine.delegate_to_agent()
        
        machine.error()
        assert machine.state == "error_state"
    
    def test_export_state(self):
        """Test state export."""
        machine = ConversationStateMachine(user_id="user_123")
        machine.active_agent = "AgendaAgent"
        machine.delegate_to_agent()
        
        exported = machine.export_state()
        
        assert exported["user_id"] == "user_123"
        assert exported["session_id"] == machine.session_id
        assert exported["current_state"] == "agent_delegated"
    
    def test_merge_context_strategy_merge(self):
        """Test context merging with merge strategy."""
        machine = ConversationStateMachine(user_id="user_123")
        machine.update_context(key1="value1", key2="value2")
        
        result = machine.merge_context({"key2": "updated_value", "key3": "value3"})
        
        assert machine.context["key1"] == "value1"
        assert machine.context["key2"] == "updated_value"
        assert machine.context["key3"] == "value3"
    
    def test_set_pending_message(self):
        """Test setting pending message."""
        machine = ConversationStateMachine(user_id="user_123")
        
        machine.set_pending_message(
            "Create event for tomorrow",
            ["create_event", "search_events", "modify_event"]
        )
        
        assert machine.pending_message == "Create event for tomorrow"
        assert machine.candidate_intents == ["create_event", "search_events", "modify_event"]
    
    def test_full_conversation_flow(self):
        """Test complete conversation workflow."""
        machine = ConversationStateMachine(
            user_id="user_123",
            session_id="session_abc"
        )
        
        assert machine.state == "initial"
        
        machine.set_pending_message(
            "Create event tomorrow at 2pm",
            ["create_event", "search_events"]
        )
        machine.request_disambiguation()
        assert machine.state == "awaiting_disambiguation"
        
        machine.active_agent = "AgendaAgent"
        machine.resolve_disambiguation()
        assert machine.state == "agent_delegated"
        
        machine.complete_conversation()
        assert machine.state == "completed"
        
        exported = machine.export_state()
        assert exported["current_state"] == "completed"
        assert exported["session_id"] == "session_abc"


class TestConversationFlowWithAgendaAgent:
    """Integration tests simulating AgendaAgent interaction."""
    
    def test_agenda_agent_create_event(self):
        """Simulate AgendaAgent creating an event."""
        machine = ConversationStateMachine(user_id="user_123")
        
        machine.set_pending_message(
            "Create event for team meeting",
            ["create_event", "modify_event", "delete_event"]
        )
        machine.request_disambiguation()
        
        machine.active_agent = "AgendaAgent"
        machine.update_context(
            selected_intent="create_event",
            event_title="Team Meeting",
            event_time="2025-12-10 10:00"
        )
        machine.resolve_disambiguation()
        
        assert machine.state == "agent_delegated"
        assert machine.context["selected_intent"] == "create_event"
        
        machine.update_context(
            event_id="evt_123",
            status="created"
        )
        machine.complete_conversation()
        
        assert machine.state == "completed"
        assert machine.context["event_id"] == "evt_123"
    
    def test_agenda_agent_search_events(self):
        """Simulate AgendaAgent searching for events."""
        machine = ConversationStateMachine(user_id="user_123")
        
        machine.active_agent = "AgendaAgent"
        machine.update_context(
            intent="search_events",
            query="meetings next week"
        )
        machine.delegate_to_agent()
        
        assert machine.state == "agent_delegated"
        
        machine.update_context(
            results_count=3,
            results=[
                {"title": "Team Standup", "date": "2025-12-10"},
                {"title": "Project Review", "date": "2025-12-11"},
                {"title": "Client Call", "date": "2025-12-12"}
            ]
        )
        machine.complete_conversation()
        
        assert machine.state == "completed"
        assert machine.context["results_count"] == 3


class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_invalid_transition(self):
        """Test attempting invalid transition."""
        machine = ConversationStateMachine(user_id="user_123")
        
        with pytest.raises(Exception):
            machine.complete_conversation()
    
    def test_recovery_from_error_state(self):
        """Test recovery from error state."""
        machine = ConversationStateMachine(user_id="user_123")
        machine.active_agent = "AgendaAgent"
        machine.delegate_to_agent()
        
        machine.error()
        assert machine.state == "error_state"
        
        machine.reset()
        assert machine.state == "initial"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])