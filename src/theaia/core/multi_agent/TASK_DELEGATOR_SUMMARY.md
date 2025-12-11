# Task Delegator Module - Summary

**File:** `src/theaia/core/multi_agent/task_delegator.py`  
**Author:** Álvaro Fernández Mota  
**Date:** 11 December 2025  
**Version:** 1.0.0  
**Lines of Code:** 620  
**Test Coverage:** 89%

---

## 📋 Purpose

Comprehensive task delegation and lifecycle management system for multi-agent architecture. Handles intelligent task assignment, timeout monitoring, automatic retries, and complete task state tracking.

---

## 🎯 Key Features

- ✅ **Intelligent Agent Selection** - Uses DiscoveryService with load balancing
- ✅ **Automatic Timeout Detection** - Background monitoring with configurable intervals
- ✅ **Retry Logic** - Exponential backoff with max retry limits
- ✅ **Priority-based Assignment** - Maps task priority to message priority
- ✅ **Complete Lifecycle Tracking** - From creation to completion/failure
- ✅ **Thread-safe Statistics** - Real-time metrics and reporting
- ✅ **Message Broker Integration** - Seamless agent communication

---

## 🏗️ Components

### Enumerations

#### `TaskPriority`

Priority levels for task execution.

| Value | Level | Use Case |
|-------|-------|----------|
| `LOW` | 1 | Background jobs, cleanup |
| `NORMAL` | 2 | Default user requests |
| `HIGH` | 3 | Important user actions |
| `URGENT` | 4 | Critical system operations |

---

#### `TaskStatus`

Complete task lifecycle states.

| Status | Description | Terminal? |
|--------|-------------|-----------|
| `PENDING` | Created, awaiting assignment | ❌ |
| `ASSIGNED` | Assigned to agent | ❌ |
| `IN_PROGRESS` | Agent actively working | ❌ |
| `COMPLETED` | Successfully finished | ✅ |
| `FAILED` | Failed permanently | ✅ |
| `TIMEOUT` | Exceeded timeout limit | ✅ |
| `CANCELLED` | Manually cancelled | ✅ |

---

### Dataclasses

#### `Task`

Complete task representation with metadata and tracking.

@dataclass
class Task:
# Identity
task_id: str = field(default_factory=lambda: str(uuid4()))
task_type: str = ""

text
# Data
payload: Dict[str, Any] = field(default_factory=dict)
metadata: Dict[str, Any] = field(default_factory=dict)

# Priority & Timing
priority: TaskPriority = TaskPriority.NORMAL
timeout_seconds: int = 300  # 5 minutes default

# Retry Logic
max_retries: int = 3
retry_count: int = 0

# State Tracking
status: TaskStatus = TaskStatus.PENDING
assigned_agent_id: Optional[str] = None

# Timestamps
created_at: datetime = field(default_factory=datetime.now)
assigned_at: Optional[datetime] = None
completed_at: Optional[datetime] = None

# Results
result: Optional[Any] = None
error: Optional[str] = None
text

**Key Methods:**

Timeout Detection
def is_timed_out(self) -> bool:
"""Check if task exceeded timeout"""

def can_retry(self) -> bool:
"""Check if task can be retried"""

State Transitions
def mark_assigned(self, agent_id: str) -> None
def mark_in_progress(self) -> None
def mark_completed(self, result: Any) -> None
def mark_failed(self, error: str) -> None
def mark_timeout(self) -> None
def increment_retry(self) -> None

text

---

## 📊 Core Class: TaskDelegator

### Initialization

def init(
self,
agent_registry: AgentRegistry,
discovery_service: DiscoveryService,
message_broker: MessageBroker,
enable_auto_reassignment: bool = True,
):
"""
Initialize task delegator.

text
Args:
    agent_registry: Registry of available agents
    discovery_service: Service for agent discovery
    message_broker: Broker for agent communication
    enable_auto_reassignment: Enable automatic reassignment on timeout/failure
"""
text

