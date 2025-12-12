"""
Unit tests for Task Delegation System
Tests task creation, assignment, lifecycle, and monitoring.

Author: Álvaro Fernández Mota
Date: 12 December 2025
Version: 2.0.1 - Fixed batch delegation load distribution test
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from theaia.core.multi_agent.task_delegator import (
    TaskDelegator,
    Task,
    TaskPriority,
    TaskStatus,
    RetryPolicy,
)
from theaia.core.multi_agent.agent_registry import AgentRegistry
from theaia.core.multi_agent.agent_metadata import (
    AgentMetadata,
    AgentStatus,
    AgentCapability,
)
from theaia.core.multi_agent.discovery_service import (
    DiscoveryService,
    LoadBalancingStrategy,
)
from theaia.core.multi_agent.message.broker import MessageBroker
from theaia.core.multi_agent.message.types import MessageType, MessagePriority


@pytest.fixture
def agent_registry():
    """Create agent registry with test agents"""
    registry = AgentRegistry()
    
    # ✅ FIX SINGLETON: Limpiar antes de empezar
    registry.clear()
    
    agent1 = AgentMetadata(
        agent_id="agent1",
        agent_type="worker",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT, AgentCapability.EVENT_CREATION},
        max_capacity=10,  # ✅ AUMENTADO para soportar batch tests
        status=AgentStatus.HEALTHY,
    )
    agent2 = AgentMetadata(
        agent_id="agent2",
        agent_type="worker",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT},
        max_capacity=10,  # ✅ AUMENTADO para soportar batch tests
        status=AgentStatus.HEALTHY,
    )
    
    registry.register(agent1)
    registry.register(agent2)
    
    yield registry
    
    # ✅ FIX SINGLETON: Limpiar después de cada test
    registry.clear()


@pytest.fixture
def discovery_service(agent_registry):
    """Create discovery service"""
    return DiscoveryService(agent_registry)


@pytest.fixture
def message_broker():
    """Create message broker"""
    return MessageBroker()


@pytest.fixture
def task_delegator(agent_registry, discovery_service, message_broker):
    """Create task delegator"""
    return TaskDelegator(agent_registry, discovery_service, message_broker)


@pytest.fixture
def custom_retry_policy():
    """Create custom retry policy for testing"""
    return RetryPolicy(
        base_delay=0.1,  # Fast for testing
        max_delay=1.0,
        multiplier=2.0,
        jitter=0.0,  # No jitter for predictable tests
    )


# ============================================================================
# TASK CREATION TESTS
# ============================================================================

def test_create_task(task_delegator):
    """Test basic task creation"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        priority=TaskPriority.HIGH,
    )
    
    assert task.task_id in task_delegator.tasks
    assert task.task_type == AgentCapability.CALENDAR_MANAGEMENT.value
    assert task.payload == {"data": "test"}
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.PENDING


def test_create_task_with_metadata(task_delegator):
    """Test task creation with metadata"""
    metadata = {"user_id": "user123", "session_id": "session456"}
    
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        metadata=metadata,
    )
    
    assert task.metadata == metadata


