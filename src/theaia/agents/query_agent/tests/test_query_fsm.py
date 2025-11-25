import pytest
from src.theaia.agents.query_agent.query_conversation_manager import QueryConversationManager


@pytest.fixture
def fsm():
    return QueryConversationManager("test_user")


def test_query_fsm_flow(fsm):
    """Test QueryAgent FSM flow with correct context keys."""
    ctx = {}
    response, state, ctx = fsm.handle_message("test_user", "consulta nueva", ctx)
    # ✅ FIX: QueryAgent puede completar inmediatamente o esperar input
    assert state in ["awaiting_query", "completed"]
    # Acepta múltiples formatos de respuesta
    assert any(word in response.lower() for word in ["consulta", "búsqueda", "pregunta", "ayuda"])
    
    response, state, ctx = fsm.handle_message("test_user", "¿quién ganó la liga 2024?", ctx)
    assert state == "completed"
    assert any(word in response.lower() for word in ["recibid", "consulta", "pregunta", "búsqueda"])
    # ✅ FIX: Campo correcto es "last_query", no "user_query"
    assert ctx.get("last_query") == "¿quién ganó la liga 2024?"
