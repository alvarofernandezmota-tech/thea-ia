import pytest
from theaia.core.router import CoreRouter

@pytest.mark.e2e
def test_e2e_agenda_flow():
    router = CoreRouter()
    uid = "u1"
    state = "initial"
    context = {}

    # Paso 1: iniciar agendado
    resp, state, context = router.handle(uid, "quiero agendar cita", state, context)
    assert "fecha" in resp.lower()
    assert state == "awaiting_datetime"

    # Paso 2: indicar fecha y hora
    resp, state, context = router.handle(uid, "2025-10-10 09:00", state, context)
    assert "confirmas" in resp.lower()
    assert state == "awaiting_confirmation"

    # Paso 3: confirmar
    resp, state, context = router.handle(uid, "sí", state, context)
    assert "confirmada" in resp.lower()
    assert state == "completed"

    # El contexto debería incluir el evento agendado
    assert context.get("last_event") is not None
    assert context["last_event"]["datetime"] == "2025-10-10 09:00"
