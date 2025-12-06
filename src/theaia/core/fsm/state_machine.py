from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple, Set
from transitions import Machine
import logging
from datetime import datetime
import uuid

# H03 FASE 1 - BLOQUE 1.2 - Imports
from src.theaia.core.fsm.callbacks_mixin import CallbacksMixin
from src.theaia.core.fsm.context_merging import ContextMergingEngine

logger = logging.getLogger(__name__)


class BaseStateMachine(ABC):
    """Base class for all state machines"""
    
    VALID_STATES = []
    INITIAL_STATE = "initial"
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.state = self.INITIAL_STATE
        self.context = {}
        self._setup_machine()
    
    def _setup_machine(self):
        """Setup the transitions machine"""
        self.machine = Machine(
            model=self,
            states=self.VALID_STATES,
            initial=self.INITIAL_STATE,
            auto_transitions=False
        )
    
    def validate_state(self, state: str) -> bool:
        """Validate if a state is valid"""
        return state in self.VALID_STATES
    
    def get_valid_transitions_set(self) -> Set[str]:
        """Get set of valid transitions from current state"""
        valid_transitions = set()
        
        if hasattr(self.machine, 'models'):
            for model in self.machine.models:
                if hasattr(model, '_transitions'):
                    for trigger in model._transitions.get(self.state, []):
                        valid_transitions.add(trigger)
        
        # Always add reset and error as universal transitions
        valid_transitions.add('reset')
        valid_transitions.add('error')
        
        return valid_transitions
    
    def can_transition_to(self, trigger: str) -> bool:
        """Check if a transition is possible"""
        return trigger in self.get_valid_transitions_set()
    
    def transition_safe(self, trigger: str) -> bool:
        """Safely transition using a trigger"""
        if not self.can_transition_to(trigger):
            raise Exception(f"Transition '{trigger}' not allowed from state '{self.state}'")
        
        getattr(self, trigger)()
        return True
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information"""
        return {
            "current_state": self.state,
            "valid_transitions": list(self.get_valid_transitions_set()),
            "context": self.context.copy(),
            "timestamp": datetime.now().isoformat()
        }
    
    def update_context(self, **kwargs):
        """Update context with new values"""
        self.context.update(kwargs)
    
    def get_context(self, key: str = None, default: Any = None) -> Any:
        """Get context value by key or all context"""
        if key is None:
            return self.context.copy()
        return self.context.get(key, default)
    
    def clear_context(self):
        """Clear all context except session_id"""
        session_id = self.context.get('session_id')
        self.context.clear()
        if session_id:
            self.context['session_id'] = session_id


class ConversationStateMachine(BaseStateMachine, CallbacksMixin, ContextMergingEngine):
    """State machine for conversation flow management"""
    
    VALID_STATES = [
        'initial',
        'awaiting_disambiguation',
        'agent_delegated',
        'completed',
        'error_state',
        'session_timeout'
    ]
    
    def __init__(self, user_id: str, session_id: str = None):
        super().__init__(user_id)
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.active_agent = None
        self.pending_message = None
        self.candidate_intents = []
        
        # Initialize context
        self.update_context(session_id=self.session_id)
        
        # Setup transitions
        self._setup_transitions()
    
    def _setup_transitions(self):
        """Setup state machine transitions"""
        self.machine = Machine(
            model=self,
            states=self.VALID_STATES,
            initial=self.INITIAL_STATE,
            auto_transitions=False
        )
        
        # From initial state
        self.machine.add_transition('request_disambiguation', 'initial', 'awaiting_disambiguation',
                                   before=self._on_request_disambiguation)
        self.machine.add_transition('delegate_to_agent', 'initial', 'agent_delegated',
                                   before=self._on_delegate_to_agent)
        
        # From awaiting_disambiguation
        self.machine.add_transition('delegate_to_agent', 'awaiting_disambiguation', 'agent_delegated',
                                   before=self._on_delegate_to_agent)
        self.machine.add_transition('resolve_disambiguation', 'awaiting_disambiguation', 'agent_delegated',
                                   before=self._on_resolve_disambiguation)
        self.machine.add_transition('complete_conversation', 'awaiting_disambiguation', 'completed',
                                   before=self._on_complete_conversation)
        
        # From agent_delegated
        self.machine.add_transition('complete_conversation', 'agent_delegated', 'completed',
                                   before=self._on_complete_conversation)
        
        # Global transitions
        self.machine.add_transition('reset', '*', 'initial', before=self._on_reset)
        self.machine.add_transition('error', '*', 'error_state', before=self._on_error)
        self.machine.add_transition('timeout_session', '*', 'session_timeout', before=self._on_timeout)
    
    # Callback methods
    def _on_request_disambiguation(self):
        """Handle disambiguation request"""
        self.update_context(disambiguation_started=True)
    
    def _on_delegate_to_agent(self):
        """Handle delegation to agent"""
        self.update_context(active_agent=self.active_agent)
    
    def _on_resolve_disambiguation(self):
        """Handle disambiguation resolution"""
        self.update_context(disambiguation_resolved=True)
    
    def _on_complete_conversation(self):
        """Handle conversation completion"""
        self.update_context(status="completed")
    
    def _on_reset(self):
        """Handle reset"""
        self.clear_context()
        self.active_agent = None
        self.pending_message = None
        self.candidate_intents = []
    
    def _on_error(self):
        """Handle error state"""
        pass
    
    def _on_timeout(self):
        """Handle session timeout"""
        self.clear_context()
    
    # Session tracking methods
    def get_session_duration(self) -> float:
        """Get session duration in seconds"""
        return (datetime.now() - self.created_at).total_seconds()
    
    def track_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def export_state(self) -> Dict[str, Any]:
        """Export complete state"""
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "current_state": self.state,
            "context": self.context.copy(),
            "session_duration_seconds": self.get_session_duration(),
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "valid_transitions": list(self.get_valid_transitions_set())
        }
    
    # Pending message management
    def set_pending_message(self, message: str, intents: List[str]):
        """Set pending message and candidate intents"""
        self.pending_message = message
        self.candidate_intents = intents
        self.update_context(pending_message=message, candidate_intents=intents)
    
    def get_pending_data(self) -> tuple:
        """Get pending message and intents"""
        return self.pending_message, self.candidate_intents
    
    def clear_pending_data(self):
        """Clear pending data"""
        self.pending_message = None
        self.candidate_intents = []
        self.update_context(pending_message=None, candidate_intents=[])
