# Discovery Service Module - Summary

**File:** `src/theaia/core/multi_agent/discovery_service.py`  
**Author:** Álvaro Fernández Mota  
**Date:** 11 December 2025  
**Version:** 1.0.0  
**Lines of Code:** 240  
**Test Coverage:** 63%

---

## 📋 Purpose

Intelligent agent discovery and selection service with multiple load balancing strategies. Enables finding the best agent(s) for task execution based on capabilities, status, load, and custom criteria.

---

## 🎯 Key Features

- ✅ **Multi-criteria Search** - Filter by capabilities, type, status, tags
- ✅ **4 Load Balancing Strategies** - Least loaded, priority, round-robin, random
- ✅ **Complex Queries** - Combine multiple filters in single query
- ✅ **State Management** - Round-robin state persistence per agent type
- ✅ **System Metrics** - Real-time aggregated statistics

---

## 🏗️ Components

### Enumerations

#### `LoadBalancingStrategy`

Strategy for agent selection when multiple agents match criteria.

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `LEAST_LOADED` | Select agent with lowest load percentage | Default, best for balanced distribution |
| `PRIORITY` | Select by priority (with load tiebreaker) | Critical tasks to high-priority agents |
| `ROUND_ROBIN` | Rotate through agents cyclically | Fair distribution, testing |
| `RANDOM` | Random selection | A/B testing, chaos engineering |

---

### Dataclasses

#### `DiscoveryQuery`

Complete query specification for agent discovery.

@dataclass
class DiscoveryQuery:
# Filtering criteria
capabilities: Optional[Set[AgentCapability]] = None
agent_type: Optional[str] = None
min_available_capacity: int = 1
status: Optional[AgentStatus] = None
tags: Optional[Dict[str, str]] = None

text
# Result control
max_results: Optional[int] = None
load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED
text

**Attributes:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `capabilities` | `Set[AgentCapability]` | `None` | Required capabilities (ALL must match) |
| `agent_type` | `str` | `None` | Filter by agent type |
| `min_available_capacity` | `int` | `1` | Minimum free slots required |
| `status` | `AgentStatus` | `None` | Filter by status (None = available only) |
| `tags` | `Dict[str, str]` | `None` | Custom tag filters (ALL must match) |
| `max_results` | `int` | `None` | Limit number of results |
| `load_balancing` | `LoadBalancingStrategy` | `LEAST_LOADED` | Selection strategy |

---

## 📊 Core Methods

### Primary Discovery

#### `discover()`

def discover(self, query: DiscoveryQuery) -> List[AgentMetadata]:
"""
Discover agents matching query criteria.

text
Args:
    query: Discovery query with filters and strategy
    
Returns:
    List of matching agents, ordered by strategy
    
Process:
    1. Get all agents from registry
    2. Apply filters (capabilities, type, status, tags, capacity)
    3. Apply load balancing strategy
    4. Limit results if max_results specified
"""
text

**Example:**
from theaia.core.multi_agent.discovery_service import (
DiscoveryService,
DiscoveryQuery,
LoadBalancingStrategy
)
from theaia.core.multi_agent.agent_metadata import AgentCapability

discovery = DiscoveryService(agent_registry)

Complex query
query = DiscoveryQuery(
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.EVENT_CREATION
},
agent_type="CalendarAgent",
min_available_capacity=3,
tags={"environment": "production"},
max_results=5,
load_balancing=LoadBalancingStrategy.LEAST_LOADED
)

agents = discovery.discover(query)

for agent in agents:
print(f"{agent.agent_id}: {agent.load_percentage:.1f}% load")

text

---

### Convenience Methods

#### `discover_by_capability()`

def discover_by_capability(
self,
capability: AgentCapability,
max_results: Optional[int] = None,
strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED
) -> List[AgentMetadata]:
"""
Simplified discovery by single capability.

text
Args:
    capability: Required capability
    max_results: Limit results (None = all)
    strategy: Load balancing strategy
    
Returns:
    List of agents with capability, ordered by strategy
"""
text

**Example:**
Find calendar agents, get 3 least loaded
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
max_results=3,
strategy=LoadBalancingStrategy.LEAST_LOADED
)

if agents:
best_agent = agents
print(f"Best agent: {best_agent.agent_id}")

text

---

