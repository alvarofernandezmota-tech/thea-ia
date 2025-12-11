# Message Types Module - Summary

**File:** `src/theaia/core/multi_agent/message/types.py`  
**Author:** Álvaro Fernández Mota  
**Date:** 11 December 2025  
**Version:** 1.0.0  
**Lines of Code:** 130  
**Test Coverage:** 64%

---

## 📋 Purpose

Defines core message structures, types, and priorities for inter-agent communication in the multi-agent system. Provides complete message lifecycle tracking and serialization support.

---

## 🎯 Key Features

- ✅ **Type-safe Messages** - Strongly typed message structures
- ✅ **Priority Levels** - 4-level priority system
- ✅ **Status Tracking** - Complete message lifecycle states
- ✅ **Correlation Support** - Request-response correlation
- ✅ **Metadata Extensibility** - Custom metadata per message
- ✅ **Serialization** - JSON-compatible dictionary conversion

---

## 🏗️ Components

### Enumerations

#### `MessageType`

Categories of messages in the system.

| Type | Description | Direction | Example Use Case |
|------|-------------|-----------|------------------|
| `REQUEST` | Request for action/data | Client → Agent | "Create event" |
| `RESPONSE` | Response to request | Agent → Client | "Event created" |
| `EVENT` | Notification of state change | Agent → System | "Task completed" |
| `COMMAND` | Direct command | System → Agent | "Shutdown" |
| `NOTIFICATION` | Informational broadcast | System → All | "Maintenance mode" |

**Example:**
from theaia.core.multi_agent.message.types import MessageType

Request-response pattern
request = Message(
message_type=MessageType.REQUEST,
sender_id="orchestrator",
recipient_id="calendar-agent-1",
payload={"action": "create_event", "title": "Meeting"}
)

response = Message(
message_type=MessageType.RESPONSE,
sender_id="calendar-agent-1",
recipient_id="orchestrator",
correlation_id=request.message_id, # Link to request
payload={"status": "success", "event_id": "evt123"}
)

text

---

#### `MessagePriority`

Priority levels for message processing and queue ordering.

| Priority | Level | Use Case | Processing Order |
|----------|-------|----------|------------------|
| `LOW` | 1 | Background jobs, cleanup | Last |
| `NORMAL` | 2 | Standard operations | Default |
| `HIGH` | 3 | Important user requests | Prioritized |
| `CRITICAL` | 4 | System critical, urgent tasks | First |

**Example:**
from theaia.core.multi_agent.message.types import MessagePriority

Normal user request
user_request = Message(
message_type=MessageType.REQUEST,
priority=MessagePriority.NORMAL,
...
)

Critical system command
shutdown_cmd = Message(
message_type=MessageType.COMMAND,
priority=MessagePriority.CRITICAL,
payload={"command": "shutdown", "reason": "emergency"}
)

Background cleanup
cleanup_request = Message(
message_type=MessageType.REQUEST,
priority=MessagePriority.LOW,
payload={"action": "cleanup_logs"}
)

text

---

#### `MessageStatus`

Message lifecycle states for tracking.

| Status | Description | Terminal? | Next States |
|--------|-------------|-----------|-------------|
| `PENDING` | Created, not sent yet | ❌ | SENT, FAILED |
| `SENT` | Sent to recipient | ❌ | DELIVERED, FAILED |
| `DELIVERED` | Received by recipient | ❌ | PROCESSED, FAILED |
| `PROCESSED` | Successfully processed | ✅ | - |
| `FAILED` | Processing failed | ✅ | - |

**State Transition Diagram:**
PENDING → SENT → DELIVERED → PROCESSED
↓ ↓ ↓
└────────┴─────────┴────→ FAILED

text

**Example:**
message = Message(...)
print(message.status) # PENDING

await broker.send(message)
message.mark_sent()
print(message.status) # SENT

Agent receives message
message.mark_delivered()
print(message.status) # DELIVERED

