from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from transitions import Machine
import logging

logger = logging.getLogger(__name__)

class BaseStateMachine(ABC):
    """
    Clase base abstracta para todas las máquinas de estado en Thea IA 2.0
    """
    def __init__(self, user_id: str, initial_state: str = 'initial'):
        self.user_id = user_id
        self.context = {}
        self.machine = None
        self._setup_machine(initial_state)
    
    @abstractmethod
    def get_states(self) -> List[str]:
        """Retorna lista de estados para esta máquina"""
        pass
    
    @abstractmethod
    def setup_transitions(self):
        """Configura las transiciones específicas de la máquina"""
        pass
    
    def _setup_machine(self, initial_state: str):
        """Inicializa la máquina de estados"""
        states = self.get_states()
        self.machine = Machine(
            model=self,
            states=states,
            initial=initial_state,
            auto_transitions=False,
            send_event=True,
            finalize_event='finalize'
        )
        self.setup_transitions()
        self._setup_universal_transitions()
    
    def _setup_universal_transitions(self):
        """Transiciones disponibles en cualquier estado"""
        self.machine.add_transition(
            trigger='reset',
            source='*',
            dest='initial',
            after='_on_reset'
        )
        self.machine.add_transition(
            trigger='error',
            source='*', 
            dest='error_state',
            after='_on_error'
        )
    
    def can_transition(self, trigger: str) -> bool:
        return self.machine.get_trigger(trigger).may_trigger(self)
    
    def get_valid_transitions(self) -> List[str]:
        return [t.trigger for t in self.machine.get_triggers(self.state)]
    
    def update_context(self, **kwargs):
        self.context.update(kwargs)
        logger.debug(f"Context updated for user {self.user_id}: {kwargs}")
    
    def get_context(self, key: str = None, default=None):
        if key is None:
            return self.context
        return self.context.get(key, default)
    
    def clear_context(self):
        essential_keys = ['user_id', 'session_id']
        essential_data = {k: v for k, v in self.context.items() if k in essential_keys}
        self.context.clear()
        self.context.update(essential_data)
    
    def _on_reset(self, event):
        logger.info(f"State machine reset for user {self.user_id}")
        self.clear_context()
    
    def _on_error(self, event):
        logger.error(f"State machine error for user {self.user_id}: {event}")

class ConversationStateMachine(BaseStateMachine):
    """Máquina de estado específica para conversaciones"""

    def __init__(self, user_id: str):
        self.pending_message = None
        self.candidate_intents = []
        self.active_agent = None
        super().__init__(user_id, 'initial')
    
    def get_states(self) -> List[str]:
        return [
            'initial',
            'awaiting_disambiguation',
            'agent_delegated',
            'session_timeout',
            'error_state',
            'completed'
        ]
    
    def setup_transitions(self):
        self.machine.add_transition(
            trigger='request_disambiguation',
            source='initial',
            dest='awaiting_disambiguation',
            after='_after_disambiguation'
        )
        self.machine.add_transition(
            trigger='delegate_to_agent',
            source='initial',
            dest='agent_delegated',
            after='_after_delegation'
        )
        self.machine.add_transition(
            trigger='resolve_disambiguation',
            source='awaiting_disambiguation',
            dest='agent_delegated',
            after='_after_resolution'
        )
        self.machine.add_transition(
            trigger='complete_conversation',
            source=['agent_delegated'],
            dest='completed',
            after='_on_completion'
        )
        self.machine.add_transition(
            trigger='timeout_session',
            source='*',
            dest='session_timeout',
            after='_on_timeout'
        )
    
    def _after_disambiguation(self, event):
        self.update_context(disambiguation_started=True)
    
    def _after_delegation(self, event):
        self.update_context(active_agent=self.active_agent)
    
    def _after_resolution(self, event):
        self.update_context(disambiguation_resolved=True)
    
    def _on_completion(self, event):
        logger.info(f"Conversation completed for user {self.user_id}")
    
    def _on_timeout(self, event):
        logger.warning(f"Session timeout for user {self.user_id}")
        self.clear_context()
    
    def set_pending_message(self, message: str, intents: List[str]):
        self.pending_message = message
        self.candidate_intents = intents
        self.update_context(
            pending_message=message,
            candidate_intents=intents
        )
    
    def get_pending_data(self) -> Tuple[Optional[str], List[str]]:
        return self.pending_message, self.candidate_intents
    
    def clear_pending_data(self):
        self.pending_message = None
        self.candidate_intents = []

    # === Métodos para tests unitarios ===

    def _test_handle_ambiguity(self, intents):
        self.set_pending_message("input_test", intents)
        self.request_disambiguation()
        return f"¿Quieres guardar esto como {intents[0]} o {intents[1]}?"

    def _test_resolve_disambiguation(self, choice):
        if choice not in self.candidate_intents:
            return "Por favor, elige"
        self.active_agent = choice
        self.resolve_disambiguation()
        return f"Procesando tu solicitud como {choice}"

    def _test_delegate_to_agent(self, agent):
        self.active_agent = agent
        self.delegate_to_agent()
        return f"Procesando tu solicitud como {agent}"

    def _test_complete_task(self):
        self.complete_conversation()
        return "Tarea completada"
