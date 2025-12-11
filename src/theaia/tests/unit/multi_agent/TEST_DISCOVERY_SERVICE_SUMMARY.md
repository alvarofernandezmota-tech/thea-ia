# Test Discovery Service - Summary

**File:** `tests/unit/multi_agent/test_discovery_service.py`  
**Module Under Test:** `src/theaia/core/multi_agent/discovery_service.py`  
**Author:** Álvaro Fernández Mota  
**Date:** 11 December 2025  
**Version:** 1.0.0  
**Lines of Code:** ~600  
**Total Tests:** 26  
**Status:** ✅ 26/26 PASSED

---

## 📋 Purpose

Comprehensive testing of intelligent agent discovery and selection with multiple load balancing strategies, complex query filtering, and system metrics aggregation.

---

## 🎯 Test Coverage

### Module Coverage: 63%

| Component | Coverage | Missing Lines |
|-----------|----------|---------------|
| Basic Discovery | 95% | Edge cases |
| Load Balancing | 85% | Advanced strategies |
| Query Filters | 80% | Complex combinations |
| System Metrics | 70% | Aggregations |

---

## 🧪 Test Categories

### 1. Basic Discovery Tests (4 tests)

#### `test_discover_by_single_capability`
**Purpose:** Test discovery with single capability requirement

**Test Code:**
def test_discover_by_single_capability(discovery_service, sample_agents):
"""Test discovering agents by single capability"""
# Register agents with different capabilities
for agent in sample_agents:
discovery_service.registry.register(agent)

text
# Discover by capability
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

agents = discovery_service.discover(query)

assert len(agents) > 0
assert all(
    AgentCapability.CALENDAR_MANAGEMENT in agent.capabilities
    for agent in agents
)
text

**Verifies:**
- ✅ Returns agents with capability
- ✅ All results have required capability
- ✅ Non-empty result set

---

#### `test_discover_by_multiple_capabilities`
**Purpose:** Test discovery requiring multiple capabilities

**Test Code:**
def test_discover_by_multiple_capabilities(discovery_service):
"""Test discovering agents with multiple capabilities"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.EVENT_CREATION
}
)

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="TestAgent",
    capabilities={
        AgentCapability.CALENDAR_MANAGEMENT,
        AgentCapability.EVENT_CREATION,
        AgentCapability.EVENT_MODIFICATION
    }
)

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

# Require both capabilities
query = DiscoveryQuery(
    capabilities={
        AgentCapability.CALENDAR_MANAGEMENT,
        AgentCapability.EVENT_CREATION
    }
)

agents = discovery_service.discover(query)

# Only agent-1 and agent-3 have both
assert len(agents) == 2
assert all(
    AgentCapability.CALENDAR_MANAGEMENT in agent.capabilities and
    AgentCapability.EVENT_CREATION in agent.capabilities
    for agent in agents
)
text

**Verifies:**
- ✅ AND logic for multiple capabilities
- ✅ All capabilities must match
- ✅ Correct filtering

---

#### `test_discover_by_type`
**Purpose:** Test filtering by agent type

**Test Code:**
def test_discover_by_type(discovery_service):
"""Test discovering agents by type"""
calendar_agent = AgentMetadata(
agent_id="calendar-1",
agent_type="CalendarAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

text
note_agent = AgentMetadata(
    agent_id="note-1",
    agent_type="NoteAgent",
    capabilities={AgentCapability.NOTE_MANAGEMENT}
)

discovery_service.registry.register(calendar_agent)
discovery_service.registry.register(note_agent)

# Discover CalendarAgent type
query = DiscoveryQuery(agent_type="CalendarAgent")

agents = discovery_service.discover(query)

assert len(agents) == 1
assert agents.agent_type == "CalendarAgent"
assert agents.agent_id == "calendar-1"
text

**Verifies:**
- ✅ Type filtering works
- ✅ Returns only matching type
- ✅ Correct agent returned

---

#### `test_discover_no_matches`
**Purpose:** Test query with no matching agents

**Test Code:**
def test_discover_no_matches(discovery_service, sample_agents):
"""Test discovering with no matches"""
for agent in sample_agents:
discovery_service.registry.register(agent)

text
# Query for non-existent capability
query = DiscoveryQuery(
    capabilities={AgentCapability.FILE_MANAGEMENT}
)

agents = discovery_service.discover(query)

assert len(agents) == 0
assert agents == []
text

**Verifies:**
- ✅ Returns empty list
- ✅ No error raised
- ✅ Graceful handling

---

### 2. Load Balancing Strategy Tests (5 tests)

#### `test_least_loaded_strategy`
**Purpose:** Test LEAST_LOADED selection strategy

**Test Code:**
def test_least_loaded_strategy(discovery_service):
"""Test LEAST_LOADED load balancing strategy"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
max_capacity=10
)
agent1.current_load = 8 # 80% load

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    max_capacity=10
)
agent2.current_load = 3  # 30% load (least loaded)

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    max_capacity=10
)
agent3.current_load = 5  # 50% load

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    load_balancing=LoadBalancingStrategy.LEAST_LOADED
)

