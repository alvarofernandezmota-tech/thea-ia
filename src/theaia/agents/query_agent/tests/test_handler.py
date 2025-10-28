import pytest
from src.theaia.agents.query_agent.handler import QueryAgent

@pytest.fixture
def agent():
    user_id = "test_user"
    return QueryAgent(user_id)

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("consulta")
    assert agent.can_handle("buscar")
    assert agent.can_handle("pregunta")
    assert agent.can_handle("información")
    assert agent.can_handle("query")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("nota")
    assert not agent.can_handle("evento")

def test_query_flow(agent):
    ctx = {}
    uid = "test_user"
    # Primer mensaje: espera consulta
    out = agent.handle(uid, "quiero buscar información", ctx)
    assert "consulta" in out[0].lower() or "búsqueda" in out[0].lower()
    # Segundo mensaje: procesa consulta
    out = agent.handle(uid, "¿qué tiempo hace en Madrid?", out[2])
    assert "recibid" in out[0].lower()
    assert out[1] == "completed"
