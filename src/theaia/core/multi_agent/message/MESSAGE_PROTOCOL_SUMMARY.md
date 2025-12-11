# Message Protocol Module - Summary

**File:** `src/theaia/core/multi_agent/message/protocol.py`  
**Author:** Álvaro Fernández Mota  
**Date:** 11 December 2025  
**Version:** 1.0.0  
**Lines of Code:** 80  
**Test Coverage:** 42%

---

## 📋 Purpose

Defines abstract protocol interface and validation utilities for message communication in the multi-agent system. Provides contract for message transport implementations and ensures message integrity.

---

## 🎯 Key Features

- ✅ **Abstract Protocol** - Interface contract for message brokers
- ✅ **Message Validation** - Structural and content validation
- ✅ **Type Safety** - Enforce message structure compliance
- ✅ **Extensibility** - Support for custom protocol implementations
- ✅ **Payload Validation** - Ensure data integrity

---

## 🏗️ Components

### Abstract Base Class: MessageProtocol

Defines the contract that all message transport implementations must follow.

from abc import ABC, abstractmethod
from typing import Optional

class MessageProtocol(ABC):
"""
Abstract protocol for message communication.

text
All message broker implementations must inherit from this
and implement the required methods.
"""

@abstractmethod
async def send(self, message: Message) -> bool:
    """
    Send message to recipient.
    
    Args:
        message: Message to send
        
    Returns:
        True if sent successfully, False otherwise
        
    Raises:
        ConnectionError: If connection to recipient fails
        ValidationError: If message validation fails
    """
    pass

@abstractmethod
async def receive(
    self,
    timeout: Optional[float] = None
) -> Optional[Message]:
    """
    Receive next message from queue.
    
    Args:
        timeout: Maximum time to wait in seconds (None = wait forever)
        
    Returns:
        Next message or None if timeout
        
    Raises:
        TimeoutError: If timeout exceeded (optional)
    """
    pass
text

---

### Implementations

Different transport implementations can be created by inheriting from `MessageProtocol`:

#### Example: In-Memory Protocol

class InMemoryProtocol(MessageProtocol):
"""Simple in-memory message queue for testing"""

text
def __init__(self):
    self.queue = asyncio.Queue()

async def send(self, message: Message) -> bool:
    """Send message to in-memory queue"""
    await self.queue.put(message)
    return True

async def receive(
    self,
    timeout: Optional[float] = None
) -> Optional[Message]:
    """Receive from in-memory queue"""
    try:
        if timeout:
            return await asyncio.wait_for(
                self.queue.get(),
                timeout=timeout
            )
        else:
            return await self.queue.get()
    except asyncio.TimeoutError:
        return None
text

---

#### Example: Redis Protocol

class RedisProtocol(MessageProtocol):
"""Redis-based message queue"""

text
def __init__(self, redis_url: str):
    self.redis = aioredis.from_url(redis_url)

async def send(self, message: Message) -> bool:
    """Send message to Redis queue"""
    channel = f"agent:{message.recipient_id}"
    msg_json = json.dumps(message.to_dict())
    
    await self.redis.rpush(channel, msg_json)
    return True

async def receive(
    self,
    timeout: Optional[float] = None
) -> Optional[Message]:
    """Receive from Redis queue"""
    channel = f"agent:{self.agent_id}"
    
    if timeout:
        result = await self.redis.blpop(channel, timeout=timeout)
    else:
        result = await self.redis.lpop(channel)
    
    if result:
        _, msg_json = result
        msg_dict = json.loads(msg_json)
        return Message(**msg_dict)
    
    return None
text

---

#### Example: RabbitMQ Protocol

class RabbitMQProtocol(MessageProtocol):
"""RabbitMQ-based message queue"""

text
def __init__(self, amqp_url: str):
    self.connection = await aio_pika.connect_robust(amqp_url)
    self.channel = await self.connection.channel()

async def send(self, message: Message) -> bool:
    """Send message to RabbitMQ"""
    exchange = await self.channel.declare_exchange(
        "agents",
        aio_pika.ExchangeType.DIRECT
    )
    
    msg_body = json.dumps(message.to_dict()).encode()
    
    await exchange.publish(
        aio_pika.Message(
            body=msg_body,
            priority=message.priority.value
        ),
        routing_key=message.recipient_id
    )
    
    return True