Agent processes message
message.mark_processed()
print(message.status) # PROCESSED

text

---

### Dataclass: Message

Complete message structure with metadata and lifecycle tracking.

@dataclass
class Message:
# Identity
message_id: str = field(default_factory=lambda: str(uuid4()))
message_type: MessageType = MessageType.REQUEST

text
# Routing
sender_id: str = ""
recipient_id: str = ""

# Content
payload: Dict[str, Any] = field(default_factory=dict)

# Priority & Status
priority: MessagePriority = MessagePriority.NORMAL
status: MessageStatus = MessageStatus.PENDING

# Timing
timestamp: datetime = field(default_factory=datetime.now)

# Correlation & Reply
correlation_id: Optional[str] = None
reply_to: Optional[str] = None

# Metadata
metadata: Dict[str, Any] = field(default_factory=dict)
text

---

## 📊 Message Attributes

### Core Identity

#### `message_id`
- **Type:** `str`
- **Default:** Auto-generated UUID4
- **Purpose:** Unique identifier for message
- **Immutable:** Should not be changed after creation

**Example:**
msg = Message(sender_id="agent1", recipient_id="agent2")
print(msg.message_id) # "f47ac10b-58cc-4372-a567-0e02b2c3d479"

text

---

#### `message_type`
- **Type:** `MessageType`
- **Default:** `MessageType.REQUEST`
- **Purpose:** Categorize message for routing and processing

**Example:**
Request
request_msg = Message(
message_type=MessageType.REQUEST,
payload={"action": "get_events"}
)

Event notification
event_msg = Message(
message_type=MessageType.EVENT,
payload={"event": "task_completed", "task_id": "task123"}
)

text

---

### Routing Information

#### `sender_id`
- **Type:** `str`
- **Required:** Yes
- **Purpose:** Identify message sender
- **Format:** Agent ID, system component ID, or user ID

#### `recipient_id`
- **Type:** `str`
- **Required:** Yes (except for broadcasts)
- **Purpose:** Target recipient for message
- **Special Values:**
  - `"*"` - Broadcast to all agents
  - `"system"` - System-level message

**Example:**
Point-to-point
msg = Message(
sender_id="orchestrator",
recipient_id="calendar-agent-1",
payload={"action": "sync"}
)

Broadcast
broadcast = Message(
sender_id="system",
recipient_id="*",
message_type=MessageType.NOTIFICATION,
payload={"message": "System maintenance in 5 minutes"}
)

text

---

### Content

#### `payload`
- **Type:** `Dict[str, Any]`
- **Default:** `{}`
- **Purpose:** Message data/parameters
- **Format:** JSON-serializable dictionary

**Common Patterns:**

**Task Request:**
payload = {
"task_id": "task123",
"task_type": "calendar_management",
"action": "create_event",
"parameters": {
"title": "Team Meeting",
"start_time": "2025-12-11T15:00:00",
"duration_minutes": 60
}
}

text

**Response:**
payload = {
"status": "success",
"result": {
"event_id": "evt789",
"created_at": "2025-12-11T14:30:00"
}
}

text

**Error:**
payload = {
"status": "error",
"error_code": "CALENDAR_API_ERROR",
"error_message": "Failed to connect to calendar service",
"retry_after": 60
}

text

---

### Priority & Status

#### `priority`
- **Type:** `MessagePriority`
- **Default:** `MessagePriority.NORMAL`
- **Purpose:** Queue ordering and processing priority

**Example:**
User request - normal priority
user_msg = Message(
priority=MessagePriority.NORMAL,
payload={"action": "list_events"}
)

System alert - critical priority
alert_msg = Message(
priority=MessagePriority.CRITICAL,
payload={"alert": "disk_space_critical"}
)

text

---

#### `status`
- **Type:** `MessageStatus`
- **Default:** `MessageStatus.PENDING`
- **Purpose:** Track message lifecycle
- **Mutable:** Changes as message progresses

---

### Timing

