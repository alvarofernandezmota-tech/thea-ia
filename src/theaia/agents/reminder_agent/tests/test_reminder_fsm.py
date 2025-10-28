import pytest
from src.theaia.agents.reminder_agent.reminder_conversation_manager import ReminderConversationManager

@pytest.fixture
def fsm():
    return ReminderConversationManager("test_user")

def test_reminder_fsm_flow(fsm):
    ctx = {}
    response, state, ctx = fsm.handle_message("test_user", "nuevo recordatorio", ctx)
    # Cambiado aquí también
    assert "recuerd" in response.lower()
    assert state == "awaiting_reminder_message"
    response, state, ctx = fsm.handle_message("test_user", "llamar al médico", ctx)
    assert state == "awaiting_reminder_time"
    assert "cuándo" in response.lower()
    response, state, ctx = fsm.handle_message("test_user", "mañana a las 9", ctx)
    assert state == "completed"
    assert "te recordaré" in response.lower()
    assert ctx["reminder_message"] == "llamar al médico"
    assert ctx["reminder_time"] == "mañana a las 9"
