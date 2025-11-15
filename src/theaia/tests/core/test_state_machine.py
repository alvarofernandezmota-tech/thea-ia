"""Tests for FSM State Machine."""

import pytest
from src.theaia.core.fsm.state_machine import ConversationStateMachine


class TestConversationStateMachine:
    """Test ConversationStateMachine class."""
    
    @pytest.fixture
    def state_machine(self):
        """Create conversation state machine for testing."""
        return ConversationStateMachine(user_id="test_user_123")
    
    def test_state_machine_initialization(self, state_machine):
        """Test state machine initialization."""
        assert state_machine.state == "initial"
        assert state_machine.user_id == "test_user_123"
    
    def test_state_attributes(self, state_machine):
        """Test state machine attributes."""
        assert hasattr(state_machine, 'pending_message')
        assert hasattr(state_machine, 'candidate_intents')
        assert hasattr(state_machine, 'active_agent')
        
        assert state_machine.pending_message is None
        assert state_machine.candidate_intents == []
        assert state_machine.active_agent is None
    
    def test_get_states(self, state_machine):
        """Test get_states method."""
        states = state_machine.get_states()
        assert isinstance(states, list)
        assert len(states) > 0
    
    def test_user_id_property(self, state_machine):
        """Test user_id access."""
        assert state_machine.user_id == "test_user_123"