#### `timestamp`
- **Type:** `datetime`
- **Default:** `datetime.now()`
- **Purpose:** Message creation time
- **Timezone:** UTC recommended

**Example:**
from datetime import datetime, timezone

msg = Message(
timestamp=datetime.now(timezone.utc),
payload={"data": "test"}
)

Check message age
age = datetime.now(timezone.utc) - msg.timestamp
print(f"Message age: {age.total_seconds()} seconds")

text

---

### Correlation & Reply

#### `correlation_id`
- **Type:** `Optional[str]`
- **Default:** `None`
- **Purpose:** Link response to original request
- **Pattern:** Set to `message_id` of original request

**Request-Response Pattern:**
1. Client sends request
request = Message(
message_id="req-123",
message_type=MessageType.REQUEST,
sender_id="client",
recipient_id="agent1",
payload={"action": "process_data"}
)

2. Agent sends response
response = Message(
message_type=MessageType.RESPONSE,
sender_id="agent1",
recipient_id="client",
correlation_id="req-123", # Link to request
payload={"status": "success", "result": {...}}
)

3. Client correlates response
if response.correlation_id == request.message_id:
print("Response received for request")

text

---

#### `reply_to`
- **Type:** `Optional[str]`
- **Default:** `None`
- **Purpose:** Specify alternate reply destination
- **Use Case:** Async callbacks, proxy patterns

**Example:**
Request with custom reply destination
request = Message(
sender_id="proxy",
recipient_id="agent1",
reply_to="original-client", # Reply should go here
payload={"action": "query"}
)

Agent replies to specified destination
response = Message(
sender_id="agent1",
recipient_id=request.reply_to, # Use reply_to
correlation_id=request.message_id,
payload={"result": "data"}
)

text

---

### Metadata

#### `metadata`
- **Type:** `Dict[str, Any]`
- **Default:** `{}`
- **Purpose:** Extensible custom data
- **Use Cases:** Tracing, debugging, custom routing

**Common Metadata:**
metadata = {
# Tracing
"trace_id": "trace-xyz-789",
"span_id": "span-abc-123",

text
# User context
"user_id": "user123",
"session_id": "session456",

# Routing hints
"timeout_ms": 5000,
"retry_count": 0,
"max_retries": 3,

# Custom data
"environment": "production",
"api_version": "v2"
}

msg = Message(
payload={"action": "process"},
metadata=metadata
)

text

---

## 📋 Message Methods

### State Transitions

#### `mark_sent()`
def mark_sent(self) -> None:
"""Mark message as sent"""
self.status = MessageStatus.SENT

text

#### `mark_delivered()`
def mark_delivered(self) -> None:
"""Mark message as delivered to recipient"""
self.status = MessageStatus.DELIVERED

text

#### `mark_processed()`
def mark_processed(self) -> None:
"""Mark message as successfully processed"""
self.status = MessageStatus.PROCESSED

text

#### `mark_failed()`
def mark_failed(self, error: str) -> None:
"""
Mark message as failed.

text
Args:
    error: Error description
"""
self.status = MessageStatus.FAILED
self.metadata["error"] = error
text

**Example:**
msg = Message(
sender_id="agent1",
recipient_id="agent2",
payload={"action": "sync"}
)

try:
# Send message
await broker.send(msg)
msg.mark_sent()

text
# Message delivered
msg.mark_delivered()

# Process message
result = await process(msg)
msg.mark_processed()
except Exception as e:
msg.mark_failed(str(e))
logger.error(f"Message failed: {e}")

text

---

### Type Checking

#### `is_request()`
def is_request(self) -> bool:
"""Check if message is a REQUEST"""
return self.message_type == MessageType.REQUEST

text

#### `is_response()`
def is_response(self) -> bool:
"""Check if message is a RESPONSE"""
return self.message_type == MessageType.RESPONSE

text

**Example:**
def handle_message(msg: Message):
if msg.is_request():
# Process request
result = process_request(msg.payload)

