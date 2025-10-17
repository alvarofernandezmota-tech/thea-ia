# src/theaia/agents/fallback_agent/tests/test_fallback_fsm.py

import pytest
from src.theaia.agents.fallback_agent.model.fallback_fsm import FallbackFSM

@pytest.fixture
def fsm():
    return FallbackFSM()

def test_initial_state(fsm):
    """Test que el estado inicial es unrecognized."""
    assert fsm.state == "unrecognized"

def test_unrecognized_message(fsm):
    """Test que procesa mensajes no reconocidos."""
    response, state = fsm.process_message("xyz123 comando desconocido", {})
    assert "Lo siento, no he entendido" in response
    assert "ayuda" in response.lower()
    assert state == "completed"
    assert fsm.context["unrecognized_message"] == "xyz123 comando desconocido"

def test_provides_help_options(fsm):
    """Test que proporciona opciones de ayuda."""
    response, state = fsm.process_message("blablabla", {})
    assert "Agendar citas" in response
    assert "Crear notas" in response
    assert "recordatorios" in response.lower()
    assert "eventos" in response.lower()

def test_context_persistence(fsm):
    """Test que el contexto guarda el mensaje no reconocido."""
    response, state = fsm.process_message("mensaje raro", {})
    assert fsm.context["unrecognized_message"] == "mensaje raro"

def test_multiple_unrecognized_messages(fsm):
    """Test que procesa múltiples mensajes no reconocidos."""
    response1, state1 = fsm.process_message("primer mensaje", {})
    assert state1 == "completed"
    
    fsm.state = "unrecognized"
    response2, state2 = fsm.process_message("segundo mensaje", {})
    assert state2 == "completed"
    assert fsm.context["unrecognized_message"] == "segundo mensaje"
