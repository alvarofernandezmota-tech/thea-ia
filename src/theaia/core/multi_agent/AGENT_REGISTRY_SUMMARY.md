# Agent Registry Module - Summary

**File:** `src/theaia/core/multi_agent/agent_registry.py`  
**Author:** Álvaro Fernández Mota  
**Date:** 11 December 2025  
**Version:** 1.0.0  
**Lines of Code:** 260  
**Test Coverage:** 50%

---

## 📋 Purpose

Centralized, thread-safe registry for managing agent lifecycle in the multi-agent system. Implements the **Singleton pattern** to ensure a single source of truth for all agent metadata.

---

## 🎯 Key Features

- ✅ **Thread-safe Singleton** - Single global instance with lock protection
- ✅ **Multiple Indexes** - Fast lookups by ID, type, and capability
- ✅ **Lifecycle Management** - Register, unregister, update agents
- ✅ **Health Monitoring** - Track heartbeats and detect stale agents
- ✅ **Load Balancing Support** - Track and update agent load in real-time

---

## 🏗️ Architecture

### Design Pattern: Singleton

class AgentRegistry:
_instance = None
_lock = threading.Lock()

text
def __new__(cls):
    if cls._instance is None:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
    return cls._instance
text

**Why Singleton?**
- Single source of truth for all agents
- Consistent state across the application
- Thread-safe access from multiple components

---

### Internal Data Structures

Primary storage
self._agents: Dict[str, AgentMetadata] = {}

Indexes for fast lookup
self._agents_by_type: Dict[str, List[str]] = defaultdict(list)
self._agents_by_capability: Dict[AgentCapability, List[str]] = defaultdict(list)

Thread safety
self._lock: threading.Lock = threading.Lock()

text

---

## 📊 Core Methods

### Registration

#### `register()`
def register(
self,
metadata: AgentMetadata,
force: bool = False
) -> str:
"""
Register new agent or update existing (with force=True).

text
Args:
    metadata: Agent metadata to register
    force: If True, overwrite existing agent with same ID
    
Returns:
    agent_id: ID of registered agent
    
Raises:
    RegistrationError: If agent_id already exists and force=False
"""
text

**Example:**
from theaia.core.multi_agent.agent_registry import AgentRegistry
from theaia.core.multi_agent.agent_metadata import AgentMetadata, AgentCapability

registry = AgentRegistry()

