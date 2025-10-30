import pytest
from src.theaia.core import router
from src.theaia.tests.mocks.mock_intent_detector import MockIntentDetector

# --- Importación completa de todos los agentes ---
from src.theaia.agents.agenda_agent import AgendaAgent
from src.theaia.agents.note_agent import NoteAgent
from src.theaia.agents.reminder_agent import ReminderAgent
from src.theaia.agents.event_agent import EventAgent
from src.theaia.agents.query_agent import QueryAgent
from src.theaia.agents.help_agent import HelpAgent
# from src.theaia.agents.scheduler_agent import SchedulerAgent  # <--- ELIMINADO O COMENTADO
from src.theaia.agents.fallback_agent import FallbackAgent

@pytest.fixture
def core_router(monkeypatch):
    """Prepara un CoreRouter para tests, usando un mock del detector."""
    monkeypatch.setattr(router, "IntentDetector", MockIntentDetector)
    core = router.CoreRouter()
    core.agents = [
        AgendaAgent(), NoteAgent(), ReminderAgent(), EventAgent(),
        QueryAgent(), HelpAgent(), FallbackAgent(),  # SchedulerAgent eliminado
    ]
    return core

# ... (resto de los tests igual) ...
