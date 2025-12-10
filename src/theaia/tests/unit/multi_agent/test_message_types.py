"""
Tests for Message Types - H07.2
"""
import pytest
from datetime import datetime, timedelta
from src.theaia.core.multi_agent.message.types import (
    Message,
    MessageType,
    MessagePriority,
    MessageStatus
)


class TestMessageCreation:
    """Test message creation"""
    
    def test_create_basic_message(self):
        """Test creating basic message"""
        msg = Message(sender_id="agent1", recipient_id="agent2")
        
        assert msg.message_id
        assert msg.sender_id == "agent1"
        assert msg.recipient_id == "agent2"
        assert msg.message_type == MessageType.REQUEST
        assert msg.priority == MessagePriority.NORMAL
        assert msg.status == MessageStatus.PENDING
    
    def test_create_with_payload(self):
        """Test creating message with payload"""
        payload = {"action": "test", "data": 123}
        msg = Message(sender_id="agent1", payload=payload)
        
        assert msg.payload == payload
    
    def test_create_with_priority(self):
        """Test creating message with priority"""
        msg = Message(
            sender_id="agent1",
            priority=MessagePriority.HIGH
        )
        
        assert msg.priority == MessagePriority.HIGH


class TestMessageStatus:
    """Test message status management"""
    
    def test_initial_status_pending(self):
        """Test initial status is pending"""
        msg = Message(sender_id="agent1")
        
        assert msg.status == MessageStatus.PENDING
        assert msg.sent_at is None
        assert msg.delivered_at is None
    
    def test_mark_sent(self):
        """Test marking message as sent"""
        msg = Message(sender_id="agent1")
        
        msg.mark_sent()
        
        assert msg.status == MessageStatus.SENT
        assert msg.sent_at is not None
    
    def test_mark_delivered(self):
        """Test marking message as delivered"""
        msg = Message(sender_id="agent1")
        
        msg.mark_delivered()
        
        assert msg.status == MessageStatus.DELIVERED
        assert msg.delivered_at is not None
    
    def test_mark_failed(self):
        """Test marking message as failed"""
        msg = Message(sender_id="agent1")
        
        msg.mark_failed()
        
        assert msg.status == MessageStatus.FAILED
    
    def test_mark_expired(self):
        """Test marking message as expired"""
        msg = Message(sender_id="agent1")
        
        msg.mark_expired()
        
        assert msg.status == MessageStatus.EXPIRED


class TestMessageExpiration:
    """Test message expiration"""
    
    def test_message_not_expired_by_default(self):
        """Test message doesn't expire by default"""
        msg = Message(sender_id="agent1")
        
        assert not msg.is_expired
    
    def test_message_expired_when_past_expiration(self):
        """Test message is expired when past expiration time"""
        expires = datetime.utcnow() - timedelta(seconds=1)
        msg = Message(sender_id="agent1", expires_at=expires)
        
        assert msg.is_expired
    
    def test_message_not_expired_before_expiration(self):
        """Test message not expired before expiration time"""
        expires = datetime.utcnow() + timedelta(hours=1)
        msg = Message(sender_id="agent1", expires_at=expires)
        
        assert not msg.is_expired


class TestMessageRetry:
    """Test message retry logic"""
    
    def test_can_retry_initially(self):
        """Test message can be retried initially"""
        msg = Message(sender_id="agent1")
        
        assert msg.can_retry()
    
    def test_increment_retry(self):
        """Test incrementing retry count"""
        msg = Message(sender_id="agent1")
        
        msg.increment_retry()
        
        assert msg.retry_count == 1
        assert msg.can_retry()
    
    def test_cannot_retry_after_max_retries(self):
        """Test cannot retry after max retries"""
        msg = Message(sender_id="agent1", max_retries=2)
        
        msg.increment_retry()
        msg.increment_retry()
        
        assert not msg.can_retry()


class TestMessageSerialization:
    """Test message serialization"""
    
    def test_to_dict(self):
        """Test converting message to dict"""
        msg = Message(
            sender_id="agent1",
            recipient_id="agent2",
            payload={"test": "data"}
        )
        
        data = msg.to_dict()
        
        assert data["sender_id"] == "agent1"
        assert data["recipient_id"] == "agent2"
        assert data["payload"] == {"test": "data"}
        assert data["message_type"] == MessageType.REQUEST.value
    
    def test_from_dict(self):
        """Test creating message from dict"""
        data = {
            "message_id": "test-id",
            "message_type": "request",
            "sender_id": "agent1",
            "recipient_id": "agent2",
            "payload": {"test": "data"},
            "priority": 2,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
            "retry_count": 0,
            "max_retries": 3,
        }
        
        msg = Message.from_dict(data)
        
        assert msg.message_id == "test-id"
        assert msg.sender_id == "agent1"
        assert msg.recipient_id == "agent2"
        assert msg.payload == {"test": "data"}


class TestRequestMessage:
    """Test request message"""
    
    def test_create_request_message(self):
        """Test creating request message"""
        msg = Message(
            message_type=MessageType.REQUEST,
            sender_id="agent1",
            recipient_id="agent2"
        )
        
        assert msg.message_type == MessageType.REQUEST
    
    def test_request_with_custom_timeout(self):
        """Test request with custom timeout"""
        msg = Message(
            message_type=MessageType.REQUEST,
            sender_id="agent1",
            recipient_id="agent2"
        )
        msg.set_expiration(60)
        
        assert msg.expires_at is not None


class TestResponseMessage:
    """Test response message"""
    
    def test_create_response_message(self):
        """Test creating response message"""
        msg = Message(
            message_type=MessageType.RESPONSE,
            sender_id="agent2",
            recipient_id="agent1",
            correlation_id="req-123"
        )
        
        assert msg.message_type == MessageType.RESPONSE
        assert msg.correlation_id == "req-123"


class TestEventMessage:
    """Test event message"""
    
    def test_create_event_message(self):
        """Test creating event message"""
        msg = Message(
            message_type=MessageType.EVENT,
            sender_id="agent1",
            payload={"event_name": "test.event"}
        )
        
        assert msg.message_type == MessageType.EVENT
        assert msg.payload["event_name"] == "test.event"
    
    def test_event_requires_event_name(self):
        """Test event requires event_name"""
        with pytest.raises(ValueError, match="event_name is required"):
            Message(
                message_type=MessageType.EVENT,
                sender_id="agent1",
                payload={}
            )


class TestErrorMessage:
    """Test error message"""
    
    def test_create_error_message(self):
        """Test creating error message"""
        msg = Message(
            message_type=MessageType.COMMAND,
            sender_id="agent1",
            payload={
                "error_code": "ERR_001",
                "error_message": "Test error"
            }
        )
        
        assert msg.payload["error_code"] == "ERR_001"
        assert msg.payload["error_message"] == "Test error"
