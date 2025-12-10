"""Message broker for agent communication."""
import asyncio
from collections import defaultdict, deque
from datetime import datetime
from typing import Callable, Deque, Dict, List, Optional, Set
from .protocol import MessageProtocol
from .types import Message, MessagePriority, MessageStatus


class MessageBroker:
    """Manages message routing and delivery between agents."""
    
    def __init__(self, protocol: Optional[MessageProtocol] = None):
        """Initialize message broker."""
        self._protocol = protocol or MessageProtocol()
        self._queues: Dict[str, Dict[MessagePriority, Deque[Message]]] = defaultdict(
            lambda: {priority: deque() for priority in MessagePriority}
        )
        self._handlers: Dict[str, Callable] = {}
        self._subscriptions: Dict[str, Set[str]] = defaultdict(set)
        self._dead_letter: Deque[Message] = deque()
        self._stats = {
            "sent": 0,
            "received": 0,
            "delivered": 0,
            "failed": 0,
            "dead_letter": 0,
            "queued": 0,
        }

    @property
    def handlers(self) -> Dict[str, Callable]:
        """Get registered handlers."""
        return self._handlers
    
    @property
    def subscriptions(self) -> Dict[str, Set[str]]:
        """Get event subscriptions."""
        return self._subscriptions

    def register_handler(self, agent_id: str, handler: Callable) -> None:
        """Register message handler for agent."""
        self._handlers[agent_id] = handler

    def unregister_handler(self, agent_id: str) -> None:
        """Unregister message handler for agent."""
        self._handlers.pop(agent_id, None)

    async def send(self, message: Message) -> bool:
        """Send message to recipient."""
        # Validate message
        if not self._protocol.validate(message):
            self._stats["failed"] += 1
            return False
        
        # Mark as sent
        message.mark_sent()
        
        # Add to recipient's queue
        if message.recipient_id:
            priority_queues = self._queues[message.recipient_id]
            priority_queues[message.priority].append(message)
            self._stats["queued"] += 1
        
        self._stats["sent"] += 1
        return True

    async def receive(self, agent_id: str, timeout: Optional[float] = None) -> Optional[Message]:
        """Receive message for agent."""
        start_time = datetime.utcnow()
        
        while True:
            # Check all priority queues (highest first)
            for priority in sorted(MessagePriority, key=lambda p: p.value, reverse=True):
                queue = self._queues[agent_id][priority]
                if queue:
                    message = queue.popleft()
                    message.mark_delivered()
                    self._stats["received"] += 1
                    self._stats["delivered"] += 1
                    self._stats["queued"] -= 1
                    return message
            
            # Check timeout
            if timeout is not None:
                elapsed = (datetime.utcnow() - start_time).total_seconds()
                if elapsed >= timeout:
                    return None
            else:
                return None
            
            # Small delay before retry
            await asyncio.sleep(0.01)

    async def broadcast(self, message: Message, agent_ids: List[str]) -> int:
        """Broadcast message to multiple agents."""
        sent_count = 0
        for agent_id in agent_ids:
            # Create copy for each recipient
            msg_copy = Message(**message.to_dict())
            msg_copy.recipient_id = agent_id
            if await self.send(msg_copy):
                sent_count += 1
        return sent_count

    async def request(
        self,
        message: Message,
        timeout: float = 5.0
    ) -> Optional[Message]:
        """Send request and wait for response."""
        if not await self.send(message):
            return None
        
        # Wait for response with correlation_id
        start_time = datetime.utcnow()
        
        while True:
            # Check sender's queue for response
            if message.sender_id:
                for priority in MessagePriority:
                    queue = self._queues[message.sender_id][priority]
                    for i, msg in enumerate(queue):
                        if msg.correlation_id == message.message_id:
                            response = queue[i]
                            del queue[i]
                            response.mark_delivered()
                            self._stats["received"] += 1
                            self._stats["delivered"] += 1
                            self._stats["queued"] -= 1
                            return response
            
            # Check timeout
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            if elapsed >= timeout:
                return None
            
            await asyncio.sleep(0.01)
    
    async def respond(self, message: Message) -> bool:
        """Send a response message."""
        return await self.send(message)

    def subscribe(self, agent_id: str, event_name: str) -> None:
        """Subscribe agent to event."""
        self._subscriptions[event_name].add(agent_id)

    def unsubscribe(self, agent_id: str, event_name: str) -> None:
        """Unsubscribe agent from event."""
        self._subscriptions[event_name].discard(agent_id)

    async def publish(self, message: Message) -> int:
        """Publish event to subscribers."""
        event_name = message.payload.get("event_name")
        if not event_name:
            return 0
        
        subscribers = self._subscriptions.get(event_name, set())
        return await self.broadcast(message, list(subscribers))

    def get_queue_size(self, agent_id: str, priority: Optional[MessagePriority] = None) -> int:
        """Get size of agent's message queue."""
        if priority:
            return len(self._queues[agent_id][priority])
        return sum(len(q) for q in self._queues[agent_id].values())
    
    def get_queue_size_by_priority(self, agent_id: str, priority: MessagePriority) -> int:
        """Get size of agent's queue for specific priority."""
        return len(self._queues[agent_id][priority])

    def peek(self, agent_id: str) -> Optional[Message]:
        """Peek at next message without removing it."""
    def peek(self, agent_id: str) -> Optional[Message]:
        """Peek at next message without removing it."""
        for priority in sorted(MessagePriority, key=lambda p: p.value, reverse=True):
            queue = self._queues[agent_id][priority]
            if queue:
                return queue[0]
        return None

    def clear_queue(self, agent_id: str) -> int:
        """Clear all messages for agent."""
        count = 0
        for priority in MessagePriority:
            count += len(self._queues[agent_id][priority])
            self._queues[agent_id][priority].clear()
        self._stats["queued"] -= count
        return count

    def move_to_dead_letter(self, message: Message) -> None:
        """Move message to dead letter queue."""
        message.mark_failed()
        self._dead_letter.append(message)
        self._stats["failed"] += 1
        self._stats["dead_letter"] += 1

    def get_dead_letter_queue(self) -> List[Message]:
        """Get dead letter queue."""
        return list(self._dead_letter)

    def get_stats(self) -> Dict[str, int]:
        """Get broker statistics."""
        return self._stats.copy()
