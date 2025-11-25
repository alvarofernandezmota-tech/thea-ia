"""
E2E tests for HelpAgent.

Tests help workflows: tutorials, guidance, support.
"""

import pytest
from src.theaia.agents.help_agent.handler import HelpAgent


class TestHelpAgentE2E:
    """End-to-End tests for HelpAgent."""
    
    @pytest.fixture
    def agent(self, test_user):
        """Create fresh agent for each test."""
        return HelpAgent(user_id=test_user.id)
    
    @pytest.fixture
    def context(self, test_user):
        """Create basic context."""
        return {
            "user_id": test_user.id,
            "tenant_id": test_user.tenant_id,
            "session_id": "session_456",
            "state": "initial"
        }
    
    # ==================== GENERAL HELP TESTS ====================
    
    def test_help_overview(self, agent, context, test_user):
        """Test general help overview."""
        user_input = "ayuda"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "help_provided", "idle"]
        assert isinstance(response, str)
    
    def test_help_features(self, agent, context, test_user):
        """Test listing features."""
        user_input = "¿qué puedo hacer?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "help_provided", "idle"]
    
    def test_help_commands(self, agent, context, test_user):
        """Test help with commands."""
        user_input = "¿cuáles son los comandos disponibles?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "help_provided", "idle"]
    
    # ==================== AGENDA HELP TESTS ====================
    
    def test_help_create_event(self, agent, context, test_user):
        """Test help creating events."""
        user_input = "¿cómo creo un evento?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    def test_help_schedule_meeting(self, agent, context, test_user):
        """Test help scheduling meeting."""
        user_input = "¿cómo agendo una reunión?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    def test_help_recurring_events(self, agent, context, test_user):
        """Test help with recurring events."""
        user_input = "¿cómo creo eventos recurrentes?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    # ==================== NOTES HELP TESTS ====================
    
    def test_help_create_note(self, agent, context, test_user):
        """Test help creating notes."""
        user_input = "¿cómo tomo una nota?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    def test_help_organize_notes(self, agent, context, test_user):
        """Test help organizing notes."""
        user_input = "¿cómo organizo mis notas?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    def test_help_search_notes(self, agent, context, test_user):
        """Test help searching notes."""
        user_input = "¿cómo busco notas?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    # ==================== REMINDERS HELP TESTS ====================
    
    def test_help_create_reminder(self, agent, context, test_user):
        """Test help creating reminders."""
        user_input = "¿cómo creo un recordatorio?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    def test_help_set_notifications(self, agent, context, test_user):
        """Test help setting notifications."""
        user_input = "¿cómo configuro notificaciones?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    def test_help_recurring_reminders(self, agent, context, test_user):
        """Test help with recurring reminders."""
        user_input = "¿cómo creo recordatorios repetidos?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "tutorial", "idle"]
    
    # ==================== TROUBLESHOOTING TESTS ====================
    
    def test_help_troubleshooting(self, agent, context, test_user):
        """Test general troubleshooting."""
        user_input = "tengo un problema"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "troubleshooting", "idle"]
    
    def test_help_not_working(self, agent, context, test_user):
        """Test help when feature not working."""
        user_input = "¿por qué no funciona la agenda?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)
        
        assert response is not None
        assert state in ["completed", "troubleshooting", "idle"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