async def receive(
    self,
    timeout: Optional[float] = None
) -> Optional[Message]:
    """Receive from RabbitMQ"""
    queue = await self.channel.declare_queue(
        f"agent.{self.agent_id}"
    )
    
    try:
        async with async_timeout.timeout(timeout):
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        msg_dict = json.loads(message.body.decode())
                        return Message(**msg_dict)
    except asyncio.TimeoutError:
        return None
text

---

### Validation: MessageValidator

Static validation utilities for message integrity.

class MessageValidator:
"""
Message validation utilities.

text
Provides static methods for validating message structure
and content before sending/processing.
"""

@staticmethod
def validate_message(message: Message) -> bool:
    """
    Validate complete message structure.
    
    Args:
        message: Message to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If validation fails
    """
    # Check required fields
    if not message.sender_id:
        raise ValidationError("sender_id is required")
    
    if not message.recipient_id:
        raise ValidationError("recipient_id is required")
    
    # Validate message type
    if not isinstance(message.message_type, MessageType):
        raise ValidationError("Invalid message_type")
    
    # Validate priority
    if not isinstance(message.priority, MessagePriority):
        raise ValidationError("Invalid priority")
    
    # Validate payload
    if not MessageValidator.validate_payload(message.payload):
        raise ValidationError("Invalid payload")
    
    return True

@staticmethod
def validate_payload(payload: Dict[str, Any]) -> bool:
    """
    Validate payload structure.
    
    Args:
        payload: Payload dictionary to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If payload is invalid
    """
    # Check payload is a dictionary
    if not isinstance(payload, dict):
        raise ValidationError("Payload must be a dictionary")
    
    # Check payload is JSON-serializable
    try:
        json.dumps(payload, default=str)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Payload not JSON-serializable: {e}")
    
    return True
text

---

## 💡 Usage Examples

### Implementing Custom Protocol

from theaia.core.multi_agent.message.protocol import MessageProtocol
from theaia.core.multi_agent.message.types import Message
import asyncio
from typing import Optional

class CustomProtocol(MessageProtocol):
"""Custom protocol implementation"""

text
def __init__(self, config: dict):
    self.config = config
    self.queues = {}

async def send(self, message: Message) -> bool:
    """Send message using custom logic"""
    # Validate message
    MessageValidator.validate_message(message)
    
    # Get or create queue for recipient
    recipient_id = message.recipient_id
    if recipient_id not in self.queues:
        self.queues[recipient_id] = asyncio.Queue()
    
    # Send to queue
    await self.queues[recipient_id].put(message)
    
    # Mark as sent
    message.mark_sent()
    
    return True

async def receive(
    self,
    timeout: Optional[float] = None
) -> Optional[Message]:
    """Receive message using custom logic"""
    agent_id = self.config.get("agent_id")
    
    if agent_id not in self.queues:
        return None
    
    queue = self.queues[agent_id]
    
    try:
        if timeout:
            message = await asyncio.wait_for(
                queue.get(),
                timeout=timeout
            )
        else:
            message = await queue.get()
        
        # Mark as delivered
        message.mark_delivered()
        
        return message
        
    except asyncio.TimeoutError:
        return None
text

---

### Using Protocol with Broker

from theaia.core.multi_agent.message.broker import MessageBroker

Create broker with custom protocol
protocol = CustomProtocol(config={"agent_id": "agent1"})
broker = MessageBroker(protocol=protocol)

Register agent
broker.register_agent("agent1")

Send message
msg = Message(
sender_id="client",
recipient_id="agent1",
payload={"action": "process"}
)

success = await broker.send(msg)

Receive message
received = await broker.receive("agent1", timeout=5.0)

text

---

### Message Validation

from theaia.core.multi_agent.message.protocol import MessageValidator
from theaia.core.multi_agent.message.types import Message

def safe_send(protocol: MessageProtocol, message: Message) -> bool:
"""Send message with validation"""
try:
# Validate before sending
MessageValidator.validate_message(message)

text
    # Send if valid
    return await protocol.send(message)
    
