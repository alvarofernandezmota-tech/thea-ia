# src/theaia/core/fsm/conversation_manager.py

from typing import Tuple, Dict, Any, List, Optional
from .state_machine import ConversationStateMachine
from .states.global_states import GlobalState, AgentStates
from .transitions import TransitionConfig
import logging
import time

logger = logging.getLogger(__name__)

class ConversationManager:
    """
    Manager principal de conversaciones para Thea IA 2.0
    Integra FSM con lógica de desambiguación y delegación de agentes
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.fsm = ConversationStateMachine(user_id)
        self.transition_config = TransitionConfig()
        self.last_activity_time = time.time()
        
        # Configuración de timeouts
        self.session_timeout_minutes = 30
        self.disambiguation_timeout_minutes = 5
        self.max_disambiguation_retries = 3
        
        # Estado interno
        self._disambiguation_retry_count = 0
        self._disambiguation_start_time = None
        
    @property
    def state(self) -> str:
        """Estado actual del FSM"""
        return self.fsm.state
    
    @property
    def context(self) -> Dict[str, Any]:
        """Contexto actual del FSM"""
        return self.fsm.context
    
    def process_input(self, message: str, candidate_intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        """
        Procesa input del usuario con FSM
        
        Args:
            message: Mensaje del usuario
            candidate_intents: Lista de intents candidatos detectados
            
        Returns:
            Tupla (respuesta, nuevo_estado, contexto_actualizado)
        """
        try:
            self.last_activity_time = time.time()
            
            # Verificar timeout de sesión
            if self._is_session_expired():
                return self._handle_session_timeout()
            
            # Procesar según estado actual
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
                logger.warning(f"Unknown state {self.state} for user {self.user_id}")
                return self._handle_unknown_state(message, candidate_intents)
                
        except Exception as e:
            logger.error(f"Error processing input for user {self.user_id}: {e}")
            return self._handle_error(str(e))
    
    def _handle_initial_state(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja estado inicial"""
        
        if len(intents) > 1:
            # Múltiples intents detectados -> desambiguación
            return self._start_disambiguation(message, intents)
        
        elif len(intents) == 1:
            # Intent claro -> delegar directamente
            return self._delegate_to_agent(intents[0], message)
        
        else:
            # Sin intents claros -> fallback
            return self._handle_fallback(message)
    
    def _start_disambiguation(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        """Inicia proceso de desambiguación"""
        
        # Configurar FSM para desambiguación
        self.fsm.set_pending_message(message, intents)
        self.fsm.request_disambiguation()
        
        # Resetear contadores
        self._disambiguation_retry_count = 0
        self._disambiguation_start_time = time.time()
        
        # Generar pregunta de desambiguación
        question = self._generate_disambiguation_question(intents)
        
        logger.info(f"Starting disambiguation for user {self.user_id} with intents: {intents}")
        
        return question, self.state, self.context
    
    def _generate_disambiguation_question(self, intents: List[str]) -> str:
        """Genera pregunta de desambiguación moderna"""
        
        # Mapear intents a opciones user-friendly
        option_mapping = {
            'notas': 'nota',
            'agenda': 'cita', 
            'recordatorio': 'recordatorio',
            'event': 'evento',
            'scheduler': 'programación'
        }
        
        options = []
        for intent in intents:
            if intent in option_mapping:
                options.append(option_mapping[intent])
        
        # Generar pregunta según opciones disponibles
        if len(options) == 2:
            return f"¿Quieres guardar esto como {options[0]} o como {options[1]}?"
        elif len(options) == 3:
            return f"¿Quieres guardar esto como {', '.join(options[:-1])} o {options[-1]}?"
        else:
            return "¿Qué tipo de acción prefieres? Por favor, especifica: nota, cita o recordatorio."
    
    def _handle_disambiguation_state(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja estado de desambiguación"""
        
        # Verificar timeout de desambiguación
        if self._is_disambiguation_expired():
            return self._handle_disambiguation_timeout()
        
        # Parsear elección del usuario
        chosen_intent = self._parse_user_choice(message)
        
        if chosen_intent:
            # Elección válida -> resolver y delegar
            return self._resolve_disambiguation(chosen_intent)
        else:
            # Elección inválida -> retry o timeout
            return self._handle_invalid_choice(message)
    
    def _parse_user_choice(self, message: str) -> Optional[str]:
        """Parsea elección del usuario desde el mensaje"""
        
        message_lower = message.lower().strip()
        
        # Mapeo de palabras del usuario a intents
        choice_mapping = {
            # Nota/Notas
            'nota': 'notas',
            'notas': 'notas',
            'apunte': 'notas',
            'apuntar': 'notas',
            'anotar': 'notas',
            'guardar': 'notas',
            
            # Cita/Agenda
            'cita': 'agenda',
            'evento': 'agenda',
            'agenda': 'agenda',
            'agendar': 'agenda',
            'reunion': 'agenda',
            'reunión': 'agenda',
            'meeting': 'agenda',
            
            # Recordatorio
            'recordatorio': 'recordatorio',
            'recordar': 'recordatorio',
            'avisar': 'recordatorio',
            'alerta': 'recordatorio',
            'alertar': 'recordatorio',
            'notificar': 'recordatorio'
        }
        
        # Buscar coincidencias exactas
        if message_lower in choice_mapping:
            return choice_mapping[message_lower]
        
        # Buscar coincidencias parciales
        for keyword, intent in choice_mapping.items():
            if keyword in message_lower:
                return intent
        
        return None
    
    def _resolve_disambiguation(self, chosen_intent: str) -> Tuple[str, str, Dict[str, Any]]:
        """Resuelve desambiguación y delega al agente"""
        
        # Obtener mensaje original pendiente
        pending_message, _ = self.fsm.get_pending_data()
        
        # Resolver en FSM
        self.fsm.resolve_disambiguation()
        
        # Limpiar datos de desambiguación
        self._disambiguation_start_time = None
        self._disambiguation_retry_count = 0
        self.fsm.clear_pending_data()
        
        # Delegar al agente elegido
        return self._delegate_to_agent(chosen_intent, pending_message)
    
    def _handle_invalid_choice(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja elección inválida del usuario"""
        
        self._disambiguation_retry_count += 1
        
        if self._disambiguation_retry_count >= self.max_disambiguation_retries:
            # Demasiados reintentos -> timeout
            return self._handle_disambiguation_timeout()
        
        # Generar mensaje de retry
        retry_message = self._generate_retry_message()
        
        logger.warning(f"Invalid disambiguation choice for user {self.user_id}: '{message}'. Retry #{self._disambiguation_retry_count}")
        
        return retry_message, self.state, self.context
    
    def _generate_retry_message(self) -> str:
        """Genera mensaje de reintento para desambiguación"""
        
        retry_messages = [
            "Por favor, elige una de estas opciones: nota, cita o recordatorio.",
            "No he entendido tu elección. ¿Es una nota, cita o recordatorio?",
            "Especifica si quieres: nota, cita o recordatorio."
        ]
        
        # Usar mensaje más específico según número de reintentos
        index = min(self._disambiguation_retry_count - 1, len(retry_messages) - 1)
        return retry_messages[index]
    
    def _delegate_to_agent(self, intent: str, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Delega procesamiento al agente específico"""
        
        # Configurar FSM
        agent_class = AgentStates.get_agent_class(intent)
        self.fsm.active_agent = agent_class
        self.fsm.delegate_to_agent()
        
        # Preparar respuesta de delegación
        # NOTA: Aquí es donde se conectaría con los agentes reales
        # Por ahora retornamos placeholder para integración posterior
        
        response = f"Procesando tu solicitud como {intent}..."
        
        logger.info(f"Delegated to agent {agent_class} for user {self.user_id} with intent: {intent}")
        
        return response, self.state, {
            **self.context,
            'delegated_intent': intent,
            'delegated_agent': agent_class,
            'original_message': message
        }
    
    def _handle_agent_delegated_state(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja estado cuando está delegado a agente"""
        
        # NOTA: Esta lógica se implementará cuando integremos con agentes reales
        # Por ahora, simular procesamiento completado
        
        self.fsm.complete_conversation()
        
        return "Tarea completada. ¿En qué más puedo ayudarte?", self.state, self.context
    
    def _handle_session_timeout(self) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja timeout de sesión"""
        
        self.fsm.timeout_session()
        self.fsm.clear_context()
        
        logger.info(f"Session timeout for user {self.user_id}")
        
        return "Tu sesión ha expirado por inactividad. ¿En qué puedo ayudarte?", self.state, self.context
    
    def _handle_disambiguation_timeout(self) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja timeout de desambiguación"""
        
        self.fsm.timeout_session()
        self.fsm.clear_pending_data()
        self._disambiguation_start_time = None
        self._disambiguation_retry_count = 0
        
        logger.warning(f"Disambiguation timeout for user {self.user_id}")
        
        return "La desambiguación ha expirado. Por favor, repite tu solicitud.", self.state, self.context
    
    def _handle_timeout_recovery(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja recuperación desde timeout"""
        
        self.fsm.reset()
        return self._handle_initial_state(message, intents)
    
    def _handle_error_recovery(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja recuperación desde error"""
        
        self.fsm.reset()
        return self._handle_initial_state(message, intents)
    
    def _handle_fallback(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja caso de fallback"""
        
        return self._delegate_to_agent('fallback', message)
    
    def _handle_unknown_state(self, message: str, intents: List[str]) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja estado desconocido"""
        
        logger.error(f"Unknown state {self.state} for user {self.user_id}")
        self.fsm.reset()
        return self._handle_initial_state(message, intents)
    
    def _handle_error(self, error_message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja errores generales"""
        
        self.fsm.error()
        self.fsm.update_context(error_message=error_message)
        
        return "Ha ocurrido un error. Por favor, intenta de nuevo.", self.state, self.context
    
    def _is_session_expired(self) -> bool:
        """Verifica si la sesión ha expirado"""
        return (time.time() - self.last_activity_time) > (self.session_timeout_minutes * 60)
    
    def _is_disambiguation_expired(self) -> bool:
        """Verifica si la desambiguación ha expirado"""
        if self._disambiguation_start_time is None:
            return False
        return (time.time() - self._disambiguation_start_time) > (self.disambiguation_timeout_minutes * 60)
    
    def reset_conversation(self):
        """Resetea completamente la conversación"""
        self.fsm.reset()
        self._disambiguation_retry_count = 0
        self._disambiguation_start_time = None
        self.last_activity_time = time.time()
        
        logger.info(f"Conversation reset for user {self.user_id}")
    
    def get_conversation_info(self) -> Dict[str, Any]:
        """Obtiene información completa de la conversación"""
        return {
            'user_id': self.user_id,
            'current_state': self.state,
            'context': self.context.copy(),
            'last_activity': self.last_activity_time,
            'active_agent': self.fsm.active_agent,
            'disambiguation_active': self.state == GlobalState.AWAITING_DISAMBIGUATION.value,
            'session_expired': self._is_session_expired()
        }

# Exportaciones
__all__ = ['ConversationManager']
