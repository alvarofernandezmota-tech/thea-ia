import pytest
from src.theaia.agents.reminder_agent.handler import ReminderAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return ReminderAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("recordatorio")
    assert agent.can_handle("alarma")
    assert agent.can_handle("recuérdame")
    assert agent.can_handle("reminder")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("nota")
    assert not agent.can_handle("evento")

def test_reminder_flow(agent):
    ctx = {}
    uid = "test_user"
    # Primer mensaje: pide qué recordar
    out = agent.handle(uid, "quiero un recordatorio", ctx)
    # Cambiado: buscamos "recuerd" (admite "recuerde", "recuerda", "recordar"...)
    assert "recuerd" in out[0].lower()
    # Segundo mensaje: pide cuándo
    out = agent.handle(uid, "comprar leche", out[2])
    assert "cuándo" in out[0].lower()
    assert out[1] == "awaiting_reminder_time"
    # Tercer mensaje: confirma recordatorio
    out = agent.handle(uid, "a las 19:00", out[2])
    assert "te recordaré" in out[0].lower()
    assert out[1] == "completed"