#### `discover_best_agent()`

def discover_best_agent(
self,
query: DiscoveryQuery
) -> Optional[AgentMetadata]:
"""
Find single best agent matching criteria.

text
Args:
    query: Discovery query
    
Returns:
    Best matching agent or None if no matches
"""
text

**Example:**
query = DiscoveryQuery(
capabilities={AgentCapability.EVENT_CREATION},
min_available_capacity=5
)

best_agent = discovery.discover_best_agent(query)

if best_agent:
print(f"Selected: {best_agent.agent_id}")
else:
print("No agent available")

text

---

### System Metrics

#### `get_agent_summary()`

def get_agent_summary(self) -> Dict[str, Any]:
"""
Get aggregated statistics across all agents.

text
Returns:
    Dictionary with system-wide metrics
"""
text

**Response Structure:**
{
"total_agents": 10,
"healthy_agents": 8,
"available_agents": 6,
"overloaded_agents": 2,
"total_capacity": 100,
"used_capacity": 45,
"average_load_percentage": 45.0,
"capabilities": {
"calendar_management": 5,
"event_creation": 5,
"note_management": 3,
"reminder_management": 2
}
}

text

**Example:**
summary = discovery.get_agent_summary()

print(f"System Health:")
print(f" Total Agents: {summary['total_agents']}")
print(f" Available: {summary['available_agents']}")
print(f" Load: {summary['average_load_percentage']:.1f}%")
print(f" Capacity: {summary['used_capacity']}/{summary['total_capacity']}")

print(f"\nCapabilities Distribution:")
for cap, count in summary['capabilities'].items():
print(f" {cap}: {count} agents")

text

---

## 🎲 Load Balancing Strategies

### 1. LEAST_LOADED

**Strategy:** Select agents with lowest load percentage.

**Algorithm:**
sorted(agents, key=lambda a: a.load_percentage)

text

**Best For:**
- Default choice for production
- Balanced load distribution
- Preventing overload

**Example:**
Get 3 least loaded calendar agents
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
max_results=3,
strategy=LoadBalancingStrategy.LEAST_LOADED
)

Agents ordered: 20% load, 35% load, 50% load
text

---

### 2. PRIORITY

**Strategy:** Select agents by priority (descending), use load as tiebreaker.

**Algorithm:**
sorted(agents, key=lambda a: (-a.priority, a.load_percentage))

text

**Best For:**
- Critical tasks requiring high-priority agents
- Multi-tier agent architectures
- SLA-sensitive workloads

**Example:**
Priority 5 agents first, then priority 3, etc.
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
strategy=LoadBalancingStrategy.PRIORITY
)

Result: [priority=5, load=20%], [priority=5, load=40%], [priority=3, load=10%]
text

---

### 3. ROUND_ROBIN

**Strategy:** Rotate through agents cyclically. State persists per agent type.

**Algorithm:**
State: self._round_robin_state[agent_type] = current_index
agents_rotated = agents[index:] + agents[:index]
self._round_robin_state[agent_type] = (index + 1) % len(agents)

text

**Best For:**
- Fair distribution across all agents
- Testing/debugging
- Predictable selection patterns

**Example:**
First call: agent-1
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
strategy=LoadBalancingStrategy.ROUND_ROBIN
)
print(agents.agent_id) # agent-1

Second call: agent-2
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
strategy=LoadBalancingStrategy.ROUND_ROBIN
)
print(agents.agent_id) # agent-2

Third call: agent-3
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
strategy=LoadBalancingStrategy.ROUND_ROBIN
)
print(agents.agent_id) # agent-3

Fourth call: back to agent-1
text

**Note:** State is maintained separately per agent type.

---

### 4. RANDOM

**Strategy:** Random shuffle for unpredictable selection.

**Algorithm:**
import random
random.shuffle(agents)

text

**Best For:**
- A/B testing
- Chaos engineering
- Load testing with randomness

**Example:**
Get random agent each time
for _ in range(5):
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
max_results=1,
strategy=LoadBalancingStrategy.RANDOM
)
print(agents.agent_id) # Different each time (likely)

text

---

## 🔍 Filtering Logic

### Filter Order

1. **Capabilities** - ALL must be present
2. **Agent Type** - Exact match
3. **Status** - Default: `is_available` (healthy + capacity)
4. **Minimum Capacity** - Must have at least N free slots
5. **Tags** - ALL tag key-value pairs must match

