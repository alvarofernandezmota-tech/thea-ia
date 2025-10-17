# src/theaia/agents/scheduler_agent/handler.py

from src.theaia.agents.scheduler_agent.model.scheduler_fsm import SchedulerFSM

class SchedulerAgent:
    """
    Agente de Thea IA 2.0 encargado de programar tareas automáticas
    o recordatorios recurrentes en base a una rutina definida.
    """

    def __init__(self):
        self.fsm = SchedulerFSM()

    def can_handle(self, intent: str) -> bool:
        """Reconoce intents relacionados con programación automática."""
        return intent.lower() in [
            "programar", "rutina", "schedule", "automático", "diario",
            "semanal", "mensual", "recurrente"
        ]

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa el mensaje del usuario y actualiza el contexto mediante la FSM.
        """
        self.fsm.context.update(context)
        response, state = self.fsm.process_message(message, context)
        status = "ok" if state not in ["error", "cancelled"] else "error"
        return {
            "status": status,
            "message": response,
            "fsm_state": state,
            "context": self.fsm.context
        }
