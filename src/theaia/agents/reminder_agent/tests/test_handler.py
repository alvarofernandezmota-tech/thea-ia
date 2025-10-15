import pytest
from src.theaia.agents.reminder_agent.handler import ReminderAgent

@pytest.fixture
def agent():
    return ReminderAgent()

def test_can_handle():
    assert agent().can_handle("recordatorio")
    assert agent().can_handle("notificacion")
    assert not agent().can_handle("agenda")

def test_full_flow(monkeypatch):
    agent = ReminderAgent()
    ctx = {}
    # Texto
    out = agent.handle("u1", "Llamar a Juan", ctx)
    assert "¿Cuándo quieres la notificación?" in out["message"]
    assert out["fsm_state"] == "awaiting_time"
    # Hora
    out = agent.handle("u1", "hoy 5pm", out["context"])
    assert "Confirmo que te notifique" in out["message"]
    assert out["fsm_state"] == "confirmation"
    # Confirmación
    out = agent.handle("u1", "sí", out["context"])
    assert out["status"] == "ok"
    assert out["fsm_state"] == "scheduled"
