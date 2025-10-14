# src/theaia/tests/core/test_state_machine.py

import pytest
from src.theaia.core.state_machine import StateMachine, State, Transition

# Callbacks para pruebas
def ok_callback(context):
    return "ok"

def help_callback(context):
    return "help"

def fallback_callback(context):
    return "fallback"

def error_callback(context):
    return "error"

@pytest.mark.parametrize("trigger, expected_state, callback", [
    ("create_agenda", State.AGENDA, ok_callback),
    ("schedule_task", State.SCHEDULER, ok_callback),
    ("add_event", State.EVENT, ok_callback),
    ("save_note", State.NOTE, ok_callback),
    ("run_query", State.QUERY, ok_callback),
    ("get_help", State.HELP, help_callback),
    ("fallback", State.FALLBACK, fallback_callback),
    ("error", State.ERROR, error_callback),
])
def test_flows(trigger, expected_state, callback):
    transitions = [
        Transition(trigger, State.INIT, expected_state, callback),
        Transition(f"{trigger}_complete", expected_state, State.COMPLETED, callback),
    ]
    fsm = StateMachine(initial=State.INIT, transitions=transitions)
    # Estado inicial
    assert fsm.current_state() == State.INIT
    # Disparo de trigger
    assert fsm.advance(trigger) == callback({})
    # Verificación de cambio de estado
    assert fsm.current_state() == expected_state

def test_reset_functionality():
    transitions = [
        Transition("create_agenda", State.INIT, State.AGENDA, ok_callback),
        Transition("agenda_complete", State.AGENDA, State.COMPLETED, ok_callback),
    ]
    fsm = StateMachine(initial=State.INIT, transitions=transitions)
    fsm.advance("create_agenda")
    fsm.advance("agenda_complete")
    assert fsm.current_state() == State.COMPLETED
    fsm.reset()
    assert fsm.current_state() == State.INIT

def test_invalid_trigger():
    transitions = [
        Transition("create_agenda", State.INIT, State.AGENDA, ok_callback),
    ]
    fsm = StateMachine(initial=State.INIT, transitions=transitions)
    result = fsm.advance("unknown_trigger")
    assert result == "Transición no válida desde el estado actual."
