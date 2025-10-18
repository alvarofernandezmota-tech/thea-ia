"""
Tests unitarios del CoreRouter integrados con Thea IA 2.0.
Valida el flujo de manejo de intenciones y la interacción con los agentes del ecosistema.
"""

import pytest
from src.theaia.core.router import CoreRouter
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.fallback_agent.handler import FallbackAgent


# ---------------------------------------------------------
# Mocks y utilidades para pruebas en entorno Thea IA 2.0
# ---------------------------------------------------------

class DummyAgent:
    """Agente simulado que reemplaza agentes reales durante las pruebas."""
    def __init__(self, response_text="ok"):
        self.response_text = response_text

    def get_supported_intents(self):
        return ["dummy_intent"]

    def can_handle(self, intent: str) -> bool:
        return True

    def handle(self, user_id: str, message: str, context: dict):
        print(f"[DummyAgent] Simulando respuesta para '{message}'")
        return {
            "status": "ok",
            "message": self.response_text,
            "context": context,
        }


def ensure_agents_loaded(router):
    """
    Asegura que el CoreRouter tenga agentes cargados.
    En algunos entornos de prueba los agentes deben registrarse manualmente.
    """
    if not hasattr(router, "agents") or not router.agents:
        print("[WARN] CoreRouter no tiene agentes cargados. Registrando manualmente...")
        router.agents = [
            AgendaAgent(),
            NoteAgent(),
            FallbackAgent(),
        ]
    else:
        print(f"[INFO] CoreRouter tiene {len(router.agents)} agentes cargados.")


def replace_agent(router, target_cls, dummy_agent):
    """Busca un agente por clase exacta o por nombre y lo reemplaza por el DummyAgent."""
    ensure_agents_loaded(router)
    replaced = False

    for i, agent in enumerate(router.agents):
        # Algunas versiones del ecosistema usan importaciones dinámicas
        if isinstance(agent, target_cls) or target_cls.__name__.lower() in agent.__class__.__name__.lower():
            router.agents[i] = dummy_agent
            replaced = True
            print(f"[INFO] Reemplazado {agent.__class__.__name__} por DummyAgent")
            break

    if not replaced:
        raise AssertionError(
            f"No se encontró el agente {target_cls.__name__} en {', '.join([a.__class__.__name__ for a in router.agents])}"
        )


# ---------------------------------------------------------
# TESTS UNITARIOS
# ---------------------------------------------------------

def test_handle_agenda():
    """Debe delegar correctamente solicitudes 'agendar' al AgendaAgent."""
    router = CoreRouter()
    dummy = DummyAgent("ok agenda")
    replace_agent(router, AgendaAgent, dummy)

    result = router.handle("user1", "quiero agendar una cita", {})
    assert result["status"] == "ok"
    assert "ok agenda" in result["message"].lower()


def test_handle_notes():
    """Debe delegar correctamente solicitudes de notas al NoteAgent."""
    router = CoreRouter()
    dummy = DummyAgent("ok nota")
    replace_agent(router, NoteAgent, dummy)

    result = router.handle("user2", "crear nota de prueba", {})
    assert result["status"] == "ok"
    assert "ok nota" in result["message"].lower()


def test_handle_fallback():
    """Debe usar el FallbackAgent cuando no se reconoce una intención."""
    router = CoreRouter()
    dummy = DummyAgent("ok fallback")
    replace_agent(router, FallbackAgent, dummy)

    result = router.handle("user3", "esto no tiene sentido", {})
    assert result["status"] == "ok"
    assert "ok fallback" in result["message"].lower()
