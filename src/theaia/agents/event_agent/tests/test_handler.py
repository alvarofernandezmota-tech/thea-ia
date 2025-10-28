import pytest
from src.theaia.agents.event_agent.handler import EventAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return EventAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("evento")
    assert agent.can_handle("fiesta")
    assert agent.can_handle("celebración")
    assert agent.can_handle("conferencia")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("nota")
    assert not agent.can_handle("recordatorio")
    assert not agent.can_handle("agenda")

def test_full_flow_success(agent):
    ctx = {}
    uid = "test_user"
    # Primer mensaje: pregunta por título evento
    out = agent.handle(uid, "quiero crear un evento", ctx)
    assert "evento" in out[0].lower()
    # Segundo mensaje: recibe título -> pregunta por fecha
    out = agent.handle(uid, "Cumpleaños Ana", out[2])
    assert "fecha" in out[0].lower()
    assert out[1] == "awaiting_event_date"
    # Tercer mensaje: recibe fecha -> evento agendado
    out = agent.handle(uid, "15 de noviembre", out[2])
    assert "agendado" in out[0].lower()
    assert out[1] == "completed"
