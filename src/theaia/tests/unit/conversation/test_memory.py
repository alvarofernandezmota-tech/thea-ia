"""
Tests for Conversation Memory (H08.3)
"""

import pytest
from datetime import datetime
from theaia.core.conversation.memory import (
    Message,
    ConversationMemory,
    ContextBuilder
)


class TestMessage:
    """Test Message dataclass"""
    
    def test_message_creation(self):
        """Test creating a message"""
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.timestamp is not None


class TestConversationMemory:
    """Test ConversationMemory class"""
    
    def test_memory_creation(self):
        """Test creating memory"""
        memory = ConversationMemory()
        assert memory.get_message_count() == 0
        assert memory.session_id is not None
    
    def test_add_single_message(self):
        """Test adding single message"""
        memory = ConversationMemory()
        memory.add_message("user", "Hello")
        
        assert memory.get_message_count() == 1
        history = memory.get_history()
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello"
    
    def test_add_multiple_messages(self):
        """Test adding multiple messages"""
        memory = ConversationMemory()
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there")
        memory.add_message("user", "How are you?")
        
        assert memory.get_message_count() == 3
    
    def test_get_history_limit(self):
        """Test getting limited history"""
        memory = ConversationMemory()
        for i in range(10):
            memory.add_message("user", f"Message {i}")
        
        history = memory.get_history(last_n=5)
        assert len(history) == 5
    
    def test_search_messages(self):
        """Test searching messages"""
        memory = ConversationMemory()
        memory.add_message("user", "I like Python")
        memory.add_message("assistant", "Python is great")
        memory.add_message("user", "What about Java?")
        
        results = memory.search("Python")
        assert len(results) == 2
    
    def test_get_user_messages(self):
        """Test getting user messages only"""
        memory = ConversationMemory()
        memory.add_message("user", "User message 1")
        memory.add_message("assistant", "Assistant response")
        memory.add_message("user", "User message 2")
        
        user_msgs = memory.get_user_messages()
        assert len(user_msgs) == 2
        assert "User message 1" in user_msgs
    
    def test_get_assistant_messages(self):
        """Test getting assistant messages only"""
        memory = ConversationMemory()
        memory.add_message("user", "User message")
        memory.add_message("assistant", "Assistant message 1")
        memory.add_message("assistant", "Assistant message 2")
        
        assistant_msgs = memory.get_assistant_messages()
        assert len(assistant_msgs) == 2
    
    def test_clear_memory(self):
        """Test clearing memory"""
        memory = ConversationMemory()
        memory.add_message("user", "Test")
        assert memory.get_message_count() == 1
        
        memory.clear()
        assert memory.get_message_count() == 0
    
    def test_memory_summary(self):
        """Test getting memory summary"""
        memory = ConversationMemory()
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi")
        
        summary = memory.get_summary()
        assert summary["total_messages"] == 2
        assert summary["user_messages"] == 1
        assert summary["assistant_messages"] == 1
        assert "session_id" in summary
    
    def test_max_messages_limit(self):
        """Test max messages limit"""
        memory = ConversationMemory(max_messages=5)
        
        for i in range(10):
            memory.add_message("user", f"Message {i}")
        
        assert memory.get_message_count() == 5
    
    def test_add_message_with_metadata(self):
        """Test adding message with metadata"""
        memory = ConversationMemory()
        metadata = {"user_id": "123", "context": "test"}
        memory.add_message("user", "Hello", metadata=metadata)
        
        assert memory.get_message_count() == 1


class TestContextBuilder:
    """Test ContextBuilder class"""
    
    def test_build_from_memory(self):
        """Test building context from memory"""
        memory = ConversationMemory()
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there")
        
        context = ContextBuilder.build_from_memory(memory)
        assert "Conversation context" in context
        assert "USER" in context
        assert "ASSISTANT" in context
    
    def test_build_with_summary(self):
        """Test building context with summary"""
        memory = ConversationMemory()
        memory.add_message("user", "Test 1")
        memory.add_message("assistant", "Response 1")
        
        context = ContextBuilder.build_with_summary(memory)
        assert "Memory Summary" in context
        assert "Total messages: 2" in context
        assert "User messages: 1" in context
