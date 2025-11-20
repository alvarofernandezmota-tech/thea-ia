"""
Unit tests for AgentRegistry.

Tests registration, discovery, and instance management.
"""

import pytest
from src.theaia.agents.agent_registry import (
    AgentRegistry,
    get_global_registry,
    register_agent,
    get_agent,
    list_all_agents,
    reset_global_registry
)
from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.agent_config import AgentConfig, AgentPriority


# Test agent classes
class TestAgent(BaseAgent):
    """Test agent for registry testing."""
    
    def get_supported_intents(self) -> list:
        """Return supported intents."""
        return ["test_intent"]
    
    def handle(self, user_input: str, context: dict) -> tuple:
        return "test response", "completed", context


class AnotherAgent(BaseAgent):
    """Another test agent."""
    
    def get_supported_intents(self) -> list:
        """Return supported intents."""
        return ["another_intent"]
    
    def handle(self, user_input: str, context: dict) -> tuple:
        return "another response", "completed", context


class EnabledAgent(BaseAgent):
    """Enabled test agent."""
    
    def get_supported_intents(self) -> list:
        return ["test"]
    
    def handle(self, user_input: str, context: dict) -> tuple:
        return "response", "completed", context


class DisabledAgent(BaseAgent):
    """Disabled test agent."""
    
    def get_supported_intents(self) -> list:
        return ["test"]
    
    def handle(self, user_input: str, context: dict) -> tuple:
        return "response", "completed", context