def test_create_task_with_custom_timeout(task_delegator):
    """Test task creation with custom timeout"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        timeout_seconds=600,
        max_retries=5,
    )
    
    assert task.timeout_seconds == 600
    assert task.max_retries == 5


def test_create_task_with_dependencies(task_delegator):
    """Test task creation with dependencies"""
    task1 = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "task1"},
    )
    
    task2 = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "task2"},
        depends_on=[task1.task_id],
    )
    
    assert task2.depends_on == [task1.task_id]
    assert len(task1.depends_on) == 0


# ============================================================================
# RETRY POLICY TESTS (NEW FEATURE 1)
# ============================================================================

def test_retry_policy_exponential_backoff():
    """Test exponential backoff calculation"""
    policy = RetryPolicy(base_delay=1.0, multiplier=2.0, jitter=0.0)
    
    assert policy.calculate_delay(0) == 1.0  # 1 * 2^0
    assert policy.calculate_delay(1) == 2.0  # 1 * 2^1
    assert policy.calculate_delay(2) == 4.0  # 1 * 2^2
    assert policy.calculate_delay(3) == 8.0  # 1 * 2^3


def test_retry_policy_max_delay():
    """Test max delay cap"""
    policy = RetryPolicy(base_delay=1.0, max_delay=5.0, multiplier=2.0, jitter=0.0)
    
    assert policy.calculate_delay(10) == 5.0  # Capped at max_delay


def test_retry_policy_with_jitter():
    """Test jitter adds randomness"""
    policy = RetryPolicy(base_delay=1.0, multiplier=2.0, jitter=0.2)
    
    delays = [policy.calculate_delay(1) for _ in range(10)]
    
    # All delays should be around 2.0 +/- 20%
    assert all(1.6 <= d <= 2.4 for d in delays)
    # Should have some variation
    assert len(set(delays)) > 1


def test_task_delegator_uses_retry_policy(agent_registry, discovery_service, message_broker, custom_retry_policy):
    """Test TaskDelegator uses custom retry policy"""
    delegator = TaskDelegator(
        agent_registry,
        discovery_service,
        message_broker,
        retry_policy=custom_retry_policy,
    )
    
    assert delegator.retry_policy == custom_retry_policy


@pytest.mark.asyncio
async def test_retry_uses_exponential_backoff(task_delegator):
    """Test retry delay increases exponentially"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        max_retries=3,
    )
    
    await task_delegator.delegate_task(task)
    agent_id = task.assigned_agent_id
    
    # Fail task multiple times and check delays
    for i in range(3):
        await task_delegator.fail_task(task.task_id, f"error {i}", agent_id)
        
        if task.can_retry():
            # Delay should increase with each retry
            expected_min_delay = task_delegator.retry_policy.base_delay * (2 ** i)
            assert task.retry_delay >= expected_min_delay * 0.9  # Account for jitter


# ============================================================================
# TASK CANCELLATION TESTS (NEW FEATURE 2)
# ============================================================================

@pytest.mark.asyncio
async def test_cancel_pending_task(task_delegator):
    """Test cancelling pending task"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    success = await task_delegator.cancel_task(task.task_id, "User requested")
    
    assert success is True
    assert task.status == TaskStatus.CANCELLED
    assert task.error == "User requested"
    assert task.completed_at is not None
    assert task_delegator.stats["total_cancelled"] == 1


@pytest.mark.asyncio
async def test_cancel_assigned_task(task_delegator):
    """Test cancelling assigned task sends message to agent"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    agent_id = task.assigned_agent_id
    
    success = await task_delegator.cancel_task(task.task_id, "Priority changed")
    
    assert success is True
    assert task.status == TaskStatus.CANCELLED
    # Agent should be unloaded
    assert agent_id not in task_delegator.agent_tasks or task.task_id not in task_delegator.agent_tasks[agent_id]


