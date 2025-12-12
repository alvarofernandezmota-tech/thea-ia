"""
Agent Communication Protocol
Sistema de mensajería inter-agentes con soporte para broadcast, ACK/NACK y buffer.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class MessageType(Enum):
    """Tipos de mensajes inter-agentes"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    ACK = "acknowledgment"
    NACK = "negative_acknowledgment"


class MessagePriority(Enum):
    """Prioridad de mensajes"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Message:
    """Mensaje entre agentes"""
    sender_id: str
    receiver_id: Optional[str]  # None para broadcast
    message_type: MessageType
    payload: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.utcnow)
    requires_ack: bool = False
    correlation_id: Optional[str] = None  # Para responses
    ttl_seconds: int = 300  # Time to live
    
    def is_expired(self) -> bool:
        """Check if message has exceeded TTL"""
        age = (datetime.utcnow() - self.timestamp).total_seconds()
        return age > self.ttl_seconds
    
    def create_ack(self) -> "Message":
        """Create acknowledgment for this message"""
        return Message(
            sender_id=self.receiver_id,
            receiver_id=self.sender_id,
            message_type=MessageType.ACK,
            payload={"original_message_id": self.message_id},
            correlation_id=self.message_id,
            requires_ack=False
        )
    
    def create_nack(self, reason: str) -> "Message":
        """Create negative acknowledgment"""
        return Message(
            sender_id=self.receiver_id,
            receiver_id=self.sender_id,
            message_type=MessageType.NACK,
            payload={
                "original_message_id": self.message_id,
                "reason": reason
            },
            correlation_id=self.message_id,
            requires_ack=False
        )


class CommunicationProtocol:
    """Protocolo de comunicación inter-agentes"""
    
    def __init__(self):
        self._message_buffer: List[Message] = []
        self._pending_acks: Dict[str, Message] = {}  # message_id -> Message
        self._max_buffer_size: int = 1000
    
    def send_message(self, message: Message) -> None:
        """Enviar mensaje"""
        if len(self._message_buffer) >= self._max_buffer_size:
            raise BufferError("Message buffer full")
        
        self._message_buffer.append(message)
        
        if message.requires_ack:
            self._pending_acks[message.message_id] = message
    
    def receive_messages(
        self, 
        receiver_id: str, 
        message_type: Optional[MessageType] = None
    ) -> List[Message]:
        """Recibir mensajes para un agente"""
        messages = [
            msg for msg in self._message_buffer
            if (msg.receiver_id == receiver_id or msg.receiver_id is None)
            and not msg.is_expired()
        ]
        
        if message_type:
            messages = [msg for msg in messages if msg.message_type == message_type]
        
        # Remove received messages from buffer
        for msg in messages:
            self._message_buffer.remove(msg)
        
        return messages
    
    def acknowledge_message(self, message_id: str) -> None:
        """Marcar mensaje como acknowledged"""
        if message_id in self._pending_acks:
            del self._pending_acks[message_id]
    
    def get_pending_acks(self) -> List[Message]:
        """Obtener mensajes pendientes de ACK"""
        return list(self._pending_acks.values())
    
    def cleanup_expired(self) -> int:
        """Limpiar mensajes expirados"""
        expired = [msg for msg in self._message_buffer if msg.is_expired()]
        for msg in expired:
            self._message_buffer.remove(msg)
            if msg.message_id in self._pending_acks:
                del self._pending_acks[msg.message_id]
        return len(expired)
    
    def broadcast(
        self, 
        sender_id: str, 
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL
    ) -> Message:
        """Enviar mensaje broadcast"""
        message = Message(
            sender_id=sender_id,
            receiver_id=None,
            message_type=MessageType.BROADCAST,
            payload=payload,
            priority=priority,
            requires_ack=False
        )
        self.send_message(message)
        return message
    
    def get_buffer_stats(self) -> Dict[str, int]:
        """Estadísticas del buffer"""
        return {
            "total_messages": len(self._message_buffer),
            "pending_acks": len(self._pending_acks),
            "max_buffer_size": self._max_buffer_size,
            "available_space": self._max_buffer_size - len(self._message_buffer)
        }
