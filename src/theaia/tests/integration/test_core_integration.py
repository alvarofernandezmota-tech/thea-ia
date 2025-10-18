# src/theaia/tests/integration/test_core_integration.py
"""
Tests de integración del Core de Thea IA 2.0.
Valida la interacción entre CoreRouter, IntentDetector y agentes reales.
"""

import pytest
from src.theaia.core.router import CoreRouter
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.fallback_agent.handler import FallbackAgent

def ensure_agents_loaded(router):
    """
    Asegura que el CoreRouter tenga los agentes reales cargados.
    """
    if not hasattr(router, "agents") or not router.agents:
        router.agents = [
            AgendaAgent(),
            NoteAgent(),
            FallbackAgent(),
        ]

def test_router_with_real_intent_detector():
    """
    Valida que las intenciones se delegan correctamente.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    
    # Test con intención de agenda
    result = router.handle("user1", "quiero agendar una cita", {})
    assert result["status"] == "ok"
    assert isinstance(result["message"], str)  # Solo verifica que haya un mensaje
    
    # Test con intención de nota
    result = router.handle("user2", "crear una nota importante", {})
    assert result["status"] == "ok"
    # El NoteAgent pide confirmación, eso es un comportamiento esperado
    assert "¿confirmo" in result["message"].lower()

def test_multi_turn_conversation():
    """
    Valida que el contexto se mantiene entre mensajes.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    context = {}
    
    # Turno 1: Iniciar creación de nota
    result1 = router.handle("user1", "crear una nota", context)
    context = result1.get("context", {})
    assert result1["status"] == "ok"
    assert context.get("active_agent") == "NoteAgent"
    
    # Turno 2: Responder "no" a la confirmación
    result2 = router.handle("user1", "no", context)
    assert result2["status"] == "ok"
    # El agente debería cancelar la operación
    assert "cancelada" in result2["message"].lower()

def test_error_handling_with_none_context():
    """
    Valida que el router maneja 'context=None' sin fallar.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    
    result = router.handle("user2", "texto aleatorio", None)
    assert result is not None
    assert result["status"] == "ok"
    # Debería delegar al FallbackAgent
    assert "lo siento" in result["message"].lower()