**Example:**
from theaia.core.multi_agent.task_delegator import TaskDelegator
from theaia.core.multi_agent.agent_registry import AgentRegistry
from theaia.core.multi_agent.discovery_service import DiscoveryService
from theaia.core.multi_agent.message.broker import MessageBroker

registry = AgentRegistry()
discovery = DiscoveryService(registry)
broker = MessageBroker()

delegator = TaskDelegator(
agent_registry=registry,
discovery_service=discovery,
message_broker=broker,
enable_auto_reassignment=True
)

text

---

### Task Creation

#### `create_task()`

def create_task(
self,
task_type: str,
payload: Dict[str, Any],
priority: TaskPriority = TaskPriority.NORMAL,
timeout_seconds: int = 300,
max_retries: int = 3,
metadata: Optional[Dict[str, Any]] = None,
) -> Task:
"""
Create new task.

text
Args:
    task_type: Task type (matches AgentCapability value)
    payload: Task data/parameters
    priority: Task priority level
    timeout_seconds: Maximum execution time
    max_retries: Maximum retry attempts
    metadata: Additional task metadata
    
Returns:
    Created task with unique ID
"""
text

**Example:**
from theaia.core.multi_agent.agent_metadata import AgentCapability

task = delegator.create_task(
task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
payload={
"action": "create_event",
"title": "Team Meeting",
"start_time": "2025-12-11T15:00:00",
"duration_minutes": 60
},
priority=TaskPriority.HIGH,
timeout_seconds=600,
max_retries=5,
metadata={
"user_id": "user123",
"request_id": "req456"
}
)

print(f"Task created: {task.task_id}")

text

---

### Task Delegation

#### `delegate_task()`

async def delegate_task(
self,
task: Task,
strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
) -> bool:
"""
Delegate task to best available agent.

text
Args:
    task: Task to delegate
    strategy: Load balancing strategy
    
Returns:
    True if task was successfully assigned, False otherwise
    
Process:
    1. Convert task_type string to AgentCapability enum
    2. Discover best agent using strategy
    3. Mark task as assigned
    4. Increment agent load
    5. Send message to agent via broker
    6. Update statistics
"""
text

**Example:**
from theaia.core.multi_agent.discovery_service import LoadBalancingStrategy

task = delegator.create_task(
task_type=AgentCapability.EVENT_CREATION.value,
payload={"event_data": {...}}
)

Delegate with default strategy (LEAST_LOADED)
success = await delegator.delegate_task(task)

if success:
print(f"Task {task.task_id} assigned to {task.assigned_agent_id}")
else:
print("No agent available for task")

text

**With Custom Strategy:**
Use priority-based selection
success = await delegator.delegate_task(
task,
strategy=LoadBalancingStrategy.PRIORITY
)

text

---

#### `delegate_to_best_agent()`

async def delegate_to_best_agent(
self,
task_type: str,
payload: Dict[str, Any],
priority: TaskPriority = TaskPriority.NORMAL,
strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
) -> Optional[str]:
"""
Create and delegate task in one call.

text
Args:
    task_type: Task type
    payload: Task data
    priority: Task priority
    strategy: Load balancing strategy
    
Returns:
    Task ID if successful, None otherwise
"""
text

**Example:**
Single-call task creation and delegation
task_id = await delegator.delegate_to_best_agent(
task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
payload={"action": "list_events", "date": "2025-12-11"},
priority=TaskPriority.NORMAL,
strategy=LoadBalancingStrategy.LEAST_LOADED
)

if task_id:
print(f"Task {task_id} delegated successfully")
task = delegator.get_task(task_id)
print(f"Assigned to: {task.assigned_agent_id}")

text

---

### Task Completion

#### `complete_task()`