### Filter Examples

#### By Multiple Capabilities

query = DiscoveryQuery(
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.EVENT_CREATION,
AgentCapability.REMINDER_MANAGEMENT
}
)

Only agents with ALL three capabilities
agents = discovery.discover(query)

text

---

#### By Type and Status

query = DiscoveryQuery(
agent_type="CalendarAgent",
status=AgentStatus.HEALTHY
)

Only CalendarAgent type with HEALTHY status
agents = discovery.discover(query)

text

---

#### By Capacity

query = DiscoveryQuery(
capabilities={AgentCapability.EVENT_CREATION},
min_available_capacity=5
)

Only agents with 5+ free slots
agents = discovery.discover(query)

text

---

#### By Custom Tags

query = DiscoveryQuery(
tags={
"environment": "production",
"region": "us-east-1",
"version": "2.0.0"
}
)

Only agents matching ALL tags
agents = discovery.discover(query)

text

---

#### Complex Combined Query

query = DiscoveryQuery(
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.NOTIFICATION_SENDING
},
agent_type="CalendarAgent",
min_available_capacity=3,
status=AgentStatus.HEALTHY,
tags={
"environment": "production",
"tier": "premium"
},
max_results=10,
load_balancing=LoadBalancingStrategy.PRIORITY
)

agents = discovery.discover(query)

text

---

## 💡 Usage Examples

### Basic Discovery

from theaia.core.multi_agent.discovery_service import DiscoveryService
from theaia.core.multi_agent.agent_registry import AgentRegistry
from theaia.core.multi_agent.agent_metadata import AgentCapability

Setup
registry = AgentRegistry()
discovery = DiscoveryService(registry)

Find agents for calendar tasks
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
max_results=1,
strategy=LoadBalancingStrategy.LEAST_LOADED
)

if agents:
agent = agents
print(f"Selected: {agent.agent_id}")
print(f"Load: {agent.load_percentage:.1f}%")
print(f"Available: {agent.available_capacity} slots")

text

---

### Production-Ready Selection

def select_agent_for_task(
discovery: DiscoveryService,
required_capability: AgentCapability,
min_capacity: int = 1
) -> Optional[AgentMetadata]:
"""
Select best agent with error handling.
"""
query = DiscoveryQuery(
capabilities={required_capability},
min_available_capacity=min_capacity,
status=AgentStatus.HEALTHY,
tags={"environment": "production"},
load_balancing=LoadBalancingStrategy.LEAST_LOADED
)

text
agents = discovery.discover(query)

if not agents:
    logger.warning(
        f"No agent available for {required_capability} "
        f"with {min_capacity} capacity"
    )
    return None

agent = agents
logger.info(
    f"Selected {agent.agent_id} "
    f"({agent.load_percentage:.1f}% load, "
    f"{agent.available_capacity} slots free)"
)

return agent
text

---

### Monitoring Dashboard

def print_system_health(discovery: DiscoveryService):
"""Print system health dashboard"""
summary = discovery.get_agent_summary()

text
total = summary['total_agents']
available = summary['available_agents']
overloaded = summary['overloaded_agents']
avg_load = summary['average_load_percentage']

print("=" * 60)
print("MULTI-AGENT SYSTEM HEALTH")
print("=" * 60)

# Agent Status
print(f"\n📊 Agent Status:")
print(f"   Total:       {total}")
print(f"   Available:   {available} ({available/total*100:.1f}%)")
print(f"   Overloaded:  {overloaded}")

# Capacity
print(f"\n💾 Capacity:")
print(f"   Total:       {summary['total_capacity']}")
print(f"   Used:        {summary['used_capacity']}")
print(f"   Free:        {summary['total_capacity'] - summary['used_capacity']}")
print(f"   Avg Load:    {avg_load:.1f}%")

# Load bar
load_bar = "█" * int(avg_load / 5) + "░" * (20 - int(avg_load / 5))
print(f"   [{load_bar}]")

# Capabilities
print(f"\n🎯 Capabilities:")
for cap, count in summary['capabilities'].items():
    print(f"   {cap:30s} {count} agents")

print("=" * 60)
text

---

### Strategy Comparison

