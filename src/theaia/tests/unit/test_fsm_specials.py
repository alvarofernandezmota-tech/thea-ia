import pytest
from src.theaia.core.fsm.state_machine import ConversationStateMachine
from src.theaia.core.fsm.states.global_states import GlobalState

@pytest.fixture
def state_machine():
    return ConversationStateMachine("test_user")

def test_timeout_transition(state_machine):
    state_machine._test_handle_ambiguity(["agenda", "notas"])
    state_machine.timeout_session()
    assert state_machine.state == GlobalState.SESSION_TIMEOUT.value

def test_error_transition(state_machine):
    state_machine._test_handle_ambiguity(["agenda", "notas"])
    state_machine.error()
    assert state_machine.state == GlobalState.ERROR_STATE.value

def test_reset_transition(state_machine):
    state_machine._test_handle_ambiguity(["agenda", "notas"])
    state_machine.reset()
    assert state_machine.state == GlobalState.INITIAL.value
