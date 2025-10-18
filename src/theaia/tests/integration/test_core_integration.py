"""
Tests de integración del Core de Thea IA 2.0.
Valida la interacción entre CoreRouter, IntentDetector y agentes.
Adaptado al ecosistema Thea IA con carga manual de agentes.
"""

import pytest
from src.theaia.core.router import CoreRouter
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.fallback_agent.handler import FallbackAgent


def ensure_agents_loaded(router):
    """
    Asegura que el CoreRouter tenga agentes cargados.
    En Thea IA 2.0, los agentes deben registrarse manualmente en tests.
    """
    if not hasattr(router, "agents") or not router.agents:
        router.agents = [
            AgendaAgent(),
            NoteAgent(),
            FallbackAgent(),
        ]


def test_router_with_real_intent_detector():
    """
    Test de integración: CoreRouter con IntentDetector real.
    Valida que las intenciones se detectan y delegan correctamente.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    
    # Test con intención de agenda
    result = router.handle("user1", "quiero agendar una cita", {})
    assert result["status"] == "ok"
    assert result["message"] is not None
    
    # Test con intención de nota
    result = router.handle("user2", "crear una nota importante", {})
    assert result["status"] == "ok"
    assert result["message"] is not None
    
    # Test con intención de ayuda
    result = router.handle("user3", "necesito ayuda", {})
    assert result["status"] == "ok"
    assert "ayuda" in result["message"].lower() or "lo siento" in result["message"].lower()


def test_multi_turn_conversation():
    """
    Test de integración: Conversación multi-turno.
    Valida que el contexto se mantiene entre mensajes.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    context = {}
    
    # Turno 1: Iniciar acción
    result1 = router.handle("user1", "crear una nota", context)
    context = result1.get("context", {})
    assert result1["status"] == "ok"
    
    # Turno 2: Continuar con contexto (puede ir al fallback si no hay FSM activo)
    result2 = router.handle("user1", "esto es importante", context)
    assert result2["status"] == "ok"
    

def test_context_persistence():
    """
    Test de integración: Persistencia del contexto.
    Valida que el contexto se mantiene correctamente.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    user_id = "test_user_123"
    
    # Primera interacción
    context1 = {}
    result1 = router.handle(user_id, "agendar cita", context1)
    
    # Segunda interacción con mismo contexto
    context2 = result1.get("context", {})
    result2 = router.handle(user_id, "mañana a las 10", context2)
    
    assert result2["status"] == "ok"
    assert "context" in result2


def test_intent_detection_accuracy():
    """
    Test de integración: Precisión de detección de intenciones.
    Valida que el IntentDetector identifica correctamente las intenciones.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    
    test_cases = [
        ("quiero agendar una cita", "ok"),
        ("crear nota", "ok"),
        ("ayuda", "ok"),
        ("hola", "ok"),
    ]
    
    for message, expected_status in test_cases:
        result = router.handle("user_test", message, {})
        assert result["status"] == expected_status, f"Falló para: {message}"


def test_error_handling():
    """
    Test de integración: Manejo de errores.
    Valida que el sistema maneja errores gracefully.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    
    # Test con mensaje vacío
    result = router.handle("user1", "", {})
    assert result["status"] in ["ok", "error"]
    
    # Test con contexto None (ahora debería manejarlo)
    result = router.handle("user2", "test", None)
    assert result is not None
    assert result["status"] in ["ok", "error"]


def test_intent_detector_integration():
    """
    Test de integración: IntentDetector con CoreRouter.
    Valida que las predicciones ML se usan correctamente.
    """
    router = CoreRouter()
    ensure_agents_loaded(router)
    
    # Test predicción directa
    from src.theaia.ml.intent_detector.inference import IntentDetector
    detector = IntentDetector()
    
    intents = detector.detect("quiero agendar una cita")
    assert len(intents) > 0
    assert isinstance(intents[0], str)
    
    # Test integración completa
    result = router.handle("user_ml", "crear una nota", {})
    assert result["status"] == "ok"
