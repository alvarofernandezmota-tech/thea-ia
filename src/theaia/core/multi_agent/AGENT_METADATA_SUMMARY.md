# Agent Metadata Module - Summary

**File:** `src/theaia/core/multi_agent/agent_metadata.py`  
**Author:** Álvaro Fernández Mota  
**Date:** 11 December 2025  
**Version:** 1.0.0  
**Lines of Code:** 200  
**Test Coverage:** 73%

---

## 📋 Purpose

Defines data structures and enumerations for representing agents in the multi-agent system. Provides metadata, capabilities, performance metrics, and health status for each agent.

---

## 🎯 Key Components

### Enumerations

#### `AgentStatus`
Agent health states.

| Value | Description |
|-------|-------------|
| `HEALTHY` | Agent operating normally |
| `DEGRADED` | Agent experiencing issues |
| `UNAVAILABLE` | Agent not responding |
| `MAINTENANCE` | Agent in maintenance mode |

#### `AgentCapability`
Agent functional capabilities.

| Value | Description |
|-------|-------------|
| `CALENDAR_MANAGEMENT` | Manage calendar events |
| `EVENT_CREATION` | Create new events |
| `EVENT_MODIFICATION` | Modify existing events |
| `EVENT_DELETION` | Delete events |
| `NOTE_MANAGEMENT` | Manage notes |
| `REMINDER_MANAGEMENT` | Manage reminders |
| `QUERY_PROCESSING` | Process queries |
| `NOTIFICATION_SENDING` | Send notifications |

---

### Dataclasses

#### `PerformanceMetrics`
Performance tracking for agents.

**Attributes:**
- `average_response_time: float` - Average response time in seconds
- `total_requests: int` - Total requests processed
- `successful_requests: int` - Successfully completed requests
- `failed_requests: int` - Failed requests

**Calculated Properties:**
@property
def success_rate(self) -> float:
"""Success rate (0.0 to 1.0)"""

@property
def error_rate(self) -> float:
"""Error rate (0.0 to 1.0)"""

text

---

#### `AgentMetadata`
Complete agent metadata and state.

**Core Attributes:**
agent_id: str # Unique identifier
agent_type: str # Agent type/class
version: str = "1.0.0" # Agent version
capabilities: Set[AgentCapability] # Agent capabilities

text

**Status & Load:**
status: AgentStatus = AgentStatus.HEALTHY # Current health status
current_load: int = 0 # Current task load
max_capacity: int = 10 # Maximum concurrent tasks
priority: int = 0 # Priority level (higher = more priority)

text

**Metrics & Monitoring:**
metrics: PerformanceMetrics # Performance metrics
last_heartbeat: datetime # Last heartbeat timestamp
heartbeat_interval_seconds: int = 60 # Expected heartbeat interval

text

**Configuration:**
tags: Dict[str, str] # Custom metadata tags
metadata: Dict[str, Any] # Additional metadata

text

---

## 🔧 Calculated Properties

### `load_percentage`
@property
def load_percentage(self) -> float:
"""Current load as percentage (0.0 to 100.0)"""
return (self.current_load / self.max_capacity) * 100

text

### `available_capacity`
@property
def available_capacity(self) -> int:
"""Available capacity for new tasks"""
return max(0, self.max_capacity - self.current_load)

text

### `is_available`
@property
def is_available(self) -> bool:
"""Agent is healthy and has capacity"""
return (
self.status == AgentStatus.HEALTHY and
self.current_load < self.max_capacity
)

text

### `is_overloaded`
@property
def is_overloaded(self) -> bool:
"""Agent is at or above capacity"""
return self.current_load >= self.max_capacity

text

---

## 📊 Methods

### Capability Management

def has_capability(self, capability: AgentCapability) -> bool:
"""Check if agent has specific capability"""

def add_capability(self, capability: AgentCapability) -> None:
"""Add new capability to agent"""

def remove_capability(self, capability: AgentCapability) -> None:
"""Remove capability from agent"""

