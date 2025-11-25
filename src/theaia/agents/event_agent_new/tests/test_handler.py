"""
Unit tests for EventAgent handler.
"""

import pytest
from src.theaia.agents.event_agent_new.handler import EventAgent


class TestEventAgent:
    """Unit tests for EventAgent."""
    
    @pytest.fixture
    def agent(self):
        """Create agent instance."""
        return EventAgent(user_id="test_user_123")
    
    def test_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent.user_id == "test_user_123"
        assert agent.conversation_manager is not None
    
    def test_get_supported_intents(self, agent):
        """Test supported intents."""
        intents = agent.get_supported_intents()
        assert "crear_evento" in intents
        assert "evento" in intents
        assert "listar_eventos" in intents
        assert "calendario" in intents
        assert len(intents) >= 5
    
    @pytest.mark.asyncio
    async def test_handle_basic_message(self, agent):
        """Test basic message handling."""
        context = {
            "user_id": "test_user_123",
            "tenant_id": "tenant_abc"
        }
        
        response, state, updated_context = await agent.handle(
            user_id="test_user_123",
            message="crear evento",
            context=context
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert state in ["completed", "in_progress", "cancelled", "error"]
        assert "fsm_state" in updated_context


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
