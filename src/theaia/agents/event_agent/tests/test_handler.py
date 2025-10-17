# src/theaia/agents/event_agent/tests/test_handler.py

import pytest
from src.theaia.agents.event_agent.handler import EventAgent

@pytest.fixture
def agent():
    return EventAgent()

def test_can_handle_valid_intents(agent):
    """Test que el agente reconoce sus intents válidos."""
    assert agent.can_handle("evento")
    assert agent.can_handle("cumpleaños")
    assert agent.can_handle("aniversario")
    assert agent.can_handle("celebración")

def test_cannot_handle_other_intents(agent):
    """Test que el agente rechaza intents que no le corresponden."""
    assert not agent.can_handle("nota")
    assert not agent.can_handle("agenda")
    assert not agent.can_handle("recordatorio")

def test_full_flow_recurrent_event(agent):
    """Test del flujo completo con evento recurrente."""
    ctx = {}
    
    # Nombre
    out = agent.handle("u1", "Cumpleaños de Ana", ctx)
    assert "¿Cuándo es" in out["message"]
    assert out["fsm_state"] == "awaiting_date"

    # Fecha
    out = agent.handle("u1", "5 de marzo", out["context"])
    assert "se repite cada año" in out["message"]
    assert out["fsm_state"] == "awaiting_recurrence"

    # Recurrencia
    out = agent.handle("u1", "sí", out["context"])
    assert "anualmente" in out["message"]
    assert out["fsm_state"] == "confirmation"

    # Confirmación
    out = agent.handle("u1", "sí", out["context"])
    assert "programado correctamente" in out["message"]
    assert out["fsm_state"] == "scheduled"

def test_full_flow_non_recurrent_event(agent):
    """Test del flujo completo con evento no recurrente."""
    ctx = {}
    
    out = agent.handle("u1", "Conferencia Tech", ctx)
    out = agent.handle("u1", "25 de noviembre", out["context"])
    out = agent.handle("u1", "no", out["context"])
    
    assert "una sola vez" in out["message"]
    
    out = agent.handle("u1", "ok", out["context"])
    assert "programado correctamente" in out["message"]

def test_full_flow_cancelled(agent):
    """Test del flujo cancelado."""
    ctx = {}
    
    out = agent.handle("u1", "Fiesta", ctx)
    out = agent.handle("u1", "mañana", out["context"])
    out = agent.handle("u1", "no", out["context"])
    out = agent.handle("u1", "no", out["context"])
    
    assert "cancelado" in out["message"]
    assert out["status"] == "error"
