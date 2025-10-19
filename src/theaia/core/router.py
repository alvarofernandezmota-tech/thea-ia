"""
CoreRouter de Thea IA 2.0 con integración FSM.
"""

from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.database.repositories.context_repository import load_context, save_context
from src.theaia.core.fsm import ConversationManager
from typing import Dict, Any


class CoreRouter:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.agents = []
        self.conversation_managers: Dict[str, ConversationManager] = {}
        print("CoreRouter inicializado con soporte FSM.")

    def _get_or_create_conversation_manager(self, user_id: str) -> ConversationManager:
        """Obtiene o crea un ConversationManager para el usuario."""
        if user_id not in self.conversation_managers:
            self.conversation_managers[user_id] = ConversationManager(user_id)
        return self.conversation_managers[user_id]

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa un mensaje usando ConversationManager + FSM.
        """
        if context is None:
            context = {}

        # Obtener o crear ConversationManager para este usuario
        conv_manager = self._get_or_create_conversation_manager(user_id)

        # Detectar intenciones
        try:
            raw_intents = self.intent_detector.detect(message)
            if hasattr(raw_intents, '__iter__') and not isinstance(raw_intents, str):
                intents = [str(i) for i in raw_intents]
            else:
                intents = [str(raw_intents)]
        except Exception as e:
            print(f"Error en detección de intenciones: {e}")
            intents = []

        # Procesar con ConversationManager
        try:
            response_text, new_state, updated_context = conv_manager.process_input(
                message=message,
                candidate_intents=intents
            )
            
            # Guardar contexto actualizado
            try:
                save_context(user_id, updated_context)
            except Exception:
                pass

            return {
                "status": "ok",
                "message": response_text,
                "context": updated_context,
                "state": new_state
            }

        except Exception as e:
            print(f"Error en ConversationManager: {e}")
            return {
                "status": "error",
                "message": "Ha ocurrido un error procesando tu solicitud.",
                "context": context
            }

    def _get_agent_by_name(self, agent_name: str):
        """Busca un agente por nombre de clase."""
        return next((a for a in self.agents if a.__class__.__name__ == agent_name), None)

    def _get_fallback_agent(self):
        """Obtiene la instancia de FallbackAgent."""
        return next((a for a in self.agents if a.__class__.__name__ == "FallbackAgent"), None)
