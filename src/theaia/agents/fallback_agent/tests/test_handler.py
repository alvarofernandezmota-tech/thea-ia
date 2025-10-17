# src/theaia/agents/fallback_agent/tests/test_handler.py

import pytest
from src.theaia.agents.fallback_agent.handler import FallbackAgent

@pytest.fixture
def agent():
    return FallbackAgent()

def test_can_handle_always_true(agent):
    """Test que el fallback siempre puede manejar cualquier intent."""
    assert agent.can_handle("cualquier cosa")
    assert agent.can_handle("xyz123")
    assert agent.can_handle("")
    assert agent.can_handle("mensaje desconocido")

def test_unrecognized_message_response(agent):
    """Test que responde apropiadamente a mensajes no reconocidos."""
    ctx = {}
    out = agent.handle("u1", "comando inexistente", ctx)
    
    assert "Lo siento, no he entendido" in out["message"]
    assert out["fsm_state"] == "completed"
    assert out["status"] == "ok"

def test_provides_help_menu(agent):
    """Test que proporciona un menú de ayuda."""
    ctx = {}
    out = agent.handle("u1", "asdfghjkl", ctx)
    
    assert "Agendar citas" in out["message"]
    assert "Crear notas" in out["message"]
    assert "ayuda" in out["message"].lower()

def test_context_stores_unrecognized(agent):
    """Test que el contexto almacena el mensaje no reconocido."""
    ctx = {}
    out = agent.handle("u1", "mensaje extraño", ctx)
    
    assert out["context"]["unrecognized_message"] == "mensaje extraño"

def test_consistent_response(agent):
    """Test que diferentes mensajes no reconocidos tienen respuesta consistente."""
    ctx = {}
    
    out1 = agent.handle("u1", "mensaje1", ctx)
    out2 = agent.handle("u1", "mensaje2", ctx)
    
    # Las respuestas deberían tener estructura similar
    assert "Lo siento" in out1["message"]
    assert "Lo siento" in out2["message"]
    assert out1["status"] == "ok"
    assert out2["status"] == "ok"
