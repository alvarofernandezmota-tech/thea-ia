"""
Tests for CLI Interface (H08.5)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from theaia.core.conversation.cli import ConversationCLI


class TestConversationCLI:
    """Test ConversationCLI class"""
    
    def test_cli_creation(self):
        """Test creating CLI instance"""
        cli = ConversationCLI()
        assert cli.agent is not None
        assert cli.memory is not None
        assert cli.tool_registry is not None
        assert cli.running is False
    
    def test_cli_with_custom_name(self):
        """Test CLI with custom agent name"""
        cli = ConversationCLI(agent_name="CustomAgent")
        assert cli.agent.config.name == "CustomAgent"
    
    def test_cli_components_initialized(self):
        """Test all components are initialized"""
        cli = ConversationCLI()
        
        # Check LLM
        assert cli.llm_client is not None
        
        # Check Agent
        assert cli.agent is not None
        assert cli.agent.config.name == "THEA"
        
        # Check Memory
        assert cli.memory is not None
        assert cli.memory.get_message_count() == 0
        
        # Check Tools
        assert cli.tool_registry is not None
        assert cli.tool_executor is not None
    
    @pytest.mark.asyncio
    async def test_process_message(self):
        """Test processing a message"""
        cli = ConversationCLI()
        cli.user_name = "TestUser"
        
        # Mock the agent.chat method
        cli.agent.chat = AsyncMock(return_value="This is a test response")
        
        # Process message
        await cli.process_message("Hello THEA")
        
        # Check memory was updated
        assert cli.memory.get_message_count() == 2
        
        messages = cli.memory.get_full_history()
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Hello THEA"
        assert messages[1]["role"] == "assistant"
    
    def test_show_help(self, capsys):
        """Test help display"""
        cli = ConversationCLI()
        cli.show_help()
        
        captured = capsys.readouterr()
        assert "Available Commands" in captured.out
        assert "help" in captured.out
        assert "quit" in captured.out
    
    def test_show_memory(self, capsys):
        """Test memory summary display"""
        cli = ConversationCLI()
        cli.user_name = "TestUser"
        
        # Add some messages
        cli.memory.add_message("user", "Test message 1")
        cli.memory.add_message("assistant", "Test response 1")
        
        # Show memory
        cli.show_memory()
        
        captured = capsys.readouterr()
        assert "Memory Summary" in captured.out
        assert "Total Messages: 2" in captured.out
    
    @pytest.mark.asyncio
    async def test_shutdown(self, capsys):
        """Test shutdown procedure"""
        cli = ConversationCLI()
        cli.user_name = "TestUser"
        cli.running = True
        
        await cli.shutdown()
        
        assert cli.running is False
        captured = capsys.readouterr()
        assert "Thanks for chatting" in captured.out
    
    def test_memory_integration(self):
        """Test memory integration with CLI"""
        cli = ConversationCLI()
        cli.user_name = "TestUser"
        
        # Add messages manually
        cli.memory.add_message("user", "Hello", {"user": "TestUser"})
        cli.memory.add_message("assistant", "Hi there!")
        
        # Check memory state
        assert cli.memory.get_message_count() == 2
        
        user_msgs = cli.memory.get_user_messages()
        assert len(user_msgs) == 1
        assert user_msgs[0] == "Hello"
    
    def test_tool_registry_integration(self):
        """Test tool registry is accessible from CLI"""
        cli = ConversationCLI()
        
        # Register a simple tool
        def test_func(x: int) -> int:
            return x * 2
        
        from theaia.core.conversation.tools import ToolParameter
        
        params = [ToolParameter("x", "int", "Input value")]
        cli.tool_registry.register_function(
            test_func,
            "double",
            "Double a number",
            parameters=params
        )
        
        # Verify tool is registered
        assert cli.tool_registry.get("double") is not None
        assert len(cli.tool_registry.get_all()) == 1


class TestCLIIntegration:
    """Integration tests for CLI"""
    
    def test_full_cli_setup(self):
        """Test full CLI setup"""
        cli = ConversationCLI(
            agent_name="IntegrationTest",
            model="gpt-4-turbo"
        )
        
        # Verify all components work together
        assert cli.agent.config.name == "IntegrationTest"
        assert cli.memory.session_id is not None
        assert cli.tool_registry is not None
        assert cli.tool_executor is not None
    
    @pytest.mark.asyncio
    async def test_message_flow(self):
        """Test complete message flow"""
        cli = ConversationCLI()
        cli.user_name = "Alice"
        
        # Mock agent response
        cli.agent.chat = AsyncMock(return_value="I understand")
        
        # Send message
        await cli.process_message("What is AI?")
        
        # Verify full flow
        assert cli.memory.get_message_count() == 2
        summary = cli.memory.get_summary()
        assert summary["user_messages"] == 1
        assert summary["assistant_messages"] == 1
