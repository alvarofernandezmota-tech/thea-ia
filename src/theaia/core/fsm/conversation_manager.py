from typing import Tuple, Dict, Any, List, Optional
import logging
import time

from src.theaia.ml.intent_detector import IntentDetector
from .state_machine import ConversationStateMachine
from .states.global_states import GlobalState, AgentStates
from .transitions import TransitionConfig
from .agenda_conversation_manager import AgendaConversationManager

logger = logging.getLogger(__name__)

class ConversationManager:
    """
    [translate:Manager principal que orquesta la conversación, integra la detección de intenciones
    y delega a managers especializados.]
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.fsm = ConversationStateMachine(user_id)
        # --- CORRECCIÓN 1 de 2: Instanciamos el detector de intenciones ---
        self.intent_detector = IntentDetector()
        self.transition_config = TransitionConfig()
        self.last_activity_time = time.time()
        
        self.session_timeout_minutes = 30
        self.disambiguation_timeout_minutes = 5
        self.max_disambiguation_retries = 3
        
        self._disambiguation_retry_count = 0
        self._disambiguation_start_time = None
        
        self.agenda_manager = AgendaConversationManager(user_id)
    
    @property
    def state(self) -> str:
        return self.fsm.state
    
    @property
    def context(self) -> Dict[str, Any]:
        return self.fsm.context
    
    def process_input(self, message: str, candidate_intents: List[str] = None) -> Tuple[str, str, Dict[str, Any]]:
        # [translate:Permitimos que candidate_intents sea opcional]
        if candidate_intents is None:
            candidate_intents = []

        try:
            self.last_activity_time = time.time()
            if self.state == GlobalState.COMPLETED.value:
                self.fsm.reset()

            if self.state == GlobalState.INITIAL.value:
                return self._handle_initial_state(message, candidate_intents)
            elif self.state == GlobalState.AWAITING_DISAMBIGUATION.value:
                return self._handle_disambiguation_state(message)
            elif self.state == GlobalState.AGENT_DELEGATED.value:
                return self._handle_agent_delegated_state(message)
            elif self.state == GlobalState.SESSION_TIMEOUT.value:
                return self._handle_timeout_recovery(message, candidate_intents)
            elif self.state == GlobalState.ERROR_STATE.value:
                return self._handle_error_recovery(message, candidate_intents)
            else:
                logger.warning(f"[translate:Estado desconocido] {self.state} [translate:para el usuario] {self.user_id}")
                return self._handle_unknown_state(message, candidate_intents)
        except Exception as e:
            logger.error(f"Error processing input for user {self.user_id}: {e}", exc_info=True)
            return self._handle_error(str(e))

    def _handle_initial_state(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        # --- CORRECCIÓN 2 de 2: Usamos el detector si no hay intenciones ---
        if not intents:
            intents = self.intent_detector.predict(message)

        if len(intents) > 1: return self._start_disambiguation(message, intents)
        elif len(intents) == 1: return self._delegate_to_agent(intents[0], message)
        else: return self._handle_fallback(message)

    # --- [translate:El resto de tu código completo y correcto va aquí sin cambios] ---

    def _handle_agent_delegated_state(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        active_agent_intent = self.context.get('delegated_intent')
        if active_agent_intent == 'agenda':
            response, updated_context = self.agenda_manager.handle_message(message, self.context)
            if updated_context.get('fsm_state') in ['completed', 'cancelled']:
                self.fsm.complete_conversation()
            return response, self.state, updated_context
        logger.info(f"Agent flow for '{active_agent_intent}' completed.")
        self.fsm.complete_conversation()
        return "[translate:Tarea completada. ¿En qué más puedo ayudarte?]", self.state, self.context

    def _delegate_to_agent(self, intent: str, message: str) -> Tuple[str, str, Dict[str, Any]]:
        agent_class_name = AgentStates.get_agent_class(intent)
        self.fsm.active_agent = agent_class_name
        self.fsm.delegate_to_agent()
        logger.info(f"Delegating to agent '{agent_class_name}' for intent: '{intent}'")
        self.fsm.update_context(**{'delegated_intent': intent, 'delegated_agent_name': agent_class_name, 'original_message': message})
        if intent == 'agenda':
            return self._handle_agent_delegated_state(message)
        response = f"[translate:Procesando tu solicitud como] {intent}..."
        return response, self.state, self.context
    
    def _start_disambiguation(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        self.fsm.set_pending_message(message, intents); self.fsm.request_disambiguation()
        self._disambiguation_retry_count = 0; self._disambiguation_start_time = time.time()
        question = self._generate_disambiguation_question(intents)
        logger.info(f"Starting disambiguation for user {self.user_id} with intents: {intents}")
        return question, self.state, self.context

    def _generate_disambiguation_question(self, intents: List[str]) -> str:
        option_mapping = {'notas': 'nota', 'agenda': 'cita', 'recordatorio': 'recordatorio'}
        options = [option_mapping[i] for i in intents if i in option_mapping]
        if len(options) == 2: return f"[translate:¿Quieres guardar esto como] {options[0]} [translate:o como] {options[1]}?"
        if len(options) > 2: return f"[translate:¿Quieres guardar esto como] {', '.join(options[:-1])} [translate:o] {options[-1]}?"
        return "[translate:¿Qué tipo de acción prefieres? Por favor, especifica: nota, cita o recordatorio.]"

    def _handle_disambiguation_state(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        if self._is_disambiguation_expired(): return self._handle_disambiguation_timeout()
        chosen_intent = self._parse_user_choice(message)
        if chosen_intent: return self._resolve_disambiguation(chosen_intent)
        else: return self._handle_invalid_choice(message)

    def _parse_user_choice(self, message: str) -> Optional[str]:
        choice_mapping = {'nota': 'notas', 'apunte': 'notas', 'cita': 'agenda', 'evento': 'agenda', 'recordatorio': 'recordatorio'}
        message_lower = message.lower().strip()
        if message_lower in choice_mapping: return choice_mapping[message_lower]
        for keyword, intent in choice_mapping.items():
            if keyword in message_lower: return intent
        return None

    def _resolve_disambiguation(self, chosen_intent: str) -> Tuple[str, str, Dict[str, Any]]:
        pending_message, _ = self.fsm.get_pending_data()
        self.fsm.resolve_disambiguation()
        self._disambiguation_start_time = None; self._disambiguation_retry_count = 0
        self.fsm.clear_pending_data()
        return self._delegate_to_agent(chosen_intent, pending_message)

    def _handle_invalid_choice(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        self._disambiguation_retry_count += 1
        if self._disambiguation_retry_count >= self.max_disambiguation_retries: return self._handle_disambiguation_timeout()
        retry_message = self._generate_retry_message()
        logger.warning(f"Invalid disambiguation choice for user {self.user_id}: '{message}'. Retry #{self._disambiguation_retry_count}")
        return retry_message, self.state, self.context

    def _generate_retry_message(self) -> str:
        messages = ["[translate:Por favor, elige una de estas opciones: nota, cita o recordatorio.]", "[translate:No he entendido tu elección. ¿Es una nota, cita o recordatorio?]", "[translate:Especifica si quieres: nota, cita o recordatorio.]"]
        return messages[min(self._disambiguation_retry_count - 1, len(messages) - 1)]

    def _handle_fallback(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        return self._delegate_to_agent('fallback', message)

    def _is_session_expired(self) -> bool:
        return (time.time() - self.last_activity_time) > (self.session_timeout_minutes * 60)

    def _is_disambiguation_expired(self) -> bool:
        if self._disambiguation_start_time is None: return False
        return (time.time() - self._disambiguation_start_time) > (self.disambiguation_timeout_minutes * 60)

    def _handle_session_timeout(self) -> Tuple[str, str, Dict[str, Any]]:
        self.fsm.timeout_session(); self.fsm.clear_context()
        logger.info(f"Session timeout for user {self.user_id}")
        return "[translate:Tu sesión ha expirado por inactividad. ¿En qué puedo ayudarte?]", self.state, self.context

    def _handle_disambiguation_timeout(self) -> Tuple[str, str, Dict[str, Any]]:
        self.fsm.timeout_session(); self.fsm.clear_pending_data()
        self._disambiguation_start_time = None; self._disambiguation_retry_count = 0
        logger.warning(f"Disambiguation timeout for user {self.user_id}")
        return "[translate:La desambiguación ha expirado. Por favor, repite tu solicitud.]", self.state, self.context

    def _handle_timeout_recovery(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        self.fsm.reset(); return self._handle_initial_state(message, intents)

    def _handle_error_recovery(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        self.fsm.reset(); return self._handle_initial_state(message, intents)

    def _handle_unknown_state(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        logger.error(f"Unknown state {self.state} for user {self.user_id}"); self.fsm.reset()
        return self._handle_initial_state(message, intents)

    def _handle_error(self, error_message: str) -> Tuple[str, str, Dict[str, Any]]:
        self.fsm.error(); self.fsm.update_context(error_message=error_message)
        return "[translate:Ha ocurrido un error. Por favor, intenta de nuevo.]", self.state, self.context

__all__ = ['ConversationManager']
