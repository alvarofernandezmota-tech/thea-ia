# Archivo: src/theaia/agents/note_agent/handler.py

from src.theaia.agents.base_agent import BaseAgent

class NoteAgent(BaseAgent):
    def get_supported_intents(self) -> list[str]:
        return ["nota", "apunte"]

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        # Estado inicial: El agente acaba de ser activado
        if not context.get("fsm_state"):
            context["note_content"] = message
            context["fsm_state"] = "awaiting_confirmation"
            context["active_agent"] = self.__class__.__name__
            return {
                "status": "ok",
                "message": f"¿Confirmo que guarde la nota: '{message}'? (responde sí o no)",
                "context": context,
            }

        # Estado de confirmación: El agente está esperando un "sí" o "no"
        elif context.get("fsm_state") == "awaiting_confirmation":
            user_confirmation = message.lower().strip()
            if user_confirmation == "sí":
                # Lógica para guardar la nota (aquí simulada)
                print(f"Guardando nota para {user_id} con contenido: {context['note_content']}")
                context["fsm_state"] = "completed"
                return {
                    "status": "ok",
                    "message": "Nota guardada con éxito.",
                    "context": context,
                }
            else:
                context["fsm_state"] = "cancelled"
                return {
                    "status": "ok",
                    "message": "Operación cancelada.",
                    "context": context,
                }
        
        # Si el estado no es ninguno de los anteriores, no sabe qué hacer
        return super().handle(user_id, message, context)
