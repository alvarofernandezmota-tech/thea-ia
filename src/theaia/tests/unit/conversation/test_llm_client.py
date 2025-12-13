"""
Tests for LLM Client (H08.1)
"""

import pytest
import asyncio
from theaia.core.conversation.llm_client import (
    LLMConfig,
    PromptTemplate,
    LLMClient
)


class TestLLMConfig:
    """Test LLMConfig class"""
    
    def test_config_defaults(self):
        """Test default configuration"""
        config = LLMConfig()
        assert config.provider == "openai"
        assert config.model == "gpt-4-turbo"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.timeout == 30
        assert config.max_retries == 3
    
    def test_config_custom(self):
        """Test custom configuration"""
        config = LLMConfig(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=1000
        )
        assert config.model == "gpt-3.5-turbo"
        assert config.temperature == 0.5
        assert config.max_tokens == 1000


class TestPromptTemplate:
    """Test PromptTemplate class"""
    
    def test_format_message(self):
        """Test message formatting"""
        msg = PromptTemplate.format_message("user", "Hello")
        assert msg["role"] == "user"
        assert msg["content"] == "Hello"
    
    def test_build_context_empty(self):
        """Test context building with empty history"""
        context = PromptTemplate.build_context([])
        assert "Recent conversation" in context
    
    def test_build_context_with_history(self):
        """Test context building with messages"""
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        context = PromptTemplate.build_context(history)
        assert "USER" in context
        assert "ASSISTANT" in context


class TestLLMClient:
    """Test LLMClient class"""
    
    @pytest.mark.asyncio
    async def test_client_creation(self):
        """Test creating LLM client"""
        client = LLMClient()
        assert client is not None
        assert client.conversation_history == []
    
    @pytest.mark.asyncio
    async def test_mock_response(self):
        """Test mock response generation"""
        client = LLMClient()
        response = await client.generate_response("hello")
        assert "THEA" in response or "Hello" in response
        assert len(client.conversation_history) == 2  # user + assistant
    
    @pytest.mark.asyncio
    async def test_conversation_history(self):
        """Test history tracking"""
        client = LLMClient()
        await client.generate_response("hello")
        await client.generate_response("how are you")
        
        history = client.get_history()
        assert len(history) == 4  # 2 exchanges
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"
    
    def test_clear_history(self):
        """Test clearing history"""
        client = LLMClient()
        client.conversation_history = [{"role": "user", "content": "test"}]
        client.clear_history()
        assert client.conversation_history == []
    
    @pytest.mark.asyncio
    async def test_history_length(self):
        """Test history length"""
        client = LLMClient()
        assert client.get_history_length() == 0
        
        await client.generate_response("test")
        assert client.get_history_length() == 2
