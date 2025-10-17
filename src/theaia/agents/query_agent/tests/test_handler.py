# src/theaia/agents/query_agent/tests/test_handler.py

import pytest
from src.theaia.agents.query_agent.handler import QueryAgent

@pytest.fixture
def agent():
    return QueryAgent()

def test_can_handle_valid_intents(agent):
    """Test que el agente reconoce sus intents válidos."""
    assert agent.can_handle("consulta")
    assert agent.can_handle("pregunta")
    assert agent.can_handle("buscar")
    assert agent.can_handle("qué")
    assert agent.can_handle("cómo")

def test_cannot_handle_other_intents(agent):
    """Test que el agente rechaza intents que no le corresponden."""
    assert not agent.can_handle("nota")
    assert not agent.can_handle("agenda")
    assert not agent.can_handle("recordatorio")

def test_single_query_flow(agent):
    """Test de flujo simple de una consulta."""
    ctx = {}
    
    out = agent.handle("u1", "¿Qué es Thea IA?", ctx)
    assert "He procesado tu consulta" in out["message"]
    assert out["fsm_state"] == "answered"
    assert out["status"] == "ok"

def test_follow_up_completion(agent):
    """Test de seguimiento con cierre."""
    ctx = {}
    
    out = agent.handle("u1", "¿Cómo funciona Python?", ctx)
    out = agent.handle("u1", "gracias", out["context"])
    
    assert "algo más" in out["message"].lower()
    assert out["fsm_state"] == "completed"

def test_multiple_queries_flow(agent):
    """Test de múltiples consultas en secuencia."""
    ctx = {}
    
    out = agent.handle("u1", "¿Qué es Git?", ctx)
    assert out["fsm_state"] == "answered"
    
    out = agent.handle("u1", "¿Y GitHub?", out["context"])
    assert out["fsm_state"] == "answered"
    assert "GitHub" in out["context"]["user_query"]

def test_context_persistence(agent):
    """Test que el contexto se mantiene entre llamadas."""
    ctx = {}
    
    out = agent.handle("u1", "Primera pregunta", ctx)
    assert out["context"]["user_query"] == "Primera pregunta"
    
    out = agent.handle("u1", "Segunda pregunta", out["context"])
    assert out["context"]["user_query"] == "Segunda pregunta"
