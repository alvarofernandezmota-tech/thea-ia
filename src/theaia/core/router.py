"""
TheaRouter: Orquestador multiagente central de Thea IA.
- Router de intents a agentes especializados.
- Mantiene el contexto de sesión y estado conversacional por usuario (FSM).
- 100% compatible con testing automático: exporta `CoreRouter` como alias legacy.
"""

from src.theaia.core.session_manager import SessionManager
from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.help_agent import HelpAgent
from src.theaia.agents.event_agent.handler import EventAgent
from src.theaia.agents.fallback_agent import FallbackAgent
from src.theaia.agents.query_agent.handler import QueryAgent
from src.theaia.agents.reminder_agent.handler import ReminderAgent
# El ScheduleAgent puede que no exista en tu core; si da error, comenta o elimina la línea siguiente:
try:
    from src.theaia.agents.schedule_agent.handler import ScheduleAgent
    HAS_SCHEDULE_AGENT = True
except ImportError:
    ScheduleAgent = None
    HAS_SCHEDULE_AGENT = False

class TheaRouter:
    """
    Orquesta el flujo de mensajes, detecta intents y delega en el agente adecuado.
    Guarda y restaura el contexto/fsm de usuario con SessionManager.
    """
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
        }
        if HAS_SCHEDULE_AGENT and ScheduleAgent:
            self.agent_registry["horario"] = ScheduleAgent

    def handle(self, user_id: str, message: str):
        """
        Ruta principal para procesamiento de mensajes conversacionales.
        Ejecuta detección de intent, selecciona agente y ejecuta, manteniendo FSM/contexto robusto.
        """
        # --- 1. Detección de intent, blindada ---
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

        # --- 2. Selección de agente por intent, fallback si necesario ---
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

        # --- 3. Recupera contexto y estado FSM del usuario ---
        context = self.session_manager.get_context(user_id)
        fsm_state = context.get("fsm_state")

        # --- 4. Ejecuta el agente y maneja errores internos ---
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

        # --- 5. Actualiza contexto de usuario ---
        updated_context["fsm_state"] = new_state
        updated_context["last_intent"] = current_intent
        self.session_manager.update_context(user_id, updated_context)

        # --- 6. Respuesta unificada para consumo por adapters/tests ---
        return {
            "status": "ok" if new_state != "error" else "error",
            "message": response,
            "state": new_state,
            "context": updated_context,
        }

    def reset_session(self, user_id: str):
        """
        Elimina completamente el contexto FSM y variables de sesión de un usuario.
        """
        self.session_manager.reset_context(user_id)

# ----------------- ALIAS DE COMPATIBILIDAD TESTING ---------------------
# Exporta CoreRouter para que todos los tests legacy importen tu nuevo router correctamente.
CoreRouter = TheaRouter
