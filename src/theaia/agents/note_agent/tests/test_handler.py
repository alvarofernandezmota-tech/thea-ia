# src/theaia/agents/note_agent/tests/test_handler.py

import pytest
from src.theaia.agents.note_agent.handler import NoteAgent

@pytest.fixture
def agent():
    return NoteAgent()

def test_can_handle_valid_intents(agent):
    """Test que el agente reconoce sus intents válidos."""
    assert agent.can_handle("nota")
    assert agent.can_handle("notas")
    assert agent.can_handle("apuntar")
    assert agent.can_handle("anotar")
    assert agent.can_handle("guardar")

def test_cannot_handle_other_intents(agent):
    """Test que el agente rechaza intents que no le corresponden."""
    assert not agent.can_handle("agenda")
    assert not agent.can_handle("recordatorio")
    assert not agent.can_handle("cita")

def test_full_flow_success(agent):
    """Test del flujo completo de guardado exitoso."""
    ctx = {}
    
    # Paso 1: Contenido
    out = agent.handle("u1", "Llamar al dentista mañana", ctx)
    assert "¿Confirmo que guarde" in out["message"]
    assert out["fsm_state"] == "confirmation"
    assert out["status"] == "ok"

    # Paso 2: Confirmación
    out = agent.handle("u1", "sí", out["context"])
    assert "guardada correctamente" in out["message"]
    assert out["fsm_state"] == "saved"
    assert out["status"] == "ok"

def test_full_flow_cancelled(agent):
    """Test del flujo de nota cancelada."""
    ctx = {}
    
    # Contenido
    out = agent.handle("u1", "Revisar documentación", ctx)
    
    # Cancelación
    out = agent.handle("u1", "no", out["context"])
    assert "cancelada" in out["message"]
    assert out["fsm_state"] == "cancelled"
    assert out["status"] == "error"

def test_context_persistence(agent):
    """Test que el contexto se mantiene entre llamadas."""
    ctx = {}
    
    out = agent.handle("u1", "Preparar presentación", ctx)
    assert out["context"]["note_content"] == "Preparar presentación"
    
    out = agent.handle("u1", "sí", out["context"])
    assert out["context"]["note_content"] == "Preparar presentación"
