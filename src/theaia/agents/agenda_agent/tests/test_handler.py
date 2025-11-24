"""
Tests for AgendaAgent Handler v3.0
Updated: 24 Nov 2025 - Match handler.py v3.0 implementation

Tests cover:
- Initialization
- async handle() method
- Supported intents
- FSM per-user instances
- Entity extraction
- Complete flows
"""

import pytest
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.base_agent import AgentConfig
from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates


# ========================================
# FIXTURES
# ========================================

@pytest.fixture
def agent():
    """Create AgendaAgent instance with proper config."""
    config = AgentConfig(name="AgendaAgent")
    return AgendaAgent(config)


@pytest.fixture
def agent_no_config():
    """Create AgendaAgent instance without config (tests default)."""
    return AgendaAgent()


# ========================================
# INITIALIZATION TESTS
# ========================================

class TestAgendaAgentInitialization:
    """Test AgendaAgent initialization."""
    
    def test_init_with_config(self, agent):
        """Test initialization with explicit config."""
        assert agent is not None
        assert agent.config.name == "AgendaAgent"
    
    def test_init_without_config(self, agent_no_config):
        """Test initialization with default config."""
        assert agent_no_config is not None
        assert agent_no_config.config.name == "AgendaAgent"
    
    def test_fsm_instances_initialized(self, agent):
        """Test FSM instances dict is initialized."""
        assert hasattr(agent, 'fsm_instances')
        assert isinstance(agent.fsm_instances, dict)
        assert len(agent.fsm_instances) == 0  # Empty at start
    
    def test_ml_extractors_initialized(self, agent):
        """Test ML extractors are initialized."""
        assert hasattr(agent, 'entity_extractor')
        assert hasattr(agent, 'date_extractor')


# ========================================
# SUPPORTED INTENTS TESTS
# ========================================

class TestSupportedIntents:
    """Test supported intents."""
    
    def test_get_supported_intents(self, agent):
        """Test that agent returns supported intents."""
        intents = agent.get_supported_intents()
        
        assert "agenda" in intents
        assert "cita" in intents
        assert "reunión" in intents
        assert "evento" in intents
        assert "agendar" in intents
        assert "calendario" in intents
    
    def test_returns_list(self, agent):
        """Test get_supported_intents returns a list."""
        intents = agent.get_supported_intents()
        assert isinstance(intents, list)
        assert len(intents) > 0


# ========================================
# FSM PER-USER TESTS
# ========================================

class TestFSMPerUser:
    """Test FSM per-user instance management."""
    
    def test_get_fsm_creates_instance(self, agent):
        """Test _get_fsm creates new instance for new user."""
        user_id = "user_123"
        fsm = agent._get_fsm(user_id)
        
        assert fsm is not None
        assert user_id in agent.fsm_instances
        assert fsm.current_state == AgendaStates.IDLE
    
    def test_get_fsm_reuses_instance(self, agent):
        """Test _get_fsm reuses existing instance."""
        user_id = "user_456"
        
        fsm1 = agent._get_fsm(user_id)
        fsm2 = agent._get_fsm(user_id)
        
        assert fsm1 is fsm2  # Same instance
        assert len(agent.fsm_instances) == 1
    
    def test_different_users_get_different_fsm(self, agent):
        """Test different users get isolated FSM instances."""
        user1 = "user_001"
        user2 = "user_002"
        
        fsm1 = agent._get_fsm(user1)
        fsm2 = agent._get_fsm(user2)
        
        assert fsm1 is not fsm2
        assert len(agent.fsm_instances) == 2


# ========================================
# HANDLE METHOD TESTS
# ========================================

class TestHandleMethod:
    """Test async handle() method (main entry point)."""
    
    @pytest.mark.asyncio
    async def test_handle_exists(self, agent):
        """Test handle method exists and is async."""
        assert hasattr(agent, 'handle')
        assert callable(agent.handle)
    
    @pytest.mark.asyncio
    async def test_handle_creates_fsm_for_new_user(self, agent):
        """Test handle creates FSM for new user."""
        user_id = "new_user"
        message = "Quiero agendar una reunión"
        context = {}
        
        # Before handle
        assert user_id not in agent.fsm_instances
        
        # Call handle
        response = await agent.handle(user_id, message, context)
        
        # After handle
        assert user_id in agent.fsm_instances
        assert response is not None
        assert "response" in response
        assert "state" in response
        assert "context" in response
    
    @pytest.mark.asyncio
    async def test_handle_returns_correct_format(self, agent):
        """Test handle returns correct response format."""
        user_id = "test_user"
        message = "crear evento"
        context = {}
        
        response = await agent.handle(user_id, message, context)
        
        assert isinstance(response, dict)
        assert "response" in response
        assert "state" in response
        assert "context" in response
        assert "status" in response
        assert isinstance(response["response"], str)
    
    @pytest.mark.asyncio
    async def test_handle_start_create_flow(self, agent):
        """Test handle starts create event flow."""
        user_id = "test_user"
        message = "crear evento"
        context = {}
        
        response = await agent.handle(user_id, message, context)
        
        assert response["status"] == "ok"
        assert "título" in response["response"].lower()
        assert str(response["state"]) == str(AgendaStates.AWAITING_TITLE)
    
    @pytest.mark.asyncio
    async def test_handle_list_events(self, agent):
        """Test handle lists events."""
        user_id = "test_user"
        message = "listar eventos"
        context = {}
        
        response = await agent.handle(user_id, message, context)
        
        assert response["status"] == "ok"
        assert "evento" in response["response"].lower()


