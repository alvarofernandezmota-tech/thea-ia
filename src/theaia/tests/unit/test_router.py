import pytest

from src.theaia.core.router import CoreRouter

@pytest.fixture
def router():
    return CoreRouter()

def test_detect_intents_agenda(router):
    intents = router._detect_multiple_intents("Quiero agendar reunión")
    assert "agenda" in intents

def test_detect_intents_nota(router):
    intents = router._detect_multiple_intents("Apunta una nota por favor")
    assert "notas" in intents

def test_handle_simple_agenda(router):
    resp, state, ctx = router.handle("user1", "Agendar reunión mañana", "initial", {})
    assert isinstance(resp, str)
    assert state in ("awaiting_disambiguation", "agent_delegated")

def test_handle_fallback(router):
    resp, state, ctx = router.handle("user1", "palabra sin sentido", "initial", {})
    # Pasa si el mensaje o el estado hacen referencia al fallback
    assert "fallback" in resp.lower() or "fallback" in (state or "").lower()

