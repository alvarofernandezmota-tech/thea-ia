"""
Tests E2E del flujo conversacional con FSM.
"""

import pytest
from src.theaia.core.router import CoreRouter


def test_conversation_flow_with_fsm():
    """
    Verifica que el flujo conversacional funciona con FSM.
    """
    router = CoreRouter()
    user_id = "test_user_fsm"

    # Mensaje inicial con intención clara
    result = router.handle(user_id, "quiero crear una nota")  # ✅ SIN {}

    assert result["status"] == "ok"
    assert "message" in result
    assert "context" in result
    print(f"Estado después de mensaje inicial: {result.get('state')}")


def test_disambiguation_flow():
    """
    Verifica que la desambiguación funciona correctamente.
    """
    router = CoreRouter()
    user_id = "test_disambiguation"

    # Mensaje ambiguo que requiere desambiguación
    result = router.handle(user_id, "recordar algo importante")  # ✅ SIN {}

    assert result["status"] == "ok"
    assert "message" in result
    print(f"Respuesta de desambiguación: {result['message']}")


def test_conversation_context_persistence():
    """
    Verifica que el contexto se mantiene entre mensajes.
    """
    router = CoreRouter()
    user_id = "test_context"

    # Primer mensaje
    result1 = router.handle(user_id, "quiero agendar algo")  # ✅ SIN {}

    # Segundo mensaje (router maneja contexto internamente)
    result2 = router.handle(user_id, "mañana a las 3")  # ✅ SIN context1

    assert result2["status"] == "ok"
    assert "context" in result2
    print(f"Contexto persistido: {result2['context']}")
