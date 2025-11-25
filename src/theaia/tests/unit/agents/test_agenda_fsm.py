"""
Unit tests for AgendaFSM v2.0
Tests state machine transitions, callbacks, and validation
"""

import pytest
from datetime import datetime
from src.theaia.agents.agenda_agent.model.agenda_fsm import AgendaFSM
from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates


class TestAgendaFSMBasics:
    """Test basic FSM initialization and state"""
    
    def test_fsm_initialization(self):
        """Test FSM starts in IDLE state"""
        fsm = AgendaFSM()
        assert fsm.current_state == AgendaStates.IDLE
        assert fsm._event_draft is None
    
    def test_fsm_has_transitions(self):
        """Test FSM has configured transitions"""
        fsm = AgendaFSM()
        assert len(fsm._transitions) > 0
        assert AgendaStates.IDLE in fsm._transitions
    
    def test_fsm_has_callbacks(self):
        """Test FSM has configured callbacks"""
        fsm = AgendaFSM()
        assert len(fsm._callbacks_pre) > 0
        assert len(fsm._callbacks_post) > 0


class TestAgendaFSMCreateFlow:
    """Test complete create event flow"""
    
    @pytest.fixture
    def fsm(self):
        return AgendaFSM()
    
    @pytest.fixture
    def context(self):
        return {
            'user_id': 'test_user',
            'tenant_id': 'test_tenant'
        }
    
    def test_start_create_success(self, fsm, context):
        """Test starting create flow"""
        result = fsm.start_create(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
        assert 'event_draft' in context
        assert context['event_draft']['user_id'] == 'test_user'
    
    def test_start_create_missing_user_id(self, fsm):
        """Test create fails without user_id"""
        context = {'tenant_id': 'test'}
        result = fsm.start_create(context)
        
        assert result is False
        assert fsm.current_state == AgendaStates.IDLE
    
    def test_provide_title_success(self, fsm, context):
        """Test providing title"""
        fsm.start_create(context)
        context['event_title'] = 'Test Event'
        
        result = fsm.provide_title(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_DATE
        assert fsm._event_draft['title'] == 'Test Event'
    
    def test_provide_title_empty_fails(self, fsm, context):
        """Test empty title fails validation"""
        fsm.start_create(context)
        context['event_title'] = ''
        
        result = fsm.provide_title(context)
        
        assert result is False
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
    
    def test_provide_date_success(self, fsm, context):
        """Test providing date"""
        fsm.start_create(context)
        context['event_title'] = 'Test'
        fsm.provide_title(context)
        context['event_date'] = '2025-11-21'
        
        result = fsm.provide_date(context)
        
        assert result is True
        assert fsm.current_state == AgendaStates.AWAITING_TIME
        assert fsm._event_draft['date'] == '2025-11-21'
    
    def test_complete_create_flow(self, fsm, context):
        """Test complete create flow from start to finish"""
        # Start
        assert fsm.start_create(context) is True
        
        # Title
        context['event_title'] = 'Meeting'
        assert fsm.provide_title(context) is True
        
        # Date
        context['event_date'] = '2025-11-21'
        assert fsm.provide_date(context) is True
        
        # Time
        context['event_time'] = '10:00'
        assert fsm.provide_time(context) is True
        
        # Location (skip)
        assert fsm.skip_location(context) is True
        assert fsm.current_state == AgendaStates.PROCESSING
        
        # Save
        context['db_event_id'] = 123
        assert fsm.save_event(context) is True
        assert fsm.current_state == AgendaStates.EVENT_SAVED
        assert context['event_saved'] is True
        
        # Finish
        assert fsm.finish(context) is True
        assert fsm.current_state == AgendaStates.IDLE
        assert fsm._event_draft is None


class TestAgendaFSMListFlow:
    """Test list events flow"""
    
    def test_list_flow_complete(self):
        """Test complete list flow"""
        fsm = AgendaFSM()
        context = {'user_id': 'test'}
        
        assert fsm.start_list(context) is True
        assert fsm.current_state == AgendaStates.LISTING_EVENTS
        
        assert fsm.finish_list(context) is True
        assert fsm.current_state == AgendaStates.IDLE


class TestAgendaFSMCancelFlow:
    """Test cancel operations"""
    
    def test_cancel_from_awaiting_title(self):
        """Test cancel during create flow"""
        fsm = AgendaFSM()
        context = {'user_id': 'test', 'tenant_id': 'test'}
        
        fsm.start_create(context)
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
        
        assert fsm.cancel(context) is True
        assert fsm.current_state == AgendaStates.CANCELLED
        assert fsm._event_draft is None
    
    def test_reset_from_cancelled(self):
        """Test reset to IDLE"""
        fsm = AgendaFSM()
        context = {'user_id': 'test', 'tenant_id': 'test'}
        
        fsm.start_create(context)
        fsm.cancel(context)
        
        assert fsm.reset(context) is True
        assert fsm.current_state == AgendaStates.IDLE


class TestAgendaFSMEdgeCases:
    """Test edge cases and error handling"""
    
    def test_invalid_transition(self):
        """Test invalid state transition"""
        fsm = AgendaFSM()
        context = {}
        
        # Can't provide_title from IDLE
        result = fsm.provide_title(context)
        assert result is False
        assert fsm.current_state == AgendaStates.IDLE
    
    def test_title_too_long(self):
        """Test title validation (max 200 chars)"""
        fsm = AgendaFSM()
        context = {'user_id': 'test', 'tenant_id': 'test'}
        
        fsm.start_create(context)
        context['event_title'] = 'A' * 201
        
        result = fsm.provide_title(context)
        assert result is False
    
    def test_save_without_draft(self):
        """Test save fails without draft"""
        fsm = AgendaFSM()
        context = {}
        
        # Manually change state (should never happen in real usage)
        fsm.current_state = AgendaStates.PROCESSING
        
        result = fsm.save_event(context)
        assert result is False
    
    def test_get_event_draft_returns_copy(self):
        """Test draft is returned as copy (immutability)"""
        fsm = AgendaFSM()
        context = {'user_id': 'test', 'tenant_id': 'test'}
        
        fsm.start_create(context)
        draft1 = fsm.get_event_draft()
        draft2 = fsm.get_event_draft()
        
        assert draft1 is not draft2  # Different objects
        assert draft1 == draft2       # Same content
    
    def test_is_in_creation_flow(self):
        """Test helper method for checking creation flow"""
        fsm = AgendaFSM()
        context = {'user_id': 'test', 'tenant_id': 'test'}
        
        assert fsm.is_in_creation_flow() is False
        
        fsm.start_create(context)
        assert fsm.is_in_creation_flow() is True
        
        fsm.cancel(context)
        assert fsm.is_in_creation_flow() is False
    
    def test_get_next_required_field(self):
        """Test helper for getting next required field"""
        fsm = AgendaFSM()
        context = {'user_id': 'test', 'tenant_id': 'test'}
        
        fsm.start_create(context)
        assert fsm.get_next_required_field() == 'title'
        
        context['event_title'] = 'Test'
        fsm.provide_title(context)
        assert fsm.get_next_required_field() == 'date'