agents = discovery_service.discover(query)

# Should be ordered by load: agent-2, agent-3, agent-1
assert agents.agent_id == "agent-2"
assert agents.agent_id == "agent-3"
assert agents.agent_id == "agent-1"
text

**Verifies:**
- ✅ Orders by load percentage
- ✅ Least loaded first
- ✅ Correct ordering

---

#### `test_priority_strategy`
**Purpose:** Test PRIORITY selection strategy

**Test Code:**
def test_priority_strategy(discovery_service):
"""Test PRIORITY load balancing strategy"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
priority=1 # Low priority
)

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    priority=10  # High priority
)

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    priority=5  # Medium priority
)

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    load_balancing=LoadBalancingStrategy.PRIORITY
)

agents = discovery_service.discover(query)

# Should be ordered by priority: agent-2, agent-3, agent-1
assert agents.agent_id == "agent-2"
assert agents.agent_id == "agent-3"
assert agents.agent_id == "agent-1"
text

**Verifies:**
- ✅ Orders by priority
- ✅ Highest priority first
- ✅ Correct ordering

---

#### `test_round_robin_strategy`
**Purpose:** Test ROUND_ROBIN selection strategy

**Test Code:**
def test_round_robin_strategy(discovery_service):
"""Test ROUND_ROBIN load balancing strategy"""
agents = []
for i in range(3):
agent = AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)
discovery_service.registry.register(agent)
agents.append(agent)

text
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    load_balancing=LoadBalancingStrategy.ROUND_ROBIN,
    max_results=1
)

# Call multiple times
results = []
for _ in range(6):
    discovered = discovery_service.discover(query)
    if discovered:
        results.append(discovered.agent_id)

# Should cycle through agents: 0, 1, 2, 0, 1, 2
assert results == [
    "agent-0", "agent-1", "agent-2",
    "agent-0", "agent-1", "agent-2"
]
text

**Verifies:**
- ✅ Rotates through agents
- ✅ Cycles back to start
- ✅ Fair distribution

---

#### `test_random_strategy`
**Purpose:** Test RANDOM selection strategy

**Test Code:**
def test_random_strategy(discovery_service):
"""Test RANDOM load balancing strategy"""
for i in range(5):
agent = AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)
discovery_service.registry.register(agent)

text
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    load_balancing=LoadBalancingStrategy.RANDOM
)

# Call multiple times
agent_counts = {}
for _ in range(100):
    agents = discovery_service.discover(query)
    if agents:
        agent_id = agents.agent_id
        agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1

# All agents should be selected at least once
assert len(agent_counts) == 5

# Distribution should be roughly even (within 50% variance)
avg = 100 / 5  # 20
for count in agent_counts.values():
    assert 10 <= count <= 30  # ±50% of average
text

**Verifies:**
- ✅ Random selection
- ✅ All agents eventually selected
- ✅ Roughly even distribution

---

#### `test_priority_with_load_tiebreaker`
**Purpose:** Test PRIORITY with load as tiebreaker

**Test Code:**
def test_priority_with_load_tiebreaker(discovery_service):
"""Test PRIORITY strategy uses load as tiebreaker"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
priority=10,
max_capacity=10
)
agent1.current_load = 8 # High load

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    priority=10,  # Same priority
    max_capacity=10
)
agent2.current_load = 2  # Low load

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)

