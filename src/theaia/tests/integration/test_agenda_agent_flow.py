import pytest
from src.theaia.core.fsm.conversation_manager import ConversationManager
from src.theaia.core.fsm.states.global_states import GlobalState

@pytest.mark.asyncio
async def test_full_agenda_conversation_flow():
    """
    [translate:Prueba el flujo completo, desde la delegación del manager global
    hasta la conversación multi-turno del manager especialista de agenda.]
    """
    user_id = "test_user_123"
    manager = ConversationManager(user_id)
    
    # --- [translate:Turno 1: Usuario inicia la conversación de agenda] ---
    response, state, context = manager.process_input("Quiero agendar una reunión", ["agenda"])
    assert "fecha" in response.lower()
    assert state == GlobalState.AGENT_DELEGATED.value
    assert context.get('fsm_state') == 'awaiting_date'

    # --- [translate:Turno 2: Usuario da la fecha] ---
    response, state, context = manager.process_input("mañana", [])
    assert "hora" in response.lower()
    assert state == GlobalState.AGENT_DELEGATED.value
    assert context.get('fsm_state') == 'awaiting_time'

    # --- [translate:Turno 3: Usuario da la hora] ---
    response, state, context = manager.process_input("a las 5pm", [])
    assert "confirma" in response.lower()
    assert state == GlobalState.AGENT_DELEGATED.value
    assert context.get('fsm_state') == 'awaiting_confirmation'

    # --- [translate:Turno 4: Usuario confirma y finaliza el flujo] ---
    response, state, context = manager.process_input("sí, confirmo", [])
    assert "agendado" in response.lower()
    assert context.get('fsm_state') == 'completed'
    # --- ¡LA COMPROBACIÓN CORREGIDA! ---
    # [translate:Al final del turno 4, el estado global DEBE ser 'completed'.]
    assert state == GlobalState.COMPLETED.value, "[translate:El estado global debe ser COMPLETED al finalizar el flujo]"

    # --- [translate:Turno 5: Se inicia una nueva conversación para verificar el reseteo] ---
    # [translate:Al recibir un nuevo mensaje, el manager debe haberse reseteado a 'initial']
    # [translate:y procesar esto como una intención desconocida (fallback).]
    response, state, context = manager.process_input("gracias", [])
    
    # [translate:Esperamos que haya delegado al FallbackAgent]
    assert state == GlobalState.AGENT_DELEGATED.value
    assert context.get('delegated_intent') == 'fallback'
