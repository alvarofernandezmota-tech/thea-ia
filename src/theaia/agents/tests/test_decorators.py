import pytest
from src.theaia.agents.decorators import (
    agent_handler,
    validate_input,
    require_context_keys,
    log_execution,
    get_registered_agents,
    get_agent_by_name,
    get_agents_by_intent,
    clear_registry,
)
from src.theaia.agents.base_agent import BaseAgent


class TestAgentHandler:
    """Tests for @agent_handler decorator."""
    
    def setup_method(self):
        """Clean registry before each test."""
        clear_registry()
    
    def test_agent_handler_registers_agent(self):
        """Test agent_handler decorator registers agent."""
        @agent_handler(name="test_agent", intents=["test"])
        class TestAgent(BaseAgent):
            def get_supported_intents(self):
                return ["test"]
        
        agents = get_registered_agents()
        assert "test_agent" in agents
    
    def test_agent_handler_stores_metadata(self):
        """Test agent_handler stores correct metadata."""
        @agent_handler(name="test_agent", intents=["intent1", "intent2"], priority=5)
        class TestAgent(BaseAgent):
            def get_supported_intents(self):
                return ["intent1", "intent2"]
        
        agent_meta = get_agent_by_name("test_agent")
        assert agent_meta is not None
        assert agent_meta["intents"] == ["intent1", "intent2"]
        assert agent_meta["priority"] == 5
    
    def test_agent_handler_default_priority(self):
        """Test agent_handler default priority is 5."""
        @agent_handler(name="test_agent", intents=["test"])
        class TestAgent(BaseAgent):
            def get_supported_intents(self):
                return ["test"]
        
        agent_meta = get_agent_by_name("test_agent")
        assert agent_meta["priority"] == 5
    
    def test_agent_handler_requires_auth(self):
        """Test agent_handler stores requires_auth."""
        @agent_handler(name="auth_agent", intents=["test"], requires_auth=True)
        class AuthAgent(BaseAgent):
            def get_supported_intents(self):
                return ["test"]
        
        agent_meta = get_agent_by_name("auth_agent")
        assert agent_meta["requires_auth"] is True
    
    def test_get_registered_agents_returns_dict(self):
        """Test get_registered_agents returns dictionary."""
        @agent_handler(name="agent1", intents=["test"])
        class Agent1(BaseAgent):
            def get_supported_intents(self):
                return ["test"]
        
        agents = get_registered_agents()
        assert isinstance(agents, dict)
        assert len(agents) > 0


class TestValidateInput:
    """Tests for @validate_input decorator."""
    
    def test_validate_input_decorator_exists(self):
        """Test validate_input decorator can be imported."""
        assert validate_input is not None
        assert callable(validate_input)
    
    def test_validate_input_accepts_validator(self):
        """Test validate_input accepts validator function."""
        def validator(msg):
            return len(msg) > 0
        
        decorator = validate_input(validator)
        assert callable(decorator)
    
    @pytest.mark.asyncio
    async def test_validate_input_runs_validator(self):
        """Test validate_input calls validator function."""
        call_count = 0
        
        def validator(msg):
            nonlocal call_count
            call_count += 1
            return len(msg) > 0
        
        @validate_input(validator)
        async def handler(self, msg, *args, **kwargs):
            return "ok"
        
        class MockAgent:
            pass
        
        agent = MockAgent()
        result = await handler(agent, "test")
        assert call_count >= 1


class TestRequireContextKeys:
    """Tests for @require_context_keys decorator."""
    
    def test_require_context_keys_decorator_exists(self):
        """Test require_context_keys decorator exists."""
        assert require_context_keys is not None
        assert callable(require_context_keys)
    
    def test_require_context_keys_accepts_keys(self):
        """Test require_context_keys accepts list of keys."""
        decorator = require_context_keys(["key1", "key2"])
        assert callable(decorator)


class TestLogExecution:
    """Tests for @log_execution decorator."""
    
    def test_log_execution_decorator_exists(self):
        """Test log_execution decorator exists."""
        assert log_execution is not None
        assert callable(log_execution)
    
    def test_log_execution_default_loglevel(self):
        """Test log_execution works with default loglevel."""
        decorator = log_execution()
        assert callable(decorator)
    
    def test_log_execution_custom_loglevel(self):
        """Test log_execution works with custom loglevel."""
        decorator = log_execution("DEBUG")
        assert callable(decorator)


class TestAgentRegistry:
    """Tests for agent registry functions."""
    
    def setup_method(self):
        """Clean registry before each test."""
        clear_registry()
    
    def test_get_agents_by_intent(self):
        """Test get_agents_by_intent finds agents."""
        @agent_handler(name="calendar_agent", intents=["calendar", "schedule"])
        class CalendarAgent(BaseAgent):
            def get_supported_intents(self):
                return ["calendar", "schedule"]
        
        @agent_handler(name="note_agent", intents=["notes", "reminder"])
        class NoteAgent(BaseAgent):
            def get_supported_intents(self):
                return ["notes", "reminder"]
        
        calendar_agents = get_agents_by_intent("calendar")
        assert len(calendar_agents) > 0
        assert any(a["name"] == "calendar_agent" for a in calendar_agents)
    
    def test_clear_registry(self):
        """Test clear_registry empties registry."""
        @agent_handler(name="test_agent", intents=["test"])
        class TestAgent(BaseAgent):
            def get_supported_intents(self):
                return ["test"]
        
        assert len(get_registered_agents()) > 0
        clear_registry()
        assert len(get_registered_agents()) == 0
    
    def test_get_agent_by_name_returns_none_if_not_found(self):
        """Test get_agent_by_name returns None if agent not found."""
        result = get_agent_by_name("nonexistent_agent")
        assert result is None


class TestDecoratorIntegration:
    """Integration tests for multiple decorators."""
    
    def setup_method(self):
        """Clean registry before each test."""
        clear_registry()
    
    def test_multiple_agents_in_registry(self):
        """Test multiple agents can be registered."""
        @agent_handler(name="agent1", intents=["intent1"])
        class Agent1(BaseAgent):
            def get_supported_intents(self):
                return ["intent1"]
        
        @agent_handler(name="agent2", intents=["intent2"])
        class Agent2(BaseAgent):
            def get_supported_intents(self):
                return ["intent2"]
        
        @agent_handler(name="agent3", intents=["intent3"])
        class Agent3(BaseAgent):
            def get_supported_intents(self):
                return ["intent3"]
        
        agents = get_registered_agents()
        assert len(agents) == 3
    
    def test_decorators_preserve_class_functionality(self):
        """Test decorators don't break class functionality."""
        @agent_handler(name="functional_agent", intents=["test"])
        class FunctionalAgent(BaseAgent):
            def __init__(self):
                super().__init__()
                self.initialized = True
            
            def get_supported_intents(self):
                return ["test"]
        
        agent = FunctionalAgent()
        assert agent.initialized is True
