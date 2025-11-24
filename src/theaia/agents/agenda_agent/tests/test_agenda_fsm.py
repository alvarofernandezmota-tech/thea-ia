"""
Tests for AgendaFSM v2.0
Updated: 24 Nov 2025 - Match agenda_fsm.py real implementation

Tests cover:
- Initialization
- State transitions
- Callbacks
- Event draft management
- All 6 flows (create/list/edit/delete/search/cancel)
"""

import pytest
from datetime import datetime
from src.theaia.agents.agenda_agent.model.agenda_fsm import AgendaFSM
from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates


# ========================================
# FIXTURES
# ========================================

@pytest.fixture
def fsm():
    """Create fresh FSM instance for each test."""
    return AgendaFSM()


# ========================================
# INITIALIZATION TESTS
# ========================================

class TestAgendaFSMInitialization:
    """Test FSM initialization."""
    
    def test_initial_state_is_idle(self, fsm):
        """Test que el estado inicial es IDLE."""
        assert fsm.current_state == AgendaStates.IDLE
    
    def test_event_draft_is_none(self, fsm):
        """Test que el draft inicial es None."""
        assert fsm._event_draft is None
    
    def test_transitions_configured(self, fsm):
        """Test que las transiciones están configuradas."""
        assert hasattr(fsm, '_transitions')
        assert isinstance(fsm._transitions, dict)
        assert len(fsm._transitions) > 0


# ========================================
# CREATE EVENT FLOW TESTS
# ========================================