@pytest.mark.asyncio
async def test_cancel_completed_task_fails(task_delegator):
    """Test cannot cancel already completed task"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    await task_delegator.complete_task(task.task_id, {"result": "done"}, task.assigned_agent_id)
    
    success = await task_delegator.cancel_task(task.task_id)
    
    assert success is False
    assert task.status == TaskStatus.COMPLETED  # Unchanged


@pytest.mark.asyncio
async def test_cancel_nonexistent_task(task_delegator):
    """Test cancelling nonexistent task"""
    success = await task_delegator.cancel_task("nonexistent_id")
    
    assert success is False


# ============================================================================
# BATCH DELEGATION TESTS (NEW FEATURE 3)
# ============================================================================

@pytest.mark.asyncio
async def test_batch_delegation_success(task_delegator):
    """Test batch delegating multiple tasks"""
    tasks = [
        task_delegator.create_task(
            AgentCapability.CALENDAR_MANAGEMENT.value,
            {"data": f"test{i}"}
        )
        for i in range(5)
    ]
    
    results = await task_delegator.delegate_tasks_batch(tasks)
    
    assert len(results) == 5
    assert all(results.values())  # All should succeed
    assert all(t.status == TaskStatus.ASSIGNED for t in tasks)


@pytest.mark.asyncio
async def test_batch_delegation_partial_failure(task_delegator):
    """Test batch delegation with some invalid tasks"""
    valid_tasks = [
        task_delegator.create_task(
            AgentCapability.CALENDAR_MANAGEMENT.value,
            {"data": f"valid{i}"}
        )
        for i in range(3)
    ]
    
    invalid_tasks = [
        task_delegator.create_task(
            "nonexistent_capability",
            {"data": f"invalid{i}"}
        )
        for i in range(2)
    ]
    
    all_tasks = valid_tasks + invalid_tasks
    results = await task_delegator.delegate_tasks_batch(all_tasks)
    
    assert len(results) == 5
    assert sum(results.values()) == 3  # Only valid tasks succeed


@pytest.mark.asyncio
async def test_batch_delegation_load_distribution(task_delegator):
    """Test batch delegation distributes load across agents"""
    tasks = [
        task_delegator.create_task(
            AgentCapability.CALENDAR_MANAGEMENT.value,
            {"data": f"test{i}"}
        )
        for i in range(10)
    ]
    
    await task_delegator.delegate_tasks_batch(tasks, strategy=LoadBalancingStrategy.LEAST_LOADED)
    
    # Both agents should have tasks
    agent1_tasks = task_delegator.get_agent_tasks("agent1")
    agent2_tasks = task_delegator.get_agent_tasks("agent2")
    
    # ✅ FIX: Verify all tasks were assigned
    assert len(agent1_tasks) + len(agent2_tasks) == 10
    # Both agents should participate in load distribution
    assert len(agent1_tasks) > 0
    assert len(agent2_tasks) > 0
    # Load should be relatively balanced (within 60% of each other)
    ratio = min(len(agent1_tasks), len(agent2_tasks)) / max(len(agent1_tasks), len(agent2_tasks))
    assert ratio >= 0.4  # Allow for some imbalance due to strategy


# ============================================================================
# PROGRESS TRACKING TESTS (NEW FEATURE 4)
# ============================================================================

@pytest.mark.asyncio
async def test_update_task_progress(task_delegator):
    """Test updating task progress"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    agent_id = task.assigned_agent_id
    
    success = await task_delegator.update_task_progress(
        task.task_id, 50, "Halfway done", agent_id
    )
    
    assert success is True
    assert task.progress_percent == 50
    assert task.progress_message == "Halfway done"


@pytest.mark.asyncio
async def test_progress_clamped_to_range(task_delegator):
    """Test progress is clamped to 0-100"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    task.update_progress(-10, "negative")
    assert task.progress_percent == 0
    
    task.update_progress(150, "over 100")
    assert task.progress_percent == 100


@pytest.mark.asyncio
async def test_progress_callback_triggered(task_delegator):
    """Test progress callbacks are triggered"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    agent_id = task.assigned_agent_id
    
    # Register callback
    callback_data = []
    def callback(task_id, percent, message):
        callback_data.append((task_id, percent, message))
    
    task_delegator.register_progress_callback(task.task_id, callback)
    
    # Update progress
    await task_delegator.update_task_progress(task.task_id, 25, "Starting", agent_id)
    await task_delegator.update_task_progress(task.task_id, 75, "Almost done", agent_id)
    
    assert len(callback_data) == 2
    assert callback_data[0] == (task.task_id, 25, "Starting")
    assert callback_data[1] == (task.task_id, 75, "Almost done")


@pytest.mark.asyncio
async def test_progress_update_wrong_agent_rejected(task_delegator):
    """Test progress update from wrong agent is rejected"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    
    wrong_agent = "wrong_agent_id"
    success = await task_delegator.update_task_progress(
        task.task_id, 50, "Progress", wrong_agent
    )
    
    assert success is False
    assert task.progress_percent == 0  # Unchanged


@pytest.mark.asyncio
async def test_multiple_progress_callbacks(task_delegator):
    """Test multiple callbacks can be registered"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    
    callback1_data = []
    callback2_data = []
    
    task_delegator.register_progress_callback(
        task.task_id,
        lambda tid, p, m: callback1_data.append(p)
    )
    task_delegator.register_progress_callback(
        task.task_id,
        lambda tid, p, m: callback2_data.append(p)
    )
    
    await task_delegator.update_task_progress(task.task_id, 60, "Progress", task.assigned_agent_id)
    
    assert callback1_data == [60]
    assert callback2_data == [60]