agent = AgentMetadata(
agent_id="calendar-agent-1",
agent_type="CalendarAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

Register new agent
agent_id = registry.register(agent)

Update existing agent
agent.max_capacity = 20
agent_id = registry.register(agent, force=True)

text

---

#### `unregister()`
def unregister(self, agent_id: str) -> bool:
"""
Remove agent from registry.

text
Args:
    agent_id: ID of agent to remove
    
Returns:
    True if agent was removed, False if not found
"""
text

**Example:**
success = registry.unregister("calendar-agent-1")
if success:
print("Agent removed successfully")

text

---

### Retrieval

#### `get()` / `get_agent()` 
def get(self, agent_id: str) -> Optional[AgentMetadata]:
"""Get agent by ID"""

def get_agent(self, agent_id: str) -> Optional[AgentMetadata]:
"""Alias for get() - compatibility method"""

text

**Example:**
agent = registry.get("calendar-agent-1")

or
agent = registry.get_agent("calendar-agent-1")

if agent:
print(f"Agent status: {agent.status}")

text

---

#### `get_all()`
def get_all(self) -> List[AgentMetadata]:
"""Get all registered agents"""

text

**Example:**
all_agents = registry.get_all()
print(f"Total agents: {len(all_agents)}")

for agent in all_agents:
print(f"- {agent.agent_id}: {agent.status}")

text

---

#### `get_by_type()`
def get_by_type(self, agent_type: str) -> List[AgentMetadata]:
"""Get all agents of specific type"""

text

**Example:**
calendar_agents = registry.get_by_type("CalendarAgent")
print(f"Found {len(calendar_agents)} calendar agents")

text

---

#### `get_by_capability()`
def get_by_capability(
self,
capability: AgentCapability
) -> List[AgentMetadata]:
"""Get all agents with specific capability"""

text

**Example:**
from theaia.core.multi_agent.agent_metadata import AgentCapability

event_agents = registry.get_by_capability(AgentCapability.EVENT_CREATION)
print(f"Found {len(event_agents)} agents that can create events")

text

---

### Status Management

#### `update_status()`
def update_status(
self,
agent_id: str,
status: AgentStatus
) -> bool:
"""
Update agent health status.

text
Args:
    agent_id: ID of agent to update
    status: New status
    
Returns:
    True if updated, False if agent not found
"""
text

**Example:**
from theaia.core.multi_agent.agent_metadata import AgentStatus

Mark agent as degraded
registry.update_status("calendar-agent-1", AgentStatus.DEGRADED)

Mark agent as healthy again
registry.update_status("calendar-agent-1", AgentStatus.HEALTHY)

Put agent in maintenance
registry.update_status("calendar-agent-1", AgentStatus.MAINTENANCE)

text

---

### Load Management

#### `increment_load()`
def increment_load(self, agent_id: str) -> bool:
"""
Increment agent's current load by 1.

text
Args:
    agent_id: ID of agent
    
Returns:
    True if incremented, False if agent not found
"""
text

#### `decrement_load()`
def decrement_load(self, agent_id: str) -> bool:
"""
Decrement agent's current load by 1.

text
Args:
    agent_id: ID of agent
    
Returns:
    True if decremented, False if agent not found
"""
text

**Example:**
Task assigned to agent
registry.increment_load("calendar-agent-1")
agent = registry.get("calendar-agent-1")
print(f"Current load: {agent.current_load}/{agent.max_capacity}")

Task completed
registry.decrement_load("calendar-agent-1")

text

---

### Heartbeat Management

#### `update_heartbeat()`
def update_heartbeat(self, agent_id: str) -> bool:
"""
Update agent's heartbeat timestamp to now.

text
Args:
    agent_id: ID of agent
    
Returns:
    True if updated, False if agent not found
"""
text

**Example:**
Agent sends heartbeat every 30 seconds
import asyncio

async def heartbeat_loop(agent_id: str):
while True:
registry.update_heartbeat(agent_id)
await asyncio.sleep(30)

text

---

#### `check_stale_heartbeats()`
def check_stale_heartbeats(
self,
timeout_seconds: Optional[int] = None
) -> List[str]:
"""
Find agents with stale heartbeats.

text
Args:
    timeout_seconds: Custom timeout (uses agent's interval if None)
    
Returns:
    List of agent IDs with stale heartbeats
"""
text

**Example:**
stale_agents = registry.check_stale_heartbeats()

if stale_agents:
print(f"⚠️ Stale agents detected: {stale_agents}")

text
for agent_id in stale_agents:
    registry.update_status(agent_id, AgentStatus.UNAVAILABLE)
text

---

#### `mark_stale_as_unavailable()`
def mark_stale_as_unavailable(
self,
timeout_seconds: Optional[int] = None
) -> int:
"""
Mark all stale agents as UNAVAILABLE.

text
Args:
    timeout_seconds: Custom timeout (uses agent's interval if None)
    
Returns:
    Number of agents marked as unavailable
"""
text

**Example:**
Run periodically to detect dead agents
count = registry.mark_stale_as_unavailable()
if count > 0:
print(f"Marked {count} agents as unavailable")

text

---

### Health Queries

#### `get_healthy_agents()`
def get_healthy_agents(self) -> List[AgentMetadata]:
"""Get all agents with status=HEALTHY"""

text

#### `get_available_agents()`
def get_available_agents(self) -> List[AgentMetadata]:
"""Get all agents that are healthy AND have capacity"""

text

**Example:**
Get only healthy agents
healthy = registry.get_healthy_agents()
print(f"Healthy agents: {len(healthy)}")

Get agents ready to accept tasks
available = registry.get_available_agents()
print(f"Available agents: {len(available)}")

for agent in available:
print(f"- {agent.agent_id}: {agent.available_capacity} slots free")

text

---

### Statistics

#### `get_count()`
def get_count(self) -> int:
"""Total number of registered agents"""

text

#### `get_count_by_status()`
def get_count_by_status(self, status: AgentStatus) -> int:
"""Count agents with specific status"""

text

#### `get_total_capacity()`
def get_total_capacity(self) -> int:
"""Sum of max_capacity across all agents"""

text

#### `get_used_capacity()`
def get_used_capacity(self) -> int:
"""Sum of current_load across all agents"""

text

**Example:**
print(f"Total agents: {registry.get_count()}")
print(f"Healthy: {registry.get_count_by_status(AgentStatus.HEALTHY)}")
print(f"Degraded: {registry.get_count_by_status(AgentStatus.DEGRADED)}")
print(f"Capacity: {registry.get_used_capacity()}/{registry.get_total_capacity()}")

text

---

### Maintenance

#### `clear()`
def clear(self) -> None:
"""Remove all agents from registry"""

text

**Example:**
Clear all agents (useful for testing)
registry.clear()
assert registry.get_count() == 0

text

---

## 🔒 Thread Safety

All public methods are **thread-safe** using `threading.Lock`:

def register(self, metadata: AgentMetadata, force: bool = False) -> str:
with self._lock:
# Critical section protected
...

text

### Concurrent Access Example

import threading

def register_agent(agent_id: str):
agent = AgentMetadata(
agent_id=agent_id,
agent_type="Worker",
capabilities={AgentCapability.QUERY_PROCESSING}
)
registry.register(agent)

Multiple threads can register simultaneously
threads = [
threading.Thread(target=register_agent, args=(f"agent-{i}",))
for i in range(10)
]

for t in threads:
t.start()

for t in threads:
t.join()

print(f"Registered {registry.get_count()} agents") # 10

text

---

## 💡 Usage Examples

### Complete Agent Lifecycle

from theaia.core.multi_agent.agent_registry import AgentRegistry
from theaia.core.multi_agent.agent_metadata import (
AgentMetadata,
AgentCapability,
AgentStatus
)

registry = AgentRegistry()

1. Register agent
agent = AgentMetadata(
agent_id="calendar-agent-1",
agent_type="CalendarAgent",
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.EVENT_CREATION
},
max_capacity=10
)
registry.register(agent)

