# Archivo: src/theaia/tests/e2e/test_notas_flow.py

"""Test notas flow end-to-end."""

import pytest
from src.theaia.core.fsm.conversation_manager import ConversationManager


@pytest.mark.e2e
def test_notas_flow():
    """Test notas flow end-to-end."""
    cm = ConversationManager("test_user_notas")
    
    # Iniciar flujo de notas
    response, state, context = cm.process_input("Apuntar comprar leche", ["nota"])
    
    # Verificaciones básicas
    assert response is not None
    assert len(response) > 0
    assert state is not None
    assert context is not None
