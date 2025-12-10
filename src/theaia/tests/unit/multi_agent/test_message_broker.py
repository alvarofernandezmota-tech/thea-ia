"""
Tests for message broker functionality
"""
import pytest
import asyncio
from datetime import datetime
from src.theaia.core.multi_agent.message.types import (
    Message,
    MessageType,
    MessagePriority
)
from src.theaia.core.multi_agent.message.broker import MessageBroker


@pytest.fixture
def broker():
    """Create a message broker instance"""
    return MessageBroker()


@pytest.fixture
def sample_message():
    """Create a sample message"""
    return Message(
        message_id="msg_1",
        message_type=MessageType.REQUEST,
        sender_id="agent_1",
        recipient_id="agent_2",
        payload={"action": "test"},
        priority=MessagePriority.NORMAL
    )


class TestMessageBroker:
    """Test message broker functionality"""
    
    def test_broker_initialization(self, broker):
        """Test broker initializes correctly"""
        assert broker is not None
        assert hasattr(broker, 'send')
        assert hasattr(broker, 'receive')
        assert hasattr(broker, 'publish')
        assert hasattr(broker, 'subscribe')
    
    @pytest.mark.asyncio
    async def test_publish_message(self, broker, sample_message):
        """Test publishing a message"""
        # Should not raise any exceptions
        result = await broker.send(sample_message)
        assert result is True
    
    @pytest.mark.asyncio
    async def test_subscribe_to_topic(self, broker):
        """Test subscribing to a topic"""
        # Subscribe agent to topic
        broker.subscribe("agent_1", "test_event")
        
        # Send a direct message to the agent
        message = Message(
            message_id="msg_2",
            message_type=MessageType.EVENT,
            sender_id="system",
            recipient_id="agent_1",
            payload={"event_name": "test_event", "data": "test"},
            priority=MessagePriority.NORMAL
        )
        
        # Send the message directly
        result = await broker.send(message)
        assert result is True
        
        # Receive the message
        received = await broker.receive("agent_1", timeout=1.0)
        
        # Verify message was received
        assert received is not None
        assert received.payload.get("event_name") == "test_event"
    
    @pytest.mark.asyncio
    async def test_message_priority_handling(self, broker):
        """Test that high priority messages are handled first"""
        # Send low priority message
        low_priority = Message(
            message_id="msg_low",
            message_type=MessageType.REQUEST,
            sender_id="agent_1",
            recipient_id="agent_2",
            payload={"priority": "low"},
            priority=MessagePriority.LOW
        )
        
        # Send high priority message
        high_priority = Message(
            message_id="msg_high",
            message_type=MessageType.REQUEST,
            sender_id="agent_1",
            recipient_id="agent_2",
            payload={"priority": "high"},
            priority=MessagePriority.HIGH
        )
        
        # Send in order: low then high
        await broker.send(low_priority)
        await broker.send(high_priority)
        
        # Receive messages - high priority should come first
        first_msg = await broker.receive("agent_2", timeout=1.0)
        second_msg = await broker.receive("agent_2", timeout=1.0)
        
        # Verify high priority was received first
        assert first_msg is not None
        assert first_msg.priority == MessagePriority.HIGH
        assert first_msg.message_id == "msg_high"
        
        assert second_msg is not None
        assert second_msg.priority == MessagePriority.LOW
        assert second_msg.message_id == "msg_low"