text

### Load Management

def increment_load(self) -> None:
"""Increment current load (max: max_capacity)"""

def decrement_load(self) -> None:
"""Decrement current load (min: 0)"""

text

### Heartbeat

def update_heartbeat(self) -> None:
"""Update last heartbeat timestamp to now"""

text

### Performance Metrics

def update_metrics(self, response_time: float, success: bool) -> None:
"""
Update performance metrics with new request data.

text
Args:
    response_time: Request response time in seconds
    success: Whether request was successful
"""
text

### Serialization

def to_dict(self) -> Dict[str, Any]:
"""Convert to dictionary representation"""

text

---

## 💡 Usage Examples

### Create Agent Metadata

from theaia.core.multi_agent.agent_metadata import (
AgentMetadata,
AgentCapability,
AgentStatus,
PerformanceMetrics
)

agent = AgentMetadata(
agent_id="calendar-agent-1",
agent_type="CalendarAgent",
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.EVENT_CREATION
},
max_capacity=10,
priority=1,
tags={"environment": "production", "region": "us-east-1"}
)

text

### Check Availability

if agent.is_available:
print(f"Agent has {agent.available_capacity} slots available")
print(f"Current load: {agent.load_percentage:.1f}%")

text

### Manage Load

Assign task
agent.increment_load()
print(f"Load: {agent.current_load}/{agent.max_capacity}")

Complete task
agent.decrement_load()

text

### Track Performance

Record successful request
agent.update_metrics(response_time=0.5, success=True)

Record failed request
agent.update_metrics(response_time=2.0, success=False)

Check metrics
print(f"Success rate: {agent.metrics.success_rate:.2%}")
print(f"Avg response time: {agent.metrics.average_response_time:.3f}s")

text

### Update Heartbeat

Keep agent alive
agent.update_heartbeat()

Check last heartbeat
from datetime import datetime, timedelta
time_since_heartbeat = datetime.now() - agent.last_heartbeat

if time_since_heartbeat > timedelta(seconds=agent.heartbeat_interval_seconds):
print("Agent heartbeat is stale!")

text

---

## 🧪 Testing

**Test File:** `tests/unit/multi_agent/test_agent_metadata.py`  
**Total Tests:** 26  
**Status:** ✅ All passing

### Test Coverage

- ✅ Initialization and validation
- ✅ Calculated properties
- ✅ Capability management
- ✅ Load management with boundaries
- ✅ Heartbeat updates
- ✅ Performance metrics calculation
- ✅ Serialization

---

## 🔒 Validations

### On Creation
- `agent_type` cannot be empty
- `max_capacity` must be > 0
- `heartbeat_interval_seconds` must be > 0

### Runtime Constraints
- `current_load` cannot go negative
- `current_load` cannot exceed `max_capacity`
- Performance metrics maintain running averages

---

## 📈 Performance Characteristics

- **Memory:** ~2KB per agent instance
- **CPU:** O(1) for all operations
- **Thread Safety:** Not thread-safe (use AgentRegistry for thread-safe operations)

---

## 🔄 Integration Points

### Used By
- `AgentRegistry` - Stores and manages agent metadata
- `DiscoveryService` - Queries agent capabilities and status
- `TaskDelegator` - Checks agent availability for task assignment

### Dependencies
- `datetime` - Timestamp management
- `enum.Enum` - Status and capability enumerations
- `dataclasses` - Structure definitions

---

## 📝 Notes

- Agents start with `status=HEALTHY` and `current_load=0`
- Heartbeat must be updated regularly to avoid stale detection
- Performance metrics use exponential moving average for response time
- Tags can be used for custom filtering in discovery queries

---

## 🚀 Future Enhancements

- [ ] Add circuit breaker state tracking
- [ ] Implement rate limiting metadata
- [ ] Add historical performance data
- [ ] Support for agent versioning and upgrades
- [ ] Add resource utilization metrics (CPU, memory)
