# src/theaia/agents/help_agent/tests/test_help_fsm.py

import pytest
from src.theaia.agents.help_agent.model.help_fsm import HelpFSM

@pytest.fixture
def fsm():
    return HelpFSM()

def test_initial_state(fsm):
    """Test que el estado inicial es awaiting_topic."""
    assert fsm.state == "awaiting_topic"

def test_general_help(fsm):
    """Test de ayuda general."""
    response, state = fsm.process_message("necesito ayuda", {})
    assert "Thea IA puede ayudarte" in response
    assert "¿Necesitas ayuda con algo más?" in response
    assert state == "providing_help"

def test_specific_help_agenda(fsm):
    """Test de ayuda específica sobre agenda."""
    response, state = fsm.process_message("cómo agendar una cita", {})
    assert "agendar una cita" in response.lower()
    assert state == "providing_help"
    assert fsm.context["help_topic"] == "agenda"

def test_specific_help_notes(fsm):
    """Test de ayuda específica sobre notas."""
    response, state = fsm.process_message("cómo crear una nota", {})
    assert "nota" in response.lower()
    assert state == "providing_help"

def test_specific_help_reminder(fsm):
    """Test de ayuda específica sobre recordatorios."""
    response, state = fsm.process_message("ayuda con recordatorios", {})
    assert "recordar" in response.lower()
    assert state == "providing_help"

def test_follow_up_yes(fsm):
    """Test de seguimiento afirmativo."""
    fsm.state = "providing_help"
    
    response, state = fsm.process_message("sí", {})
    assert "¿Sobre qué tema" in response
    assert state == "awaiting_topic"

def test_follow_up_no(fsm):
    """Test de seguimiento negativo."""
    fsm.state = "providing_help"
    
    response, state = fsm.process_message("no", {})
    assert "Perfecto" in response
    assert state == "completed"

def test_completed_to_new_help(fsm):
    """Test que después de completed se puede pedir nueva ayuda."""
    fsm.state = "completed"
    
    response, state = fsm.process_message("comandos disponibles", {})
    assert "Comandos disponibles" in response
    assert state == "providing_help"

def test_error_state(fsm):
    """Test que estados inválidos llevan a error."""
    fsm.state = "unknown_state"
    
    response, state = fsm.process_message("test", {})
    assert "error" in response.lower()
    assert state == "error"
    