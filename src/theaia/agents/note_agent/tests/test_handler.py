import pytest
from src.theaia.agents.note_agent.handler import NoteAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return NoteAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("nota")
    assert agent.can_handle("notas")
    assert agent.can_handle("apunte")
    assert agent.can_handle("memoria")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("evento")
    assert not agent.can_handle("ayuda")
    assert not agent.can_handle("agenda")

def test_note_flow(agent):
    ctx = {}
    uid = "test_user"
    # Primer mensaje: pregunta contenido nota
    out = agent.handle(uid, "quiero guardar una nota", ctx)
    assert "nota" in out[0].lower()
    # Segundo mensaje: guarda nota
    out = agent.handle(uid, "lista de la compra", out[2])
    assert "guardad" in out[0].lower()
    assert out[1] == "completed"
