"""
Tests for Message Broker - H07.2
"""
import pytest
import time
import asyncio
from datetime import datetime, timedelta
from src.theaia.core.multi_agent.message_broker import (
  Message,
  MessageBroker,
  MessageType,
  MessagePriority,
  get_global_broker,
  reset_global_broker
)


@pytest.fixture
def broker():
  """Create a fresh broker for each test"""
  reset_global_broker()
  return MessageBroker()


@pytest.fixture
def sample_message():
  """Create a sample message"""
  return Message(
    message_type=MessageType.REQUEST,
    sender_id="agent1",
    recipient_id="agent2",
    topic="test_topic",
    payload={"key": "value"}
  )


class TestMessage:
  """Test Message dataclass"""
  
  def test_message_creation(self):
    """Test message creation with default values"""
    msg = Message(
      sender_id="agent1",
      topic="test"
    )
    assert msg.sender_id == "agent1"
    assert msg.topic == "test"
    assert msg.message_type == MessageType.REQUEST
    assert msg.priority == MessagePriority.NORMAL
    assert msg.message_id is not None
  
  def test_message_validation_no_sender(self):
    """Test message validation fails without sender"""
    with pytest.raises(ValueError, match="sender_id is required"):
      Message(sender_id="", topic="test")
  
  def test_message_validation_no_topic(self):
    """Test message validation fails without topic"""
    with pytest.raises(ValueError, match="topic is required"):
      Message(sender_id="agent1", topic="")
  
  def test_message_expiration(self):
    """Test message expiration"""
    past_time = datetime.now() - timedelta(seconds=1)
    msg = Message(
      sender_id="agent1",
      topic="test",
      expires_at=past_time
    )
    assert msg.is_expired is True
  
  def test_message_not_expired(self):
    """Test message not expired"""
    future_time = datetime.now() + timedelta(hours=1)
    msg = Message(
      sender_id="agent1",
      topic="test",
      expires_at=future_time
    )
    assert msg.is_expired is False
  
  def test_message_no_expiration(self):
    """Test message with no expiration"""
    msg = Message(sender_id="agent1", topic="test")
    assert msg.is_expired is False
  
  def test_message_age(self):
    """Test message age calculation"""
    msg = Message(sender_id="agent1", topic="test")
    time.sleep(0.1)
    assert msg.age_seconds >= 0.1
  
  def test_message_to_dict(self):
    """Test message conversion to dict"""
    msg = Message(
      sender_id="agent1",
      recipient_id="agent2",
      topic="test",
      payload={"data": "value"}
    )
    msg_dict = msg.to_dict()
    assert msg_dict["sender_id"] == "agent1"
    assert msg_dict["recipient_id"] == "agent2"
    assert msg_dict["topic"] == "test"
    assert msg_dict["payload"]["data"] == "value"


