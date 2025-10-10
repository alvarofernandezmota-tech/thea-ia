import pytest
from theaia.core.router import CoreRouter
from theaia.database.repositories.context_repository import load_context

@pytest.mark.e2e
def test_e2e_context_flow(tmp_path, monkeypatch):
    """
    Verifica que CoreRouter.handle recargue y persista contexto
    correctamente entre interacciones.
    """
    # Forzar uso de un archivo temporal como repositorio de contexto
    db_file = tmp_path / "context_store.json"
    monkeypatch.setenv("CONTEXT_DB_PATH", str(db_file))

    router = CoreRouter()
    uid = "u42"
    state = "initial"
    context = {}

    # Paso 1: Iniciar cita y persistir estado awaiting_datetime
    resp1, state1, context1 = router.handle(uid, "quiero agendar cita", state, context)
    assert "fecha" in resp1.lower()
    assert state1 == "awaiting_datetime"
    # Context debería contener pending_intent
    assert context1.get("pending_intent") == "agenda"

    # Simular reinicio: nueva instancia sin pasar state/context
    router2 = CoreRouter()
    # Al invocar handle con estado inicial y contexto vacío,
    # CoreRouter debe recargar desde el repositorio
    resp2, state2, context2 = router2.handle(uid, "2025-12-01 14:30", "initial", {})
    assert "confirmas" in resp2.lower()
    assert state2 == "awaiting_confirmation"
    # pending_datetime debe haber sido restaurado
    assert context2.get("pending_datetime") == "2025-12-01 14:30"

    # Paso final: confirmar cita
    resp3, state3, context3 = router2.handle(uid, "sí", state2, context2)
    assert "confirmada" in resp3.lower()
    assert state3 == "completed"
    # Context final debe incluir el evento agendado
    last_evt = context3.get("last_event")
    assert last_evt is not None
    assert last_evt["uid"] == uid
    assert last_evt["datetime"] == "2025-12-01 14:30"

    # Además, verificar directamente en el repositorio
    saved = load_context(uid)
    assert saved["state"] == "completed"
    assert saved["data"].get("last_event") == last_evt
