# src/theaia/agents/query_agent/tests/test_query_fsm.py

import pytest
from src.theaia.agents.query_agent.model.query_fsm import QueryFSM

@pytest.fixture
def fsm():
    return QueryFSM()

def test_initial_state(fsm):
    """Test que el estado inicial es awaiting_query."""
    assert fsm.state == "awaiting_query"

def test_transition_to_answered(fsm):
    """Test transición desde awaiting_query a answered."""
    response, state = fsm.process_message("¿Qué es Python?", {})
    assert "He procesado tu consulta" in response
    assert state == "answered"
    assert fsm.context["user_query"] == "¿Qué es Python?"

def test_follow_up_completion(fsm):
    """Test que seguimiento con agradecimiento completa la consulta."""
    fsm.state = "answered"
    fsm.context["user_query"] = "Algo"
    
    response, state = fsm.process_message("gracias", {})
    assert "algo más" in response.lower()
    assert state == "completed"

def test_follow_up_new_question(fsm):
    """Test que nueva pregunta en estado answered la procesa."""
    fsm.state = "answered"
    
    response, state = fsm.process_message("¿Y qué es JavaScript?", {})
    assert "He procesado tu consulta" in response
    assert state == "answered"
    assert "JavaScript" in fsm.context["user_query"]

def test_completed_to_new_query(fsm):
    """Test que después de completed se puede hacer nueva consulta."""
    fsm.state = "completed"
    
    response, state = fsm.process_message("¿Cómo funciona Git?", {})
    assert "He procesado tu consulta" in response
    assert state == "answered"

def test_error_state(fsm):
    """Test que estados inválidos llevan a error."""
    fsm.state = "unknown_state"
    
    response, state = fsm.process_message("test", {})
    assert "error" in response.lower()
    assert state == "error"

def test_context_persistence(fsm):
    """Test que el contexto mantiene las consultas."""
    response, state = fsm.process_message("Primera consulta", {})
    assert fsm.context["user_query"] == "Primera consulta"
