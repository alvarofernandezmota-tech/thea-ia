# src/theaia/tests/core/test_router.py
import pytest
from src.theaia.core.router import CoreRouter
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.fallback_agent.handler import FallbackAgent

def test_handle_agenda(agent_replacer, dummy_agent_factory):
    """
    Verifica que CoreRouter delega correctamente al AgendaAgent.
    """
    router = CoreRouter()
    dummy = dummy_agent_factory("ok agenda")
    router.agents = [AgendaAgent()]
    agent_replacer(router, AgendaAgent, dummy)
    
    result = router.handle("user1", "quiero agendar una cita", {})
    assert result["status"] == "ok"
    assert "ok agenda" in result["message"].lower()

def test_handle_notes(agent_replacer, dummy_agent_factory):
    """
    Verifica que CoreRouter delega correctamente al NoteAgent.
    """
    router = CoreRouter()
    dummy = dummy_agent_factory("ok nota")
    router.agents = [NoteAgent()]
    agent_replacer(router, NoteAgent, dummy)
    
    result = router.handle("user2", "crear nota de prueba", {})
    assert result["status"] == "ok"
    assert "ok nota" in result["message"].lower()

def test_handle_fallback(agent_replacer, dummy_agent_factory):
    """
    Verifica que CoreRouter usa el FallbackAgent cuando no reconoce la intención.
    """
    router = CoreRouter()
    dummy = dummy_agent_factory("ok fallback")
    router.agents = [FallbackAgent()]
    agent_replacer(router, FallbackAgent, dummy)
    
    result = router.handle("user3", "mensaje sin sentido", {})
    assert result["status"] == "ok"
    assert "ok fallback" in result["message"].lower()