async def complete_task(
self,
task_id: str,
result: Any,
agent_id: str,
) -> bool:
"""
Mark task as completed.

text
Args:
    task_id: ID of completed task
    result: Task execution result
    agent_id: Agent that completed task (verification)
    
Returns:
    True if task was marked completed, False otherwise
    
Process:
    1. Verify agent_id matches assigned agent
    2. Mark task as completed with result
    3. Decrement agent load
    4. Update statistics
"""
text

**Example:**
Agent completes task
result = {
"status": "success",
"events_created": 1,
"event_id": "evt789"
}

success = await delegator.complete_task(
task_id=task.task_id,
result=result,
agent_id=task.assigned_agent_id
)

if success:
print(f"Task completed: {task.result}")

text

---

#### `fail_task()`

async def fail_task(
self,
task_id: str,
error: str,
agent_id: str,
) -> bool:
"""
Mark task as failed.

text
Args:
    task_id: ID of failed task
    error: Error description
    agent_id: Agent that failed task (verification)
    
Returns:
    True if processed, False otherwise
    
Process:
    1. Verify agent_id matches assigned agent
    2. Decrement agent load
    3. Check if retries available
    4. If yes: increment retry and reassign
    5. If no: mark as permanently failed
"""
text

**Example:**
Task fails with retry
error = "Database connection timeout"
success = await delegator.fail_task(
task_id=task.task_id,
error=error,
agent_id=task.assigned_agent_id
)

Check if retried
task = delegator.get_task(task.task_id)
if task.status == TaskStatus.ASSIGNED:
print(f"Task retried (attempt {task.retry_count}/{task.max_retries})")
elif task.status == TaskStatus.FAILED:
print(f"Task failed permanently: {task.error}")

text

---

### Task Reassignment

#### `reassign_task()`

async def reassign_task(
self,
task_id: str,
new_agent_id: Optional[str] = None,
strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
) -> bool:
"""
Reassign task to different agent.

text
Args:
    task_id: ID of task to reassign
    new_agent_id: Specific agent to assign to (None for auto-selection)
    strategy: Load balancing strategy if auto-selecting
    
Returns:
    True if reassignment successful
    
Process:
    1. Remove from old agent
    2. Decrement old agent load
    3. Reset task status
    4. Assign to new agent (specific or auto-select)
    5. Increment new agent load
"""
text

**Examples:**

**Manual Reassignment:**
Reassign to specific agent
success = await delegator.reassign_task(
task_id=task.task_id,
new_agent_id="calendar-agent-2"
)

text

**Automatic Reassignment:**
Let system choose best agent
success = await delegator.reassign_task(
task_id=task.task_id,
strategy=LoadBalancingStrategy.ROUND_ROBIN
)

text

---

### Timeout Monitoring

#### `start_monitoring()`

async def start_monitoring(self) -> None:
"""
Start background monitoring for timeouts.

text
Creates asyncio task that runs _monitor_timeouts() loop.
Monitoring interval: 10 seconds (configurable).
"""
text

#### `stop_monitoring()`

async def stop_monitoring(self) -> None:
"""
Stop background monitoring.

text
Cancels monitoring task gracefully.
"""
text

**Example:**
Start monitoring when application starts
await delegator.start_monitoring()

try:
# Application runs...
await run_application()
finally:
# Stop monitoring on shutdown
await delegator.stop_monitoring()

text

---

#### Automatic Timeout Handling

**Internal Process:**

async def _monitor_timeouts(self) -> None:
"""Background task monitoring loop"""
while True:
await asyncio.sleep(10) # Check every 10 seconds
await self._check_timeouts()

async def _check_timeouts(self) -> None:
"""Check all in-progress tasks for timeouts"""
for task in self.tasks.values():
if task.status in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]:
if task.is_timed_out():
await self._handle_timeout(task)

async def _handle_timeout(self, task: Task) -> None:
"""
Handle timed-out task.

text
Process:
    1. Mark task as TIMEOUT
    2. Remove from agent's task list
    3. Decrement agent load
    4. If retries available and auto_reassignment enabled:
       - Increment retry count
       - Delegate task again
    5. Else:
       - Mark as permanently failed
"""
text

