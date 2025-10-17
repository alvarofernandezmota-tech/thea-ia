# src/theaia/agents/scheduler_agent/tests/test_handler.py

import pytest
from src.theaia.agents.scheduler_agent.handler import SchedulerAgent

@pytest.fixture
def agent():
    return SchedulerAgent()

def test_can_handle_valid_intents(agent):
    assert agent.can_handle("programar")
    assert agent.can_handle("rutina")
    assert agent.can_handle("schedule")
    assert not agent.can_handle("nota")

def test_cannot_handle_other_intents(agent):
    assert not agent.can_handle("agenda")
    assert not agent.can_handle("consulta")

def test_full_flow_success(agent):
    ctx = {}
    out = agent.handle("u1", "Limpiar inbox", ctx)
    assert "¿Con qué frecuencia" in out["message"]
    out = agent.handle("u1", "semanal", out["context"])
    assert "Confirmas programar" in out["message"]
    out = agent.handle("u1", "sí", out["context"])
    assert "Rutina programada correctamente" in out["message"]
    assert out["status"] == "ok"

def test_full_flow_cancelled(agent):
    ctx = {}
    out = agent.handle("u1", "Hacer backup", ctx)
    out = agent.handle("u1", "mensual", out["context"])
    out = agent.handle("u1", "no", out["context"])
    assert "cancelada" in out["message"]
    assert out["status"] == "error"

def test_context_persistence(agent):
    ctx = {}
    out = agent.handle("u1", "Enviar emails", ctx)
    assert out["context"]["task_description"] == "Enviar emails"
    out = agent.handle("u1", "diaria", out["context"])
    assert out["context"]["frequency"] == "diaria"
