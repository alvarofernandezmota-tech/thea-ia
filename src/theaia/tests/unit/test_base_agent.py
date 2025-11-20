# Archivo: src/theaia/tests/unit/test_base_agent.py

"""
Unit tests for BaseAgent class.
Tests the refactored base agent functionality.
"""

import pytest
import logging
from src.theaia.agents.base_agent import BaseAgent, AgentConfig


# Mock agent for testing
class MockAgent(BaseAgent):
    """Mock agent implementation for testing."""
    
    def get_supported_intents(self):
        return ["test", "mock", "sample"]
    
    def _process_message(self, user_id, message, context):
        """Simple mock implementation."""
        return {
            "status": "ok",
            "message": f"Mock processed: {message}",
            "context": context,
        }


class TestBaseAgentConfig:
    """Tests for AgentConfig dataclass."""
    
    def test_agent_config_default_values(self):
        """Test AgentConfig with default values."""
        config = AgentConfig(name="TestAgent")
        
        assert config.name == "TestAgent"
        assert config.enabled is True
        assert config.max_retries == 3
        assert config.timeout == 30
        assert config.log_level == "INFO"
        assert config.custom_config is None
    
    def test_agent_config_custom_values(self):
        """Test AgentConfig with custom values."""
        config = AgentConfig(
            name="CustomAgent",
            enabled=False,
            max_retries=5,
            timeout=60,
            log_level="DEBUG",
            custom_config={"key": "value"}
        )
        
        assert config.name == "CustomAgent"
        assert config.enabled is False
        assert config.max_retries == 5
        assert config.timeout == 60
        assert config.log_level == "DEBUG"
        assert config.custom_config == {"key": "value"}


class TestBaseAgent:
    """Tests for BaseAgent class."""
    
    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent for testing."""
        config = AgentConfig(name="MockAgent", log_level="ERROR")
        return MockAgent(config=config)
    
    def test_agent_initialization(self, mock_agent):
        """Test agent initialization."""
        assert mock_agent.config.name == "MockAgent"
        assert mock_agent.logger is not None
        assert mock_agent._is_initialized is False
    
    def test_get_supported_intents(self, mock_agent):
        """Test get_supported_intents method."""
        intents = mock_agent.get_supported_intents()
        
        assert isinstance(intents, list)
        assert "test" in intents
        assert "mock" in intents
        assert "sample" in intents
        assert len(intents) == 3
    
    def test_can_handle_valid_intent(self, mock_agent):
        """Test can_handle with valid intent."""
        assert mock_agent.can_handle("test") is True
        assert mock_agent.can_handle("TEST") is True  # Case insensitive
        assert mock_agent.can_handle("mock") is True
    
    def test_can_handle_invalid_intent(self, mock_agent):
        """Test can_handle with invalid intent."""
        assert mock_agent.can_handle("invalid") is False
        assert mock_agent.can_handle("unknown") is False
    
    def test_can_handle_disabled_agent(self):
        """Test can_handle when agent is disabled."""
        config = AgentConfig(name="DisabledAgent", enabled=False)
        agent = MockAgent(config=config)
        
        assert agent.can_handle("test") is False
    
    def test_handle_message_success(self, mock_agent):
        """Test successful message handling."""
        response = mock_agent.handle(
            user_id="user_123",
            message="test message",
            context={"key": "value"}
        )
        
        assert response["status"] == "ok"
        assert "Mock processed" in response["message"]
        assert "context" in response
        assert response["context"]["key"] == "value"
    
    def test_handle_message_with_empty_context(self, mock_agent):
        """Test message handling with empty context."""
        response = mock_agent.handle(
            user_id="user_456",
            message="another test"
        )
        
        assert response["status"] == "ok"
        assert "context" in response
        assert isinstance(response["context"], dict)
    
    def test_initialize_agent(self, mock_agent):
        """Test agent initialization."""
        result = mock_agent.initialize()
        
        assert result is True
        assert mock_agent._is_initialized is True
    
    def test_initialize_already_initialized(self, mock_agent):
        """Test initializing an already initialized agent."""
        mock_agent.initialize()
        result = mock_agent.initialize()  # Second call
        
        assert result is True
        assert mock_agent._is_initialized is True
    
    def test_cleanup_agent(self, mock_agent):
        """Test agent cleanup."""
        mock_agent.initialize()
        assert mock_agent._is_initialized is True
        
        mock_agent.cleanup()
        assert mock_agent._is_initialized is False
    
    def test_get_status(self, mock_agent):
        """Test get_status method."""
        status = mock_agent.get_status()
        
        assert isinstance(status, dict)
        assert status["name"] == "MockAgent"
        assert status["enabled"] is True
        assert status["initialized"] is False
        assert "supported_intents" in status
        assert len(status["supported_intents"]) == 3
    
    def test_agent_repr(self, mock_agent):
        """Test agent string representation."""
        repr_str = repr(mock_agent)
        
        assert "MockAgent" in repr_str
        assert "MockAgent" in repr_str
        assert "enabled=True" in repr_str


class TestBaseAgentErrorHandling:
    """Tests for BaseAgent error handling."""
    
    class FailingAgent(BaseAgent):
        """Mock agent that raises an error."""
        
        def get_supported_intents(self):
            return ["fail"]
        
        def _process_message(self, user_id, message, context):
            raise ValueError("Intentional test error")
    
    @pytest.fixture
    def failing_agent(self):
        """Create an agent that fails on purpose."""
        config = AgentConfig(name="FailingAgent", log_level="ERROR")
        return self.FailingAgent(config=config)
    
    def test_handle_error_response(self, failing_agent):
        """Test error handling in handle method."""
        response = failing_agent.handle(
            user_id="user_789",
            message="trigger error",
            context={}
        )
        
        assert response["status"] == "error"
        assert "error" in response["message"].lower()
        assert "context" in response
        assert "error" in response["context"]
        assert "error_type" in response["context"]
        assert response["context"]["error_type"] == "ValueError"