**Monitoring Example:**
task = delegator.create_task(
task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
payload={"action": "sync_calendar"},
timeout_seconds=30 # 30 second timeout
)

await delegator.delegate_task(task)

After 30 seconds, if agent hasn't completed:
- Task marked as TIMEOUT
- Automatically reassigned (if retries available)
- Statistics updated
text

---

### Query Methods

#### `get_task()`

def get_task(self, task_id: str) -> Optional[Task]:
"""Get task by ID"""

text

#### `get_agent_tasks()`

def get_agent_tasks(self, agent_id: str) -> List[Task]:
"""Get all tasks assigned to specific agent"""

text

#### `get_tasks_by_status()`

def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
"""Get all tasks with specific status"""

text

**Examples:**
Get specific task
task = delegator.get_task("task-123")

Get all tasks for an agent
agent_tasks = delegator.get_agent_tasks("calendar-agent-1")
print(f"Agent has {len(agent_tasks)} tasks")

Get all pending tasks
pending = delegator.get_tasks_by_status(TaskStatus.PENDING)
print(f"{len(pending)} tasks awaiting assignment")

Get all completed tasks
completed = delegator.get_tasks_by_status(TaskStatus.COMPLETED)

text

---

### Statistics

#### `get_statistics()`

def get_statistics(self) -> Dict[str, Any]:
"""
Get comprehensive delegation statistics.

text
Returns:
    Dictionary with current and cumulative stats
"""
text

**Response Structure:**
{
# Cumulative stats
"total_assigned": 150,
"total_completed": 120,
"total_failed": 10,
"total_timeout": 5,
"total_retries": 15,

text
# Current state
"current_pending": 5,
"current_assigned": 8,
"current_in_progress": 12,
"current_completed": 120,
"current_failed": 10,
"current_timeout": 5,
"total_tasks": 160
}

text

**Example:**
stats = delegator.get_statistics()

print("Task Delegator Statistics:")
print(f" Total Assigned: {stats['total_assigned']}")
print(f" Total Completed: {stats['total_completed']} "
f"({stats['total_completed']/stats['total_assigned']*100:.1f}%)")
print(f" Total Failed: {stats['total_failed']}")
print(f" Total Timeouts: {stats['total_timeout']}")
print(f" Total Retries: {stats['total_retries']}")
print(f"\nCurrent State:")
print(f" Pending: {stats['current_pending']}")
print(f" In Progress: {stats['current_assigned'] + stats['current_in_progress']}")
print(f" Completed: {stats['current_completed']}")

text

---

### Maintenance

#### `clear_completed_tasks()`

def clear_completed_tasks(self, older_than_minutes: int = 60) -> int:
"""
Clear completed/failed/timeout tasks older than specified time.

text
Args:
    older_than_minutes: Clear tasks completed before N minutes ago
    
Returns:
    Number of tasks cleared
"""
text

**Example:**
Clear tasks older than 1 hour
cleared = delegator.clear_completed_tasks(older_than_minutes=60)
print(f"Cleared {cleared} old tasks")

Clear tasks older than 24 hours
cleared = delegator.clear_completed_tasks(older_than_minutes=1440)

text

---

## 🔄 Complete Task Lifecycle Example

from theaia.core.multi_agent.task_delegator import (
TaskDelegator,
TaskPriority,
TaskStatus
)
from theaia.core.multi_agent.agent_metadata import AgentCapability

Setup
delegator = TaskDelegator(registry, discovery, broker)
await delegator.start_monitoring()

1. Create task
task = delegator.create_task(
task_type=AgentCapability.EVENT_CREATION.value,
payload={
"title": "Project Review",
"date": "2025-12-15",
"attendees": ["alice@example.com", "bob@example.com"]
},
priority=TaskPriority.HIGH,
timeout_seconds=300,
max_retries=3
)

print(f"✅ Task created: {task.task_id}")
print(f" Status: {task.status}") # PENDING

