# src/theaia/tests/integration/test_core_integration.py

import pytest
from unittest.mock import patch
from src.theaia.core.fsm.conversation_manager import ConversationManager
from src.theaia.core.fsm.states.global_states import GlobalState

@pytest.fixture
def manager() -> ConversationManager:
    """
    [translate:Crea una instancia fresca del ConversationManager para cada test.]
    """
    return ConversationManager("integration_test_user")

@patch('src.theaia.core.fsm.conversation_manager.IntentDetector')
def test_smart_intent_delegation_and_entity_extraction(mock_IntentDetector, manager: ConversationManager):
    """
    [translate:PRUEBA CRÍTICA: Valida que el ConversationManager no solo delega correctamente,
    sino que el especialista (`AgendaConversationManager`) es capaz de extraer entidades
    (como la fecha) desde el primer mensaje del usuario para optimizar el flujo.]
    """
    # 1. Configuración de la Simulación (Mock)
    mock_instance = mock_IntentDetector.return_value
    mock_instance.predict.return_value = ['agenda']

    # 2. Ejecución con un mensaje que ya contiene información de fecha
    message = "[translate:Quiero agendar una reunión para mañana a las 5]"
    response, state, context = manager.process_input(message)

    # 3. Verificación del comportamiento INTELIGENTE
    assert "hora" in response.lower(), "[translate:La respuesta debe pedir la hora, ya que la fecha se extrajo del primer mensaje.]"
    assert state == GlobalState.AGENT_DELEGATED.value
    assert context.get('fsm_state') == 'awaiting_time', "[translate:El estado interno del especialista debe ser 'awaiting_time'.]"
    assert context.get('date') is not None, "[translate:El contexto debe contener la fecha extraída del primer mensaje.]"

def test_simple_intent_delegation(manager: ConversationManager):
    """
    [translate:Valida el flujo simple donde el usuario no da información inicial,
    forzando al agente a pedir la fecha.]
    """
    message = "[translate:Agendar una cita]"
    response, state, context = manager.process_input(message, ['agenda'])

    assert "fecha" in response.lower(), "[translate:Con un mensaje simple, la respuesta debe pedir la fecha.]"
    assert state == GlobalState.AGENT_DELEGATED.value
    assert context.get('fsm_state') == 'awaiting_date'

# --- [translate:AQUÍ ES DONDE AÑADES EL NUEVO TEST] ---
def test_context_persistence_between_messages(manager: ConversationManager):
    """
    [translate:Valida que el contexto se mantiene y enriquece correctamente
    a lo largo de una conversación multi-turno.]
    """
    # --- [translate:Turno 1: Usuario inicia la conversación de agenda] ---
    message1 = "[translate:Quiero agendar una reunión]"
    response1, state1, context1 = manager.process_input(message1, ['agenda'])

    # [translate:Verificaciones del primer turno]
    assert "fecha" in response1.lower()
    assert state1 == GlobalState.AGENT_DELEGATED.value
    assert context1.get('fsm_state') == 'awaiting_date'
    
    # --- [translate:Turno 2: Usuario proporciona la fecha] ---
    # [translate:Pasamos el 'context1' que nos devolvió el turno anterior.]
    # [translate:Aquí está la magia de la persistencia de contexto.]
    message2 = "[translate:mañana]"
    # [translate:La clave es que no hay un tercer argumento `context` en `process_input`.]
    # [translate:El contexto se gestiona internamente en la instancia del manager.]
    response2, state2, context2 = manager.process_input(message2)

    # [translate:Verificaciones del segundo turno]
    assert "hora" in response2.lower(), "[translate:La respuesta debe pedir la hora después de recibir la fecha.]"
    assert state2 == GlobalState.AGENT_DELEGATED.value, "[translate:El estado global debe seguir siendo de delegación.]"
    assert context2.get('fsm_state') == 'awaiting_time', "[translate:El estado interno debe haber avanzado a 'awaiting_time'.]"
    assert context2.get('date') is not None, "[translate:El contexto debe ahora contener la información de la fecha.]"