# ========================================
# ENTITY EXTRACTION TESTS
# ========================================

class TestEntityExtraction:
    """Test ML entity extraction."""
    
    def test_extract_entities_exists(self, agent):
        """Test _extract_entities method exists."""
        assert hasattr(agent, '_extract_entities')
        assert callable(agent._extract_entities)
    
    def test_extract_entities_returns_dict(self, agent):
        """Test _extract_entities returns dictionary."""
        message = "reunión mañana a las 3pm"
        entities = agent._extract_entities(message)
        
        assert isinstance(entities, dict)
    
    def test_extract_datetime_legacy(self, agent):
        """Test legacy _extract_datetime method."""
        message = "mañana a las 15:00"
        result = agent._extract_datetime(message)
        
        assert result is not None
        assert isinstance(result, dict)


# ========================================
# TRIGGER DETERMINATION TESTS
# ========================================

class TestTriggerDetermination:
    """Test FSM trigger determination."""
    
    def test_determine_trigger_exists(self, agent):
        """Test _determine_trigger method exists."""
        assert hasattr(agent, '_determine_trigger')
        assert callable(agent._determine_trigger)
    
    def test_determine_trigger_create_from_idle(self, agent):
        """Test determines 'start_create' trigger from IDLE."""
        message = "crear evento"
        entities = {}
        
        trigger = agent._determine_trigger(AgendaStates.IDLE, message, entities)
        
        assert trigger == 'start_create'
    
    def test_determine_trigger_list_from_idle(self, agent):
        """Test determines 'start_list' trigger from IDLE."""
        message = "listar eventos"
        entities = {}
        
        trigger = agent._determine_trigger(AgendaStates.IDLE, message, entities)
        
        assert trigger == 'start_list'
    
    def test_determine_trigger_cancel(self, agent):
        """Test determines 'cancel' trigger from any state."""
        message = "cancelar"
        entities = {}
        
        # From IDLE
        trigger = agent._determine_trigger(AgendaStates.IDLE, message, entities)
        assert trigger == 'cancel'
        
        # From AWAITING_TITLE
        trigger = agent._determine_trigger(AgendaStates.AWAITING_TITLE, message, entities)
        assert trigger == 'cancel'


# ========================================
# RESPONSE GENERATION TESTS
# ========================================

class TestResponseGeneration:
    """Test response generation."""
    
    def test_generate_response_exists(self, agent):
        """Test _generate_response method exists."""
        assert hasattr(agent, '_generate_response')
        assert callable(agent._generate_response)
    
    def test_generate_response_idle(self, agent):
        """Test generates correct response for IDLE state."""
        response = agent._generate_response(AgendaStates.IDLE, {})
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_generate_response_awaiting_title(self, agent):
        """Test generates correct response for AWAITING_TITLE state."""
        response = agent._generate_response(AgendaStates.AWAITING_TITLE, {})
        
        assert "título" in response.lower()


# ========================================
# INTEGRATION TESTS (FULL FLOWS)
# ========================================

class TestFullFlows:
    """Test complete conversation flows."""
    
    @pytest.mark.asyncio
    async def test_create_event_flow_basic(self, agent):
        """Test basic create event flow."""
        user_id = "flow_test_user"
        
        # Step 1: Start create
        response = await agent.handle(user_id, "crear evento", {})
        
        assert response["status"] == "ok"
        assert str(response["state"]) == str(AgendaStates.AWAITING_TITLE)
    
    @pytest.mark.asyncio
    async def test_cancel_flow(self, agent):
        """Test cancel flow from any state."""
        user_id = "cancel_test_user"
        
        # Start create
        response1 = await agent.handle(user_id, "crear evento", {})
        assert str(response1["state"]) == str(AgendaStates.AWAITING_TITLE)
        
        # Cancel
        response2 = await agent.handle(user_id, "cancelar", response1["context"])
        assert response2["status"] == "ok"
        assert "cancelad" in response2["response"].lower()


# ========================================
# LEGACY METHOD COMPATIBILITY TESTS
# ========================================

class TestLegacyMethods:
    """Test legacy methods for backward compatibility."""
    
    def test_create_event_legacy_method(self, agent):
        """Test legacy create_event() method."""
        user_id = "legacy_test"
        event_data = {
            "title": "Test Event",
            "date": "2025-11-25",
            "time": "15:00"
        }
        
        result = agent.create_event(user_id, event_data)
        
        assert isinstance(result, dict)
        assert "status" in result
    
    def test_list_events_legacy_method(self, agent):
        """Test legacy list_events() method."""
        user_id = "legacy_test"
        
        result = agent.list_events(user_id)
        
        assert isinstance(result, dict)
        assert "status" in result