query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    load_balancing=LoadBalancingStrategy.PRIORITY
)

agents = discovery_service.discover(query)

# Same priority, so should be ordered by load
assert agents.agent_id == "agent-2"  # Lower load
assert agents.agent_id == "agent-1"
text

**Verifies:**
- ✅ Priority first
- ✅ Load as tiebreaker
- ✅ Correct secondary ordering

---

### 3. Query Filter Tests (6 tests)

#### `test_min_available_capacity_filter`
**Purpose:** Test minimum capacity requirement

**Test Code:**
def test_min_available_capacity_filter(discovery_service):
"""Test filtering by minimum available capacity"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
max_capacity=10
)
agent1.current_load = 9 # Only 1 slot available

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    max_capacity=10
)
agent2.current_load = 5  # 5 slots available

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)

# Require at least 3 available slots
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    min_available_capacity=3
)

agents = discovery_service.discover(query)

# Only agent-2 has >= 3 slots
assert len(agents) == 1
assert agents.agent_id == "agent-2"
text

**Verifies:**
- ✅ Capacity filtering
- ✅ Minimum threshold enforced
- ✅ Correct filtering

---

#### `test_status_filter`
**Purpose:** Test filtering by agent status

**Test Code:**
def test_status_filter(discovery_service):
"""Test filtering by agent status"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
status=AgentStatus.HEALTHY
)

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    status=AgentStatus.DEGRADED
)

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    status=AgentStatus.UNAVAILABLE
)

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

# Default: only available agents (HEALTHY)
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

agents = discovery_service.discover(query)
assert len(agents) == 1
assert agents.status == AgentStatus.HEALTHY

# Explicitly query DEGRADED
query_degraded = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    status=AgentStatus.DEGRADED
)

agents_degraded = discovery_service.discover(query_degraded)
assert len(agents_degraded) == 1
assert agents_degraded.status == AgentStatus.DEGRADED
text

**Verifies:**
- ✅ Status filtering
- ✅ Default to available only
- ✅ Explicit status filtering

---

#### `test_tags_filter`
**Purpose:** Test filtering by custom tags

**Test Code:**
def test_tags_filter(discovery_service):
"""Test filtering by tags"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
tags={"environment": "production", "region": "us-west"}
)

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    tags={"environment": "staging", "region": "us-east"}
)

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    tags={"environment": "production", "region": "eu-west"}
)

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

# Filter by single tag
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    tags={"environment": "production"}
)

agents = discovery_service.discover(query)
assert len(agents) == 2  # agent-1 and agent-3

# Filter by multiple tags (AND logic)
query_multi = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    tags={"environment": "production", "region": "us-west"}
)

agents_multi = discovery_service.discover(query_multi)
assert len(agents_multi) == 1
assert agents_multi.agent_id == "agent-1"
text

**Verifies:**
- ✅ Tag filtering
- ✅ Single tag filter
- ✅ Multiple tags (AND logic)

---

#### `test_max_results_limit`
**Purpose:** Test result limiting

**Test Code:**
def test_max_results_limit(discovery_service):
"""Test limiting number of results"""
for i in range(10):
agent = AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)
discovery_service.registry.register(agent)

text
# No limit
query_all = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)
agents_all = discovery_service.discover(query_all)
assert len(agents_all) == 10

# Limit to 3
query_limited = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    max_results=3
)
agents_limited = discovery_service.discover(query_limited)
assert len(agents_limited) == 3

# Limit to 1
query_one = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    max_results=1
)
agents_one = discovery_service.discover(query_one)
assert len(agents_one) == 1
text

**Verifies:**
- ✅ No limit returns all
- ✅ Limit enforced
- ✅ Correct result count

---

#### `test_complex_query_combination`
**Purpose:** Test combining multiple filters

**Test Code:**
def test_complex_query_combination(discovery_service):
"""Test complex query with multiple filters"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="CalendarAgent",
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.EVENT_CREATION
},
status=AgentStatus.HEALTHY,
max_capacity=10,
tags={"environment": "production"}
)
agent1.current_load = 3

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="CalendarAgent",
    capabilities={
        AgentCapability.CALENDAR_MANAGEMENT,
        AgentCapability.EVENT_CREATION
    },
    status=AgentStatus.DEGRADED,  # Wrong status
    max_capacity=10,
    tags={"environment": "production"}
)

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="NoteAgent",  # Wrong type
    capabilities={
        AgentCapability.CALENDAR_MANAGEMENT,
        AgentCapability.EVENT_CREATION
    },
    status=AgentStatus.HEALTHY,
    max_capacity=10,
    tags={"environment": "production"}
)

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

