# src/theaia/agents/agenda_agent/tests/test_agenda_fsm.py

import pytest
from src.theaia.agents.agenda_agent.model.agenda_fsm import AgendaFSM

@pytest.fixture
def fsm():
    return AgendaFSM()

def test_initial_state(fsm):
    """Test que el estado inicial es awaiting_title."""
    assert fsm.state == "awaiting_title"

def test_transition_to_awaiting_datetime(fsm):
    """Test transición desde awaiting_title a awaiting_datetime."""
    response, state = fsm.process_message("Reunión con el equipo", {})
    assert "¿Para cuándo quieres" in response
    assert state == "awaiting_datetime"
    assert fsm.context["event_title"] == "Reunión con el equipo"

def test_transition_to_confirmation(fsm):
    """Test transición desde awaiting_datetime a confirmation."""
    fsm.context["event_title"] = "Reunión de planificación"
    fsm.state = "awaiting_datetime"
    
    response, state = fsm.process_message("mañana a las 10", {})
    assert "Confirmo" in response
    assert state == "confirmation"
    assert fsm.context["event_datetime"] == "mañana a las 10"

def test_schedule_confirmation_yes(fsm):
    """Test confirmación positiva de cita."""
    fsm.state = "confirmation"
    fsm.context["event_title"] = "Reunión con Ana"
    
    response, state = fsm.process_message("sí", {})
    assert "agendada correctamente" in response
    assert state == "scheduled"

def test_schedule_cancelled(fsm):
    """Test cancelación de cita."""
    fsm.state = "confirmation"
    
    response, state = fsm.process_message("no", {})
    assert "cancelada" in response
    assert state == "cancelled"

def test_error_state(fsm):
    """Test que estados inválidos llevan a error."""
    fsm.state = "unknown_state"
    
    response, state = fsm.process_message("test", {})
    assert "error" in response.lower()
    assert state == "error"
