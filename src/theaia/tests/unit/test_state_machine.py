import pytest
from src.theaia.core.fsm.state_machine import ConversationStateMachine
from src.theaia.core.fsm.states.global_states import GlobalState

@pytest.fixture
def state_machine():
    return ConversationStateMachine("test_user")

def test_initial_state(state_machine):
    assert state_machine.state == GlobalState.INITIAL.value

def test_handle_ambiguity_transition(state_machine):
    response = state_machine._test_handle_ambiguity(["agenda", "notas"])
    assert state_machine.state == GlobalState.AWAITING_DISAMBIGUATION.value
    assert "¿Quieres guardar esto" in response

def test_disambiguation_choice_valid(state_machine):
    state_machine._test_handle_ambiguity(["agenda", "notas"])
    response = state_machine._test_resolve_disambiguation("agenda")
    assert state_machine.state == GlobalState.AGENT_DELEGATED.value
    assert "agenda" in response.lower()

def test_disambiguation_choice_invalid(state_machine):
    state_machine._test_handle_ambiguity(["agenda", "notas"])
    response = state_machine._test_resolve_disambiguation("invalid_choice")
    assert state_machine.state == GlobalState.AWAITING_DISAMBIGUATION.value
    assert "Por favor, elige" in response

def test_delegate_to_agent(state_machine):
    response = state_machine._test_delegate_to_agent("agenda")
    assert state_machine.state == GlobalState.AGENT_DELEGATED.value
    assert "Procesando tu solicitud como agenda" in response

def test_complete_task(state_machine):
    state_machine._test_delegate_to_agent("agenda")
    response = state_machine._test_complete_task()
    assert state_machine.state == GlobalState.COMPLETED.value
    assert "Tarea completada" in response