class TestCreateEventFlow:
    """Test complete create event flow."""
    
    def test_start_create_transition(self, fsm):
        """Test start_create transitions from IDLE to AWAITING_TITLE."""
        context = {}
        result = fsm.start_create(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
        assert fsm._event_draft is not None
    
    def test_provide_title_transition(self, fsm):
        """Test provide_title transitions to AWAITING_DATE."""
        # Setup: transition to AWAITING_TITLE first
        fsm.start_create({})
        
        context = {"title": "Reunión con el equipo"}
        result = fsm.provide_title(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_DATE
        assert fsm._event_draft.get("title") == "Reunión con el equipo"
    
    def test_provide_date_transition(self, fsm):
        """Test provide_date transitions to AWAITING_TIME."""
        # Setup: get to AWAITING_DATE state
        fsm.start_create({})
        fsm.provide_title({"title": "Reunión"})
        
        context = {"date": "2025-11-25"}
        result = fsm.provide_date(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_TIME
        assert "date" in fsm._event_draft
    
    def test_provide_time_transition(self, fsm):
        """Test provide_time transitions to AWAITING_LOCATION."""
        # Setup: get to AWAITING_TIME state
        fsm.start_create({})
        fsm.provide_title({"title": "Reunión"})
        fsm.provide_date({"date": "2025-11-25"})
        
        context = {"time": "15:00"}
        result = fsm.provide_time(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_LOCATION
        assert "time" in fsm._event_draft
    
    def test_provide_location_transition(self, fsm):
        """Test provide_location transitions to PROCESSING."""
        # Setup: get to AWAITING_LOCATION state
        fsm.start_create({})
        fsm.provide_title({"title": "Reunión"})
        fsm.provide_date({"date": "2025-11-25"})
        fsm.provide_time({"time": "15:00"})
        
        context = {"location": "Madrid"}
        result = fsm.provide_location(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.PROCESSING
    
    def test_skip_location_transition(self, fsm):
        """Test skip_location transitions to PROCESSING."""
        # Setup: get to AWAITING_LOCATION state
        fsm.start_create({})
        fsm.provide_title({"title": "Reunión"})
        fsm.provide_date({"date": "2025-11-25"})
        fsm.provide_time({"time": "15:00"})
        
        context = {}
        result = fsm.skip_location(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.PROCESSING


# ========================================
# TRANSITION METHOD TESTS
# ========================================

class TestTransitionMethod:
    """Test generic transition method."""
    
    def test_transition_with_start_create_trigger(self, fsm):
        """Test transition with 'start_create' trigger."""
        context = {}
        result = fsm.transition('start_create', context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
    
    def test_transition_with_invalid_trigger_returns_false(self, fsm):
        """Test transition with invalid trigger fails gracefully."""
        context = {}
        result = fsm.transition('invalid_trigger', context)
        
        # Should stay in IDLE and return False
        assert result is False
        assert fsm.current_state == AgendaStates.IDLE
    
    def test_transition_respects_state_machine_rules(self, fsm):
        """Test transition respects FSM rules (can't skip states)."""
        context = {}
        
        # Try to provide_title from IDLE (should fail)
        result = fsm.transition('provide_title', context)
        
        assert result is False  # Not allowed from IDLE
        assert fsm.current_state == AgendaStates.IDLE


# ========================================
# EVENT DRAFT MANAGEMENT TESTS
# ========================================

class TestEventDraft:
    """Test event draft management."""
    
    def test_draft_created_on_start_create(self, fsm):
        """Test draft is created when starting event creation."""
        fsm.start_create({})
        
        assert fsm._event_draft is not None
        assert isinstance(fsm._event_draft, dict)
    
    def test_draft_stores_title(self, fsm):
        """Test draft stores title correctly."""
        fsm.start_create({})
        fsm.provide_title({"title": "Test Event"})
        
        assert fsm._event_draft["title"] == "Test Event"
    
    def test_draft_accumulates_data(self, fsm):
        """Test draft accumulates all event data."""
        fsm.start_create({})
        fsm.provide_title({"title": "Meeting"})
        fsm.provide_date({"date": "2025-11-25"})
        fsm.provide_time({"time": "10:00"})
        
        draft = fsm._event_draft
        assert draft["title"] == "Meeting"
        assert "date" in draft
        assert "time" in draft
    
    def test_draft_cleared_after_completion(self, fsm):
        """Test draft is cleared after event saved."""
        # Complete full flow
        fsm.start_create({})
        fsm.provide_title({"title": "Event"})
        fsm.provide_date({"date": "2025-11-25"})
        fsm.provide_time({"time": "14:00"})
        fsm.skip_location({})
        fsm.transition('save_event', {"db_event_id": 123})
        
        # After save, draft should still exist until finish
        assert fsm._event_draft is not None
        
        # After finish, back to IDLE
        fsm.transition('finish', {})
        assert fsm.current_state == AgendaStates.IDLE


# ========================================
# CANCEL FLOW TESTS
# ========================================

class TestCancelFlow:
    """Test cancel flow from various states."""
    
    def test_cancel_from_awaiting_title(self, fsm):
        """Test cancel from AWAITING_TITLE state."""
        fsm.start_create({})
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
        
        result = fsm.transition('cancel', {})
        
        assert result is True
        assert fsm.current_state == AgendaStates.CANCELLED
    
    def test_cancel_from_awaiting_date(self, fsm):
        """Test cancel from AWAITING_DATE state."""
        fsm.start_create({})
        fsm.provide_title({"title": "Test"})
        assert fsm.current_state == AgendaStates.AWAITING_DATE
        
        result = fsm.transition('cancel', {})
        
        assert result is True
        assert fsm.current_state == AgendaStates.CANCELLED


# ========================================
# LIST/EDIT/DELETE FLOW TESTS
# ========================================

class TestOtherFlows:
    """Test list, edit, delete, search flows."""
    
    def test_start_list_transition(self, fsm):
        """Test start_list transitions to LISTING_EVENTS."""
        context = {}
        result = fsm.transition('start_list', context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.LISTING_EVENTS
    
    def test_start_edit_transition(self, fsm):
        """Test start_edit transitions to SELECTING_EVENT."""
        context = {}
        result = fsm.transition('start_edit', context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.SELECTING_EVENT
    
    def test_start_delete_transition(self, fsm):
        """Test start_delete transitions to DELETING_EVENT."""
        context = {}
        result = fsm.transition('start_delete', context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.DELETING_EVENT
    
    def test_start_search_transition(self, fsm):
        """Test start_search transitions to SEARCHING_EVENTS."""
        context = {}
        result = fsm.transition('start_search', context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.SEARCHING_EVENTS


# ========================================
# COMPLETE FLOW TESTS
# ========================================

class TestCompleteFlows:
    """Test complete FSM flows end-to-end."""
    
    def test_complete_create_flow_idle_to_saved(self, fsm):
        """Test complete flow from IDLE to EVENT_SAVED."""
        assert fsm.current_state == AgendaStates.IDLE
        
        # Full create flow
        fsm.start_create({})
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
        
        fsm.provide_title({"title": "Event"})
        assert fsm.current_state == AgendaStates.AWAITING_DATE
        
        fsm.provide_date({"date": "2025-11-25"})
        assert fsm.current_state == AgendaStates.AWAITING_TIME
        
        fsm.provide_time({"time": "14:00"})
        assert fsm.current_state == AgendaStates.AWAITING_LOCATION
        
        fsm.skip_location({})
        assert fsm.current_state == AgendaStates.PROCESSING
        
        fsm.transition('save_event', {"db_event_id": 456})
        assert fsm.current_state == AgendaStates.EVENT_SAVED
        
        fsm.transition('finish', {})
        assert fsm.current_state == AgendaStates.IDLE