# Complex query
query = DiscoveryQuery(
    capabilities={
        AgentCapability.CALENDAR_MANAGEMENT,
        AgentCapability.EVENT_CREATION
    },
    agent_type="CalendarAgent",
    min_available_capacity=5,
    status=AgentStatus.HEALTHY,
    tags={"environment": "production"}
)

agents = discovery_service.discover(query)

# Only agent-1 matches all criteria
assert len(agents) == 1
assert agents.agent_id == "agent-1"
text

**Verifies:**
- ✅ Multiple filters combined
- ✅ AND logic across filters
- ✅ All criteria must match

---

#### `test_empty_query_returns_all_available`
**Purpose:** Test default query behavior

**Test Code:**
def test_empty_query_returns_all_available(discovery_service):
"""Test that empty query returns all available agents"""
for i in range(3):
agent = AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)
discovery_service.registry.register(agent)

text
# Empty query
query = DiscoveryQuery()

agents = discovery_service.discover(query)

# Should return all available agents
assert len(agents) == 3
text

**Verifies:**
- ✅ Empty query works
- ✅ Returns all available
- ✅ No filters applied

---

### 4. Convenience Methods Tests (3 tests)

#### `test_discover_by_capability_method`
**Purpose:** Test convenience method for single capability

**Test Code:**
def test_discover_by_capability_method(discovery_service, sample_agents):
"""Test discover_by_capability convenience method"""
for agent in sample_agents:
discovery_service.registry.register(agent)

text
agents = discovery_service.discover_by_capability(
    AgentCapability.CALENDAR_MANAGEMENT,
    max_results=2,
    strategy=LoadBalancingStrategy.LEAST_LOADED
)

assert len(agents) <= 2
assert all(
    AgentCapability.CALENDAR_MANAGEMENT in agent.capabilities
    for agent in agents
)
text

**Verifies:**
- ✅ Convenience method works
- ✅ Parameters passed correctly
- ✅ Returns expected results

---

#### `test_discover_best_agent`
**Purpose:** Test best single agent selection

**Test Code:**
def test_discover_best_agent(discovery_service):
"""Test discover_best_agent method"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
max_capacity=10
)
agent1.current_load = 8

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    max_capacity=10
)
agent2.current_load = 2  # Best (least loaded)

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)

query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    load_balancing=LoadBalancingStrategy.LEAST_LOADED
)

best = discovery_service.discover_best_agent(query)

assert best is not None
assert best.agent_id == "agent-2"
text

**Verifies:**
- ✅ Returns single best agent
- ✅ Uses load balancing strategy
- ✅ Correct agent selected

---

#### `test_discover_best_agent_no_match`
**Purpose:** Test best agent with no matches

**Test Code:**
def test_discover_best_agent_no_match(discovery_service):
"""Test discover_best_agent returns None when no match"""
agent = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

text
discovery_service.registry.register(agent)

query = DiscoveryQuery(
    capabilities={AgentCapability.FILE_MANAGEMENT}  # No agent has this
)

best = discovery_service.discover_best_agent(query)

assert best is None
text

**Verifies:**
- ✅ Returns None for no match
- ✅ No error raised
- ✅ Graceful handling

---

### 5. System Metrics Tests (4 tests)

#### `test_get_agent_summary`
**Purpose:** Test system-wide agent summary

**Test Code:**
def test_get_agent_summary(discovery_service):
"""Test getting system agent summary"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="CalendarAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
status=AgentStatus.HEALTHY,
max_capacity=10
)
agent1.current_load = 5

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="CalendarAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    status=AgentStatus.DEGRADED,
    max_capacity=10
)
agent2.current_load = 8

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="NoteAgent",
    capabilities={AgentCapability.NOTE_MANAGEMENT},
    status=AgentStatus.HEALTHY,
    max_capacity=5
)
agent3.current_load = 2

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

