import pytest
from src.theaia.agents.note_agent.note_conversation_manager import NoteConversationManager

@pytest.fixture
def fsm():
    return NoteConversationManager("test_user")

def test_note_fsm_flow(fsm):
    ctx = {}
    response, state, ctx = fsm.handle_message("test_user", "nueva nota", ctx)
    assert state == "awaiting_note_content"
    assert "nota" in response.lower()
    response, state, ctx = fsm.handle_message("test_user", "apuntes de reunión", ctx)
    assert state == "completed"
    assert "guardad" in response.lower()
    assert ctx["note"] == "apuntes de reunión"