text
    # Send response
    response = Message(
        message_type=MessageType.RESPONSE,
        sender_id="agent",
        recipient_id=msg.sender_id,
        correlation_id=msg.message_id,
        payload={"result": result}
    )
    return response

elif msg.is_response():
    # Handle response
    handle_response(msg)
text

---

### Serialization

#### `to_dict()`
def to_dict(self) -> Dict[str, Any]:
"""
Convert message to dictionary representation.

text
Returns:
    JSON-serializable dictionary
"""
text

**Response Structure:**
{
"message_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
"message_type": "REQUEST",
"sender_id": "agent1",
"recipient_id": "agent2",
"payload": {"action": "sync"},
"priority": "NORMAL",
"status": "PENDING",
"timestamp": "2025-12-11T15:30:00.000000",
"correlation_id": null,
"reply_to": null,
"metadata": {}
}

text

**Example:**
import json

msg = Message(
sender_id="agent1",
recipient_id="agent2",
payload={"action": "test"}
)

Serialize to JSON
msg_dict = msg.to_dict()
json_str = json.dumps(msg_dict, default=str)

Send over network
send_to_network(json_str)

Deserialize
received_dict = json.loads(json_str)
received_msg = Message(**received_dict)

text

---

## 💡 Usage Examples

### Basic Message Creation

from theaia.core.multi_agent.message.types import (
Message,
MessageType,
MessagePriority
)

Simple request
msg = Message(
message_type=MessageType.REQUEST,
sender_id="orchestrator",
recipient_id="calendar-agent-1",
payload={
"action": "create_event",
"title": "Project Review",
"date": "2025-12-15"
}
)

print(f"Message ID: {msg.message_id}")
print(f"Status: {msg.status}") # PENDING
print(f"Priority: {msg.priority}") # NORMAL

text

---

### Request-Response Pattern

1. Create request
request = Message(
message_type=MessageType.REQUEST,
sender_id="client",
recipient_id="agent",
payload={"query": "get_user_data", "user_id": "user123"}
)

2. Send and track
await broker.send(request)
request.mark_sent()

3. Wait for response
response = await broker.receive("client", timeout=10.0)

4. Verify correlation
if response and response.correlation_id == request.message_id:
if response.payload.get("status") == "success":
data = response.payload.get("data")
print(f"Data received: {data}")
else:
error = response.payload.get("error")
print(f"Error: {error}")

text

---

### Event Broadcasting

System broadcasts maintenance notification
maintenance_event = Message(
message_type=MessageType.NOTIFICATION,
sender_id="system",
recipient_id="*", # Broadcast to all
priority=MessagePriority.HIGH,
payload={
"event": "maintenance_scheduled",
"start_time": "2025-12-11T22:00:00",
"duration_minutes": 30,
"message": "System will be unavailable"
}
)

await broker.broadcast(maintenance_event)

text

---

### Priority Queue Processing

import heapq

class MessageQueue:
def init(self):
self.queue = []

text
def enqueue(self, msg: Message):
    # Use negative priority for max-heap (highest priority first)
    heapq.heappush(
        self.queue,
        (-msg.priority.value, msg.timestamp, msg)
    )

def dequeue(self) -> Optional[Message]:
    if self.queue:
        _, _, msg = heapq.heappop(self.queue)
        return msg
    return None
Usage
queue = MessageQueue()

queue.enqueue(Message(priority=MessagePriority.NORMAL, ...))
queue.enqueue(Message(priority=MessagePriority.CRITICAL, ...))
queue.enqueue(Message(priority=MessagePriority.LOW, ...))

Dequeue in priority order: CRITICAL, NORMAL, LOW
msg = queue.dequeue()
print(msg.priority) # CRITICAL

text

---

### Message Tracing

def create_traced_message(
sender_id: str,
recipient_id: str,
payload: Dict[str, Any],
trace_id: Optional[str] = None
) -> Message:
"""Create message with tracing metadata"""

