"""
EventAgent FSM State Machine Implementation
H03 FASE 1 - BLOQUE 1.4 - Core State Machine Architecture

This module provides the base state machine and conversation-specific
state machine implementations for managing event agent workflows.

Features:
    - Abstract base class for extensible state machine architectures
    - Conversation-specific implementation with multi-agent support
    - Context management for user-specific data storage
    - Session tracking and activity monitoring
    - Robust error handling and validation

Classes:
    - BaseStateMachine: Abstract base class for all state machines
    - ConversationStateMachine: Concrete implementation for conversation flow

Version: 1.1.0
Last Updated: 09-Dec-2025
Status: Production Ready - THEA IA Compatible

Changes (09-Dec-2025 FINAL v1.1.0):
    - FIX: get_valid_transitions_set() uses machine.events (correct API)
    - FIX: Removed invalid machine.triggers reference
    - FIX: All transitions properly configured in _setup_transitions()
    - COMPATIBILITY: Fully tested with transitions library
    - INTEGRATION: Designed for THEA IA ecosystem
    - Implemented merge_context() with strategy pattern
    - Added comprehensive docstrings and examples
    - Added logging throughout for debugging
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple, Set
from transitions import Machine
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class BaseStateMachine(ABC):
    """
    Abstract base class for all state machines.
    
    Provides core state machine functionality with support for:
    - State validation and transition management
    - Context management (user-specific data storage)
    - State information retrieval
    - Comprehensive logging and debugging
    
    This class is designed to be extended by specific implementations
    (e.g., ConversationStateMachine) to define custom states and transitions.
    
    Attributes:
        VALID_STATES: List of valid states for this machine
        INITIAL_STATE: Starting state when machine is created
        user_id: ID of the user this machine belongs to
        state: Current state of the machine
        context: Dictionary for storing user-specific context
        machine: transitions.Machine instance managing state transitions
    """
    
    VALID_STATES = []
    INITIAL_STATE = "initial"
    
    def __init__(self, user_id: str):
        """
        Initialize the base state machine.
        
        Args:
            user_id: Unique identifier for the user
            
        Raises:
            ValueError: If user_id is empty or None
            
        Example:
            >>> class SimpleStateMachine(BaseStateMachine):
            ...     VALID_STATES = ["initial", "running", "stopped"]
            ...     INITIAL_STATE = "initial"
            
            >>> machine = SimpleStateMachine(user_id="user123")
            >>> machine.state
            'initial'
            >>> machine.user_id
            'user123'
        """
        if not user_id:
            raise ValueError("user_id cannot be empty or None")
        
        self.user_id = user_id
        self.state = self.INITIAL_STATE
        self.context = {}
        self.machine = None
        self._setup_machine()
        
        logger.debug(f"BaseStateMachine initialized: user_id={user_id}, state={self.state}")
    
    def _setup_machine(self):
        """
        Setup the transitions machine.
        
        Creates a transitions.Machine instance with the defined states
        and initial state. Subclasses override this to add transitions.
        
        The machine is configured with:
        - auto_transitions=False (manual transition control)
        - model=self (state and transitions attached to this instance)
        """
        self.machine = Machine(
            model=self,
            states=self.VALID_STATES,
            initial=self.INITIAL_STATE,
            auto_transitions=False
        )
        logger.debug(f"State machine setup complete: states={len(self.VALID_STATES)}, initial={self.INITIAL_STATE}")
    
    def validate_state(self, state: str) -> bool:
        """
        Validate if a state is valid for this machine.
        
        Args:
            state: State name to validate
            
        Returns:
            True if state is valid, False otherwise
            
        Example:
            >>> machine.validate_state("initial")
            True
            >>> machine.validate_state("invalid_state")
            False
        """
        is_valid = state in self.VALID_STATES
        if not is_valid:
            logger.warning(f"Invalid state '{state}'. Valid states: {self.VALID_STATES}")
        return is_valid
    
    def get_valid_transitions_set(self) -> Set[str]:
        """
        Get set of valid transitions from current state.
        
        FIX FINAL v1.1.0 (09-Dec-2025): 
        - Uses machine.events dict (correct transitions API)
        - Iterates through available events/triggers
        - Uses may_<trigger>() methods to validate from current state
        - Compatible with transitions library internal structure
        
        Returns:
            Set of trigger names that can be called from current state
            
        Example:
            >>> transitions = machine.get_valid_transitions_set()
            >>> 'delegate_to_agent' in transitions
            True
            >>> len(transitions) >= 1
            True
        """
        valid_transitions = set()
        
        try:
            # Access transitions from machine.events (correct API)
            if hasattr(self.machine, 'events') and self.machine.events:
                for trigger_name in self.machine.events.keys():
                    # Skip internal triggers
                    if trigger_name.startswith('_'):
                        continue
                    
                    # Use may_<trigger> method to check if transition is valid
                    may_method_name = f'may_{trigger_name}'
                    if hasattr(self, may_method_name):
                        may_method = getattr(self, may_method_name)
                        if callable(may_method):
                            try:
                                if may_method():
                                    valid_transitions.add(trigger_name)
                            except Exception as e:
                                logger.debug(f"Error checking trigger '{trigger_name}': {e}")
            else:
                logger.warning("Machine does not have 'events' attribute or events is empty")
        except Exception as e:
            logger.error(f"Error getting valid transitions from state '{self.state}': {e}")
        
        logger.debug(f"Valid transitions for state '{self.state}': {valid_transitions}")
        return valid_transitions
    
    def can_transition_to(self, trigger: str) -> bool:
        """
        Check if a transition is possible from current state.
        
        Args:
            trigger: Transition trigger name
            
        Returns:
            True if transition is possible, False otherwise
            
        Example:
            >>> if machine.can_transition_to('delegate_to_agent'):
            ...     machine.transition_safe('delegate_to_agent')
            ... else:
            ...     print("Transition not allowed")
        """
        can_transition = trigger in self.get_valid_transitions_set()
        if not can_transition:
            logger.debug(f"Transition '{trigger}' not allowed from state '{self.state}'")
        return can_transition
    
    def transition_safe(self, trigger: str) -> bool:
        """
        Safely transition using a trigger with validation.
        
        Args:
            trigger: Transition trigger name
            
        Returns:
            True if transition succeeded
            
        Raises:
            Exception: If transition is not allowed from current state
            
        Example:
            >>> try:
            ...     machine.transition_safe('delegate_to_agent')
            ... except Exception as e:
            ...     print(f"Transition failed: {e}")
        """
        if not self.can_transition_to(trigger):
            valid = self.get_valid_transitions_set()
            error_msg = (
                f"Transition '{trigger}' not allowed from state '{self.state}'. "
                f"Valid transitions: {valid}"
            )
            logger.error(error_msg)
            raise Exception(error_msg)
        
        try:
            getattr(self, trigger)()
            logger.info(f"Transition executed: {trigger} ({self.state})")
            return True
        except Exception as e:
            logger.error(f"Error executing transition '{trigger}': {e}")
            raise
    
    def get_state_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about current state.
        
        Returns:
            Dictionary containing:
            - current_state: Current state name
            - valid_transitions: List of available transitions
            - context: Copy of current context
            - timestamp: ISO format timestamp of call
            
        Example:
            >>> info = machine.get_state_info()
            >>> info['current_state']
            'initial'
            >>> info['valid_transitions']
            ['request_disambiguation', 'delegate_to_agent']
            >>> 'timestamp' in info
            True
        """
        return {
            "current_state": self.state,
            "valid_transitions": list(self.get_valid_transitions_set()),
            "context": self.context.copy(),
            "timestamp": datetime.now().isoformat()
        }
    
    def update_context(self, **kwargs):
        """
        Update context with new values.
        
        Merges new key-value pairs into the context dictionary without
        removing existing values.
        
        Args:
            **kwargs: Key-value pairs to add/update in context
            
        Example:
            >>> machine.update_context(agent_name="AgendaAgent", priority="high")
            >>> machine.context['agent_name']
            'AgendaAgent'
            >>> machine.context['priority']
            'high'
        """
        if not kwargs:
            logger.debug("update_context called with no arguments")
            return
        
        self.context.update(kwargs)
        logger.debug(f"Context updated: keys={list(kwargs.keys())}, total_keys={len(self.context)}")
    
    def get_context(self, key: str = None, default: Any = None) -> Any:
        """
        Get context value by key or all context.
        
        Args:
            key: Optional key to retrieve. If None, returns all context
            default: Default value if key not found
            
        Returns:
            Context value for key or full context dictionary
            
        Example:
            >>> machine.update_context(agent="AgendaAgent", data="test")
            
            >>> machine.get_context("agent")
            'AgendaAgent'
            
            >>> machine.get_context("missing_key", default="N/A")
            'N/A'
            
            >>> context = machine.get_context()
            >>> type(context)
            <class 'dict'>
        """
        if key is None:
            logger.debug(f"Retrieved full context: {len(self.context)} keys")
            return self.context.copy()
        
        value = self.context.get(key, default)
        logger.debug(f"Retrieved context['{key}'] = {value}")
        return value
    
    def clear_context(self):
        """
        Clear all context data.
        
        Useful for resetting state machines or clearing sensitive data.
        Does not affect session_id if present (see ConversationStateMachine).
        
        Example:
            >>> machine.update_context(agent="AgendaAgent", data="test")
            >>> machine.clear_context()
            >>> machine.context
            {}
        """
        self.context.clear()
        logger.debug(f"Context cleared for user {self.user_id}")


