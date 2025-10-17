# src/theaia/agents/scheduler_agent/tests/test_scheduler_fsm.py

import pytest
from src.theaia.agents.scheduler_agent.model.scheduler_fsm import SchedulerFSM

@pytest.fixture
def fsm():
    return SchedulerFSM()

def test_initial_state(fsm):
    assert fsm.state == "awaiting_task"

def test_transition_to_awaiting_schedule(fsm):
    resp, state = fsm.process_message("Respaldar base de datos", {})
    assert "¿Con qué frecuencia" in resp
    assert state == "awaiting_schedule"
    assert fsm.context["task_description"] == "Respaldar base de datos"

def test_invalid_schedule(fsm):
    fsm.state = "awaiting_schedule"
    resp, state = fsm.process_message("cada hora", {})
    assert "Por favor, elige" in resp
    assert state == "awaiting_schedule"

def test_transition_to_confirmation(fsm):
    fsm.context["task_description"] = "Enviar reporte"
    fsm.state = "awaiting_schedule"
    resp, state = fsm.process_message("diaria", {})
    assert "Confirmas programar" in resp
    assert state == "confirmation"
    assert fsm.context["frequency"] == "diaria"

def test_schedule_confirmation_yes(fsm):
    fsm.state = "confirmation"
    resp, state = fsm.process_message("sí", {})
    assert "Rutina programada correctamente" in resp
    assert state == "scheduled"

def test_schedule_cancelled(fsm):
    fsm.state = "confirmation"
    resp, state = fsm.process_message("no", {})
    assert "cancelada" in resp
    assert state == "cancelled"

def test_error_state(fsm):
    fsm.state = "unknown"
    resp, state = fsm.process_message("test", {})
    assert "error" in resp.lower()
    assert state == "error"
