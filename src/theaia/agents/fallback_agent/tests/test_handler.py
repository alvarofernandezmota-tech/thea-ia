import pytest
from src.theaia.agents.fallback_agent.handler import FallbackAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return FallbackAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("fallback")
    assert agent.can_handle("ninguno")
    assert agent.can_handle("desconocido")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("evento")
    assert not agent.can_handle("nota")
    assert not agent.can_handle("agenda")

def test_fallback_response(agent):
    ctx = {}
    uid = "test_user"
    out = agent.handle(uid, "algo incomprensible", ctx)
    assert "no puedo responder" in out[0].lower()
    assert out[1] == "completed"
