# src/theaia/agents/agenda_agent/tests/test_handler.py

import pytest
from src.theaia.agents.agenda_agent.handler import AgendaAgent

@pytest.fixture
def agent():
    return AgendaAgent()

def test_can_handle_valid_intents(agent):
    """Test que el agente reconoce sus intents válidos."""
    assert agent.can_handle("agenda")
    assert agent.can_handle("cita")
    assert agent.can_handle("reunión")
    assert agent.can_handle("evento")
    assert agent.can_handle("agendar")

def test_cannot_handle_other_intents(agent):
    """Test que el agente rechaza intents que no le corresponden."""
    assert not agent.can_handle("nota")
    assert not agent.can_handle("recordatorio")
    assert not agent.can_handle("consulta")

def test_full_flow_success(agent):
    """Test del flujo completo de agendado exitoso."""
    ctx = {}
    
    # Paso 1: Título
    out = agent.handle("u1", "Cita con Pedro", ctx)
    assert "¿Para cuándo" in out["message"]
    assert out["fsm_state"] == "awaiting_datetime"
    assert out["status"] == "ok"

    # Paso 2: Fecha
    out = agent.handle("u1", "lunes a las 15:00", out["context"])
    assert "Confirmo" in out["message"]
    assert out["fsm_state"] == "confirmation"
    assert out["status"] == "ok"

    # Paso 3: Confirmación
    out = agent.handle("u1", "sí", out["context"])
    assert "agendada correctamente" in out["message"]
    assert out["fsm_state"] == "scheduled"
    assert out["status"] == "ok"

def test_full_flow_cancelled(agent):
    """Test del flujo de agendado cancelado."""
    ctx = {}
    
    # Título
    out = agent.handle("u1", "Reunión de emergencia", ctx)
    
    # Fecha
    out = agent.handle("u1", "hoy a las 20:00", out["context"])
    
    # Cancelación
    out = agent.handle("u1", "no", out["context"])
    assert "cancelada" in out["message"]
    assert out["fsm_state"] == "cancelled"
    assert out["status"] == "error"
