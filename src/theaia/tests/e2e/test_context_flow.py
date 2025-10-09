from theaia.core.router import CoreRouter

def test_e2e_agenda_flow():
    router = CoreRouter()
    uid = "u1"
    state = "initial"
    context = {}

    resp, state, context = router.handle(uid, "quiero agendar cita", state, context)
    assert "fecha" in resp.lower()
    assert state == "awaiting_datetime"

    resp, state, context = router.handle(uid, "2025-10-10 09:00", state, context)
    assert "confirmas" in resp.lower()
    assert state == "awaiting_confirmation"

    resp, state, context = router.handle(uid, "sí", state, context)
    assert "confirmada" in resp.lower()
    assert state == "completed"
