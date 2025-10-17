# src/theaia/agents/event_agent/tests/test_event_fsm.py

import pytest
from src.theaia.agents.event_agent.model.event_fsm import EventFSM

@pytest.fixture
def fsm():
    return EventFSM()

def test_initial_state(fsm):
    """Test que el estado inicial es awaiting_name."""
    assert fsm.state == "awaiting_name"

def test_transition_to_awaiting_date(fsm):
    """Test transición desde awaiting_name a awaiting_date."""
    response, state = fsm.process_message("Cumpleaños de María", {})
    assert "¿Cuándo es" in response
    assert state == "awaiting_date"
    assert fsm.context["event_name"] == "Cumpleaños de María"

def test_transition_to_awaiting_recurrence(fsm):
    """Test transición desde awaiting_date a awaiting_recurrence."""
    fsm.context["event_name"] = "Aniversario"
    fsm.state = "awaiting_date"
    
    response, state = fsm.process_message("15 de mayo", {})
    assert "se repite cada año" in response
    assert state == "awaiting_recurrence"
    assert fsm.context["event_date"] == "15 de mayo"

def test_transition_to_confirmation_recurrent(fsm):
    """Test transición a confirmation con evento recurrente."""
    fsm.context["event_name"] = "Cumpleaños"
    fsm.context["event_date"] = "10 de junio"
    fsm.state = "awaiting_recurrence"
    
    response, state = fsm.process_message("sí", {})
    assert "Confirmo el evento" in response
    assert "anualmente" in response
    assert state == "confirmation"
    assert fsm.context["is_recurrent"] is True

def test_transition_to_confirmation_non_recurrent(fsm):
    """Test transición a confirmation con evento no recurrente."""
    fsm.context["event_name"] = "Conferencia"
    fsm.context["event_date"] = "20 de octubre"
    fsm.state = "awaiting_recurrence"
    
    response, state = fsm.process_message("no", {})
    assert "Confirmo el evento" in response
    assert "una sola vez" in response
    assert state == "confirmation"
    assert fsm.context["is_recurrent"] is False

def test_schedule_confirmation_yes(fsm):
    """Test confirmación positiva de evento."""
    fsm.state = "confirmation"
    fsm.context["event_name"] = "Graduación"
    
    response, state = fsm.process_message("sí", {})
    assert "programado correctamente" in response
    assert state == "scheduled"

def test_event_cancelled(fsm):
    """Test cancelación de evento."""
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
