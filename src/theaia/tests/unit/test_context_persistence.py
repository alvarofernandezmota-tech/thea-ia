import pytest
from src.theaia.database.repositories.context_repository import save_context, load_context

def test_save_and_load_context(tmp_path):
    # Simula ciclo típico de persistencia
    uid = "test_persist"
    state = "agent_delegated"
    context = {"foo": 123, "bar": "baz"}
    save_context(uid, state, context)

    loaded = load_context(uid)
    assert loaded is not None
    assert loaded.get("state") == state            # Estado guardado
    assert loaded.get("data")["foo"] == 123        # Contexto guardado
    assert loaded.get("data")["bar"] == "baz"      # Contexto guardado
