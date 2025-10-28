import pytest
from src.theaia.agents.agenda_agent.handler import AgendaAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return AgendaAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("agenda")
    assert agent.can_handle("cita")
    assert agent.can_handle("reunión")
    assert agent.can_handle("evento")
    assert agent.can_handle("agendar")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("nota")
    assert not agent.can_handle("recordatorio")
    assert not agent.can_handle("consulta")

def test_full_flow_success(agent):
    ctx = {}
    uid = "test_user"
    out = agent.handle(uid, "Cita con Pedro", ctx)
    assert "¿Para qué día" in out[0]
    assert out[1] == "awaiting_date"

    out = agent.handle(uid, "lunes a las 15:00", out[2])
    assert "¿A qué hora" in out[0]
    assert out[1] == "awaiting_time"

    out = agent.handle(uid, "15:00", out[2])
    assert "agendada" in out[0].lower()
    assert out[1] == "completed"

def test_full_flow_completed(agent):
    ctx = {}
    uid = "test_user"
    out = agent.handle(uid, "Reunión", ctx)
    out = agent.handle(uid, "mañana", out[2])
    out = agent.handle(uid, "10:00", out[2])
    assert "agendada" in out[0].lower()
    assert out[1] == "completed"
