import pytest
from src.theaia.agents.query_agent.query_conversation_manager import QueryConversationManager

@pytest.fixture
def fsm():
    return QueryConversationManager("test_user")

def test_query_fsm_flow(fsm):
    ctx = {}
    response, state, ctx = fsm.handle_message("test_user", "consulta nueva", ctx)
    assert state == "awaiting_query"
    assert "consulta" in response.lower() or "búsqueda" in response.lower()
    response, state, ctx = fsm.handle_message("test_user", "¿quién ganó la liga 2024?", ctx)
    assert state == "completed"
    assert "recibid" in response.lower()
    assert ctx["user_query"] == "¿quién ganó la liga 2024?"
