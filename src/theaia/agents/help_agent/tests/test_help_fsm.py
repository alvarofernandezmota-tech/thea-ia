import pytest
from src.theaia.agents.help_agent.help_conversation_manager import HelpConversationManager

@pytest.fixture
def fsm():
    return HelpConversationManager("test_user")

def test_help_only_state(fsm):
    ctx = {}
    response, state, ctx = fsm.handle_message("test_user", "help", ctx)
    assert state == "completed"
    assert "ayud" in response.lower()
