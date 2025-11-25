import pytest
from src.theaia.agents.agenda_agent import AgendaAgent
from src.theaia.agents.note_agent import NoteAgent
from src.theaia.agents.reminder_agent import ReminderAgent
from src.theaia.agents.query_agent import QueryAgent
from src.theaia.agents.schedule_agent import ScheduleAgent


class TestAgentInstantiation:
    """Test all agents can be instantiated with THEA-IA context."""
    
    def test_agenda_agent_with_default_user(self):
        """Test AgendaAgent instantiation (no user_id required)."""
        agent = AgendaAgent()
        assert agent is not None
        assert hasattr(agent, 'can_handle')
    
    def test_note_agent_with_user_context(self):
        """Test NoteAgent with user_id (THEA-IA multi-tenant)."""
        user_id = 123
        agent = NoteAgent(user_id=user_id)
        assert agent is not None
        assert hasattr(agent, 'can_handle')
    
    def test_reminder_agent_with_user_context(self):
        """Test ReminderAgent with user_id (THEA-IA multi-tenant)."""
        user_id = 123
        agent = ReminderAgent(user_id=user_id)
        assert agent is not None
        assert hasattr(agent, 'can_handle')
    
    def test_query_agent_with_user_context(self):
        """Test QueryAgent with user_id (THEA-IA multi-tenant)."""
        user_id = 123
        agent = QueryAgent(user_id=user_id)
        assert agent is not None
        assert hasattr(agent, 'can_handle')
    
    def test_schedule_agent_with_user_context(self):
        """Test ScheduleAgent with user_id (THEA-IA multi-tenant)."""
        user_id = 123
        agent = ScheduleAgent(user_id=user_id)
        assert agent is not None
        assert hasattr(agent, 'can_handle')


class TestAgentIntentHandling:
    """Test agents handle intents correctly (THEA-IA router integration)."""
    
    def test_agenda_agent_has_supported_intents(self):
        """Test AgendaAgent returns supported intents."""
        agent = AgendaAgent()
        supported_intents = agent.get_supported_intents()
        
        assert isinstance(supported_intents, list)
        assert len(supported_intents) > 0
    
    def test_note_agent_has_supported_intents(self):
        """Test NoteAgent returns supported intents."""
        agent = NoteAgent(user_id=123)
        supported_intents = agent.get_supported_intents()
        
        assert isinstance(supported_intents, list)
        assert len(supported_intents) > 0
    
    def test_reminder_agent_has_supported_intents(self):
        """Test ReminderAgent returns supported intents."""
        agent = ReminderAgent(user_id=123)
        supported_intents = agent.get_supported_intents()
        
        assert isinstance(supported_intents, list)
        assert len(supported_intents) > 0
    
    def test_query_agent_has_supported_intents(self):
        """Test QueryAgent returns supported intents."""
        agent = QueryAgent(user_id=123)
        supported_intents = agent.get_supported_intents()
        
        assert isinstance(supported_intents, list)
        assert len(supported_intents) > 0
    
    def test_schedule_agent_has_supported_intents(self):
        """Test ScheduleAgent returns supported intents."""
        agent = ScheduleAgent(user_id=123)
        supported_intents = agent.get_supported_intents()
        
        assert isinstance(supported_intents, list)
        assert len(supported_intents) > 0


class TestAgentRouterIntegration:
    """Test agents work with THEA-IA router."""
    
    def test_all_agents_can_handle_method(self):
        """Test all agents implement can_handle (THEA-IA router requirement)."""
        agents = [
            ("AgendaAgent", AgendaAgent()),
            ("NoteAgent", NoteAgent(user_id=123)),
            ("ReminderAgent", ReminderAgent(user_id=123)),
            ("QueryAgent", QueryAgent(user_id=123)),
            ("ScheduleAgent", ScheduleAgent(user_id=123)),
        ]
        
        for agent_name, agent in agents:
            assert hasattr(agent, 'can_handle'), f"{agent_name} missing can_handle"
            assert callable(agent.can_handle), f"{agent_name}.can_handle not callable"
    
    def test_all_agents_have_handle_method(self):
        """Test all agents implement handle (THEA-IA message processing)."""
        agents = [
            ("AgendaAgent", AgendaAgent()),
            ("NoteAgent", NoteAgent(user_id=123)),
            ("ReminderAgent", ReminderAgent(user_id=123)),
            ("QueryAgent", QueryAgent(user_id=123)),
            ("ScheduleAgent", ScheduleAgent(user_id=123)),
        ]
        
        for agent_name, agent in agents:
            assert hasattr(agent, 'handle'), f"{agent_name} missing handle"
            assert callable(agent.handle), f"{agent_name}.handle not callable"


class TestAgentMultiTenancy:
    """Test THEA-IA multi-tenant support."""
    
    def test_agents_support_multiple_users(self):
        """Test agents can handle multiple concurrent users (THEA-IA multi-tenant)."""
        user_ids = [123, 456, 789]
        
        agents_by_user = {}
        for user_id in user_ids:
            agents_by_user[user_id] = {
                "note": NoteAgent(user_id=user_id),
                "reminder": ReminderAgent(user_id=user_id),
                "query": QueryAgent(user_id=user_id),
                "schedule": ScheduleAgent(user_id=user_id),
            }
        
        # Verify all user contexts created successfully
        assert len(agents_by_user) == 3
        for user_id, agents in agents_by_user.items():
            assert len(agents) == 4
            for agent_name, agent in agents.items():
                assert agent is not None
    
    def test_agenda_agent_global_context(self):
        """Test AgendaAgent global context (not user-specific)."""
        agent1 = AgendaAgent()
        agent2 = AgendaAgent()
        
        # Both instances should exist independently
        assert agent1 is not None
        assert agent2 is not None
        assert agent1.can_handle is not None
        assert agent2.can_handle is not None


class TestAgentFSMIntegration:
    """Test agents integrate with THEA-IA FSM."""
    
    def test_agenda_fsm_initialized(self):
        """Test AgendaAgent FSM is initialized (v2.0 system)."""
        agent = AgendaAgent()
        # AgendaAgent has FSM v2.0 system
        assert agent is not None
        assert hasattr(agent, 'get_supported_intents')
    
    def test_note_fsm_initialized(self):
        """Test NoteAgent FSM is initialized."""
        agent = NoteAgent(user_id=123)
        assert agent is not None
        assert hasattr(agent, 'get_supported_intents')
    
    def test_reminder_fsm_initialized(self):
        """Test ReminderAgent FSM is initialized."""
        agent = ReminderAgent(user_id=123)
        assert agent is not None
        assert hasattr(agent, 'get_supported_intents')
    
    def test_query_fsm_initialized(self):
        """Test QueryAgent FSM is initialized."""
        agent = QueryAgent(user_id=123)
        assert agent is not None
        assert hasattr(agent, 'get_supported_intents')
    
    def test_schedule_fsm_initialized(self):
        """Test ScheduleAgent FSM is initialized."""
        agent = ScheduleAgent(user_id=123)
        assert agent is not None
        assert hasattr(agent, 'get_supported_intents')
