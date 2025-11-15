# Archivo: src/theaia/tests/e2e/test_fsm_disambiguation.py

import pytest
from src.theaia.core.fsm.conversation_manager import ConversationManager


@pytest.mark.e2e
def test_fsm_disambiguation_flow():
    """Test FSM disambiguation flow."""
    cm = ConversationManager("test_user")
    
    # Paso 1: input ambiguo
    response, state, _ = cm.process_input("Recordar llamar y apuntar nota", ["agenda", "notas"])
    assert "¿Quieres guardar esto" in response or "qué" in response.lower()
    assert state == "awaiting_disambiguation"
    
    # Paso 2: elegir cita
    response, state, _ = cm.process_input("cita", [])
    # El sistema puede responder de varias formas
    # Verificamos que pasó a agent_delegated o está preguntando por detalles
    assert state in ["agent_delegated", "awaiting_agenda_date", "initial"]
    assert response is not None
    assert len(response) > 0
