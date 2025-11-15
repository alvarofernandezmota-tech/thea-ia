# Archivo: src/theaia/tests/e2e/test_core_flow.py

"""Test core flow end-to-end."""

import pytest
from src.theaia.core.fsm.conversation_manager import ConversationManager


@pytest.mark.e2e  
def test_e2e_agenda_flow():
    """Test agenda flow end-to-end."""
    cm = ConversationManager("test_user_agenda")
    
    # Iniciar flujo de agenda
    response, state, context = cm.process_input("Quiero agendar una cita", ["agenda"])
    
    # Verificaciones básicas
    assert response is not None
    assert len(response) > 0
    assert state is not None
    assert context is not None
