# src/theaia/agents/help_agent/tests/test_handler.py

import pytest
from src.theaia.agents.help_agent.handler import HelpAgent

@pytest.fixture
def agent():
    return HelpAgent()

def test_can_handle_valid_intents(agent):
    """Test que el agente reconoce sus intents válidos."""
    assert agent.can_handle("ayuda")
    assert agent.can_handle("help")
    assert agent.can_handle("comandos")
    assert agent.can_handle("guía")
    assert agent.can_handle("manual")

def test_cannot_handle_other_intents(agent):
    """Test que el agente rechaza intents que no le corresponden."""
    assert not agent.can_handle("nota")
    assert not agent.can_handle("agenda")
    assert not agent.can_handle("recordatorio")

def test_general_help_flow(agent):
    """Test de flujo de ayuda general."""
    ctx = {}
    
    out = agent.handle("u1", "necesito ayuda", ctx)
    assert "Thea IA puede ayudarte" in out["message"]
    assert out["fsm_state"] == "providing_help"
    assert out["status"] == "ok"

def test_specific_help_flow(agent):
    """Test de flujo de ayuda específica."""
    ctx = {}
    
    out = agent.handle("u1", "ayuda con agenda", ctx)
    assert "agendar" in out["message"].lower()
    assert out["fsm_state"] == "providing_help"

def test_multiple_help_topics(agent):
    """Test de múltiples consultas de ayuda."""
    ctx = {}
    
    # Primera ayuda
    out = agent.handle("u1", "ayuda con notas", ctx)
    assert "nota" in out["message"].lower()
    
    # Pedir más ayuda
    out = agent.handle("u1", "sí", out["context"])
    assert "¿Sobre qué tema" in out["message"]
    
    # Segunda ayuda
    out = agent.handle("u1", "recordatorios", out["context"])
    assert "recordar" in out["message"].lower()

def test_help_completion(agent):
    """Test de completar ayuda."""
    ctx = {}
    
    out = agent.handle("u1", "comandos", ctx)
    out = agent.handle("u1", "no", out["context"])
    
    assert "Perfecto" in out["message"]
    assert out["fsm_state"] == "completed"

def test_context_persistence(agent):
    """Test que el contexto se mantiene."""
    ctx = {}
    
    out = agent.handle("u1", "ayuda con eventos", ctx)
    assert out["context"]["help_topic"] == "eventos"
