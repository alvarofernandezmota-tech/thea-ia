# src/theaia/core/state_machine.py

from enum import Enum
from typing import Callable, Optional, Dict, Any
from src.theaia.core.callbacks import (
    handle_agenda,
    handle_scheduler,
    handle_event,
    handle_note,
    handle_query,
    handle_help,
    handle_fallback,
    handle_completed,
    handle_error,
)

class State(Enum):
    INIT = "init"
    AGENDA = "agenda"
    SCHEDULER = "scheduler"
    EVENT = "event"
    NOTE = "note"
    QUERY = "query"
    HELP = "help"
    FALLBACK = "fallback"
    COMPLETED = "completed"
    ERROR = "error"

class Transition:
    def __init__(self, trigger: str, from_state: State, to_state: State, callback: Callable = None):
        self.trigger = trigger
        self.from_state = from_state
        self.to_state = to_state
        self.callback = callback

class StateMachine:
    def __init__(self, initial: State, transitions: list):
        self._current_state = initial
        self._transitions = {(t.from_state, t.trigger): t for t in transitions}

    def advance(self, trigger: str, context: Optional[Dict[str, Any]] = None) -> str:
        key = (self._current_state, trigger)
        if key in self._transitions:
            transition = self._transitions[key]
            self._current_state = transition.to_state
            if transition.callback:
                return transition.callback(context or {})
            return f"Transition to {transition.to_state.value}"
        return "Transición no válida desde el estado actual."

    trigger_transition = advance

    def current_state(self) -> State:
        return self._current_state

    def reset(self):
        self._current_state = State.INIT

# Definición de transiciones
transitions = [
    Transition("create_agenda", State.INIT, State.AGENDA, handle_agenda),
    Transition("agenda_complete", State.AGENDA, State.COMPLETED, handle_completed),
    Transition("schedule_task", State.INIT, State.SCHEDULER, handle_scheduler),
    Transition("scheduler_complete", State.SCHEDULER, State.COMPLETED, handle_completed),
    Transition("add_event", State.INIT, State.EVENT, handle_event),
    Transition("event_complete", State.EVENT, State.COMPLETED, handle_completed),
    Transition("save_note", State.INIT, State.NOTE, handle_note),
    Transition("note_complete", State.NOTE, State.COMPLETED, handle_completed),
    Transition("run_query", State.INIT, State.QUERY, handle_query),
    Transition("query_complete", State.QUERY, State.COMPLETED, handle_completed),
    Transition("get_help", State.INIT, State.HELP, handle_help),
    Transition("fallback", State.INIT, State.FALLBACK, handle_fallback),
    Transition("error", State.INIT, State.ERROR, handle_error),
]

# Instancia de la máquina de estados
fsm = StateMachine(initial=State.INIT, transitions=transitions)
