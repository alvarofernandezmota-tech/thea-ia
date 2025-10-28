import pytest
from src.theaia.agents.schedule_agent.schedule_conversation_manager import ScheduleConversationManager

@pytest.fixture
def fsm():
    return ScheduleConversationManager("test_user")

def test_schedule_fsm_flow(fsm):
    ctx = {}
    response, state, ctx = fsm.handle_message("test_user", "ver agenda", ctx)
    assert state == "awaiting_day"
    assert "horario" in response.lower() or "periodo" in response.lower() or "agenda" in response.lower()
    response, state, ctx = fsm.handle_message("test_user", "lunes", ctx)
    assert state == "awaiting_action"
    assert "consultar" in response.lower() or "añadir" in response.lower() or "eliminar" in response.lower()
    response, state, ctx = fsm.handle_message("test_user", "eliminar", ctx)
    assert state == "completed"
    assert "registrada" in response.lower() or "agenda" in response.lower()
    assert ctx["day"] == "lunes"
    assert ctx["action"] == "eliminar"
