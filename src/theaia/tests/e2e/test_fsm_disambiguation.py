import pytest
from src.theaia.core.fsm.conversation_manager import ConversationManager

@pytest.mark.e2e
def test_fsm_disambiguation_flow():
    cm = ConversationManager("test_user")
    # Paso 1: input ambiguo
    response, state, _ = cm.process_input("Recordar llamar y apuntar nota", ["agenda", "notas"])
    assert "¿Quieres guardar esto" in response
    assert state == "awaiting_disambiguation"
    # Paso 2: elegir cita
    response, state, _ = cm.process_input("cita", [])
    assert "Procesando tu solicitud como agenda" in response
    assert state == "agent_delegated"
