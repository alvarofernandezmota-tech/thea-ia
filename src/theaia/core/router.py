"""
CoreRouter de Thea IA 3.0 — Integración completa FSM + Agentes (Agenda + Notas + Fallback)
Gestiona FSM, delega a agentes especializados y mantiene persistencia de contexto por usuario.
"""

from typing import Dict, Any
from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.database.repositories.context_repository import load_context, save_context
from src.theaia.core.fsm import ConversationManager
from src.theaia.agents.agenda_agent.agenda_conversation_manager import AgendaConversationManager
from src.theaia.agents.note_agent.handler import NoteAgent


class CoreRouter:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.conversation_managers: Dict[str, ConversationManager] = {}

        # Registro de agentes y alias
        self.agent_registry = {
            "agenda": AgendaConversationManager,
            "agendar": AgendaConversationManager,
            "agendar_cita": AgendaConversationManager,
            "cita": AgendaConversationManager,
            "notas": NoteAgent,
            "nota": NoteAgent,
            "crear_nota": NoteAgent,
            "recordar_nota": NoteAgent,
        }

        print("CoreRouter inicializado con FSM y agentes integrados (Agenda + Notas).")

    # --- Conversation Manager ------------------------------------------------
    def _get_or_create_conversation_manager(self, user_id: str) -> ConversationManager:
        if user_id not in self.conversation_managers:
            self.conversation_managers[user_id] = ConversationManager(user_id)
            print(f"Nuevo ConversationManager creado para {user_id}")
        return self.conversation_managers[user_id]

    # --- Main Handler --------------------------------------------------------
    def handle(self, user_id: str, message: str, context: Dict[str, Any] | None) -> Dict[str, Any]:

        context = context or {}
        conv_manager = self._get_or_create_conversation_manager(user_id)

        # 1. Detección de intención
        try:
            raw = self.intent_detector.detect(message)
            intents = [str(i) for i in raw] if isinstance(raw, (list, tuple)) else [str(raw)]
        except Exception as e:
            print(f"[Error IntentDetector] {e}")
            intents = []

        # 2. Procesamiento FSM
        try:
            response_text, new_state, updated_context = conv_manager.process_input(
                message=message, candidate_intents=intents
            )

            # Cambio dinámico de intención
            current_intent = updated_context.get("delegated_intent")
            if intents and intents[0] not in [current_intent]:
                print(f"[Cambio de intención detectado: {intents[0]}]")
                updated_context["fsm_state"] = "initial"
                updated_context["delegated_intent"] = intents[0]
                new_state = "delegated"

            # 3. Delegación a agente especializado
            delegated_intent = updated_context.get("delegated_intent")
            if delegated_intent in self.agent_registry:
                agent_cls = self.agent_registry[delegated_intent]
                try:
                    agent = agent_cls(user_id)
                    response_text, new_state, updated_context = agent.handle(message, updated_context)
                except Exception as e:
                    print(f"[Error Agente {delegated_intent}] {e}")
                    response_text = "No se pudo ejecutar la tarea del agente."
                    new_state = "error"

            # 4. Guardar contexto (corregido)
            try:
                save_context(user_id=user_id, data=updated_context)
            except TypeError:
                # Compatibilidad por si la firma de save_context es distinta
                try:
                    save_context(user_id, updated_context)
                except Exception as e:
                    print(f"[Advertencia Contexto] {e}")

            # 5. Respuesta
            return {
                "status": "ok",
                "message": response_text,
                "context": updated_context,
                "state": new_state,
            }

        except Exception as e:
            print(f"[Error ConversationManager] {e}")
            return {"status": "error", "message": "Error interno.", "context": context}