# ============================================================================
# TASK DEPENDENCIES TESTS (NEW FEATURE 5)
# ============================================================================

def test_check_dependencies_completed(task_delegator):
    """Test checking if dependencies are completed"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task2"},
        depends_on=[task1.task_id]
    )
    
    # Dependency not completed
    assert task_delegator.check_dependencies_completed(task2.task_id) is False
    
    # Complete dependency
    task1.mark_completed({"result": "done"})
    assert task_delegator.check_dependencies_completed(task2.task_id) is True


def test_check_dependencies_no_dependencies(task_delegator):
    """Test task with no dependencies returns True"""
    task = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task"}
    )
    
    assert task_delegator.check_dependencies_completed(task.task_id) is True


@pytest.mark.asyncio
async def test_delegate_task_with_unsatisfied_dependencies(task_delegator):
    """Test delegating task with unsatisfied dependencies fails"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task2"},
        depends_on=[task1.task_id]
    )
    
    success = await task_delegator.delegate_task(task2)
    
    assert success is False
    assert task2.status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_auto_delegation_after_dependency_completion(task_delegator):
    """Test task auto-delegates when dependencies complete"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task2"},
        depends_on=[task1.task_id]
    )
    
    # Start monitoring
    await task_delegator.start_monitoring()
    
    # Delegate and complete task1
    await task_delegator.delegate_task(task1)
    task1.mark_completed({"result": "done"})
    
    # Check dependencies (simulates monitoring loop)
    await task_delegator._check_dependencies()
    
    # task2 should now be assigned
    assert task2.status == TaskStatus.ASSIGNED
    
    await task_delegator.stop_monitoring()


@pytest.mark.asyncio
async def test_dependency_chain(task_delegator):
    """Test chain of dependent tasks"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task2"},
        depends_on=[task1.task_id]
    )
    task3 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task3"},
        depends_on=[task2.task_id]
    )
    
    # Only task1 can be delegated initially
    assert await task_delegator.delegate_task(task1) is True
    assert await task_delegator.delegate_task(task2) is False
    assert await task_delegator.delegate_task(task3) is False
    
    # Complete task1
    task1.mark_completed({"result": "done"})
    
    # Now task2 can be delegated
    assert await task_delegator.delegate_task(task2) is True
    assert await task_delegator.delegate_task(task3) is False
    
    # Complete task2
    task2.mark_completed({"result": "done"})
    
    # Now task3 can be delegated
    assert await task_delegator.delegate_task(task3) is True


# ============================================================================
# DEAD LETTER QUEUE TESTS (NEW FEATURE 6)
# ============================================================================

@pytest.mark.asyncio
async def test_task_moved_to_dlq_on_permanent_failure(task_delegator):
    """Test task is moved to DLQ when retries exhausted"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        max_retries=0,
    )
    
    await task_delegator.delegate_task(task)
    agent_id = task.assigned_agent_id
    
    await task_delegator.fail_task(task.task_id, "Permanent error", agent_id)
    
    assert task.task_id in task_delegator.dead_letter_queue
    assert task.status == TaskStatus.FAILED
    assert task_delegator.stats["total_dlq"] == 1


@pytest.mark.asyncio
async def test_timeout_moves_to_dlq(task_delegator):
    """Test timeout after max retries moves to DLQ"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        timeout_seconds=1,
        max_retries=0,
    )
    
    await task_delegator.delegate_task(task)
    task.assigned_at = datetime.now() - timedelta(seconds=5)
    
    await task_delegator._handle_timeout(task)
    
    assert task.task_id in task_delegator.dead_letter_queue
    assert task_delegator.stats["total_dlq"] == 1


def test_get_dlq_tasks(task_delegator):
    """Test retrieving tasks from DLQ"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task2"}
    )
    
    # Manually add to DLQ
    task_delegator.dead_letter_queue[task1.task_id] = task1
    task_delegator.dead_letter_queue[task2.task_id] = task2
    
    dlq_tasks = task_delegator.get_dlq_tasks()
    
    assert len(dlq_tasks) == 2
    assert task1 in dlq_tasks
    assert task2 in dlq_tasks


def test_clear_dlq(task_delegator):
    """Test clearing DLQ"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task2"}
    )
    
    task_delegator.dead_letter_queue[task1.task_id] = task1
    task_delegator.dead_letter_queue[task2.task_id] = task2
    
    count = task_delegator.clear_dlq()
    
    assert count == 2
    assert len(task_delegator.dead_letter_queue) == 0


