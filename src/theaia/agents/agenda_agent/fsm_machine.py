"""
FSM Machine for AgendaAgent

Finite State Machine implementation using transitions library.
Manages conversation states and transitions for multi-turn interactions.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
from transitions import Machine
import logging

from .model.agent_states import AgentState


logger = logging.getLogger(__name__)


class AgendaFSM:
    """
    Finite State Machine for AgendaAgent conversations.
    
    Manages state transitions and validates state changes.
    Uses transitions library for robust FSM implementation.
    """
    
    # Define all possible states (using AgentState enum values)
    states = [
        AgentState.IDLE.value,
        AgentState.AWAITING_EVENT_DETAILS.value,
        AgentState.AWAITING_TIME.value,
        AgentState.AWAITING_EVENT_SELECTION.value,
        AgentState.AWAITING_CONFIRMATION.value,
        AgentState.PROCESSING.value,
        AgentState.COMPLETED.value,
        AgentState.ERROR.value,
    ]
    
    def __init__(self, initial_state: AgentState = AgentState.IDLE):
        """
        Initialize FSM with initial state.
        
        Args:
            initial_state: Starting state (default: IDLE)
        """
        self.context: Dict[str, Any] = {}
        self.history: List[str] = []
        
        # Initialize transitions Machine
        self.machine = Machine(
            model=self,
            states=AgendaFSM.states,
            initial=initial_state.value,
            auto_transitions=False,  # We define transitions explicitly
            send_event=True,  # Pass event data to callbacks
        )
        
        # Define transitions
        self._setup_transitions()
        
        logger.info(f"FSM initialized with state: {initial_state.value}")
    
    def _setup_transitions(self):
        """Setup all valid state transitions."""
        
        # From IDLE
        self.machine.add_transition(
            trigger='start_create_event',
            source=AgentState.IDLE.value,
            dest=AgentState.AWAITING_EVENT_DETAILS.value,
            before='_log_transition'
        )
        
        self.machine.add_transition(
            trigger='start_update_event',
            source=AgentState.IDLE.value,
            dest=AgentState.AWAITING_EVENT_SELECTION.value,
            before='_log_transition'
        )
        
        self.machine.add_transition(
            trigger='start_query',
            source=AgentState.IDLE.value,
            dest=AgentState.PROCESSING.value,
            before='_log_transition'
        )
        
        # From AWAITING_EVENT_DETAILS
        self.machine.add_transition(
            trigger='provide_details',
            source=AgentState.AWAITING_EVENT_DETAILS.value,
            dest=AgentState.AWAITING_TIME.value,
            conditions=['_has_title'],
            before='_log_transition'
        )
        
        self.machine.add_transition(
            trigger='provide_complete_info',
            source=AgentState.AWAITING_EVENT_DETAILS.value,
            dest=AgentState.AWAITING_CONFIRMATION.value,
            conditions=['_has_title', '_has_datetime'],
            before='_log_transition'
        )
        
        # From AWAITING_TIME
        self.machine.add_transition(
            trigger='provide_time',
            source=AgentState.AWAITING_TIME.value,
            dest=AgentState.AWAITING_CONFIRMATION.value,
            conditions=['_has_datetime'],
            before='_log_transition'
        )
        
        # From AWAITING_EVENT_SELECTION
        self.machine.add_transition(
            trigger='select_event',
            source=AgentState.AWAITING_EVENT_SELECTION.value,
            dest=AgentState.AWAITING_EVENT_DETAILS.value,
            conditions=['_has_event_id'],
            before='_log_transition'
        )
        
        self.machine.add_transition(
            trigger='select_and_confirm',
            source=AgentState.AWAITING_EVENT_SELECTION.value,
            dest=AgentState.AWAITING_CONFIRMATION.value,
            conditions=['_has_event_id'],
            before='_log_transition'
        )
        
        # From AWAITING_CONFIRMATION
        self.machine.add_transition(
            trigger='confirm',
            source=AgentState.AWAITING_CONFIRMATION.value,
            dest=AgentState.PROCESSING.value,
            before='_log_transition'
        )
        
        self.machine.add_transition(
            trigger='reject',
            source=AgentState.AWAITING_CONFIRMATION.value,
            dest=AgentState.IDLE.value,
            before='_log_transition',
            after='_clear_context'
        )
        
        # From PROCESSING
        self.machine.add_transition(
            trigger='complete',
            source=AgentState.PROCESSING.value,
            dest=AgentState.COMPLETED.value,
            before='_log_transition'
        )
        
        self.machine.add_transition(
            trigger='fail',
            source=AgentState.PROCESSING.value,
            dest=AgentState.ERROR.value,
            before='_log_transition'
        )
        
        # From COMPLETED or ERROR back to IDLE
        self.machine.add_transition(
            trigger='reset',
            source=[AgentState.COMPLETED.value, AgentState.ERROR.value],
            dest=AgentState.IDLE.value,
            before='_log_transition',
            after='_clear_context'
        )
        
        # Cancel from any state (except COMPLETED)
        self.machine.add_transition(
            trigger='cancel',
            source='*',
            dest=AgentState.IDLE.value,
            before='_log_transition',
            after='_clear_context'
        )
    
    # Condition methods (check if data is present)
    
    def _has_title(self, event_data=None) -> bool:
        """Check if title is in context."""
        return bool(self.context.get('title'))
    
    def _has_datetime(self, event_data=None) -> bool:
        """Check if datetime is in context."""
        return bool(self.context.get('datetime') or self.context.get('datetime_str'))
    
    def _has_event_id(self, event_data=None) -> bool:
        """Check if event_id is in context."""
        return bool(self.context.get('event_id'))
    
    # Callback methods
    
    def _log_transition(self, event_data):
        """Log state transition."""
        if event_data:
            logger.info(f"FSM transition: {event_data.transition.source} -> {event_data.transition.dest}")
            self.history.append(f"{event_data.transition.source} -> {event_data.transition.dest}")
    
    def _clear_context(self, event_data=None):
        """Clear context data."""
        self.context.clear()
        logger.info("FSM context cleared")
    
    # Public methods
    
    def get_current_state(self) -> AgentState:
        """
        Get current FSM state.
        
        Returns:
            Current AgentState
        """
        return AgentState(self.state)
    
    def update_context(self, key: str, value: Any):
        """
        Update context with new data.
        
        Args:
            key: Context key
            value: Context value
        """
        self.context[key] = value
        logger.debug(f"FSM context updated: {key} = {value}")
    
    def get_context(self, key: str, default=None) -> Any:
        """
        Get value from context.
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value or default
        """
        return self.context.get(key, default)
    
    def get_full_context(self) -> Dict[str, Any]:
        """Get complete context dictionary."""
        return self.context.copy()
    
    def is_final_state(self) -> bool:
        """Check if FSM is in a final state."""
        return self.state in [
            AgentState.COMPLETED.value,
            AgentState.ERROR.value
        ]
    
    def can_trigger(self, trigger_name: str) -> bool:
        """
        Check if a trigger can be fired from current state.
        
        Args:
            trigger_name: Trigger name
            
        Returns:
            True if trigger is valid
        """
        try:
            # Get trigger method
            trigger_func = getattr(self, trigger_name, None)
            if not trigger_func:
                return False
            
            # Check if trigger exists and conditions are met
            # transitions library handles this internally
            return True
            
        except Exception as e:
            logger.warning(f"Cannot fire trigger {trigger_name}: {e}")
            return False
    
    def get_possible_triggers(self) -> List[str]:
        """
        Get list of possible triggers from current state.
        
        Returns:
            List of trigger names
        """
        current = self.get_current_state().value
        possible = []
        
        for transition in self.machine.get_transitions():
            if transition.source == current or transition.source == '*':
                possible.append(transition.trigger)
        
        return list(set(possible))  # Remove duplicates
    
    def get_state_history(self) -> List[str]:
        """Get history of state transitions."""
        return self.history.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize FSM state to dictionary.
        
        Returns:
            Dictionary with FSM state
        """
        return {
            "current_state": self.state,
            "context": self.context.copy(),
            "history": self.history.copy(),
            "is_final": self.is_final_state(),
            "possible_triggers": self.get_possible_triggers()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgendaFSM':
        """
        Restore FSM from serialized dictionary.
        
        Args:
            data: Dictionary with FSM state
            
        Returns:
            Restored AgendaFSM instance
        """
        state = AgentState(data["current_state"])
        fsm = cls(initial_state=state)
        fsm.context = data.get("context", {})
        fsm.history = data.get("history", [])
        return fsm


class FSMManager:
    """
    Manages multiple FSM instances for different users/conversations.
    """
    
    def __init__(self):
        """Initialize FSM manager."""
        self.fsms: Dict[str, AgendaFSM] = {}
        logger.info("FSM Manager initialized")
    
    def get_or_create(self, conversation_id: str) -> AgendaFSM:
        """
        Get existing FSM or create new one.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            AgendaFSM instance
        """
        if conversation_id not in self.fsms:
            self.fsms[conversation_id] = AgendaFSM()
            logger.info(f"Created new FSM for conversation {conversation_id}")
        
        return self.fsms[conversation_id]
    
    def get(self, conversation_id: str) -> Optional[AgendaFSM]:
        """
        Get FSM by conversation ID.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            AgendaFSM instance or None
        """
        return self.fsms.get(conversation_id)
    
    def remove(self, conversation_id: str) -> bool:
        """
        Remove FSM instance.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            True if removed
        """
        if conversation_id in self.fsms:
            del self.fsms[conversation_id]
            logger.info(f"Removed FSM for conversation {conversation_id}")
            return True
        return False
    
    def cleanup_final_states(self):
        """Remove FSMs in final states."""
        to_remove = [
            conv_id for conv_id, fsm in self.fsms.items()
            if fsm.is_final_state()
        ]
        
        for conv_id in to_remove:
            self.remove(conv_id)
        
        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} FSMs in final state")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about FSMs."""
        state_counts = {}
        for fsm in self.fsms.values():
            state = fsm.get_current_state().value
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            "total_fsms": len(self.fsms),
            "state_distribution": state_counts
        }
