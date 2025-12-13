"""
Tests for Conversational Agent (H08.2)
"""

import pytest
from theaia.core.conversation.conversational_agent import (
    ConversationalAgent,
    AgentConfig
)
from theaia.core.conversation.agent_config import SystemPrompts, AgentPersonalities


class TestAgentConfig:
    """Test AgentConfig class"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = AgentConfig()
        assert config.name == "THEA"
        assert config.personality == "helpful, friendly, professional"
        assert config.tone == "conversational"
        assert config.max_history == 20
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = AgentConfig(
            name="CustomAgent",
            max_history=50,
            tone="technical"
        )
        assert config.name == "CustomAgent"
        assert config.max_history == 50
        assert config.tone == "technical"


class TestSystemPrompts:
    """Test SystemPrompts"""
    
    def test_default_prompt(self):
        """Test default system prompt"""
        assert "THEA" in SystemPrompts.DEFAULT
        assert "multi-agent" in SystemPrompts.DEFAULT
    
    def test_professional_prompt(self):
        """Test professional prompt"""
        assert "professional" in SystemPrompts.PROFESSIONAL
        assert "expert" in SystemPrompts.PROFESSIONAL
    
    def test_friendly_prompt(self):
        """Test friendly prompt"""
        assert "friendly" in SystemPrompts.FRIENDLY
        assert "warm" in SystemPrompts.FRIENDLY


class TestAgentPersonalities:
    """Test agent personalities"""
    
    def test_helpful_personality(self):
        """Test helpful personality"""
        assert AgentPersonalities.HELPFUL["name"] == "THEA Helper"
        assert "helpful" in AgentPersonalities.HELPFUL["personality"]
    
    def test_expert_personality(self):
        """Test expert personality"""
        assert "Expert" in AgentPersonalities.EXPERT["name"]
        assert "professional" in AgentPersonalities.EXPERT["tone"]


class TestConversationalAgent:
    """Test ConversationalAgent class"""
    
    def test_agent_creation(self):
        """Test creating agent"""
        agent = ConversationalAgent()
        assert agent.agent_id == "conversational_agent"
        assert agent.config.name == "THEA"
        assert agent.conversation_history == []
    
    def test_agent_with_custom_config(self):
        """Test agent with custom config"""
        config = AgentConfig(name="CustomTHEA")
        agent = ConversationalAgent(config=config)
        assert agent.config.name == "CustomTHEA"
    
    @pytest.mark.asyncio
    async def test_simple_chat(self):
        """Test simple chat interaction"""
        agent = ConversationalAgent()
        response = await agent.chat("Hello THEA")
        
        assert response is not None
        assert len(response) > 0
        assert len(agent.conversation_history) == 2
    
    @pytest.mark.asyncio
    async def test_chat_with_context(self):
        """Test chat with user context"""
        agent = ConversationalAgent()
        user_context = {"name": "Álvaro", "role": "developer"}
        
        response = await agent.chat("Hi", user_context=user_context)
        
        assert response is not None
        assert agent.user_context["name"] == "Álvaro"
    
    @pytest.mark.asyncio
    async def test_multi_turn_conversation(self):
        """Test multi-turn conversation"""
        agent = ConversationalAgent()
        
        # First turn
        response1 = await agent.chat("Hello")
        assert len(agent.conversation_history) == 2
        
        # Second turn
        response2 = await agent.chat("How are you?")
        assert len(agent.conversation_history) == 4
        
        # Third turn
        response3 = await agent.chat("Tell me a joke")
        assert len(agent.conversation_history) == 6
    
    def test_history_management(self):
        """Test history management"""
        agent = ConversationalAgent()
        agent.conversation_history = [
            {"role": "user", "content": "test1"},
            {"role": "assistant", "content": "response1"}
        ]
        
        assert agent.get_history_length() == 2
        
        agent.clear_history()
        assert agent.get_history_length() == 0
        assert agent.conversation_history == []
    
    def test_session_info(self):
        """Test session information"""
        agent = ConversationalAgent()
        info = agent.get_session_info()
        
        assert "session_id" in info
        assert "created_at" in info
        assert "message_count" in info
        assert info["agent_id"] == "conversational_agent"
    
    @pytest.mark.asyncio
    async def test_max_history_limit(self):
        """Test max history limit"""
        config = AgentConfig(max_history=4)
        agent = ConversationalAgent(config=config)
        
        # Send 3 messages (6 entries in history)
        for i in range(3):
            await agent.chat(f"Message {i}")
        
        # History should be limited
        assert agent.get_history_length() <= config.max_history
    
    def test_system_prompt_building(self):
        """Test system prompt building"""
        agent = ConversationalAgent()
        prompt = agent._build_system_prompt()
        
        assert "THEA" in prompt
        assert agent.agent_id in prompt
        assert agent.config.personality in prompt
    
    def test_context_building(self):
        """Test context building"""
        agent = ConversationalAgent()
        agent.user_context = {"name": "Álvaro"}
        
        context = agent._build_context()
        
        assert "User Information" in context
        assert "Álvaro" in context
