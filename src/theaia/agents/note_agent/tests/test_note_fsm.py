# src/theaia/agents/note_agent/tests/test_note_fsm.py

import pytest
from src.theaia.agents.note_agent.model.note_fsm import NoteFSM

@pytest.fixture
def fsm():
    return NoteFSM()

def test_initial_state(fsm):
    """Test que el estado inicial es awaiting_content."""
    assert fsm.state == "awaiting_content"

def test_transition_to_confirmation(fsm):
    """Test transición desde awaiting_content a confirmation."""
    response, state = fsm.process_message("Comprar leche y pan", {})
    assert "¿Confirmo que guarde" in response
    assert "Comprar leche y pan" in response
    assert state == "confirmation"
    assert fsm.context["note_content"] == "Comprar leche y pan"

def test_save_confirmation_yes(fsm):
    """Test confirmación positiva de guardado de nota."""
    fsm.state = "confirmation"
    fsm.context["note_content"] = "Investigar sobre ML"
    
    response, state = fsm.process_message("sí", {})
    assert "guardada correctamente" in response
    assert state == "saved"

def test_save_confirmation_various_affirmatives(fsm):
    """Test que múltiples formas de confirmación funcionan."""
    fsm.state = "confirmation"
    
    for affirmation in ["si", "s", "confirmar", "ok", "vale"]:
        fsm_test = NoteFSM()
        fsm_test.state = "confirmation"
        response, state = fsm_test.process_message(affirmation, {})
        assert state == "saved"

def test_note_cancelled(fsm):
    """Test cancelación de nota."""
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
