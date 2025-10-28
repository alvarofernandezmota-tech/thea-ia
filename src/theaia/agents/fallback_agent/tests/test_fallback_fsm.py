import pytest
from src.theaia.agents.fallback_agent.fallback_conversation_manager import FallbackConversationManager

@pytest.fixture
def fsm():
    return FallbackConversationManager("test_user")

def test_fallback_only_state(fsm):
    ctx = {}
    response, state, ctx = fsm.handle_message("test_user", "cualquier cosa", ctx)
    assert state == "completed"
    assert "no puedo responder" in response.lower()
