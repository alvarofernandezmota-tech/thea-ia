# src/theaia/agents/agenda_agent/agenda_conversation_manager.py

from typing import Dict, Any, Tuple

class AgendaConversationManager:
    """
    Versión mínima funcional del AgendaConversationManager
    para integrarse con el FSM y el CoreRouter de Thea IA.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        """
        Flujo de conversación de agenda básico y compatible.
        """
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_date"
            response = "¿Para qué día deseas agendar tu cita?"
            next_state = "awaiting_date"
        elif context["fsm_state"] == "awaiting_date":
            context["date"] = message
            context["fsm_state"] = "awaiting_time"
            response = "¿A qué hora deseas agendarla?"
            next_state = "awaiting_time"
        elif context["fsm_state"] == "awaiting_time":
            context["time"] = message
            context["fsm_state"] = "completed"
            response = f"Tu reunión ha sido agendada para el {context['date']} a las {context['time']}."
            next_state = "completed"
        else:
            response = "El flujo de agenda ha finalizado."
            next_state = "completed"

        return response, next_state, context