def test_statistics_include_dlq(task_delegator):
    """Test statistics include DLQ count"""
    task = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "task"}
    )
    
    task_delegator.dead_letter_queue[task.task_id] = task
    
    stats = task_delegator.get_statistics()
    
    assert stats["current_dlq"] == 1
    assert "total_dlq" in stats


# ============================================================================
# TASK DELEGATION TESTS (EXISTING)
# ============================================================================

@pytest.mark.asyncio
async def test_delegate_task_success(task_delegator):
    """Test successful task delegation"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    success = await task_delegator.delegate_task(task)
    
    assert success is True
    assert task.status == TaskStatus.ASSIGNED
    assert task.assigned_agent_id in ["agent1", "agent2"]
    assert task.assigned_at is not None
    assert task_delegator.stats["total_assigned"] == 1


@pytest.mark.asyncio
async def test_delegate_task_no_available_agent(task_delegator):
    """Test delegation when no agent available"""
    task = task_delegator.create_task(
        task_type="nonexistent_capability",
        payload={"data": "test"},
    )
    
    success = await task_delegator.delegate_task(task)
    
    assert success is False
    assert task.status == TaskStatus.PENDING
    assert task.assigned_agent_id is None


@pytest.mark.asyncio
async def test_delegate_to_best_agent(task_delegator):
    """Test combined create and delegate"""
    task_id = await task_delegator.delegate_to_best_agent(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        priority=TaskPriority.URGENT,
    )
    
    assert task_id is not None
    task = task_delegator.get_task(task_id)
    assert task.status == TaskStatus.ASSIGNED
    assert task.priority == TaskPriority.URGENT


@pytest.mark.asyncio
async def test_delegate_with_load_balancing_strategy(task_delegator):
    """Test delegation with specific load balancing strategy"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    success = await task_delegator.delegate_task(
        task,
        strategy=LoadBalancingStrategy.ROUND_ROBIN,
    )
    
    assert success is True
    assert task.status == TaskStatus.ASSIGNED


# ============================================================================
# TASK LIFECYCLE TESTS (EXISTING)
# ============================================================================

@pytest.mark.asyncio
async def test_complete_task(task_delegator):
    """Test task completion"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    agent_id = task.assigned_agent_id
    
    result = {"output": "success"}
    success = await task_delegator.complete_task(task.task_id, result, agent_id)
    
    assert success is True
    assert task.status == TaskStatus.COMPLETED
    assert task.result == result
    assert task.completed_at is not None
    assert task.progress_percent == 100  # Auto-set to 100%
    assert task_delegator.stats["total_completed"] == 1


@pytest.mark.asyncio
async def test_fail_task_without_retry(task_delegator):
    """Test task failure when retries exhausted"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        max_retries=0,
    )
    
    await task_delegator.delegate_task(task)
    agent_id = task.assigned_agent_id
    
    error = "Processing error"
    success = await task_delegator.fail_task(task.task_id, error, agent_id)
    
    assert success is True
    assert task.status == TaskStatus.FAILED
    assert task.error == error
    assert task_delegator.stats["total_failed"] == 1


@pytest.mark.asyncio
async def test_fail_task_with_retry(task_delegator):
    """Test task failure triggers retry"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        max_retries=3,
    )
    
    await task_delegator.delegate_task(task)
    original_agent_id = task.assigned_agent_id
    
    error = "Temporary error"
    await task_delegator.fail_task(task.task_id, error, original_agent_id)
    
    assert task.retry_count == 1
    assert task.status == TaskStatus.ASSIGNED  # Reassigned after retry
    assert task_delegator.stats["total_retries"] == 1


# ============================================================================
# TASK REASSIGNMENT TESTS (EXISTING)
# ============================================================================

@pytest.mark.asyncio
async def test_reassign_task_to_specific_agent(task_delegator):
    """Test reassigning task to specific agent"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    original_agent = task.assigned_agent_id
    
    # Get different agent
    new_agent = "agent2" if original_agent == "agent1" else "agent1"
    
    success = await task_delegator.reassign_task(task.task_id, new_agent)
    
    assert success is True
    assert task.assigned_agent_id == new_agent
    assert task.status == TaskStatus.ASSIGNED