class TestMessageBroker:
  """Test MessageBroker functionality"""
  
  def test_broker_initialization(self, broker):
    """Test broker initializes correctly"""
    assert broker is not None
    stats = broker.get_statistics()
    assert stats["messages_sent"] == 0
    assert stats["registered_agents"] == 0
  
  def test_register_agent(self, broker):
    """Test agent registration"""
    broker.register_agent("agent1")
    assert broker.get_queue_size("agent1") == 0
    stats = broker.get_statistics()
    assert stats["registered_agents"] == 1
  
  def test_unregister_agent(self, broker):
    """Test agent unregistration"""
    broker.register_agent("agent1")
    broker.unregister_agent("agent1")
    stats = broker.get_statistics()
    assert stats["registered_agents"] == 0
  
  def test_publish_direct_message(self, broker, sample_message):
    """Test publishing direct message"""
    broker.register_agent("agent2")
    result = broker.publish(sample_message)
    assert result is True
    stats = broker.get_statistics()
    assert stats["messages_sent"] == 1
  
  def test_publish_to_unknown_agent(self, broker, sample_message):
    """Test publishing to unknown agent fails"""
    result = broker.publish(sample_message)
    assert result is False
    stats = broker.get_statistics()
    assert stats["messages_dropped"] == 1
  
  def test_publish_expired_message(self, broker):
    """Test publishing expired message"""
    broker.register_agent("agent2")
    msg = Message(
      sender_id="agent1",
      recipient_id="agent2",
      topic="test",
      expires_at=datetime.now() - timedelta(seconds=1)
    )
    result = broker.publish(msg)
    assert result is False
    stats = broker.get_statistics()
    assert stats["messages_dropped"] == 1
  
  def test_receive_message(self, broker, sample_message):
    """Test receiving a message"""
    broker.register_agent("agent2")
    broker.publish(sample_message)
    received = broker.receive("agent2")
    assert received is not None
    assert received.sender_id == "agent1"
    assert broker.get_queue_size("agent2") == 0
  
  def test_receive_from_empty_queue(self, broker):
    """Test receiving from empty queue"""
    broker.register_agent("agent1")
    received = broker.receive("agent1")
    assert received is None
  
  def test_receive_from_unregistered_agent(self, broker):
    """Test receiving from unregistered agent"""
    received = broker.receive("unknown")
    assert received is None
  
  def test_priority_queue_ordering(self, broker):
    """Test messages are ordered by priority"""
    broker.register_agent("agent1")
    
    # Send low priority first
    msg_low = Message(
      sender_id="sender",
      recipient_id="agent1",
      topic="test",
      priority=MessagePriority.LOW
    )
    broker.publish(msg_low)
    
    # Send high priority second
    msg_high = Message(
      sender_id="sender",
      recipient_id="agent1",
      topic="test",
      priority=MessagePriority.HIGH
    )
    broker.publish(msg_high)
    
    # High priority should be received first
    received = broker.receive("agent1")
    assert received.priority == MessagePriority.HIGH
    
    received = broker.receive("agent1")
    assert received.priority == MessagePriority.LOW
  
  def test_subscribe_to_topic(self, broker):
    """Test subscribing to a topic"""
    received_messages = []
    
    def callback(msg):
      received_messages.append(msg)
    
    subscription_id = broker.subscribe("test_topic", callback)
    assert subscription_id is not None
    
    stats = broker.get_statistics()
    assert stats["active_subscriptions"] == 1
  
  def test_broadcast_message(self, broker):
    """Test broadcasting message to subscribers"""
    received_messages = []
    
    def callback(msg):
      received_messages.append(msg)
    
    broker.subscribe("broadcast_topic", callback)
    broker.subscribe("broadcast_topic", callback)
    
    msg = Message(
      sender_id="broadcaster",
      recipient_id=None,
      topic="broadcast_topic",
      message_type=MessageType.BROADCAST
    )
    
    result = broker.publish(msg)
    assert result is True
    assert len(received_messages) == 2
  
  def test_unsubscribe_from_topic(self, broker):
    """Test unsubscribing from topic"""
    def callback(msg):
      pass
    
    broker.subscribe("test_topic", callback)
    result = broker.unsubscribe("test_topic", callback)
    assert result is True
    
    stats = broker.get_statistics()
    assert stats["active_subscriptions"] == 0
  
  def test_unsubscribe_nonexistent(self, broker):
    """Test unsubscribing from nonexistent subscription"""
    def callback(msg):
      pass
    
    result = broker.unsubscribe("nonexistent", callback)
    assert result is False
  
  @pytest.mark.asyncio
  async def test_async_request_response(self, broker):
    """Test async request/response pattern"""
    broker.register_agent("agent1")
    broker.register_agent("agent2")
    
    async def responder():
      await asyncio.sleep(0.1)
      msg = broker.receive("agent2")
      if msg:
        broker.send_response(msg, {"result": "success"})
    
    # Start responder in background
    responder_task = asyncio.create_task(responder())
    
    # Send request
    response = await broker.send_request(
      sender_id="agent1",
      recipient_id="agent2",
      topic="test_request",
      payload={"query": "data"},
      timeout=1.0
    )
    
    await responder_task
    
    assert response is not None
    assert response.message_type == MessageType.RESPONSE
    assert response.payload["result"] == "success"
  
  @pytest.mark.asyncio
  async def test_async_request_timeout(self, broker):
    """Test async request timeout"""
    broker.register_agent("agent2")
    
    response = await broker.send_request(
      sender_id="agent1",
      recipient_id="agent2",
      topic="test_request",
      payload={},
      timeout=0.1
    )
    
    assert response is None
  
  def test_get_queue_size(self, broker, sample_message):
    """Test getting queue size"""
    broker.register_agent("agent2")
    broker.publish(sample_message)
    assert broker.get_queue_size("agent2") == 1
  
  def test_message_history(self, broker, sample_message):
    """Test message history tracking"""
    broker.register_agent("agent2")
    broker.publish(sample_message)
    
    stats = broker.get_statistics()
    assert stats["history_size"] == 1
  
  def test_clear_history(self, broker, sample_message):
    """Test clearing message history"""
    broker.register_agent("agent2")
    broker.publish(sample_message)
    broker.clear_history()
    
    stats = broker.get_statistics()
    assert stats["history_size"] == 0
  
  def test_get_messages_by_topic(self, broker):
    """Test getting messages by topic"""
    broker.register_agent("agent1")
    
    msg1 = Message(sender_id="sender", recipient_id="agent1", topic="topic1")
    msg2 = Message(sender_id="sender", recipient_id="agent1", topic="topic2")
    msg3 = Message(sender_id="sender", recipient_id="agent1", topic="topic1")
    
    broker.publish(msg1)
    broker.publish(msg2)
    broker.publish(msg3)
    
    topic1_messages = broker.get_messages_by_topic("topic1")
    assert len(topic1_messages) == 2
  
  def test_statistics(self, broker, sample_message):
    """Test getting broker statistics"""
    broker.register_agent("agent2")
    broker.publish(sample_message)
    broker.receive("agent2")
    
    stats = broker.get_statistics()
    assert stats["messages_sent"] == 1
    assert stats["messages_received"] == 1
    assert stats["registered_agents"] == 1


class TestGlobalBroker:
  """Test global broker instance"""
  
  def test_get_global_broker(self):
    """Test getting global broker"""
    reset_global_broker()
    broker1 = get_global_broker()
    broker2 = get_global_broker()
    assert broker1 is broker2
  
  def test_reset_global_broker(self):
    """Test resetting global broker"""
    broker1 = get_global_broker()
    reset_global_broker()
    broker2 = get_global_broker()
    assert broker1 is not broker2