except ValidationError as e:
    logger.error(f"Message validation failed: {e}")
    return False
text

---

### Payload Validation

from theaia.core.multi_agent.message.protocol import MessageValidator

def create_safe_message(
sender_id: str,
recipient_id: str,
payload: Dict[str, Any]
) -> Optional[Message]:
"""Create message with payload validation"""
try:
# Validate payload first
MessageValidator.validate_payload(payload)

text
    # Create message
    return Message(
        sender_id=sender_id,
        recipient_id=recipient_id,
        payload=payload
    )
    
except ValidationError as e:
    logger.error(f"Invalid payload: {e}")
    return None
Usage
msg = create_safe_message(
sender_id="agent1",
recipient_id="agent2",
payload={"action": "sync", "data": {...}}
)

if msg:
await protocol.send(msg)

text

---

### Error Handling

async def robust_send(
protocol: MessageProtocol,
message: Message,
max_retries: int = 3
) -> bool:
"""Send with validation and retry logic"""

text
# Validate first
try:
    MessageValidator.validate_message(message)
except ValidationError as e:
    logger.error(f"Invalid message: {e}")
    return False

# Attempt send with retries
for attempt in range(max_retries):
    try:
        success = await protocol.send(message)
        if success:
            return True
            
    except ConnectionError as e:
        if attempt < max_retries - 1:
            wait = 2 ** attempt
            logger.warning(
                f"Send failed (attempt {attempt + 1}/{max_retries}), "
                f"retrying in {wait}s: {e}"
            )
            await asyncio.sleep(wait)
        else:
            logger.error(f"Failed to send after {max_retries} attempts")
            return False

return False
text

---

### Protocol Factory

from typing import Dict, Type

class ProtocolFactory:
"""Factory for creating protocol instances"""

text
_protocols: Dict[str, Type[MessageProtocol]] = {}

@classmethod
def register(cls, name: str, protocol_class: Type[MessageProtocol]):
    """Register protocol implementation"""
    cls._protocols[name] = protocol_class

@classmethod
def create(cls, name: str, **kwargs) -> MessageProtocol:
    """Create protocol instance"""
    if name not in cls._protocols:
        raise ValueError(f"Unknown protocol: {name}")
    
    protocol_class = cls._protocols[name]
    return protocol_class(**kwargs)
Register implementations
ProtocolFactory.register("memory", InMemoryProtocol)
ProtocolFactory.register("redis", RedisProtocol)
ProtocolFactory.register("rabbitmq", RabbitMQProtocol)

Create protocol
protocol = ProtocolFactory.create(
"redis",
redis_url="redis://localhost:6379"
)

text

---

### Testing Protocol Implementations

import pytest

@pytest.mark.asyncio
async def test_protocol_send_receive():
"""Test basic send/receive"""
protocol = InMemoryProtocol()

text
# Create message
msg = Message(
    sender_id="agent1",
    recipient_id="agent2",
    payload={"test": "data"}
)

# Send
success = await protocol.send(msg)
assert success

# Receive
received = await protocol.receive(timeout=1.0)
assert received is not None
assert received.message_id == msg.message_id
@pytest.mark.asyncio
async def test_protocol_timeout():
"""Test receive timeout"""
protocol = InMemoryProtocol()

text
# Receive with timeout (no messages)
received = await protocol.receive(timeout=0.1)
assert received is None
@pytest.mark.asyncio
async def test_validation():
"""Test message validation"""
# Valid message
valid_msg = Message(
sender_id="agent1",
recipient_id="agent2",
payload={"data": "test"}
)
assert MessageValidator.validate_message(valid_msg)

text
# Invalid message (no sender)
invalid_msg = Message(
    sender_id="",
    recipient_id="agent2",
    payload={}
)
with pytest.raises(ValidationError):
    MessageValidator.validate_message(invalid_msg)
text

---

## 🔧 Custom Validation Rules

class ExtendedMessageValidator(MessageValidator):
"""Extended validator with custom rules"""

