"""
Tests unitarios del CoreRouter para Thea IA 2.0.
Valida que CoreRouter delega correctamente a AgendaAgent, NoteAgent y FallbackAgent.
"""

import pytest
from src.theaia.core.router import CoreRouter
from src.theaia.tests.core.test_router import DummyAgent, replace_agent  # Reusar mocks y utilidades
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.fallback_agent.handler import FallbackAgent


def test_handle_agenda():
    """Verifica que CoreRouter delega solicitudes de agenda al agente adecuado."""
    router = CoreRouter()
    # Reemplazar el agente real por DummyAgent
    replace_agent(router, AgendaAgent, DummyAgent("ok agenda"))

    result = router.handle("user1", "quiero agendar una cita", {})
    assert result["status"] == "ok"
    assert "ok agenda" in result["message"].lower()


def test_handle_notes():
    """Verifica que CoreRouter delega solicitudes de notas al agente adecuado."""
    router = CoreRouter()
    replace_agent(router, NoteAgent, DummyAgent("ok nota"))

    result = router.handle("user2", "crear nota de prueba", {})
    assert result["status"] == "ok"
    assert "ok nota" in result["message"].lower()


def test_handle_fallback():
    """Verifica que CoreRouter usa el agente de fallback cuando no reconoce la intención."""
    router = CoreRouter()
    replace_agent(router, FallbackAgent, DummyAgent("ok fallback"))

    result = router.handle("user3", "mensaje sin sentido", {})
    assert result["status"] == "ok"
    assert "ok fallback" in result["message"].lower()
