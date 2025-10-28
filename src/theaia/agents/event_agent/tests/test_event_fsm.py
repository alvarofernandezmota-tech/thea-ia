import pytest
from src.theaia.agents.event_agent.event_conversation_manager import EventConversationManager

@pytest.fixture
def fsm():
    return EventConversationManager("test_user")

def test_initial_state(fsm):
    response, next_state, ctx = fsm.handle_message("test_user", "init", {})
    assert next_state == "awaiting_event_title"
    assert "evento" in response.lower()

def test_title_to_date_and_complete(fsm):
    ctx = {}
    # Primer mensaje: inicio, esperamos preguntar título
    response, state, ctx = fsm.handle_message("test_user", "init", ctx)
    assert state == "awaiting_event_title"
    assert "evento" in response.lower()
    # Segundo mensaje: introducimos título, esperamos preguntar fecha
    response, state, ctx = fsm.handle_message("test_user", "Evento X", ctx)
    assert state == "awaiting_event_date"
    assert "fecha" in response.lower()
    # Tercer mensaje: introducimos fecha, evento agendado
    response, state, ctx = fsm.handle_message("test_user", "25 de diciembre", ctx)
    assert state == "completed"
    assert "agendado" in response.lower()
    assert ctx["event_title"] == "Evento X"
    assert ctx["event_date"] == "25 de diciembre"

def test_invalid_state(fsm):
    ctx = {"fsm_state": "unknown"}
    response, state, ctx = fsm.handle_message("test_user", "Test", ctx)
    assert state == "completed"
    assert "finalizado" in response.lower()