summary = discovery_service.get_agent_summary()

assert summary["total_agents"] == 3
assert summary["available_agents"] == 2  # agent-1 and agent-3
assert summary["total_capacity"] == 25  # 10+10+5
assert summary["total_load"] == 15  # 5+8+2
assert summary["average_load_percentage"] == 60.0  # 15/25*100

# By type
assert summary["agents_by_type"]["CalendarAgent"] == 2
assert summary["agents_by_type"]["NoteAgent"] == 1

# By status
assert summary["agents_by_status"]["HEALTHY"] == 2
assert summary["agents_by_status"]["DEGRADED"] == 1
text

**Verifies:**
- ✅ Total counts correct
- ✅ Capacity calculations
- ✅ Load calculations
- ✅ Grouping by type and status

---

#### `test_get_capacity_report`
**Purpose:** Test capacity reporting

**Test Code:**
def test_get_capacity_report(discovery_service):
"""Test getting capacity report"""
for i in range(5):
agent = AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
max_capacity=10
)
agent.current_load = i * 2 # 0, 2, 4, 6, 8
discovery_service.registry.register(agent)

text
report = discovery_service.get_capacity_report()

assert report["total_capacity"] == 50  # 5 * 10
assert report["used_capacity"] == 20  # 0+2+4+6+8
assert report["available_capacity"] == 30  # 50-20
assert report["utilization_percentage"] == 40.0  # 20/50*100
text

**Verifies:**
- ✅ Capacity totals
- ✅ Utilization calculation
- ✅ Available capacity

---

#### `test_get_load_distribution`
**Purpose:** Test load distribution metrics

**Test Code:**
def test_get_load_distribution(discovery_service):
"""Test getting load distribution"""
loads = # Different load levels​

text
for i, load in enumerate(loads):
    agent = AgentMetadata(
        agent_id=f"agent-{i}",
        agent_type="TestAgent",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT},
        max_capacity=10
    )
    agent.current_load = load
    discovery_service.registry.register(agent)

distribution = discovery_service.get_load_distribution()

assert distribution["min_load"] == 0
assert distribution["max_load"] == 10
assert distribution["average_load"] == 5.0  # (0+2+5+8+10)/5
assert distribution["median_load"] == 5

# Load categories
assert distribution["idle"] == 1  # agent-0 (0%)
assert distribution["light"] == 1  # agent-1 (20%)
assert distribution["medium"] == 1  # agent-2 (50%)
assert distribution["heavy"] == 1  # agent-3 (80%)
assert distribution["overloaded"] == 1  # agent-4 (100%)
text

**Verifies:**
- ✅ Min/max/average calculations
- ✅ Median calculation
- ✅ Load categorization

---

#### `test_get_capability_coverage`
**Purpose:** Test capability coverage report