class TestAgentRegistry:
    """Test AgentRegistry class."""
    
    @pytest.fixture
    def registry(self):
        """Create fresh registry for each test."""
        return AgentRegistry()
    
    @pytest.fixture
    def test_config(self):
        """Create test config."""
        return AgentConfig(
            name="test",
            display_name="Test Agent",
            description="Test description",
            intents=["test_intent"]
        )
    
    def test_registry_initialization(self, registry):
        """Test registry starts empty."""
        assert len(registry.list_agents()) == 0
        assert len(registry._instances) == 0
    
    def test_register_agent(self, registry, test_config):
        """Test registering an agent."""
        registry.register(TestAgent, test_config)
        
        assert registry.is_registered("test")
        assert "test" in registry.list_agents()
        
        config = registry.get_config("test")
        assert config is not None
        assert config.name == "test"
    
    def test_register_agent_auto_config(self, registry):
        """Test registration with auto-generated config."""
        registry.register(TestAgent)
        
        assert registry.is_registered("test")
        config = registry.get_config("test")
        assert config is not None
    
    def test_register_invalid_agent(self, registry):
        """Test registering non-agent class fails."""
        class NotAnAgent:
            pass
        
        with pytest.raises(ValueError, match="must inherit from BaseAgent"):
            registry.register(NotAnAgent)
    
    def test_register_non_class(self, registry):
        """Test registering non-class fails."""
        with pytest.raises(TypeError, match="must be a class"):
            registry.register("not a class")
    
    def test_unregister_agent(self, registry, test_config):
        """Test unregistering an agent."""
        registry.register(TestAgent, test_config)
        assert registry.is_registered("test")
        
        registry.unregister("test")
        assert not registry.is_registered("test")
        assert "test" not in registry.list_agents()
    
    def test_get_agent_class(self, registry, test_config):
        """Test retrieving agent class."""
        registry.register(TestAgent, test_config)
        
        agent_class = registry.get_agent_class("test")
        assert agent_class == TestAgent
        
        # Case insensitive
        agent_class = registry.get_agent_class("TEST")
        assert agent_class == TestAgent
        
        # Non-existent
        agent_class = registry.get_agent_class("nonexistent")
        assert agent_class is None
    
    def test_create_instance(self, registry, test_config):
        """Test creating agent instance."""
        registry.register(TestAgent, test_config)
        
        instance = registry.create_instance("test")
        assert instance is not None
        assert isinstance(instance, TestAgent)
    
    def test_get_or_create_instance_caching(self, registry, test_config):
        """Test instance caching."""
        registry.register(TestAgent, test_config)
        
        instance1 = registry.get_or_create_instance("test")
        instance2 = registry.get_or_create_instance("test")
        
        # Should return same instance
        assert instance1 is instance2
    
    def test_clear_instances(self, registry, test_config):
        """Test clearing cached instances."""
        registry.register(TestAgent, test_config)
        
        instance1 = registry.get_or_create_instance("test")
        registry.clear_instances()
        instance2 = registry.get_or_create_instance("test")
        
        # Should be different instances after clear
        assert instance1 is not instance2
    
    def test_list_agents(self, registry, test_config):
        """Test listing registered agents."""
        registry.register(TestAgent, test_config)
        
        another_config = AgentConfig(
            name="another",
            display_name="Another",
            description="Another test",
            intents=["another"]
        )
        registry.register(AnotherAgent, another_config)
        
        agents = registry.list_agents()
        assert len(agents) == 2
        assert "test" in agents
        assert "another" in agents
    
    def test_list_enabled_agents(self, registry):
        """Test listing only enabled agents."""
        config1 = AgentConfig(
            name="enabled",
            display_name="Enabled",
            description="Enabled agent",
            intents=["test"],
            enabled=True
        )
        config2 = AgentConfig(
            name="disabled",
            display_name="Disabled",
            description="Disabled agent",
            intents=["test"],
            enabled=False
        )
        
        registry.register(EnabledAgent, config1)
        registry.register(DisabledAgent, config2)
        
        enabled = registry.list_enabled_agents()
        assert "enabled" in enabled
        assert "disabled" not in enabled
    
    def test_get_agent_for_intent(self, registry):
        """Test finding agent by intent."""
        config = AgentConfig(
            name="test",
            display_name="Test",
            description="Test",
            intents=["test_intent", "another_intent"],
            priority=AgentPriority.HIGH
        )
        registry.register(TestAgent, config)
        
        agent_name = registry.get_agent_for_intent("test_intent")
        assert agent_name == "test"
        
        # Case insensitive
        agent_name = registry.get_agent_for_intent("TEST_INTENT")
        assert agent_name == "test"
        
        # Unknown intent
        agent_name = registry.get_agent_for_intent("unknown")
        assert agent_name is None
    
    def test_get_registry_stats(self, registry, test_config):
        """Test getting registry statistics."""
        registry.register(TestAgent, test_config)
        registry.get_or_create_instance("test")
        
        stats = registry.get_registry_stats()
        
        assert stats["total_registered"] == 1
        assert stats["total_enabled"] == 1
        assert stats["total_instances"] == 1
        assert "test" in stats["agents"]


class TestGlobalRegistry:
    """Test global registry functions."""
    
    def setup_method(self):
        """Reset global registry before each test."""
        reset_global_registry()
    
    def teardown_method(self):
        """Reset global registry after each test."""
        reset_global_registry()
    
    def test_get_global_registry(self):
        """Test singleton pattern."""
        registry1 = get_global_registry()
        registry2 = get_global_registry()
        
        assert registry1 is registry2
    
    def test_register_agent_global(self):
        """Test registering via global function."""
        config = AgentConfig(
            name="test",
            display_name="Test",
            description="Test",
            intents=["test"]
        )
        
        register_agent(TestAgent, config)
        
        agents = list_all_agents()
        assert "test" in agents
    
    def test_get_agent_global(self):
        """Test getting agent via global function."""
        config = AgentConfig(
            name="test",
            display_name="Test",
            description="Test",
            intents=["test"]
        )
        
        register_agent(TestAgent, config)
        
        agent = get_agent("test")
        assert agent is not None
        assert isinstance(agent, TestAgent)
    
    def test_reset_global_registry(self):
        """Test resetting global registry."""
        config = AgentConfig(
            name="test",
            display_name="Test",
            description="Test",
            intents=["test"]
        )
        
        register_agent(TestAgent, config)
        assert len(list_all_agents()) > 0
        
        reset_global_registry()
        
        # After reset, should be empty again
        registry = get_global_registry()
        assert len(registry.list_agents()) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