@pytest.mark.asyncio
async def test_reassign_task_auto_select(task_delegator):
    """Test reassigning task with auto-selection"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
    )
    
    await task_delegator.delegate_task(task)
    
    success = await task_delegator.reassign_task(task.task_id)
    
    assert success is True
    assert task.status == TaskStatus.ASSIGNED


@pytest.mark.asyncio
async def test_reassign_nonexistent_task(task_delegator):
    """Test reassigning nonexistent task"""
    success = await task_delegator.reassign_task("nonexistent_id")
    
    assert success is False


# ============================================================================
# TIMEOUT HANDLING TESTS (EXISTING)
# ============================================================================

def test_task_timeout_detection():
    """Test timeout detection logic"""
    task = Task(
        task_type="test",
        timeout_seconds=10,
    )
    
    # Not assigned yet - no timeout
    assert task.is_timed_out() is False
    
    # Assign and simulate past timeout
    task.assigned_at = datetime.now() - timedelta(seconds=15)
    assert task.is_timed_out() is True


@pytest.mark.asyncio
async def test_timeout_triggers_reassignment(task_delegator):
    """Test timeout triggers automatic reassignment"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        timeout_seconds=1,
        max_retries=2,
    )
    
    await task_delegator.delegate_task(task)
    
    # Simulate timeout by manually setting assigned_at
    task.assigned_at = datetime.now() - timedelta(seconds=5)
    
    await task_delegator._handle_timeout(task)
    
    assert task.retry_count == 1
    assert task.status == TaskStatus.ASSIGNED  # Reassigned
    assert task_delegator.stats["total_timeout"] == 1
    assert task_delegator.stats["total_retries"] == 1


@pytest.mark.asyncio
async def test_timeout_max_retries_exceeded(task_delegator):
    """Test timeout when max retries exceeded"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        timeout_seconds=1,
        max_retries=0,
    )
    
    await task_delegator.delegate_task(task)
    task.assigned_at = datetime.now() - timedelta(seconds=5)
    
    await task_delegator._handle_timeout(task)
    
    assert task.status == TaskStatus.FAILED
    assert task_delegator.stats["total_failed"] == 1


@pytest.mark.asyncio
async def test_monitoring_detects_timeouts(task_delegator):
    """Test background monitoring detects timeouts"""
    task = task_delegator.create_task(
        task_type=AgentCapability.CALENDAR_MANAGEMENT.value,
        payload={"data": "test"},
        timeout_seconds=1,
    )
    
    await task_delegator.delegate_task(task)
    task.assigned_at = datetime.now() - timedelta(seconds=5)
    
    await task_delegator._check_timeouts()
    
    assert task_delegator.stats["total_timeout"] == 1


# ============================================================================
# PRIORITY TESTS (EXISTING)
# ============================================================================

def test_priority_mapping(task_delegator):
    """Test task priority maps to message priority"""
    mappings = [
        (TaskPriority.LOW, MessagePriority.LOW),
        (TaskPriority.NORMAL, MessagePriority.NORMAL),
        (TaskPriority.HIGH, MessagePriority.HIGH),
        (TaskPriority.URGENT, MessagePriority.CRITICAL),
    ]
    
    for task_priority, expected_msg_priority in mappings:
        msg_priority = task_delegator._map_priority(task_priority)
        assert msg_priority == expected_msg_priority


# ============================================================================
# STATISTICS TESTS (EXISTING + ENHANCED)
# ============================================================================

@pytest.mark.asyncio
async def test_statistics_tracking(task_delegator):
    """Test statistics are tracked correctly"""
    # Create and delegate multiple tasks
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test2"}
    )
    
    await task_delegator.delegate_task(task1)
    await task_delegator.delegate_task(task2)
    
    # Complete one
    await task_delegator.complete_task(
        task1.task_id, {"result": "success"}, task1.assigned_agent_id
    )
    
    # Fail one
    await task_delegator.fail_task(
        task2.task_id, "error", task2.assigned_agent_id
    )
    
    stats = task_delegator.get_statistics()
    
    assert stats["total_assigned"] >= 2
    assert stats["total_completed"] == 1
    assert stats["total_tasks"] == 2
    assert "total_cancelled" in stats
    assert "total_dlq" in stats
    assert "current_dlq" in stats


def test_get_tasks_by_status(task_delegator):
    """Test filtering tasks by status"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test2"}
    )
    
    task1.mark_completed("result")
    
    pending = task_delegator.get_tasks_by_status(TaskStatus.PENDING)
    completed = task_delegator.get_tasks_by_status(TaskStatus.COMPLETED)
    
    assert len(pending) == 1
    assert len(completed) == 1
    assert task2 in pending
    assert task1 in completed