**Test Code:**
def test_get_capability_coverage(discovery_service):
"""Test getting capability coverage"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={
AgentCapability.CALENDAR_MANAGEMENT,
AgentCapability.EVENT_CREATION
}
)

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={
        AgentCapability.CALENDAR_MANAGEMENT,
        AgentCapability.NOTE_MANAGEMENT
    }
)

agent3 = AgentMetadata(
    agent_id="agent-3",
    agent_type="TestAgent",
    capabilities={AgentCapability.EVENT_CREATION}
)

discovery_service.registry.register(agent1)
discovery_service.registry.register(agent2)
discovery_service.registry.register(agent3)

coverage = discovery_service.get_capability_coverage()

# Count agents per capability
assert coverage["CALENDAR_MANAGEMENT"] == 2  # agent-1, agent-2
assert coverage["EVENT_CREATION"] == 2  # agent-1, agent-3
assert coverage["NOTE_MANAGEMENT"] == 1  # agent-2

# Total unique capabilities
assert len(coverage) == 3
text

**Verifies:**
- ✅ Capability counts
- ✅ Agent-capability mapping
- ✅ Coverage reporting

---

### 6. Edge Cases Tests (4 tests)

#### `test_discover_with_all_agents_unavailable`
**Purpose:** Test when all agents unavailable

**Test Code:**
def test_discover_with_all_agents_unavailable(discovery_service):
"""Test discovering when all agents unavailable"""
for i in range(3):
agent = AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
status=AgentStatus.UNAVAILABLE
)
discovery_service.registry.register(agent)

text
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

agents = discovery_service.discover(query)

assert len(agents) == 0
text

**Verifies:**
- ✅ Returns empty for all unavailable
- ✅ Status filtering works
- ✅ Graceful handling

---

#### `test_discover_with_all_agents_overloaded`
**Purpose:** Test when all agents at capacity

**Test Code:**
def test_discover_with_all_agents_overloaded(discovery_service):
"""Test discovering when all agents overloaded"""
for i in range(3):
agent = AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
max_capacity=10
)
agent.current_load = 10 # At capacity
discovery_service.registry.register(agent)

text
query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    min_available_capacity=1
)

agents = discovery_service.discover(query)

assert len(agents) == 0
text

**Verifies:**
- ✅ Returns empty for all overloaded
- ✅ Capacity filtering works
- ✅ Graceful handling

---

#### `test_round_robin_state_isolation`
**Purpose:** Test round-robin state per agent type

**Test Code:**
def test_round_robin_state_isolation(discovery_service):
"""Test round-robin state is isolated per agent type"""
# Register CalendarAgents
for i in range(2):
agent = AgentMetadata(
agent_id=f"calendar-{i}",
agent_type="CalendarAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)
discovery_service.registry.register(agent)

text
# Register NoteAgents
for i in range(2):
    agent = AgentMetadata(
        agent_id=f"note-{i}",
        agent_type="NoteAgent",
        capabilities={AgentCapability.NOTE_MANAGEMENT}
    )
    discovery_service.registry.register(agent)

# Query CalendarAgents
calendar_query = DiscoveryQuery(
    agent_type="CalendarAgent",
    load_balancing=LoadBalancingStrategy.ROUND_ROBIN,
    max_results=1
)

# Query NoteAgents
note_query = DiscoveryQuery(
    agent_type="NoteAgent",
    load_balancing=LoadBalancingStrategy.ROUND_ROBIN,
    max_results=1
)

# Interleaved queries should maintain separate state
cal1 = discovery_service.discover(calendar_query).agent_id
note1 = discovery_service.discover(note_query).agent_id
cal2 = discovery_service.discover(calendar_query).agent_id
note2 = discovery_service.discover(note_query).agent_id

# Each type should cycle independently
assert cal1 != cal2
assert note1 != note2
text

**Verifies:**
- ✅ Round-robin state per type
- ✅ State isolation
- ✅ Independent cycling

---

#### `test_zero_capacity_agents_excluded`
**Purpose:** Test agents with zero capacity excluded

**Test Code:**
def test_zero_capacity_agents_excluded(discovery_service):
"""Test that agents with zero max_capacity are excluded"""
agent1 = AgentMetadata(
agent_id="agent-1",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
max_capacity=10
)

text
agent2 = AgentMetadata(
    agent_id="agent-2",
    agent_type="TestAgent",
    capabilities={AgentCapability.CALENDAR_MANAGEMENT},
    max_capacity=0  # Invalid capacity
)

# Only agent-1 should register successfully
discovery_service.registry.register(agent1)

with pytest.raises(ValueError):
    discovery_service.registry.register(agent2)

query = DiscoveryQuery(
    capabilities={AgentCapability.CALENDAR_MANAGEMENT}
)

agents = discovery_service.discover(query)

assert len(agents) == 1
assert agents.agent_id == "agent-1"
text

**Verifies:**
- ✅ Zero capacity rejected
- ✅ Validation at registration
- ✅ Only valid agents returned

---

## 📊 Test Execution Summary

================================ test session starts =================================
platform win32 -- Python 3.11.9, pytest-8.1.1
collected 26 items

test_discovery_service.py::test_discover_by_single_capability PASSED [ 3%]
test_discovery_service.py::test_discover_by_multiple_capabilities PASSED [ 7%]
test_discovery_service.py::test_discover_by_type PASSED [ 11%]
test_discovery_service.py::test_discover_no_matches PASSED [ 15%]
test_discovery_service.py::test_least_loaded_strategy PASSED [ 19%]
test_discovery_service.py::test_priority_strategy PASSED [ 23%]
test_discovery_service.py::test_round_robin_strategy PASSED [ 26%]
test_discovery_service.py::test_random_strategy PASSED [ 30%]
test_discovery_service.py::test_priority_with_load_tiebreaker PASSED [ 34%]
test_discovery_service.py::test_min_available_capacity_filter PASSED [ 38%]
test_discovery_service.py::test_status_filter PASSED [ 42%]
test_discovery_service.py::test_tags_filter PASSED [ 46%]
test_discovery_service.py::test_max_results_limit PASSED [ 50%]
test_discovery_service.py::test_complex_query_combination PASSED [ 53%]
test_discovery_service.py::test_empty_query_returns_all_available PASSED [ 57%]
test_discovery_service.py::test_discover_by_capability_method PASSED [ 61%]
test_discovery_service.py::test_discover_best_agent PASSED [ 65%]
test_discovery_service.py::test_discover_best_agent_no_match PASSED [ 69%]
test_discovery_service.py::test_get_agent_summary PASSED [ 73%]
test_discovery_service.py::test_get_capacity_report PASSED [ 76%]
test_discovery_service.py::test_get_load_distribution PASSED [ 80%]
test_discovery_service.py::test_get_capability_coverage PASSED [ 84%]
test_discovery_service.py::test_discover_with_all_agents_unavailable PASSED [ 88%]
test_discovery_service.py::test_discover_with_all_agents_overloaded PASSED [ 92%]
test_discovery_service.py::test_round_robin_state_isolation PASSED [ 96%]
test_discovery_service.py::test_zero_capacity_agents_excluded PASSED [100%]

================================ 26 passed in 0.35s ==================================

text

---

## 🔧 Fixtures

@pytest.fixture
def discovery_service():
"""Clean discovery service for each test"""
registry = AgentRegistry()
registry.clear()
service = DiscoveryService(registry)
yield service
registry.clear()

@pytest.fixture
def sample_agents():
"""Sample agents for testing"""
return [
AgentMetadata(
agent_id=f"agent-{i}",
agent_type="TestAgent",
capabilities={AgentCapability.CALENDAR_MANAGEMENT},
max_capacity=10
)
for i in range(3)
]

text

---

## 🚀 Running Tests

Run all discovery service tests
pytest tests/unit/multi_agent/test_discovery_service.py -v

Run specific test category
pytest tests/unit/multi_agent/test_discovery_service.py -k "strategy" -v

Run with coverage
pytest tests/unit/multi_agent/test_discovery_service.py --cov=src/theaia/core/multi_agent/discovery_service

Run with verbose output
pytest tests/unit/multi_agent/test_discovery_service.py -vv

text

---

## ✅ All Tests Passing!

**Status:** ✅ 26/26 tests passed  
**Coverage:** 63%  
**Execution Time:** 0.35s  
**Reliability:** 100%

---