2. Delegate task
success = await delegator.delegate_task(task)

if success:
print(f"✅ Task delegated to: {task.assigned_agent_id}")
print(f" Status: {task.status}") # ASSIGNED
else:
print("❌ No agent available")

3. Agent marks in progress (via message)
task.mark_in_progress()
print(f"⏳ Task in progress")
print(f" Status: {task.status}") # IN_PROGRESS

4a. Success path: Agent completes task
result = {
"event_id": "evt123",
"status": "created",
"url": "https://calendar.example.com/evt123"
}

await delegator.complete_task(
task_id=task.task_id,
result=result,
agent_id=task.assigned_agent_id
)

print(f"✅ Task completed")
print(f" Status: {task.status}") # COMPLETED
print(f" Result: {task.result}")

4b. Failure path: Agent fails task
error = "Calendar API unavailable"

await delegator.fail_task(
task_id=task.task_id,
error=error,
agent_id=task.assigned_agent_id
)

if task.status == TaskStatus.ASSIGNED:
print(f"🔄 Task retried (attempt {task.retry_count}/{task.max_retries})")
elif task.status == TaskStatus.FAILED:
print(f"❌ Task failed: {task.error}")

4c. Timeout path: Task times out
(handled automatically by monitoring)
await asyncio.sleep(task.timeout_seconds + 5)

Task automatically reassigned or failed
5. Check statistics
stats = delegator.get_statistics()
print(f"\n📊 Statistics:")
print(f" Completed: {stats['total_completed']}")
print(f" Failed: {stats['total_failed']}")
print(f" Timeouts: {stats['total_timeout']}")
print(f" Retries: {stats['total_retries']}")

6. Cleanup
await delegator.stop_monitoring()

text

---

## 🔧 Helper Function

### `_capability_from_string()`

def _capability_from_string(capability_str: str) -> Optional[AgentCapability]:
"""
Convert string to AgentCapability enum.

text
Critical for task delegation - converts task_type (string)
to AgentCapability (enum) for discovery service.

Args:
    capability_str: Capability string (e.g., "calendar_management")
    
Returns:
    AgentCapability enum or None if invalid
    
Logic:
    1. Try direct lookup: AgentCapability(capability_str)
    2. Try uppercase: AgentCapability[capability_str.upper()]
    3. Return None if both fail
"""
text

**Example:**
Direct match
cap = _capability_from_string("calendar_management")

Returns: AgentCapability.CALENDAR_MANAGEMENT
Uppercase match
cap = _capability_from_string("CALENDAR_MANAGEMENT")

Returns: AgentCapability.CALENDAR_MANAGEMENT
Invalid
cap = _capability_from_string("invalid_capability")

Returns: None
text

---

## 💡 Advanced Usage Examples

### Priority-based Task Queue

async def process_task_queue(
tasks: List[Dict[str, Any]],
delegator: TaskDelegator
):
"""Process tasks in priority order"""

text
# Create all tasks
task_objects = []
for task_data in tasks:
    task = delegator.create_task(
        task_type=task_data["type"],
        payload=task_data["payload"],
        priority=task_data.get("priority", TaskPriority.NORMAL)
    )
    task_objects.append(task)

# Sort by priority (URGENT first)
task_objects.sort(key=lambda t: t.priority.value, reverse=True)

# Delegate in priority order
for task in task_objects:
    success = await delegator.delegate_task(task)
    if success:
        print(f"Delegated {task.priority.name} task: {task.task_id}")
    else:
        print(f"Failed to delegate task: {task.task_id}")
text

---

### Retry with Exponential Backoff

async def delegate_with_backoff(
delegator: TaskDelegator,
task_type: str,
payload: Dict[str, Any],
max_attempts: int = 5
) -> Optional[str]:
"""
Delegate task with exponential backoff on failure.
"""
backoff_seconds = 1

