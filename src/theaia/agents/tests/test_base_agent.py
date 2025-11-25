import pytest
from src.theaia.agents.base_agent import BaseAgent


class ConcreteAgent(BaseAgent):
    """Concrete implementation for testing."""
    
    def __init__(self):
        super().__init__()
        self.test_attr = "initialized"
    
    def get_supported_intents(self):
        return ["test_intent", "another_intent"]


class TestBaseAgentInitialization:
    """Tests for BaseAgent initialization."""
    
    def test_base_agent_can_be_subclassed(self):
        """Test BaseAgent can be subclassed."""
        agent = ConcreteAgent()
        assert isinstance(agent, BaseAgent)
    
    def test_base_agent_initialization_preserves_subclass_attrs(self):
        """Test BaseAgent initialization preserves subclass attributes."""
        agent = ConcreteAgent()
        assert agent.test_attr == "initialized"


class TestBaseAgentMethods:
    """Tests for BaseAgent methods."""
    
    def test_get_supported_intents_returns_list(self):
        """Test get_supported_intents returns list."""
        agent = ConcreteAgent()
        intents = agent.get_supported_intents()
        assert isinstance(intents, list)
    
    def test_get_supported_intents_not_empty(self):
        """Test get_supported_intents returns non-empty list."""
        agent = ConcreteAgent()
        intents = agent.get_supported_intents()
        assert len(intents) > 0
    
    def test_can_handle_method_exists(self):
        """Test can_handle method exists."""
        agent = ConcreteAgent()
        assert hasattr(agent, "can_handle")
        assert callable(agent.can_handle)
    
    def test_handle_method_exists(self):
        """Test handle method exists."""
        agent = ConcreteAgent()
        assert hasattr(agent, "handle")
        assert callable(agent.handle)


class TestBaseAgentCanHandle:
    """Tests for can_handle functionality."""
    
    def test_can_handle_with_supported_intent(self):
        """Test can_handle returns True for supported intent."""
        agent = ConcreteAgent()
        assert agent.can_handle("test_intent") is True
    
    def test_can_handle_with_unsupported_intent(self):
        """Test can_handle returns False for unsupported intent."""
        agent = ConcreteAgent()
        assert agent.can_handle("unsupported_intent") is False
    
    def test_can_handle_case_insensitive(self):
        """Test can_handle is case insensitive."""
        agent = ConcreteAgent()
        assert agent.can_handle("TEST_INTENT") is True


class TestBaseAgentInheritance:
    """Tests for inheritance behavior."""
    
    def test_multiple_agents_independent(self):
        """Test multiple agent instances are independent."""
        agent1 = ConcreteAgent()
        agent2 = ConcreteAgent()
        
        # Both should work independently
        assert agent1.test_attr == "initialized"
        assert agent2.test_attr == "initialized"
    
    def test_subclass_can_override_methods(self):
        """Test subclass can override methods."""
        class CustomAgent(BaseAgent):
            def get_supported_intents(self):
                return ["custom"]
        
        agent = CustomAgent()
        assert agent.get_supported_intents() == ["custom"]


class TestBaseAgentEdgeCases:
    """Tests for edge cases."""
    
    def test_can_handle_empty_string(self):
        """Test can_handle with empty string."""
        agent = ConcreteAgent()
        result = agent.can_handle("")
        assert isinstance(result, bool)
    
    def test_get_supported_intents_called_multiple_times(self):
        """Test get_supported_intents can be called multiple times."""
        agent = ConcreteAgent()
        intents1 = agent.get_supported_intents()
        intents2 = agent.get_supported_intents()
        assert intents1 == intents2
    
    def test_subclass_attributes_preserved(self):
        """Test subclass custom attributes are preserved."""
        class AgentWithAttrs(BaseAgent):
            def __init__(self):
                super().__init__()
                self.custom_id = 42
                self.custom_data = {"key": "value"}
            
            def get_supported_intents(self):
                return ["test"]
        
        agent = AgentWithAttrs()
        assert agent.custom_id == 42
        assert agent.custom_data["key"] == "value"
    
    def test_multiple_intents_handling(self):
        """Test agent handles multiple intents correctly."""
        agent = ConcreteAgent()
        intents = agent.get_supported_intents()
        
        # Should handle all intents
        for intent in intents:
            assert agent.can_handle(intent) is True
    
    def test_can_handle_returns_boolean(self):
        """Test can_handle always returns boolean."""
        agent = ConcreteAgent()
        
        result1 = agent.can_handle("test_intent")
        result2 = agent.can_handle("unknown")
        
        assert isinstance(result1, bool)
        assert isinstance(result2, bool)
    
    def test_agent_interface_compliance(self):
        """Test agent implements required interface."""
        agent = ConcreteAgent()
        
        # Check all required methods exist
        assert callable(agent.get_supported_intents)
        assert callable(agent.can_handle)
        assert callable(agent.handle)
