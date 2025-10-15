import pytest
from src.theaia.agents.reminder_agent.model.reminder_fsm import ReminderFSM

@pytest.fixture
def fsm():
    return ReminderFSM()

def test_initial_state(fsm):
    assert fsm.state == "awaiting_text"

def test_awaiting_time_transition(fsm):
    resp, state = fsm.process_message("Comprar leche", {})
    assert "¿Cuándo quieres la notificación?" in resp
    assert state == "awaiting_time"
    assert fsm.context["notification_text"] == "Comprar leche"

def test_confirmation_transition(fsm):
    fsm.state = "awaiting_time"
    resp, state = fsm.process_message("mañana 9am", {})
    assert "Confirmo que te notifique" in resp
    assert state == "confirmation"
    assert fsm.context["notification_time"] == "mañana 9am"

def test_scheduled_state(fsm):
    fsm.state = "confirmation"
    resp, state = fsm.process_message("sí", {})
    assert "programada correctamente" in resp
    assert state == "scheduled"

def test_cancelled_state(fsm):
    fsm.state = "confirmation"
    resp, state = fsm.process_message("no", {})
    assert "cancelada" in resp
    assert state == "cancelled"

def test_error_state(fsm):
    fsm.state = "unknown"
    resp, state = fsm.process_message("algo", {})
    assert "Error en el flujo" in resp
    assert state == "error"
