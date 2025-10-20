import pytest
import os
import json
from src.theaia.core.router import CoreRouter
from src.theaia.database.repositories.context_repository import (
    load_context,
    save_context,
    clear_context,
    _get_path
)

@pytest.fixture(scope="module")
def router():
    return CoreRouter()

@pytest.fixture(autouse=True)
def clean_context():
    clear_context()
    yield
    clear_context()

def test_context_persistence_across_agents(router):
    """
    Verifica que el contexto se guarda y recupera entre agentes FSM.
    """
    user_id = "user_testpersistence_001"
    context = {}

    # Paso 1 — Crear evento en Agenda
    response1 = router.handle(user_id, "quiero agendar una reunión", context)
    assert response1["status"] == "ok"
    assert "día" in response1["message"].lower()
    context = response1["context"]

    # Guardar manualmente
    save_context(user_id, context.get("fsm_state", "awaiting_date"), context)
    stored = load_context(user_id)
    assert stored and "data" in stored

    # Paso 2 — Cambiar a Notas
    response2 = router.handle(user_id, "crea una nota recordando comprar pan", stored["data"])
    assert response2["status"] == "ok"
    assert "guardar" in response2["message"].lower()

    # Paso 3 — Validar persistencia física
    path = _get_path()
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert user_id in content
    print("\n✅ Persistencia de contexto validada correctamente.")