2. Update heartbeat (agent is alive)
registry.update_heartbeat("calendar-agent-1")

3. Assign task
registry.increment_load("calendar-agent-1")

4. Check availability
agent = registry.get("calendar-agent-1")
if agent.is_available:
print("Agent can accept more tasks")

5. Complete task
registry.decrement_load("calendar-agent-1")

6. Degrade agent
registry.update_status("calendar-agent-1", AgentStatus.DEGRADED)

7. Remove agent
registry.unregister("calendar-agent-1")

text

---

### Monitoring Dashboard

def print_registry_status():
"""Print registry statistics"""
total = registry.get_count()
healthy = registry.get_count_by_status(AgentStatus.HEALTHY)
degraded = registry.get_count_by_status(AgentStatus.DEGRADED)
unavailable = registry.get_count_by_status(AgentStatus.UNAVAILABLE)

text
used = registry.get_used_capacity()
total_cap = registry.get_total_capacity()

print("=" * 50)
print("AGENT REGISTRY STATUS")
print("=" * 50)
print(f"Total Agents:    {total}")
print(f"  Healthy:       {healthy}")
print(f"  Degraded:      {degraded}")
print(f"  Unavailable:   {unavailable}")
print(f"Capacity:        {used}/{total_cap} ({used/total_cap*100:.1f}%)")
print("=" * 50)
text

---

## 🧪 Testing

**Test File:** `tests/unit/multi_agent/test_agent_registry.py`  
**Total Tests:** 26  
**Status:** ✅ All passing

### Test Coverage

- ✅ Singleton pattern verification
- ✅ Thread-safe concurrent operations
- ✅ Registration and deregistration
- ✅ Duplicate handling (with/without force)
- ✅ Retrieval by ID, type, capability
- ✅ Status updates
- ✅ Load management
- ✅ Heartbeat tracking
- ✅ Stale agent detection
- ✅ Statistics calculation

---

## ⚠️ Error Handling

### `RegistrationError`

Raised when attempting to register duplicate agent without `force=True`.

from theaia.core.multi_agent.exceptions import RegistrationError

try:
registry.register(agent)
registry.register(agent) # Duplicate!
except RegistrationError as e:
print(f"Registration failed: {e}")
# Solution: use force=True to overwrite

text

---

## 📈 Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| `register()` | O(k) where k = # capabilities | O(1) |
| `unregister()` | O(k + t) where k = caps, t = types | O(1) |
| `get()` | O(1) | O(1) |
| `get_all()` | O(n) | O(n) |
| `get_by_type()` | O(m) where m = agents of type | O(m) |
| `get_by_capability()` | O(m) where m = agents with cap | O(m) |
| `update_*()` | O(1) | O(1) |

**Memory Usage:** ~1KB per agent + indexes overhead

---

## 🔄 Integration Points

### Used By
- `DiscoveryService` - Queries registry for agent discovery
- `TaskDelegator` - Updates load and retrieves agents
- `HealthMonitor` - Checks heartbeats and marks unavailable

### Dependencies
- `AgentMetadata` - Agent data structure
- `threading.Lock` - Thread safety
- `datetime` - Heartbeat timestamps

---

## 🚀 Future Enhancements

- [ ] Persistent storage (database integration)
- [ ] Event-driven notifications on agent state changes
- [ ] Historical state tracking
- [ ] Agent grouping/clustering
- [ ] Automatic failover on unavailability
- [ ] Performance metrics aggregation

---

## 📝 Best Practices

### ✅ DO
- Always update heartbeat regularly from agents
- Check `is_available` before assigning tasks
- Use `mark_stale_as_unavailable()` in periodic health checks
- Increment/decrement load when assigning/completing tasks

### ❌ DON'T
- Don't bypass registry for direct agent updates
- Don't assume agent is available without checking
- Don't forget to unregister agents on shutdown
- Don't share AgentMetadata references across threads (get fresh copy)

---

## 🔍 Troubleshooting

### "Agent not found" errors
- Ensure agent is registered before operations
- Check if agent was unregistered elsewhere
- Verify agent_id spelling

### Stale heartbeat detection
- Confirm agents are sending heartbeats
- Check network connectivity
- Verify heartbeat_interval_seconds configuration

### Registry state inconsistency
- Ensure all operations use the Singleton instance
- Check for manual AgentMetadata modifications
- Use `clear()` to reset state in tests

---
