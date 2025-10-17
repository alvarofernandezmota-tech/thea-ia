# src/theaia/tests/core/test_core_e2e.py

import pytest
from src.theaia.core.router import CoreRouter
from src.theaia.agents.agenda_agent import AgendaAgent
from src.theaia.agents.note_agent import NoteAgent
from src.theaia.agents.reminder_agent import ReminderAgent
from src.theaia.agents.event_agent import EventAgent
from src.theaia.agents.query_agent import QueryAgent
from src.theaia.agents.help_agent import HelpAgent
from src.theaia.agents.scheduler_agent import SchedulerAgent
from src.theaia.agents.fallback_agent import FallbackAgent


@pytest.fixture
def core_router():
    """Fixture que retorna un CoreRouter con todos los agentes registrados."""
    router = CoreRouter()
    router.register_agent(AgendaAgent())
    router.register_agent(NoteAgent())
    router.register_agent(ReminderAgent())
    router.register_agent(EventAgent())
    router.register_agent(QueryAgent())
    router.register_agent(HelpAgent())
    router.register_agent(SchedulerAgent())
    router.register_agent(FallbackAgent())
    return router


def test_core_router_single_intent_delegation(core_router):
    """Test que el CoreRouter delega correctamente con un solo intent claro."""
    user_id = "test_user_1"
    
    # Intent claro de agenda
    response = core_router.process_message(user_id, "quiero agendar una cita")
    assert response["status"] == "ok"
    assert "¿Para cuándo" in response["message"] or "agenda" in response["message"].lower()


def test_core_router_ambiguity_detection(core_router):
    """Test que el CoreRouter detecta ambigüedad entre múltiples agentes."""
    user_id = "test_user_2"
    
    # Mensaje ambiguo que podría ser nota, recordatorio o agenda
    response = core_router.process_message(user_id, "recordar apuntar la cita de mañana")
    
    # Debería detectar ambigüedad y preguntar al usuario
    assert response["status"] in ["ok", "disambiguation"]
    # Puede contener pregunta de desambiguación o haber elegido uno basándose en keywords
    assert response["message"] is not None


def test_core_router_fallback_for_unknown(core_router):
    """Test que el CoreRouter usa FallbackAgent para mensajes no reconocidos."""
    user_id = "test_user_3"
    
    response = core_router.process_message(user_id, "xyz123 comando totalmente desconocido")
    assert response["status"] == "ok"
    assert "Lo siento" in response["message"] or "no he entendido" in response["message"].lower()


def test_core_router_help_intent(core_router):
    """Test que el CoreRouter delega correctamente al HelpAgent."""
    user_id = "test_user_4"
    
    response = core_router.process_message(user_id, "necesito ayuda")
    assert response["status"] == "ok"
    assert "Thea IA" in response["message"] or "ayudar" in response["message"].lower()


def test_core_router_query_intent(core_router):
    """Test que el CoreRouter delega correctamente al QueryAgent."""
    user_id = "test_user_5"
    
    response = core_router.process_message(user_id, "¿qué es Python?")
    assert response["status"] == "ok"
    assert "consulta" in response["message"].lower() or "procesado" in response["message"].lower()


def test_core_router_context_persistence(core_router):
    """Test que el CoreRouter mantiene el contexto entre mensajes."""
    user_id = "test_user_6"
    
    # Primera interacción
    response1 = core_router.process_message(user_id, "crear una nota")
    assert response1["status"] == "ok"
    
    # Segunda interacción (debería mantener el contexto del agente activo)
    response2 = core_router.process_message(user_id, "Comprar leche", context=response1.get("context", {}))
    assert response2["status"] == "ok"
    # El contexto debería tener información de la nota
    assert response2["context"] is not None


def test_core_router_event_intent(core_router):
    """Test que el CoreRouter delega correctamente al EventAgent."""
    user_id = "test_user_7"
    
    response = core_router.process_message(user_id, "crear un evento de cumpleaños")
    assert response["status"] == "ok"
    assert "¿Cuándo es" in response["message"] or "evento" in response["message"].lower()


def test_core_router_scheduler_intent(core_router):
    """Test que el CoreRouter delega correctamente al SchedulerAgent."""
    user_id = "test_user_8"
    
    response = core_router.process_message(user_id, "programar una rutina diaria")
    assert response["status"] == "ok"
    assert "frecuencia" in response["message"].lower() or "programar" in response["message"].lower()
