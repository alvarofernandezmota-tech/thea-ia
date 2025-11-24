"""
NoteFSM — Finite State Machine para NoteAgent
Pattern: AgendaFSM v2.0 adapted for notes
States: 12 estados (vs 15 AgendaAgent)
"""
from enum import Enum
from typing import Dict, Optional, Callable, Any
import logging


class NoteStates(Enum):
    """Estados del NoteFSM"""
    # Core states
    IDLE = "idle"
    
    # Creation flow
    AWAITING_NOTE_TITLE = "awaiting_note_title"
    AWAITING_NOTE_CONTENT = "awaiting_note_content"
    AWAITING_NOTE_CATEGORY = "awaiting_note_category"
    AWAITING_NOTE_TAGS = "awaiting_note_tags"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    
    # Management flows
    LISTING_NOTES = "listing_notes"
    SEARCHING_NOTES = "searching_notes"
    EDITING_NOTE = "editing_note"
    DELETING_NOTE = "deleting_note"
    
    # Pin flow
    PINNING_NOTE = "pinning_note"


class NoteFSM:
    """
    Finite State Machine para NoteAgent
    
    Features:
    - 12 estados definidos
    - Callbacks pre/post transition
    - Context JSONB persistence
    - State validation
    - Multi-turn conversation support
    
    Flows:
    1. Create: idle → awaiting_title → awaiting_content → confirmation → idle
    2. List: idle → listing → idle
    3. Search: idle → searching → idle
    4. Edit: idle → editing → awaiting_content → confirmation → idle
    5. Delete: idle → deleting → confirmation → idle
    6. Pin: idle → pinning → confirmation → idle
    
    Coverage target: ≥85%
    Pattern: AgendaFSM v2.0 adapted
    """
    
    def __init__(self):
        """Initialize FSM with idle state"""
        self.current_state = NoteStates.IDLE.value
        self.context: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{__name__}.NoteFSM")
        
        # Callbacks registry
        self._pre_transition_callbacks: Dict[str, Callable] = {}
        self._post_transition_callbacks: Dict[str, Callable] = {}
        
        # Register default callbacks
        self._register_default_callbacks()
    
    def _register_default_callbacks(self):
        """Register default pre/post transition callbacks"""
        # Pre-transition validations
        self._pre_transition_callbacks[NoteStates.AWAITING_NOTE_TITLE.value] = self._pre_transition_to_awaiting_note_title
        self._pre_transition_callbacks[NoteStates.AWAITING_NOTE_CONTENT.value] = self._pre_transition_to_awaiting_note_content
        
        # Post-transition actions
        self._post_transition_callbacks[NoteStates.AWAITING_NOTE_TITLE.value] = self._post_transition_to_awaiting_note_title
        self._post_transition_callbacks[NoteStates.AWAITING_CONFIRMATION.value] = self._post_transition_to_awaiting_confirmation
    
    def transition_to(self, new_state: str) -> bool:
        """
        Transition to new state with callbacks
        
        Args:
            new_state: Target state string
            
        Returns:
            True if transition successful, False otherwise
        """
        old_state = self.current_state
        
        # Validate state exists
        try:
            NoteStates(new_state)
        except ValueError:
            self.logger.error(f"Invalid state: {new_state}")
            return False
        
        # Pre-transition callback (validation)
        if new_state in self._pre_transition_callbacks:
            callback = self._pre_transition_callbacks[new_state]
            if not callback():
                self.logger.warning(f"Pre-transition callback failed for {new_state}")
                return False
        
        # Execute transition
        self.current_state = new_state
        self.logger.info(f"Transitioned: {old_state} → {new_state}")
        
        # Post-transition callback (side effects)
        if new_state in self._post_transition_callbacks:
            callback = self._post_transition_callbacks[new_state]
            callback(old_state)
        
        return True
    
    def reset(self):
        """Reset FSM to idle state and clear context"""
        self.current_state = NoteStates.IDLE.value
        self.context = {}
        self.logger.info("FSM reset to idle")
    
    def update_context(self, key: str, value: Any):
        """
        Update context value
        
        Args:
            key: Context key
            value: Context value
        """
        self.context[key] = value
        self.logger.debug(f"Context updated: {key} = {value}")
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Get context value
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value or default
        """
        return self.context.get(key, default)
    
    # ==========================================
    # PRE-TRANSITION CALLBACKS (Validation)
    # ==========================================
    
    def _pre_transition_to_awaiting_note_title(self) -> bool:
        """Validate before transitioning to awaiting_note_title"""
        # Always allow starting note creation
        return True
    
    def _pre_transition_to_awaiting_note_content(self) -> bool:
        """Validate before transitioning to awaiting_note_content"""
        # Should have title in context
        if "title" not in self.context:
            self.logger.warning("No title in context for awaiting_note_content")
            return False
        return True
    
    # ==========================================
    # POST-TRANSITION CALLBACKS (Side effects)
    # ==========================================
    
    def _post_transition_to_awaiting_note_title(self, old_state: str):
        """Actions after transitioning to awaiting_note_title"""
        self.logger.info(f"Started note creation flow from {old_state}")
        # Initialize context for new note
        self.context = {
            "creation_started": True
        }
    
    def _post_transition_to_awaiting_confirmation(self, old_state: str):
        """Actions after transitioning to awaiting_confirmation"""
        self.logger.info(f"Note ready for confirmation from {old_state}")
        # Validate required fields
        required_fields = ["title", "content"]
        for field in required_fields:
            if field not in self.context:
                self.logger.warning(f"Missing required field: {field}")
    
    # ==========================================
    # STATE QUERY METHODS
    # ==========================================
    
    def is_idle(self) -> bool:
        """Check if FSM is in idle state"""
        return self.current_state == NoteStates.IDLE.value
    
    def is_in_creation_flow(self) -> bool:
        """Check if FSM is in note creation flow"""
        creation_states = [
            NoteStates.AWAITING_NOTE_TITLE.value,
            NoteStates.AWAITING_NOTE_CONTENT.value,
            NoteStates.AWAITING_NOTE_CATEGORY.value,
            NoteStates.AWAITING_NOTE_TAGS.value,
            NoteStates.AWAITING_CONFIRMATION.value
        ]
        return self.current_state in creation_states
    
    def is_in_management_flow(self) -> bool:
        """Check if FSM is in note management flow"""
        management_states = [
            NoteStates.LISTING_NOTES.value,
            NoteStates.SEARCHING_NOTES.value,
            NoteStates.EDITING_NOTE.value,
            NoteStates.DELETING_NOTE.value,
            NoteStates.PINNING_NOTE.value
        ]
        return self.current_state in management_states
    
    def get_state_name(self) -> str:
        """Get current state name (enum value)"""
        return self.current_state
    
    def get_context_summary(self) -> Dict:
        """
        Get summary of current context (for debugging)
        
        Returns:
            Dict with context summary
        """
        return {
            "state": self.current_state,
            "context_keys": list(self.context.keys()),
            "has_title": "title" in self.context,
            "has_content": "content" in self.context,
            "has_category": "category" in self.context,
            "has_tags": "tags" in self.context
        }
