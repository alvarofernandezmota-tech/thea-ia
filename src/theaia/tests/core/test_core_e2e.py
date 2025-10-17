# Archivo: src/theaia/tests/core/test_core_e2e.py

import pytest
from src.theaia.core import router
from src.theaia.tests.mocks.mock_intent_detector import MockIntentDetector

# --- Importación completa de todos los agentes ---
from src.theaia.agents.agenda_agent import AgendaAgent
from src.theaia.agents.note_agent import NoteAgent
from src.theaia.agents.reminder_agent import ReminderAgent
from src.theaia.agents.event_agent import EventAgent
from src.theaia.agents.query_agent import QueryAgent
from src.theaia.agents.help_agent import HelpAgent
from src.theaia.agents.scheduler_agent import SchedulerAgent
from src.theaia.agents.fallback_agent import FallbackAgent

@pytest.fixture
def core_router(monkeypatch):
    """Prepara un CoreRouter para tests, usando un mock del detector."""
    monkeypatch.setattr(router, "IntentDetector", MockIntentDetector)
    core = router.CoreRouter()
    core.agents = [
        AgendaAgent(), NoteAgent(), ReminderAgent(), EventAgent(),
        QueryAgent(), HelpAgent(), SchedulerAgent(), FallbackAgent(),
    ]
    return core

def test_delegates_to_agenda_agent(core_router):
    """Verifica que 'cita' se delega correctamente al AgendaAgent."""
    response = core_router.handle("user1", "quiero agendar una cita", {})
    assert response["status"] == "ok"
    assert "¿para cuándo quieres agendar" in response["message"].lower()

def test_delegates_to_fallback_agent(core_router):
    """Verifica que un mensaje sin intención va al FallbackAgent."""
    response = core_router.handle("user2", "mensaje sin keyword", {})
    assert response["status"] == "ok"
    assert "no he entendido tu solicitud" in response["message"].lower()

def test_delegates_to_help_agent(core_router):
    """Verifica que 'ayuda' se delega correctamente al HelpAgent."""
    response = core_router.handle("user3", "necesito ayuda", {})
    assert response["status"] == "ok"
    assert "puede ayudarte con" in response["message"].lower()

def test_delegates_to_query_agent(core_router):
    """Verifica que una pregunta se delega al QueryAgent."""
    response = core_router.handle("user4", "qué es la materia oscura?", {})
    assert response["status"] == "ok"
    assert "he procesado tu consulta" in response["message"].lower()

def test_delegates_to_note_agent(core_router):
    """
    Verifica que el CoreRouter delega correctamente al NoteAgent.
    Este test valida la delegación del router, no la lógica interna
    completa del agente (que se testeará en sus propios tests unitarios).
    """
    response = core_router.handle("user5", "crear una nota sobre la reunión", {})
    assert response["status"] == "ok"
    # Verificamos que el mensaje fue recibido por el NoteAgent
    assert "note" in response.get("context", {}).get("note_content", "").lower() or \
           "confirmo" in response["message"].lower()
