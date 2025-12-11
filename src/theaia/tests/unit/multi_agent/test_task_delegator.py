"""
Unit tests for Task Delegation System
Tests task creation, assignment, lifecycle, and monitoring.

Author: Álvaro Fernández Mota
Date: 11 December 2025
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
        max_capacity=5,
        status=AgentStatus.HEALTHY,  # ✅ AGREGADO
    )
    agent2 = AgentMetadata(
        agent_id="agent2",
        agent_type="worker",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT},
        max_capacity=3,
        status=AgentStatus.HEALTHY,  # ✅ AGREGADO
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


# ============================================================================
# TASK DELEGATION TESTS
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
# TASK LIFECYCLE TESTS
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
# TASK REASSIGNMENT TESTS
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
# TIMEOUT HANDLING TESTS
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
# PRIORITY TESTS
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
# STATISTICS TESTS
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
# CLEANUP TESTS
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
    
    # Complete tasks with different times
    task1.mark_completed("result1")
    task1.completed_at = datetime.now() - timedelta(hours=2)
    
    task2.mark_completed("result2")
    task2.completed_at = datetime.now()
    
    cleared = task_delegator.clear_completed_tasks(older_than_minutes=60)
    
    assert cleared == 1
    assert task1.task_id not in task_delegator.tasks
    assert task2.task_id in task_delegator.tasks


# ============================================================================
# EDGE CASES
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
    
    task.increment_retry()
    
    assert task.retry_count == 1
    assert task.status == TaskStatus.PENDING
    assert task.assigned_agent_id is None


@pytest.mark.asyncio
async def test_monitoring_lifecycle(task_delegator):
    """Test starting and stopping monitoring"""
    await task_delegator.start_monitoring()
    assert task_delegator._monitor_task is not None
    
    await task_delegator.stop_monitoring()
    assert task_delegator._monitor_task is None
