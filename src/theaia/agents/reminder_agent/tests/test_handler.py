# src/theaia/agents/reminder_agent/tests/test_handler.py

import pytest
from src.theaia.agents.reminder_agent.handler import ReminderAgent

@pytest.fixture
def agent():
    return ReminderAgent()

def test_can_handle_valid_intents(agent):
    """Test que el agente reconoce sus intents válidos."""
    assert agent.can_handle("recordar")
    assert agent.can_handle("recordatorio")
    assert agent.can_handle("notificación")
    assert agent.can_handle("avisar")

def test_cannot_handle_other_intents(agent):
    """Test que el agente rechaza intents que no le corresponden."""
    assert not agent.can_handle("nota")
    assert not agent.can_handle("agenda")
    assert not agent.can_handle("cita")

def test_full_flow_success(agent):
    """Test del flujo completo de recordatorio exitoso."""
    ctx = {}
    
    # Paso 1: Texto
    out = agent.handle("u1", "Ir al gimnasio", ctx)
    assert "¿Cuándo quieres" in out["message"]
    assert out["fsm_state"] == "awaiting_time"
    assert out["status"] == "ok"

    # Paso 2: Tiempo
    out = agent.handle("u1", "mañana a las 18:00", out["context"])
    assert "Confirmo el recordatorio" in out["message"]
    assert out["fsm_state"] == "confirmation"

    # Paso 3: Confirmación
    out = agent.handle("u1", "sí", out["context"])
    assert "programado correctamente" in out["message"]
    assert out["fsm_state"] == "scheduled"
    assert out["status"] == "ok"

def test_full_flow_cancelled(agent):
    """Test del flujo de recordatorio cancelado."""
    ctx = {}
    
    out = agent.handle("u1", "Revisar email", ctx)
    out = agent.handle("u1", "en 2 horas", out["context"])
    out = agent.handle("u1", "no", out["context"])
    
    assert "cancelado" in out["message"]
    assert out["fsm_state"] == "cancelled"
    assert out["status"] == "error"

def test_context_persistence(agent):
    """Test que el contexto se mantiene entre llamadas."""
    ctx = {}
    
    out = agent.handle("u1", "Tomar medicina", ctx)
    assert out["context"]["reminder_text"] == "Tomar medicina"
    
    out = agent.handle("u1", "cada 8 horas", out["context"])
    assert out["context"]["reminder_text"] == "Tomar medicina"
    assert out["context"]["reminder_time"] == "cada 8 horas"