text
@staticmethod
def validate_message(message: Message) -> bool:
    """Validate with additional rules"""
    # Run base validation
    MessageValidator.validate_message(message)
    
    # Custom rules
    if message.message_type == MessageType.REQUEST:
        if "action" not in message.payload:
            raise ValidationError("REQUEST must have 'action' in payload")
    
    if message.priority == MessagePriority.CRITICAL:
        if "reason" not in message.metadata:
            raise ValidationError(
                "CRITICAL messages must have 'reason' in metadata"
            )
    
    # Validate timestamp not in future
    if message.timestamp > datetime.now():
        raise ValidationError("Message timestamp cannot be in future")
    
    return True
text

---

## 📊 Protocol Comparison

| Protocol | Latency | Throughput | Persistence | Complexity |
|----------|---------|------------|-------------|------------|
| **In-Memory** | < 1ms | Very High | ❌ No | Low |
| **Redis** | 1-5ms | High | ✅ Yes | Medium |
| **RabbitMQ** | 5-10ms | High | ✅ Yes | High |
| **Kafka** | 10-50ms | Very High | ✅ Yes | Very High |
| **gRPC** | 1-10ms | High | ❌ No | Medium |

---

## 🧪 Testing

**Test Coverage:** 42% (Included in broker tests)

### Key Test Areas

- ✅ Protocol interface contract
- ✅ Message validation
- ✅ Payload validation
- ✅ Error handling
- ⚠️ Timeout behavior (partial)
- ⚠️ Concurrent sends (partial)

---

## 📈 Performance Characteristics

- **Validation Time:** O(1) for structure, O(n) for payload serialization
- **Memory:** Minimal overhead (~100 bytes per validation)
- **Thread Safety:** Validators are stateless and thread-safe

---

## 🔄 Integration Points

### Used By
- `MessageBroker` - Primary protocol consumer
- Custom broker implementations
- Testing frameworks

### Dependencies
- `Message` - Message structure
- `MessageType`, `MessagePriority` - Enumerations
- `abc` - Abstract base class support

---

## 🚀 Future Enhancements

- [ ] Schema-based validation (JSON Schema, Protobuf)
- [ ] Message signing and verification
- [ ] Compression support interface
- [ ] Encryption protocol interface
- [ ] Batch message support
- [ ] Stream protocol support
- [ ] WebSocket protocol implementation
- [ ] HTTP protocol implementation

---

## 📝 Best Practices

### ✅ DO
- Always validate messages before sending
- Implement proper timeout handling
- Handle connection errors gracefully
- Use appropriate protocol for use case
- Test protocol implementations thoroughly

### ❌ DON'T
- Don't skip validation in production
- Don't ignore connection errors
- Don't block indefinitely on receive
- Don't assume message delivery
- Don't mix protocol implementations

---

## 🔍 Troubleshooting

### Validation Errors

**Symptom:** `ValidationError` raised on send

**Solutions:**
Check required fields
assert message.sender_id != ""
assert message.recipient_id != ""

Verify payload is serializable
import json
json.dumps(message.payload, default=str)

Use validator explicitly
try:
MessageValidator.validate_message(message)
except ValidationError as e:
print(f"Validation failed: {e}")

text

---

### Protocol Not Receiving Messages

**Symptom:** `receive()` returns None or times out

**Causes:**
- No messages in queue
- Wrong recipient_id
- Protocol not connected

**Solutions:**
Check queue status
if hasattr(protocol, 'queue'):
print(f"Queue size: {protocol.queue.qsize()}")

Verify recipient_id
print(f"Expecting messages for: {agent_id}")

Test with longer timeout
msg = await protocol.receive(timeout=30.0)

text

---

### Connection Errors

**Symptom:** `ConnectionError` on send

**Solutions:**
Implement retry logic
async def send_with_retry(protocol, message, max_retries=3):
for i in range(max_retries):
try:
return await protocol.send(message)
except ConnectionError:
if i < max_retries - 1:
await asyncio.sleep(2 ** i)
else:
raise

Add connection health check
async def check_connection(protocol):
try:
test_msg = Message(
sender_id="system",
recipient_id="health-check",
payload={}
)
await protocol.send(test_msg)
return True
except:
return False

text

---

## 📚 References

- [Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [asyncio Queues](https://docs.python.org/3/library/asyncio-queue.html)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
- [RabbitMQ Tutorial](https://www.rabbitmq.com/getstarted.html)

---