text
for attempt in range(max_attempts):
    task_id = await delegator.delegate_to_best_agent(
        task_type=task_type,
        payload=payload
    )
    
    if task_id:
        return task_id
    
    if attempt < max_attempts - 1:
        print(f"Attempt {attempt + 1} failed, retrying in {backoff_seconds}s...")
        await asyncio.sleep(backoff_seconds)
        backoff_seconds *= 2  # Exponential backoff

return None
text

---

### Task Progress Tracking

async def track_task_progress(
delegator: TaskDelegator,
task_id: str,
poll_interval: float = 1.0
) -> Any:
"""
Poll task until completion or failure.

text
Returns:
    Task result if successful, raises exception if failed
"""
while True:
    task = delegator.get_task(task_id)
    
    if task is None:
        raise ValueError(f"Task {task_id} not found")
    
    if task.status == TaskStatus.COMPLETED:
        return task.result
    
    if task.status in [TaskStatus.FAILED, TaskStatus.TIMEOUT]:
        raise RuntimeError(f"Task failed: {task.error}")
    
    # Still in progress
    print(f"Task {task_id}: {task.status.value}...")
    await asyncio.sleep(poll_interval)
text

**Usage:**
task_id = await delegator.delegate_to_best_agent(
task_type=AgentCapability.EVENT_CREATION.value,
payload={"event": "Meeting"}
)

try:
result = await track_task_progress(delegator, task_id)
print(f"Task completed: {result}")
except RuntimeError as e:
print(f"Task failed: {e}")

text

---

### Batch Task Delegation

async def delegate_batch(
delegator: TaskDelegator,
tasks: List[Dict[str, Any]],
strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN
) -> Dict[str, List[str]]:
"""
Delegate multiple tasks efficiently.

text
Returns:
    Dictionary with 'succeeded' and 'failed' task IDs
"""
results = {"succeeded": [], "failed": []}

for task_data in tasks:
    task_id = await delegator.delegate_to_best_agent(
        task_type=task_data["type"],
        payload=task_data["payload"],
        priority=task_data.get("priority", TaskPriority.NORMAL),
        strategy=strategy
    )
    
    if task_id:
        results["succeeded"].append(task_id)
    else:
        results["failed"].append(task_data)

print(f"Batch delegation: {len(results['succeeded'])} succeeded, "
      f"{len(results['failed'])} failed")

return results
text

---

### Monitoring Dashboard

def print_delegator_dashboard(delegator: TaskDelegator):
"""Print comprehensive delegator status"""
stats = delegator.get_statistics()

text
print("=" * 70)
print("TASK DELEGATOR DASHBOARD")
print("=" * 70)

# Summary
total = stats['total_assigned']
completed = stats['total_completed']
failed = stats['total_failed']
timeout = stats['total_timeout']

success_rate = (completed / total * 100) if total > 0 else 0

print(f"\n📊 Overall Statistics:")
print(f"   Total Assigned:    {total}")
print(f"   Completed:         {completed} ({success_rate:.1f}%)")
print(f"   Failed:            {failed}")
print(f"   Timeouts:          {timeout}")
print(f"   Retries:           {stats['total_retries']}")

# Current state
print(f"\n⏱️  Current State:")
print(f"   Pending:           {stats['current_pending']}")
print(f"   Assigned:          {stats['current_assigned']}")
print(f"   In Progress:       {stats['current_in_progress']}")

# Success bar
if total > 0:
    bar_length = 40
    success_bar = "█" * int(success_rate / 100 * bar_length)
    fail_bar = "░" * (bar_length - len(success_bar))
    print(f"\n   Success Rate: [{success_bar}{fail_bar}] {success_rate:.1f}%")

print("=" * 70)
text

---

## 🧪 Testing

**Test File:** `tests/unit/multi_agent/test_task_delegator.py`  
**Total Tests:** 26  
**Status:** ✅ All passing

### Test Categories

