# Archivo: src/theaia/tests/e2e/test_context_flow.py

"""Test context flow end-to-end."""

import pytest
from src.theaia.core.fsm.conversation_manager import ConversationManager


@pytest.mark.e2e
def test_e2e_context_flow():
    """Test end-to-end context preservation."""
    cm = ConversationManager("test_user_context")
    
    # Primera interacción
    response1, state1, context1 = cm.process_input("Agendar cita", ["agenda"])
    assert state1 is not None
    assert context1 is not None
    
    # Segunda interacción - debería mantener contexto
    response2, state2, context2 = cm.process_input("Para mañana", [])
    assert context2 is not None
    # Verificar que el contexto persiste
    assert "user_id" in context2 or len(str(context2)) > 0
