# src/theaia/agents/reminder_agent/tests/test_reminder_fsm.py

import pytest
from src.theaia.agents.reminder_agent.model.reminder_fsm import ReminderFSM

@pytest.fixture
def fsm():
    return ReminderFSM()

def test_initial_state(fsm):
    """Test que el estado inicial es awaiting_text."""
    assert fsm.state == "awaiting_text"

def test_transition_to_awaiting_time(fsm):
    """Test transición desde awaiting_text a awaiting_time."""
    response, state = fsm.process_message("Comprar pan", {})
    assert "¿Cuándo quieres" in response
    assert state == "awaiting_time"
    assert fsm.context["reminder_text"] == "Comprar pan"

def test_transition_to_confirmation(fsm):
    """Test transición desde awaiting_time a confirmation."""
    fsm.context["reminder_text"] = "Llamar al médico"
    fsm.state = "awaiting_time"
    
    response, state = fsm.process_message("mañana a las 9", {})
    assert "Confirmo el recordatorio" in response
    assert state == "confirmation"
    assert fsm.context["reminder_time"] == "mañana a las 9"

def test_schedule_confirmation_yes(fsm):
    """Test confirmación positiva de recordatorio."""
    fsm.state = "confirmation"
    fsm.context["reminder_text"] = "Reunión"
    
    response, state = fsm.process_message("sí", {})
    assert "programado correctamente" in response
    assert state == "scheduled"

def test_reminder_cancelled(fsm):
    """Test cancelación de recordatorio."""
    fsm.state = "confirmation"
    
    response, state = fsm.process_message("no", {})
    assert "cancelado" in response
    assert state == "cancelled"

def test_error_state(fsm):
    """Test que estados inválidos llevan a error."""
    fsm.state = "unknown_state"
    
    response, state = fsm.process_message("test", {})
    assert "error" in response.lower()
    assert state == "error"
