"""
Message Broker - H07.2
Communication protocol for inter-agent messaging
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Set, Optional, Any, Callable
from collections import defaultdict, deque
import uuid
import asyncio
import logging
import threading
from queue import Queue, Empty

logger = logging.getLogger(__name__)


class MessageType(Enum):
  """Types of inter-agent messages"""
  REQUEST = "request"
  RESPONSE = "response"
  EVENT = "event"
  BROADCAST = "broadcast"
  ERROR = "error"


class MessagePriority(Enum):
  """Message priority levels"""
  LOW = 0
  NORMAL = 1
  HIGH = 2
  URGENT = 3


@dataclass
class Message:
  """Inter-agent message structure"""
  message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
  message_type: MessageType = MessageType.REQUEST
  priority: MessagePriority = MessagePriority.NORMAL
  
  sender_id: str = ""
  recipient_id: Optional[str] = None  # None for broadcast
  
  topic: str = ""
  payload: Dict[str, Any] = field(default_factory=dict)
  
  created_at: datetime = field(default_factory=datetime.now)
  expires_at: Optional[datetime] = None
  
  correlation_id: Optional[str] = None  # For request/response matching
  reply_to: Optional[str] = None
  
  metadata: Dict[str, Any] = field(default_factory=dict)
  
  def __post_init__(self):
    """Validate message after initialization"""
    if not self.sender_id:
      raise ValueError("sender_id is required")
    if not self.topic:
      raise ValueError("topic is required")
  
  @property
  def is_expired(self) -> bool:
    """Check if message has expired"""
    if self.expires_at is None:
      return False
    return datetime.now() > self.expires_at
  
  @property
  def age_seconds(self) -> float:
    """Get message age in seconds"""
    return (datetime.now() - self.created_at).total_seconds()
  
  def to_dict(self) -> Dict[str, Any]:
    """Convert message to dictionary"""
    return {
      "message_id": self.message_id,
      "message_type": self.message_type.value,
      "priority": self.priority.value,
      "sender_id": self.sender_id,
      "recipient_id": self.recipient_id,
      "topic": self.topic,
      "payload": self.payload,
      "created_at": self.created_at.isoformat(),
      "correlation_id": self.correlation_id,
      "metadata": self.metadata,
    }


class MessageBroker:
  """
  Central message broker for inter-agent communication.
  
  Supports:
  - Request/Response pattern
  - Pub/Sub pattern
  - Message routing
  - Priority queues
  """
  
  def __init__(self):
    """Initialize message broker"""
    self._subscriptions: Dict[str, List[Callable]] = defaultdict(list)
    self._queues: Dict[str, deque] = defaultdict(deque)
    self._pending_responses: Dict[str, asyncio.Future] = {}
    self._message_history: deque = deque(maxlen=1000)
    self._lock = threading.Lock()
    self._running = False
    
    # Statistics
    self._stats = {
      "messages_sent": 0,
      "messages_received": 0,
      "messages_dropped": 0,
      "active_subscriptions": 0,
    }
    
    logger.info("MessageBroker initialized")
  
  def publish(self, message: Message) -> bool:
    """Publish a message to subscribers"""
    try:
      if message.is_expired:
        logger.warning(f"Dropping expired message {message.message_id}")
        self._stats["messages_dropped"] += 1
        return False
      
      with self._lock:
        self._message_history.append(message)
        self._stats["messages_sent"] += 1
        
        # Handle broadcast
        if message.recipient_id is None or message.message_type == MessageType.BROADCAST:
          return self._broadcast_message(message)
        
        # Handle direct message
        return self._route_message(message)
      
    except Exception as e:
      logger.error(f"Failed to publish message: {e}")
      return False
  
  def _broadcast_message(self, message: Message) -> bool:
    """Broadcast message to all topic subscribers"""
    subscribers = self._subscriptions.get(message.topic, [])
    
    if not subscribers:
      logger.debug(f"No subscribers for topic: {message.topic}")
      return False
    
    success_count = 0
    for callback in subscribers:
      try:
        callback(message)
        success_count += 1
      except Exception as e:
        logger.error(f"Subscriber callback failed: {e}")
    
    logger.info(f"Broadcast to {success_count}/{len(subscribers)} subscribers")
    return success_count > 0
  
  def _route_message(self, message: Message) -> bool:
    """Route message to specific recipient"""
    recipient_id = message.recipient_id
    
    if recipient_id not in self._queues:
      logger.warning(f"Unknown recipient: {recipient_id}")
      self._stats["messages_dropped"] += 1
      return False
    
    # Priority queue insertion
    queue = self._queues[recipient_id]
    
    # Insert based on priority
    inserted = False
    for i, queued_msg in enumerate(queue):
      if message.priority.value > queued_msg.priority.value:
        queue.insert(i, message)
        inserted = True
        break
    
    if not inserted:
      queue.append(message)
    
    logger.debug(f"Routed message to {recipient_id}")
    return True
  
  def subscribe(self, topic: str, callback: Callable[[Message], None]) -> str:
    """Subscribe to a topic"""
    subscription_id = str(uuid.uuid4())
    
    with self._lock:
      self._subscriptions[topic].append(callback)
      self._stats["active_subscriptions"] += 1
    
    logger.info(f"New subscription to topic: {topic}")
    return subscription_id
  
  def unsubscribe(self, topic: str, callback: Callable[[Message], None]) -> bool:
    """Unsubscribe from a topic"""
    with self._lock:
      if topic in self._subscriptions:
        try:
          self._subscriptions[topic].remove(callback)
          self._stats["active_subscriptions"] -= 1
          logger.info(f"Unsubscribed from topic: {topic}")
          return True
        except ValueError:
          pass
    return False
  
  def register_agent(self, agent_id: str) -> None:
    """Register an agent to receive messages"""
    with self._lock:
      if agent_id not in self._queues:
        self._queues[agent_id] = deque()
        logger.info(f"Registered agent: {agent_id}")
  
  def unregister_agent(self, agent_id: str) -> None:
    """Unregister an agent"""
    with self._lock:
      if agent_id in self._queues:
        del self._queues[agent_id]
        logger.info(f"Unregistered agent: {agent_id}")
  
  def receive(self, agent_id: str, timeout: float = 0.1) -> Optional[Message]:
    """Receive next message for agent"""
    with self._lock:
      if agent_id not in self._queues:
        return None
      
      queue = self._queues[agent_id]
      if queue:
        message = queue.popleft()
        self._stats["messages_received"] += 1
        return message
    
    return None
  
  async def send_request(
    self,
    sender_id: str,
    recipient_id: str,
    topic: str,
    payload: Dict[str, Any],
    timeout: float = 30.0
  ) -> Optional[Message]:
    """Send request and wait for response"""
    request = Message(
      message_type=MessageType.REQUEST,
      sender_id=sender_id,
      recipient_id=recipient_id,
      topic=topic,
      payload=payload,
      correlation_id=str(uuid.uuid4())
    )
    
    # Create future for response
    future = asyncio.Future()
    self._pending_responses[request.correlation_id] = future
    
    # Send request
    if not self.publish(request):
      del self._pending_responses[request.correlation_id]
      return None
    
    try:
      # Wait for response with timeout
      response = await asyncio.wait_for(future, timeout=timeout)
      return response
    except asyncio.TimeoutError:
      logger.warning(f"Request timeout: {request.correlation_id}")
      del self._pending_responses[request.correlation_id]
      return None
  
  def send_response(
    self,
    request: Message,
    payload: Dict[str, Any]
  ) -> bool:
    """Send response to a request"""
    response = Message(
      message_type=MessageType.RESPONSE,
      sender_id=request.recipient_id,
      recipient_id=request.sender_id,
      topic=request.topic,
      payload=payload,
      correlation_id=request.correlation_id
    )
    
    # Resolve pending future if exists
    if request.correlation_id in self._pending_responses:
      future = self._pending_responses[request.correlation_id]
      if not future.done():
        future.set_result(response)
      del self._pending_responses[request.correlation_id]
    
    return self.publish(response)
  
  def get_queue_size(self, agent_id: str) -> int:
    """Get message queue size for agent"""
    with self._lock:
      if agent_id in self._queues:
        return len(self._queues[agent_id])
    return 0
  
  def get_statistics(self) -> Dict[str, Any]:
    """Get broker statistics"""
    with self._lock:
      return {
        **self._stats,
        "registered_agents": len(self._queues),
        "total_subscriptions": sum(len(subs) for subs in self._subscriptions.values()),
        "pending_responses": len(self._pending_responses),
        "history_size": len(self._message_history),
      }
  
  def clear_history(self) -> None:
    """Clear message history"""
    with self._lock:
      self._message_history.clear()
      logger.info("Cleared message history")
  
  def get_messages_by_topic(self, topic: str, limit: int = 100) -> List[Message]:
    """Get recent messages for a topic"""
    with self._lock:
      messages = [
        msg for msg in self._message_history
        if msg.topic == topic
      ]
      return list(messages[-limit:])


# ==================== GLOBAL BROKER INSTANCE ====================
_global_broker: Optional[MessageBroker] = None


def get_global_broker() -> MessageBroker:
  """Get or create global message broker"""
  global _global_broker
  
  if _global_broker is None:
    _global_broker = MessageBroker()
    logger.info("Created global message broker")
  
  return _global_broker


def reset_global_broker() -> None:
  """Reset global broker (useful for testing)"""
  global _global_broker
  _global_broker = None
  logger.info("Reset global message broker")
