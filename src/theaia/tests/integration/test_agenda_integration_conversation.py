"""
Integration tests: AgendaAgent ConversationManager + FSM
Tests per-user FSM instances, context preservation, and state management

Responsable: Álvaro Fernández Mota (CEO THEA IA)
Fecha: 21 Noviembre 2025
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
Hito: H03 BLOQUE 3.4A.3.1 - ConversationManager Integration
"""

import pytest
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates


class TestAgendaConversationManagerIntegration:
    """Test ConversationManager integration with FSM"""
    
    @pytest.fixture
    def agent(self):
        """Create AgendaAgent instance"""
        return AgendaAgent()
    
    def test_conversation_manager_tracks_fsm_state(self, agent):
        """Test ConversationManager tracks FSM state changes"""
        user_id = "test_user_1"
        tenant_id = "test_tenant"
        
        # Get FSM for user
        fsm = agent._get_fsm(user_id)
        
        # Initial state
        assert fsm.current_state == AgendaStates.IDLE
        
        # Start create flow
        context = {'user_id': user_id, 'tenant_id': tenant_id}
        fsm.start_create(context)
        
        # Verify state changed
        assert fsm.current_state == AgendaStates.AWAITING_TITLE
        
        # Verify draft created in context
        assert 'event_draft' in context
        assert context['event_draft']['user_id'] == user_id
        assert context['event_draft']['tenant_id'] == tenant_id
    
    def test_multiple_users_separate_conversations(self, agent):
        """Test multiple users have separate conversation states"""
        user1 = "user_1"
        user2 = "user_2"
        tenant = "test_tenant"
        
        # User 1 starts create flow
        fsm1 = agent._get_fsm(user1)
        context1 = {'user_id': user1, 'tenant_id': tenant}
        fsm1.start_create(context1)
        
        # User 2 still in IDLE
        fsm2 = agent._get_fsm(user2)
        assert fsm2.current_state == AgendaStates.IDLE
        
        # User 1 in AWAITING_TITLE
        assert fsm1.current_state == AgendaStates.AWAITING_TITLE
        
        # Verify separate FSM instances
        assert fsm1 is not fsm2
    
    def test_context_preserved_across_messages(self, agent):
        """Test context is preserved across multiple messages"""
        user_id = "test_user"
        tenant_id = "test_tenant"
        
        # Message 1: Start create
        context = {'user_id': user_id, 'tenant_id': tenant_id}
        fsm = agent._get_fsm(user_id)
        fsm.start_create(context)
        
        # Verify draft created
        assert 'event_draft' in context
        assert context['event_draft']['user_id'] == user_id
        
        # Message 2: Provide title
        context['event_title'] = 'Test Meeting'
        fsm.provide_title(context)
        
        # Verify draft updated
        assert context['event_draft']['title'] == 'Test Meeting'
        
        # Message 3: Provide date
        context['event_date'] = '2025-11-21'
        fsm.provide_date(context)
        
        # Verify draft has all data
        draft = fsm.get_event_draft()
        assert draft is not None
        assert draft['title'] == 'Test Meeting'
        assert draft['date'] == '2025-11-21'
    
    def test_fsm_per_user_isolation(self, agent):
        """Test FSM state is isolated per user"""
        user1 = "user_1"
        user2 = "user_2"
        user3 = "user_3"
        tenant = "test_tenant"
        
        # User 1: Start create flow
        fsm1 = agent._get_fsm(user1)
        ctx1 = {'user_id': user1, 'tenant_id': tenant}
        fsm1.start_create(ctx1)
        
        # User 2: Also start create flow
        fsm2 = agent._get_fsm(user2)
        ctx2 = {'user_id': user2, 'tenant_id': tenant}
        fsm2.start_create(ctx2)
        
        # User 3: Stay in IDLE
        fsm3 = agent._get_fsm(user3)
        
        # Verify states
        assert fsm1.current_state == AgendaStates.AWAITING_TITLE
        assert fsm2.current_state == AgendaStates.AWAITING_TITLE
        assert fsm3.current_state == AgendaStates.IDLE
        
        # User 1 progresses
        ctx1['event_title'] = 'User 1 Meeting'
        fsm1.provide_title(ctx1)
        
        # User 2 and 3 unaffected
        assert fsm2.current_state == AgendaStates.AWAITING_TITLE
        assert fsm3.current_state == AgendaStates.IDLE
        
        # Verify drafts are separate
        draft1 = fsm1.get_event_draft()
        draft2 = fsm2.get_event_draft()
        
        assert draft1['title'] == 'User 1 Meeting'
        assert 'title' not in draft2  # User 2 hasn't provided title
    
    def test_fsm_cleanup_on_cancel(self, agent):
        """Test FSM cleanup when user cancels"""
        user_id = "test_user"
        tenant_id = "test_tenant"
        
        # Start create flow
        context = {'user_id': user_id, 'tenant_id': tenant_id}
        fsm = agent._get_fsm(user_id)
        fsm.start_create(context)
        
        # Add some data
        context['event_title'] = 'Test'
        fsm.provide_title(context)
        
        # Verify draft exists
        assert fsm.get_event_draft() is not None
        
        # Cancel
        fsm.cancel(context)
        
        # Verify state changed
        assert fsm.current_state == AgendaStates.CANCELLED
        
        # Reset to IDLE
        fsm.reset(context)
        assert fsm.current_state == AgendaStates.IDLE
        
        # Verify draft cleaned
        assert fsm.get_event_draft() is None
    
    def test_fsm_cleanup_on_finish(self, agent):
        """Test FSM cleanup when flow completes"""
        user_id = "test_user"
        tenant_id = "test_tenant"
        
        # Complete create flow
        context = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'event_title': 'Meeting',
            'event_date': '2025-11-21',
            'event_time': '10:00'
        }
        
        fsm = agent._get_fsm(user_id)
        
        # Full flow
        fsm.start_create(context)
        fsm.provide_title(context)
        fsm.provide_date(context)
        fsm.provide_time(context)
        fsm.skip_location(context)
        
        # Before save, draft exists
        assert fsm.get_event_draft() is not None
        
        # Save event
        context['db_event_id'] = 123
        fsm.save_event(context)
        
        # Finish
        fsm.finish(context)
        
        # Verify cleanup
        assert fsm.current_state == AgendaStates.IDLE
        assert fsm.get_event_draft() is None