text
if trace_id is None:
    trace_id = str(uuid4())

return Message(
    sender_id=sender_id,
    recipient_id=recipient_id,
    payload=payload,
    metadata={
        "trace_id": trace_id,
        "span_id": str(uuid4()),
        "parent_span_id": None,
        "timestamp_created": datetime.now().isoformat()
    }
)
Create traced request
msg = create_traced_message(
sender_id="client",
recipient_id="agent1",
payload={"action": "process"}
)

print(f"Trace ID: {msg.metadata['trace_id']}")

text

---

### Error Handling Pattern

async def safe_send_message(
broker: MessageBroker,
msg: Message,
max_retries: int = 3
) -> bool:
"""Send message with retry logic"""

text
for attempt in range(max_retries):
    try:
        await broker.send(msg)
        msg.mark_sent()
        return True
        
    except ConnectionError as e:
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(
                f"Send failed (attempt {attempt + 1}/{max_retries}), "
                f"retrying in {wait_time}s: {e}"
            )
            await asyncio.sleep(wait_time)
        else:
            msg.mark_failed(f"Max retries exceeded: {e}")
            logger.error(f"Failed to send message {msg.message_id}")
            return False

return False
text

---

## 🧪 Testing

**Test Coverage:** Included in `tests/unit/multi_agent/test_broker.py`

### Test Examples

import pytest
from theaia.core.multi_agent.message.types import (
Message,
MessageType,
MessagePriority,
MessageStatus
)

def test_message_creation():
"""Test basic message creation"""
msg = Message(
sender_id="agent1",
recipient_id="agent2",
payload={"test": "data"}
)

text
assert msg.message_id is not None
assert msg.message_type == MessageType.REQUEST
assert msg.priority == MessagePriority.NORMAL
assert msg.status == MessageStatus.PENDING
def test_state_transitions():
"""Test message state transitions"""
msg = Message(sender_id="a", recipient_id="b")

text
assert msg.status == MessageStatus.PENDING

msg.mark_sent()
assert msg.status == MessageStatus.SENT

msg.mark_delivered()
assert msg.status == MessageStatus.DELIVERED

msg.mark_processed()
assert msg.status == MessageStatus.PROCESSED
def test_correlation():
"""Test request-response correlation"""
request = Message(
message_type=MessageType.REQUEST,
sender_id="client",
recipient_id="agent"
)

text
response = Message(
    message_type=MessageType.RESPONSE,
    sender_id="agent",
    recipient_id="client",
    correlation_id=request.message_id
)

assert response.correlation_id == request.message_id
assert response.is_response()
assert request.is_request()
text

---

## 📈 Performance Characteristics

- **Memory:** ~500 bytes per message (excluding payload)
- **Creation Time:** O(1)
- **Serialization:** O(n) where n = payload size
- **Type Checking:** O(1)

---

## 🔄 Integration Points

### Used By
- `MessageBroker` - Message routing and delivery
- `TaskDelegator` - Task-to-message conversion
- `AgentBase` - Message handling in agents

### Dependencies
- `uuid` - Message ID generation
- `datetime` - Timestamp management
- `dataclasses` - Structure definition
- `enum` - Type/priority/status enums

---

## 🚀 Future Enhancements

- [ ] Message compression for large payloads
- [ ] Built-in encryption support
- [ ] Message versioning
- [ ] TTL (time-to-live) support
- [ ] Automatic retry metadata
- [ ] Message batching support
- [ ] Schema validation

---

## 📝 Best Practices

### ✅ DO
- Use correlation_id for request-response patterns
- Set appropriate priority levels
- Include trace_id in metadata for debugging
- Use payload for data, metadata for control info
- Mark status transitions accurately

### ❌ DON'T
- Don't modify message_id after creation
- Don't store large binary data in payload
- Don't use metadata for business logic
- Don't forget to set sender_id and recipient_id
- Don't reuse message instances

---