# src/theaia/tests/core/test_router.py

import pytest
from src.theaia.core.router import CoreRouter

class DummyAgent:
    def __init__(self, response):
        self._response = response
    def process(self, user_id, message, current_state, current_data):
        # Devuelve siempre ("ok", mismo estado, mismo contexto)
        return (self._response, current_state, current_data)

@pytest.fixture(autouse=True)
def mock_context_repo(monkeypatch):
    # Evita llamadas reales a la base de datos
    monkeypatch.setattr("src.theaia.database.repositories.context_repository.load_context", lambda uid: None)
    monkeypatch.setattr("src.theaia.database.repositories.context_repository.save_context", lambda uid, s, d: None)

def test_handle_agenda():
    router = CoreRouter()
    # Mockear solo el agente de agenda
    router.agents['agenda'] = DummyAgent("ok")
    resp, state, ctx = router.handle("U", "Quiero agendar una cita", "initial", {})
    assert resp == "ok"

def test_handle_notas():
    router = CoreRouter()
    router.agents['notas'] = DummyAgent("ok")
    resp, state, ctx = router.handle("U", "Apuntar una nota", "initial", {})
    assert resp == "ok"

def test_handle_fallback():
    router = CoreRouter()
    router.agents['fallback'] = DummyAgent("ok")
    resp, state, ctx = router.handle("U", "Texto random", "initial", {})
    assert resp == "ok"
