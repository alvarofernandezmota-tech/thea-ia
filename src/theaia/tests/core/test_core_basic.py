import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from theaia.core.router import CoreRouter

def test_initial_state_and_intent_detection():
    router = CoreRouter()
    uid, state, context = "user1", "initial", {}
    resp, new_state, new_context = router.handle(uid, "hola", state, context)
    assert new_state == "initial"
    assert "hola" in resp.lower()

def test_create_event_flow():
    router = CoreRouter()
    uid, state, context = "user2", "initial", {}
    resp, state, context = router.handle(uid, "quiero agendar cita", state, context)
    assert state == "awaiting_datetime"
    assert "fecha" in resp.lower()

    resp, state, context = router.handle(uid, "2025-10-20 10:00", state, context)
    assert state == "awaiting_confirmation"
    assert "confirmas" in resp.lower()
