"""Tests for Agent Communication Protocol - Coverage target: >85%"""
import pytest
from datetime import datetime, timedelta
from src.theaia.core.multi_agent.agent_communication import Message, MessageType, MessagePriority, CommunicationProtocol

class TestMessageType:
    def test_request_type(self): assert MessageType.REQUEST.value == "request"
    def test_response_type(self): assert MessageType.RESPONSE.value == "response"
    def test_notification_type(self): assert MessageType.NOTIFICATION.value == "notification"
    def test_broadcast_type(self): assert MessageType.BROADCAST.value == "broadcast"
    def test_ack_type(self): assert MessageType.ACK.value == "acknowledgment"
    def test_nack_type(self): assert MessageType.NACK.value == "negative_acknowledgment"

class TestMessagePriority:
    def test_low_priority(self): assert MessagePriority.LOW.value == 1
    def test_normal_priority(self): assert MessagePriority.NORMAL.value == 2
    def test_high_priority(self): assert MessagePriority.HIGH.value == 3
    def test_critical_priority(self): assert MessagePriority.CRITICAL.value == 4

class TestMessageBasic:
    def test_message_creation(self):
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={"action": "test"})
        assert msg.sender_id == "agent1" and msg.receiver_id == "agent2" and msg.message_type == MessageType.REQUEST
    
    def test_message_id_generated(self):
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        assert msg.message_id is not None and len(msg.message_id) > 0
    
    def test_unique_message_ids(self):
        msg1 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        msg2 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        assert msg1.message_id != msg2.message_id
    
    def test_default_priority(self):
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        assert msg.priority == MessagePriority.NORMAL
    
    def test_timestamp_set(self):
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        assert msg.timestamp is not None and isinstance(msg.timestamp, datetime)

class TestMessageExpiration:
    def test_message_not_expired(self):
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={}, ttl_seconds=300)
        assert msg.is_expired() is False
    
    def test_message_expired(self):
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={}, ttl_seconds=0)
        import time; time.sleep(0.1)
        assert msg.is_expired() is True

class TestMessageAck:
    def test_create_ack(self):
        original = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        ack = original.create_ack()
        assert ack.sender_id == "agent2" and ack.receiver_id == "agent1" and ack.message_type == MessageType.ACK
    
    def test_create_nack(self):
        original = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        nack = original.create_nack("Invalid")
        assert nack.message_type == MessageType.NACK and nack.payload["reason"] == "Invalid"

class TestCommunicationProtocolBasic:
    def test_protocol_initialization(self):
        protocol = CommunicationProtocol()
        assert len(protocol._message_buffer) == 0 and len(protocol._pending_acks) == 0
    
    def test_send_message(self):
        protocol = CommunicationProtocol()
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        protocol.send_message(msg)
        assert len(protocol._message_buffer) == 1

class TestCommunicationProtocolReceive:
    def test_receive_messages(self):
        protocol = CommunicationProtocol()
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        protocol.send_message(msg)
        received = protocol.receive_messages("agent2")
        assert len(received) == 1

class TestCommunicationProtocolBroadcast:
    def test_broadcast_message(self):
        protocol = CommunicationProtocol()
        msg = protocol.broadcast(sender_id="agent1", payload={"test": "data"})
        assert msg.message_type == MessageType.BROADCAST and msg.receiver_id is None

class TestCommunicationProtocolAdvanced:
    def test_buffer_full_raises_error(self):
        protocol = CommunicationProtocol()
        protocol._max_buffer_size = 2
        msg1 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        msg2 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        protocol.send_message(msg1)
        protocol.send_message(msg2)
        msg3 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        with pytest.raises(BufferError):
            protocol.send_message(msg3)
    
    def test_acknowledge_nonexistent_message(self):
        protocol = CommunicationProtocol()
        protocol.acknowledge_message("nonexistent")
        assert len(protocol._pending_acks) == 0
    
    def test_receive_filters_expired_messages(self):
        protocol = CommunicationProtocol()
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={}, ttl_seconds=0)
        protocol.send_message(msg)
        import time
        time.sleep(0.1)
        received = protocol.receive_messages("agent2")
        assert len(received) == 0
    
    def test_receive_with_message_type_filter(self):
        protocol = CommunicationProtocol()
        msg1 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        msg2 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.RESPONSE, payload={})
        protocol.send_message(msg1)
        protocol.send_message(msg2)
        received = protocol.receive_messages("agent2", MessageType.RESPONSE)
        assert len(received) == 1 and received[0].message_type == MessageType.RESPONSE
    
    def test_cleanup_no_expired(self):
        protocol = CommunicationProtocol()
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={}, ttl_seconds=300)
        protocol.send_message(msg)
        expired_count = protocol.cleanup_expired()
        assert expired_count == 0
    
    def test_get_buffer_stats_with_data(self):
        protocol = CommunicationProtocol()
        msg1 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={}, requires_ack=True)
        msg2 = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={})
        protocol.send_message(msg1)
        protocol.send_message(msg2)
        stats = protocol.get_buffer_stats()
        assert stats["total_messages"] == 2 and stats["pending_acks"] == 1 and stats["available_space"] == 998
    
    def test_multiple_receivers_broadcast(self):
        protocol = CommunicationProtocol()
        broadcast = protocol.broadcast(sender_id="agent1", payload={"data": "test"})
        received1 = protocol.receive_messages("agent2")
        received2 = protocol.receive_messages("agent3")
        assert len(received1) == 1
        assert len(received2) == 0
    
    def test_correlation_id_preserved(self):
        protocol = CommunicationProtocol()
        msg = Message(sender_id="agent1", receiver_id="agent2", message_type=MessageType.REQUEST, payload={}, correlation_id="test123")
        protocol.send_message(msg)
        received = protocol.receive_messages("agent2")
        assert received[0].correlation_id == "test123"
