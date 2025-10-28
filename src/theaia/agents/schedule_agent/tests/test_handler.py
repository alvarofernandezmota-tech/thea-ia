import pytest
from src.theaia.agents.schedule_agent.handler import ScheduleAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return ScheduleAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("horario")
    assert agent.can_handle("agenda semanal")
    assert agent.can_handle("planning")
    assert agent.can_handle("schedule")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("nota")
    assert not agent.can_handle("evento")
    assert not agent.can_handle("recordatorio")

def test_schedule_flow(agent):
    ctx = {}
    uid = "test_user"
    # 1. Pregunta qué día/periodo
    out = agent.handle(uid, "quiero revisar mi planning", ctx)
    assert "horario" in out[0].lower() or "periodo" in out[0].lower() or "agenda" in out[0].lower()
    # 2. Acción sobre día
    out = agent.handle(uid, "viernes", out[2])
    assert "consultar" in out[0].lower() or "añadir" in out[0].lower() or "eliminar" in out[0].lower()
    assert out[1] == "awaiting_action"
    # 3. Confirmación acción final
    out = agent.handle(uid, "consultar", out[2])
    assert "registrada" in out[0].lower() or "agenda" in out[0].lower()
    assert out[1] == "completed"