def compare_strategies(discovery: DiscoveryService):
"""Compare different load balancing strategies"""
capability = AgentCapability.CALENDAR_MANAGEMENT

text
strategies = [
    LoadBalancingStrategy.LEAST_LOADED,
    LoadBalancingStrategy.PRIORITY,
    LoadBalancingStrategy.ROUND_ROBIN,
    LoadBalancingStrategy.RANDOM
]

print("Strategy Comparison:")
print("-" * 70)

for strategy in strategies:
    agents = discovery.discover_by_capability(
        capability,
        max_results=3,
        strategy=strategy
    )
    
    print(f"\n{strategy.name}:")
    for i, agent in enumerate(agents, 1):
        print(
            f"  {i}. {agent.agent_id:20s} "
            f"Load: {agent.load_percentage:5.1f}%  "
            f"Priority: {agent.priority}"
        )
text

---

## 🧪 Testing

**Test File:** `tests/unit/multi_agent/test_discovery_service.py`  
**Total Tests:** 26  
**Status:** ✅ All passing

### Test Coverage

- ✅ Basic discovery (all agents, by capability, by type)
- ✅ Multi-criteria filtering
- ✅ All 4 load balancing strategies
- ✅ Round-robin state persistence
- ✅ Strategy ordering verification
- ✅ Edge cases (no agents, all overloaded)
- ✅ Tag filtering
- ✅ Capacity filtering
- ✅ System summary generation

---

## 📈 Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| `discover()` | O(n) where n = total agents | Full scan with filters |
| `discover_by_capability()` | O(m) where m = agents with cap | Uses registry index |
| `get_agent_summary()` | O(n) | Aggregates all agents |
| Strategy application | O(m log m) worst case | Sorting for LEAST_LOADED/PRIORITY |

**Optimization Tips:**
- Use `max_results` to limit scanning
- Prefer `discover_by_capability()` over complex queries when possible
- Cache `get_agent_summary()` results if called frequently

---

## 🔄 Integration Points

### Used By
- `TaskDelegator` - Selects agents for task assignment
- `LoadBalancer` - Distributes incoming requests
- `HealthMonitor` - System health dashboards

### Dependencies
- `AgentRegistry` - Source of agent data
- `AgentMetadata` - Agent properties and capabilities
- `AgentCapability` - Capability enumeration

---

## 🚀 Future Enhancements

- [ ] Weighted random selection
- [ ] Geolocation-aware discovery
- [ ] Time-based availability (office hours)
- [ ] Cost-based selection
- [ ] Machine learning-based predictions
- [ ] Caching layer for frequent queries
- [ ] Query optimization hints

---

## 📝 Best Practices

### ✅ DO
- Use `LEAST_LOADED` as default strategy
- Set `min_available_capacity` for safety margin
- Filter by `status=HEALTHY` for production
- Use `max_results` to limit results
- Check if agents list is empty before using

### ❌ DON'T
- Don't use `RANDOM` strategy in production without reason
- Don't query without filters if many agents
- Don't ignore agent status checks
- Don't assume first result is always best
- Don't cache agent references (always query fresh)

---

## 🔍 Troubleshooting

### No agents found

**Symptoms:** `discover()` returns empty list

**Causes:**
- All agents overloaded
- No agents with required capability
- Filters too restrictive
- All agents in unhealthy state

**Solutions:**
Check system summary
summary = discovery.get_agent_summary()
print(f"Available: {summary['available_agents']}")
print(f"Capabilities: {summary['capabilities']}")

Try broader query
query = DiscoveryQuery(
capabilities={required_capability},
status=None, # Include all statuses
min_available_capacity=0 # Allow full agents
)
agents = discovery.discover(query)

text

---

### Round-robin not rotating

**Symptoms:** Same agent returned repeatedly

**Cause:** Multiple agent types using same state

**Solution:** State is maintained per type automatically, but ensure agent types are consistent.

---

### Incorrect strategy ordering

**Symptoms:** Agents not ordered as expected

**Verification:**
agents = discovery.discover_by_capability(
AgentCapability.CALENDAR_MANAGEMENT,
strategy=LoadBalancingStrategy.LEAST_LOADED
)

Verify ordering
for i in range(len(agents) - 1):
assert agents[i].load_percentage <= agents[i+1].load_percentage

text

---