- ✅ Task creation and validation (3 tests)
- ✅ Task delegation (5 tests)
- ✅ Lifecycle management (3 tests)
- ✅ Reassignment (3 tests)
- ✅ Timeout handling (4 tests)
- ✅ Priority mapping (1 test)
- ✅ Statistics tracking (3 tests)
- ✅ Edge cases (3 tests)
- ✅ Monitoring lifecycle (1 test)

---

## 📈 Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| `create_task()` | O(1) | Simple dict insertion |
| `delegate_task()` | O(n) | Discovery scan + message send |
| `complete_task()` | O(1) | Dict lookup + updates |
| `get_task()` | O(1) | Dict lookup |
| `get_tasks_by_status()` | O(n) | Full task scan |
| `_check_timeouts()` | O(n) | Scan all in-progress tasks |

**Memory Usage:** ~1KB per task

---

## 🔄 Integration Points

### Used By
- `Orchestrator` - Main application task submission
- `API Endpoints` - User-facing task operations
- `ScheduledJobs` - Periodic task execution

### Dependencies
- `AgentRegistry` - Agent state management
- `DiscoveryService` - Agent selection
- `MessageBroker` - Agent communication
- `AgentMetadata` - Agent capabilities

---

## 🚀 Future Enhancements

- [ ] Task dependencies (wait for other tasks)
- [ ] Task scheduling (execute at specific time)
- [ ] Persistent task storage (database)
- [ ] Task cancellation support
- [ ] Task priority adjustment
- [ ] Dead letter queue for failed tasks
- [ ] Metrics export (Prometheus)
- [ ] Circuit breaker pattern
- [ ] Rate limiting per agent

---

## 📝 Best Practices

### ✅ DO
- Always start monitoring before delegating tasks
- Set appropriate timeout values per task type
- Use priority levels judiciously
- Clear completed tasks periodically
- Monitor statistics for system health
- Handle delegation failures gracefully

### ❌ DON'T
- Don't forget to stop monitoring on shutdown
- Don't set timeout too short for complex tasks
- Don't ignore failed task statistics
- Don't create tasks without payload validation
- Don't assume delegation always succeeds
- Don't keep completed tasks indefinitely

---

## 🔍 Troubleshooting

### Tasks not being delegated

**Symptoms:** `delegate_task()` returns `False`

**Causes:**
- No agents with required capability
- All agents overloaded
- Invalid task_type string

**Solutions:**
Check available agents
from theaia.core.multi_agent.agent_metadata import AgentCapability

Convert task_type to capability
cap = _capability_from_string(task.task_type)
if cap is None:
print(f"Invalid task type: {task.task_type}")

Check if agents exist
agents = discovery.discover_by_capability(cap)
if not agents:
print(f"No agents for capability: {cap}")

Check agent availability
available = [a for a in agents if a.is_available]
print(f"Available agents: {len(available)}/{len(agents)}")

text

---

### High timeout rate

**Symptoms:** Many tasks reaching `TIMEOUT` status

**Causes:**
- Timeout value too low
- Agents overloaded
- Tasks too complex

**Solutions:**
Increase timeout
task = delegator.create_task(
task_type=task_type,
payload=payload,
timeout_seconds=600 # Increase from 300
)

Check agent load
stats = delegator.get_statistics()
in_progress = stats['current_assigned'] + stats['current_in_progress']
print(f"Tasks in progress: {in_progress}")

Monitor timeout patterns
timeout_tasks = delegator.get_tasks_by_status(TaskStatus.TIMEOUT)
for task in timeout_tasks:
print(f"Timeout: {task.task_id} on {task.assigned_agent_id}")

text

---

### Memory leak from completed tasks

**Symptoms:** Increasing memory usage over time

**Cause:** Not clearing completed tasks

**Solution:**
Schedule periodic cleanup
async def cleanup_loop():
while True:
await asyncio.sleep(3600) # Every hour
cleared = delegator.clear_completed_tasks(older_than_minutes=60)
print(f"Cleaned {cleared} old tasks")

asyncio.create_task(cleanup_loop())

text

---