@pytest.mark.asyncio
async def test_get_agent_tasks(task_delegator):
    """Test getting all tasks for specific agent"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test2"}
    )
    
    await task_delegator.delegate_task(task1)
    await task_delegator.delegate_task(task2)
    
    agent_id = task1.assigned_agent_id
    agent_tasks = task_delegator.get_agent_tasks(agent_id)
    
    assert len(agent_tasks) >= 1
    assert task1 in agent_tasks


# ============================================================================
# CLEANUP TESTS (EXISTING + ENHANCED)
# ============================================================================

def test_clear_completed_tasks(task_delegator):
    """Test clearing old completed tasks"""
    task1 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test1"}
    )
    task2 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test2"}
    )
    task3 = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test3"}
    )
    
    # Complete tasks with different times
    task1.mark_completed("result1")
    task1.completed_at = datetime.now() - timedelta(hours=2)
    
    task2.mark_completed("result2")
    task2.completed_at = datetime.now()
    
    # Cancelled task (should also be cleared)
    task3.mark_cancelled("reason")
    task3.completed_at = datetime.now() - timedelta(hours=3)
    
    cleared = task_delegator.clear_completed_tasks(older_than_minutes=60)
    
    assert cleared == 2  # task1 and task3
    assert task1.task_id not in task_delegator.tasks
    assert task2.task_id in task_delegator.tasks
    assert task3.task_id not in task_delegator.tasks


# ============================================================================
# EDGE CASES (EXISTING + NEW)
# ============================================================================

@pytest.mark.asyncio
async def test_complete_task_wrong_agent(task_delegator):
    """Test completing task from wrong agent is rejected"""
    task = task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test"}
    )
    await task_delegator.delegate_task(task)
    
    wrong_agent = "wrong_agent_id"
    success = await task_delegator.complete_task(
        task.task_id, {"result": "success"}, wrong_agent
    )
    
    assert success is False
    assert task.status != TaskStatus.COMPLETED


def test_task_can_retry_logic():
    """Test retry availability logic"""
    task = Task(task_type="test", max_retries=3)
    
    assert task.can_retry() is True
    
    task.retry_count = 3
    assert task.can_retry() is False


def test_task_increment_retry():
    """Test retry increment resets task state"""
    task = Task(
        task_type="test",
        status=TaskStatus.FAILED,
        assigned_agent_id="agent1",
    )
    
    task.increment_retry(delay=2.5)
    
    assert task.retry_count == 1
    assert task.retry_delay == 2.5
    assert task.status == TaskStatus.PENDING
    assert task.assigned_agent_id is None


@pytest.mark.asyncio
async def test_monitoring_lifecycle(task_delegator):
    """Test starting and stopping monitoring"""
    await task_delegator.start_monitoring()
    assert task_delegator._monitor_task is not None
    
    await task_delegator.stop_monitoring()
    assert task_delegator._monitor_task is None


def test_task_repr(task_delegator):
    """Test TaskDelegator string representation"""
    task_delegator.create_task(
        AgentCapability.CALENDAR_MANAGEMENT.value,
        {"data": "test"}
    )
    
    repr_str = repr(task_delegator)
    
    assert "TaskDelegator" in repr_str
    assert "tasks=1" in repr_str
    assert "dlq=0" in repr_str