class ConversationStateMachine(BaseStateMachine):
    """
    State machine for managing conversation flow with event agents.
    
    Manages conversation states, transitions, and context through multi-agent
    orchestration. Supports disambiguation, agent delegation, and session timeout.
    
    This implementation is part of the THEA IA ecosystem and integrates with:
    - AgendaAgent (event management)
    - NLPEngine (intent detection)
    - Orchestrator (multi-agent coordination)
    
    States:
        - initial: Starting state, no agent active
        - awaiting_disambiguation: Waiting for user to clarify intent
        - agent_delegated: Processing with specific agent
        - completed: Conversation finished successfully
        - error_state: Error occurred during conversation
        - session_timeout: Session timed out
    
    Valid Transitions:
        From initial:
            - request_disambiguation -> awaiting_disambiguation
            - delegate_to_agent -> agent_delegated
        
        From awaiting_disambiguation:
            - delegate_to_agent -> agent_delegated
            - resolve_disambiguation -> agent_delegated
            - complete_conversation -> completed
        
        From agent_delegated:
            - complete_conversation -> completed
        
        Global (from any state):
            - reset -> initial
            - error -> error_state
            - timeout_session -> session_timeout
        
    Attributes:
        session_id: Unique session identifier (UUID or provided)
        created_at: Timestamp when session started
        last_activity: Timestamp of last activity (for timeout tracking)
        active_agent: Name/ID of currently active agent
        pending_message: Message awaiting processing (for disambiguation)
        candidate_intents: List of candidate intents for disambiguation
    """
    
    VALID_STATES = [
        'initial',
        'awaiting_disambiguation',
        'agent_delegated',
        'completed',
        'error_state',
        'session_timeout'
    ]
    INITIAL_STATE = 'initial'
    
    def __init__(self, user_id: str, session_id: str = None):
        """
        Initialize conversation state machine.
        
        Creates a new conversation session with unique identifier and
        initializes all tracking attributes.
        
        Args:
            user_id: Unique user identifier (required)
            session_id: Optional session identifier. If not provided, generates UUID.
            
        Raises:
            ValueError: If user_id is empty or None
            
        Example:
            >>> conv = ConversationStateMachine(user_id="user123")
            >>> len(conv.session_id)
            36
            
            >>> conv = ConversationStateMachine(
            ...     user_id="user123",
            ...     session_id="custom_session_456"
            ... )
            >>> conv.session_id
            'custom_session_456'
        """
        # DON'T call super().__init__ yet - we need to setup transitions first
        if not user_id:
            raise ValueError("user_id cannot be empty or None")
        
        self.user_id = user_id
        self.state = self.INITIAL_STATE
        self.context = {}
        self.machine = None
        
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.active_agent = None
        self.pending_message = None
        self.candidate_intents = []
        
        # NOW setup the machine with transitions
        self._setup_transitions()
        
        self.update_context(session_id=self.session_id)
        
        logger.info(
            f"ConversationStateMachine created: "
            f"user_id={user_id}, session_id={self.session_id}"
        )
    
    def _setup_transitions(self):
        """
        Setup state machine transitions with callbacks.
        
        Defines all valid transitions between states and their before-callbacks.
        Each transition can have a 'before' callback that executes before the transition
        is applied, allowing for state validation and side effects.
        
        Transitions are organized by source state for clarity.
        
        CRITICAL: This method configures ALL 9 transitions for THEA IA:
        - 2 from initial state
        - 3 from awaiting_disambiguation state
        - 1 from agent_delegated state
        - 3 global transitions (from any state)
        """
        # Create the machine
        self.machine = Machine(
            model=self,
            states=self.VALID_STATES,
            initial=self.INITIAL_STATE,
            auto_transitions=False
        )
        
        logger.debug("Setting up ConversationStateMachine transitions...")
        
        # From initial state
        self.machine.add_transition(
            'request_disambiguation',
            'initial',
            'awaiting_disambiguation',
            before=self._on_request_disambiguation
        )
        self.machine.add_transition(
            'delegate_to_agent',
            'initial',
            'agent_delegated',
            before=self._on_delegate_to_agent
        )
        
        # From awaiting_disambiguation
        self.machine.add_transition(
            'delegate_to_agent',
            'awaiting_disambiguation',
            'agent_delegated',
            before=self._on_delegate_to_agent
        )
        self.machine.add_transition(
            'resolve_disambiguation',
            'awaiting_disambiguation',
            'agent_delegated',
            before=self._on_resolve_disambiguation
        )
        self.machine.add_transition(
            'complete_conversation',
            'awaiting_disambiguation',
            'completed',
            before=self._on_complete_conversation
        )
        
        # From agent_delegated
        self.machine.add_transition(
            'complete_conversation',
            'agent_delegated',
            'completed',
            before=self._on_complete_conversation
        )
        
        # Global transitions (from any state)
        self.machine.add_transition(
            'reset',
            '*',
            'initial',
            before=self._on_reset
        )
        self.machine.add_transition(
            'error',
            '*',
            'error_state',
            before=self._on_error
        )
        self.machine.add_transition(
            'timeout_session',
            '*',
            'session_timeout',
            before=self._on_timeout
        )
        
        logger.debug("Transitions configured: 9 transitions added successfully")
        logger.debug(f"Available events: {list(self.machine.events.keys())}")
    
    def _on_request_disambiguation(self):
        """Callback: Handle disambiguation request."""
        self.update_context(disambiguation_started=True)
        self.track_activity()
        logger.debug(
            f"Disambiguation requested: user_id={self.user_id}, "
            f"pending_message={self.pending_message}"
        )
    
    def _on_delegate_to_agent(self):
        """Callback: Handle delegation to agent."""
        self.update_context(active_agent=self.active_agent)
        self.track_activity()
        logger.debug(
            f"Agent delegated: user_id={self.user_id}, "
            f"agent={self.active_agent}, session={self.session_id}"
        )
    
    def _on_resolve_disambiguation(self):
        """Callback: Handle disambiguation resolution."""
        self.update_context(disambiguation_resolved=True)
        self.track_activity()
        logger.debug(
            f"Disambiguation resolved: user_id={self.user_id}, "
            f"selected_agent={self.active_agent}"
        )
    
    def _on_complete_conversation(self):
        """Callback: Handle conversation completion."""
        self.update_context(status="completed")
        self.track_activity()
        duration = self.get_session_duration()
        logger.info(
            f"Conversation completed: user_id={self.user_id}, "
            f"session={self.session_id}, duration_sec={duration:.2f}"
        )
    
    def _on_reset(self):
        """Callback: Handle state machine reset."""
        self.clear_context()
        self.active_agent = None
        self.pending_message = None
        self.candidate_intents = []
        self.update_context(session_id=self.session_id)
        logger.debug(f"State machine reset: user_id={self.user_id}, session={self.session_id}")
    
    def _on_error(self):
        """Callback: Handle error state transition."""
        self.track_activity()
        logger.warning(
            f"Error state entered: user_id={self.user_id}, "
            f"session={self.session_id}, last_state={self.state}"
        )
    
    def _on_timeout(self):
        """Callback: Handle session timeout."""
        self.clear_context()
        self.update_context(session_id=self.session_id)
        logger.warning(
            f"Session timeout: user_id={self.user_id}, "
            f"session={self.session_id}, "
            f"duration_sec={self.get_session_duration():.2f}"
        )
    
    def get_session_duration(self) -> float:
        """Get session duration in seconds."""
        duration = (datetime.now() - self.created_at).total_seconds()
        logger.debug(f"Session duration: {duration:.2f} seconds")
        return duration
    
    def track_activity(self):
        """Update last activity timestamp to current time."""
        self.last_activity = datetime.now()
        logger.debug(f"Activity tracked: {self.last_activity.isoformat()}")
    
    def is_inactive(self, timeout_seconds: int = 300) -> bool:
        """Check if session has been inactive for longer than timeout."""
        inactivity = (datetime.now() - self.last_activity).total_seconds()
        is_inactive = inactivity > timeout_seconds
        if is_inactive:
            logger.warning(f"Session inactive for {inactivity:.2f}s (threshold: {timeout_seconds}s)")
        return is_inactive
    
    def export_state(self) -> Dict[str, Any]:
        """Export complete state of conversation machine."""
        exported = {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "current_state": self.state,
            "context": self.context.copy(),
            "session_duration_seconds": self.get_session_duration(),
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "valid_transitions": list(self.get_valid_transitions_set())
        }
        logger.debug(f"State exported: {self.state} with {len(exported)} fields")
        return exported
    
    def merge_context(self, new_context: dict, strategy: str = "merge") -> dict:
        """
        Merge new context with existing context.
        
        Provides flexible context merging with two strategies:
        - "merge": Update existing context (preserves current data)
        - "replace": Clear and set new context (complete reset)
        
        Args:
            new_context: Dictionary with new context data
            strategy: Merge strategy ("merge" or "replace")
            
        Returns:
            Updated context dictionary
            
        Raises:
            TypeError: If new_context is not a dict
            ValueError: If strategy is invalid
        """
        if not isinstance(new_context, dict):
            raise TypeError(f"new_context must be dict, got {type(new_context)}")
        
        if strategy == "merge":
            self.context.update(new_context)
            logger.debug(
                f"Context merged (strategy=merge): "
                f"keys={list(new_context.keys())}, total={len(self.context)}"
            )
            return self.context.copy()
        
        elif strategy == "replace":
            old_keys = list(self.context.keys())
            self.context.clear()
            self.context.update(new_context)
            logger.debug(
                f"Context replaced (strategy=replace): "
                f"removed={old_keys}, added={list(new_context.keys())}"
            )
            return self.context.copy()
        
        else:
            raise ValueError(
                f"Unknown merge strategy: '{strategy}'. "
                f"Must be 'merge' or 'replace'"
            )
    
    def set_pending_message(self, message: str, intents: List[str]):
        """Set pending message and candidate intents for disambiguation."""
        if not message or not isinstance(message, str):
            raise ValueError("message must be non-empty string")
        if not isinstance(intents, list):
            raise ValueError("intents must be a list")
        if not intents:
            raise ValueError("intents list cannot be empty")
        
        self.pending_message = message
        self.candidate_intents = intents.copy()
        self.update_context(
            pending_message=message,
            candidate_intents=self.candidate_intents
        )
        logger.debug(
            f"Pending message set: message='{message}', "
            f"intents={intents}, count={len(intents)}"
        )
    
    def get_pending_data(self) -> Tuple[Optional[str], List[str]]:
        """Get pending message and candidate intents."""
        logger.debug(
            f"Retrieved pending data: message={self.pending_message}, "
            f"intents_count={len(self.candidate_intents)}"
        )
        return self.pending_message, self.candidate_intents.copy()
    
    def clear_pending_data(self):
        """Clear pending message and candidate intents."""
        self.pending_message = None
        self.candidate_intents = []
        self.update_context(
            pending_message=None,
            candidate_intents=[]
        )
        logger.debug("Pending message data cleared")


if __name__ == "__main__":
    # Demo usage
    machine = ConversationStateMachine(
        user_id="user_001",
        session_id="session_001"
    )
    
    print(f"Initial state: {machine.state}")
    print(f"Valid transitions: {machine.get_valid_transitions_set()}")
    
    machine.pending_message = "Create event"
    machine.candidate_intents = ["create_event", "search_events"]
    machine.request_disambiguation()
    
    print(f"\nAfter disambiguation request: {machine.state}")
    print(f"Valid transitions: {machine.get_valid_transitions_set()}")
    
    machine.active_agent = "AgendaAgent"
    machine.resolve_disambiguation()
    
    print(f"\nAfter delegation: {machine.state}")
    
    machine.complete_conversation()
    
    print(f"\nFinal state: {machine.state}")
    print(f"\nExported state:\n{machine.export_state()}")
