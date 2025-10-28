# src/theaia/core/router.py

from src.theaia.core.session_manager import SessionManager
from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.help_agent import HelpAgent
from src.theaia.agents.event_agent.handler import EventAgent
from src.theaia.agents.fallback_agent import FallbackAgent
from src.theaia.agents.query_agent.handler import QueryAgent
from src.theaia.agents.reminder_agent.handler import ReminderAgent
from src.theaia.agents.schedule_agent.handler import ScheduleAgent

# Opcional: añade AgendaAgent, OcioAgent, SaludAgent cuando estén listos

class TheaRouter:
    def __init__(self):
        self.session_manager = SessionManager()
        self.intent_detector = IntentDetector()
        self.fallback_agent = FallbackAgent("global")
        self.agent_registry = {
            "nota": NoteAgent,
            "ayuda": HelpAgent,
            "evento": EventAgent,
            "consulta": QueryAgent,
            "recordatorio": ReminderAgent,
            "horario": ScheduleAgent,
            # Añade aquí más agentes
        }

    def handle(self, user_id: str, message: str):
        # 1. Detección de intent BLINDADA
        try:
            raw = self.intent_detector.detect(message)
            # Normalización defensiva
            if isinstance(raw, (list, tuple)):
                intents = [str(i).strip().lower() for i in raw if str(i).strip()]
            else:
                intents = [str(raw).strip().lower()] if str(raw).strip() else []
        except Exception as e:
            print(f"[IntentDetector ERROR]: {e}")
            intents = []

        # 2. Si hay intent claro, lo usamos; si no, fallback directo
        if intents and intents[0] in self.agent_registry:
            current_intent = intents[0]
            AgentClass = self.agent_registry[current_intent]
            agent = AgentClass(user_id)
        elif intents and intents[0] == "ayuda":
            current_intent = "ayuda"
            agent = self.agent_registry["ayuda"](user_id)
        else:
            # Sin intent claro o vacío: fallback
            current_intent = "fallback"
            agent = self.fallback_agent

        # 3. Recupera contexto y FSM robustamente
        context = self.session_manager.get_context(user_id)
        fsm_state = context.get("fsm_state")

        # 4. Ejecuta handler seguro (try/except por agente)
        try:
            response, new_state, updated_context = agent.handle(user_id, message, context)
        except Exception as e:
            print(f"[ERROR agent {current_intent}]: {e}")
            response, new_state, updated_context = (
                "Ha habido un error inesperado, ¿puedes repetir tu petición?",
                "error",
                context
            )
            current_intent = "fallback"

        # 5. Actualiza FSM y contexto de usuario blindado
        updated_context["fsm_state"] = new_state
        updated_context["last_intent"] = current_intent
        self.session_manager.update_context(user_id, updated_context)

        # 6. Devuelve respuesta estándar
        return {
            "status": "ok" if new_state != "error" else "error",
            "message": response,
            "state": new_state,
            "context": updated_context,
        }

    def reset_session(self, user_id: str):
        self.session_manager.reset_context(user_id)
