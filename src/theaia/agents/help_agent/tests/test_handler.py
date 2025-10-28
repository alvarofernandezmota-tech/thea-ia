import pytest
from src.theaia.agents.help_agent.handler import HelpAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return HelpAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("ayuda")
    assert agent.can_handle("soporte")
    assert agent.can_handle("help")
    assert agent.can_handle("asistencia")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("evento")
    assert not agent.can_handle("nota")
    assert not agent.can_handle("agenda")

def test_help_response(agent):
    ctx = {}
    uid = "test_user"
    out = agent.handle(uid, "necesito ayuda", ctx)
    assert "ayud" in out[0].lower()
    assert out[1] == "completed"
