"""Tests for TaskDelegator - Coverage target: >85%"""
import pytest
from datetime import datetime, timedelta
from src.theaia.core.multi_agent.task_delegator import Task, TaskStatus, TaskPriority, TaskDelegator

class TestTaskStatus:
    def test_pending_status(self): assert TaskStatus.PENDING.value == "pending"
    def test_assigned_status(self): assert TaskStatus.ASSIGNED.value == "assigned"
    def test_in_progress_status(self): assert TaskStatus.IN_PROGRESS.value == "in_progress"
    def test_completed_status(self): assert TaskStatus.COMPLETED.value == "completed"
    def test_failed_status(self): assert TaskStatus.FAILED.value == "failed"
    def test_cancelled_status(self): assert TaskStatus.CANCELLED.value == "cancelled"

class TestTaskPriority:
    def test_low_priority(self): assert TaskPriority.LOW.value == 1
    def test_normal_priority(self): assert TaskPriority.NORMAL.value == 2
    def test_high_priority(self): assert TaskPriority.HIGH.value == 3
    def test_critical_priority(self): assert TaskPriority.CRITICAL.value == 4

class TestTaskBasic:
    def test_task_creation(self):
        task = Task(task_type="test", payload={"data": "value"})
        assert task.task_type == "test" and task.payload == {"data": "value"}
    
    def test_task_id_generated(self):
        task = Task(task_type="test", payload={})
        assert task.task_id is not None and len(task.task_id) > 0
    
    def test_unique_task_ids(self):
        task1 = Task(task_type="test", payload={})
        task2 = Task(task_type="test", payload={})
        assert task1.task_id != task2.task_id
    
    def test_default_status(self):
        task = Task(task_type="test", payload={})
        assert task.status == TaskStatus.PENDING
    
    def test_default_priority(self):
        task = Task(task_type="test", payload={})
        assert task.priority == TaskPriority.NORMAL
    
    def test_required_capabilities(self):
        task = Task(task_type="test", payload={}, required_capabilities={"cap1", "cap2"})
        assert task.required_capabilities == {"cap1", "cap2"}

class TestTaskMethods:
    def test_mark_assigned(self):
        task = Task(task_type="test", payload={})
        task.mark_assigned("agent1")
        assert task.status == TaskStatus.ASSIGNED and task.assigned_agent_id == "agent1" and task.assigned_at is not None
    
    def test_mark_in_progress(self):
        task = Task(task_type="test", payload={})
        task.mark_in_progress()
        assert task.status == TaskStatus.IN_PROGRESS
    
    def test_mark_completed(self):
        task = Task(task_type="test", payload={})
        task.mark_completed({"result": "success"})
        assert task.status == TaskStatus.COMPLETED and task.result == {"result": "success"} and task.completed_at is not None
    
    def test_mark_failed(self):
        task = Task(task_type="test", payload={})
        task.mark_failed("Error message")
        assert task.status == TaskStatus.FAILED and task.error == "Error message" and task.retry_count == 1
    
    def test_can_retry_true(self):
        task = Task(task_type="test", payload={}, max_retries=3)
        task.retry_count = 2
        assert task.can_retry() is True
    
    def test_can_retry_false(self):
        task = Task(task_type="test", payload={}, max_retries=3)
        task.retry_count = 3
        assert task.can_retry() is False
    
    def test_is_expired_false(self):
        task = Task(task_type="test", payload={}, timeout_seconds=300)
        task.mark_assigned("agent1")
        assert task.is_expired() is False
    
    def test_is_expired_true(self):
        task = Task(task_type="test", payload={}, timeout_seconds=0)
        task.mark_assigned("agent1")
        import time
        time.sleep(0.1)
        assert task.is_expired() is True

class TestTaskDelegatorBasic:
    def test_delegator_initialization(self):
        delegator = TaskDelegator()
        assert len(delegator._tasks) == 0 and len(delegator._pending_queue) == 0
    
    def test_create_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test_type", {"data": "value"})
        assert task.task_type == "test_type" and len(delegator._tasks) == 1

class TestTaskDelegatorAssignment:
    def test_assign_task_success(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        result = delegator.assign_task(task.task_id, "agent1")
        assert result is True and task.status == TaskStatus.ASSIGNED
    
    def test_assign_nonexistent_task(self):
        delegator = TaskDelegator()
        result = delegator.assign_task("fake_id", "agent1")
        assert result is False
    
    def test_assign_already_assigned_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        result = delegator.assign_task(task.task_id, "agent2")
        assert result is False

class TestTaskDelegatorSuitability:
    def test_get_suitable_agents_match(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {}, required_capabilities={"cap1"})
        agents = {"agent1": {"cap1", "cap2"}, "agent2": {"cap3"}}
        suitable = delegator.get_suitable_agents(task.task_id, agents)
        assert "agent1" in suitable and "agent2" not in suitable
    
    def test_get_suitable_agents_no_match(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {}, required_capabilities={"cap1"})
        agents = {"agent1": {"cap2"}, "agent2": {"cap3"}}
        suitable = delegator.get_suitable_agents(task.task_id, agents)
        assert len(suitable) == 0

class TestTaskDelegatorBestAgent:
    def test_delegate_to_best_agent_by_load(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {}, required_capabilities={"cap1"})
        agents = {"agent1": {"cap1"}, "agent2": {"cap1"}}
        loads = {"agent1": 5, "agent2": 2}
        best = delegator.delegate_to_best_agent(task.task_id, agents, loads)
        assert best == "agent2"
    
    def test_delegate_no_suitable_agents(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {}, required_capabilities={"cap1"})
        agents = {"agent1": {"cap2"}}
        loads = {"agent1": 0}
        best = delegator.delegate_to_best_agent(task.task_id, agents, loads)
        assert best is None

class TestTaskDelegatorLifecycle:
    def test_start_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        result = delegator.start_task(task.task_id)
        assert result is True and task.status == TaskStatus.IN_PROGRESS
    
    def test_complete_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        result = delegator.complete_task(task.task_id, {"result": "ok"})
        assert result is True and task.status == TaskStatus.COMPLETED
    
    def test_fail_task_with_retry(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        result = delegator.fail_task(task.task_id, "error")
        assert result is True and task.retry_count == 1 and task.status == TaskStatus.PENDING

class TestTaskDelegatorPriorityQueue:
    def test_priority_queue_sorting(self):
        delegator = TaskDelegator()
        t1 = delegator.create_task("low", {}, priority=TaskPriority.LOW)
        t2 = delegator.create_task("critical", {}, priority=TaskPriority.CRITICAL)
        t3 = delegator.create_task("normal", {}, priority=TaskPriority.NORMAL)
        pending = delegator.get_pending_tasks()
        assert pending[0].task_id == t2.task_id and pending[2].task_id == t1.task_id

class TestTaskDelegatorQueries:
    def test_get_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        retrieved = delegator.get_task(task.task_id)
        assert retrieved.task_id == task.task_id
    
    def test_get_agent_tasks(self):
        delegator = TaskDelegator()
        task1 = delegator.create_task("test1", {})
        task2 = delegator.create_task("test2", {})
        delegator.assign_task(task1.task_id, "agent1")
        delegator.assign_task(task2.task_id, "agent1")
        tasks = delegator.get_agent_tasks("agent1")
        assert len(tasks) == 2

class TestTaskDelegatorCancel:
    def test_cancel_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        result = delegator.cancel_task(task.task_id)
        assert result is True and task.status == TaskStatus.CANCELLED
    
    def test_cancel_completed_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        delegator.complete_task(task.task_id, {})
        result = delegator.cancel_task(task.task_id)
        assert result is False

class TestTaskDelegatorCleanup:
    def test_cleanup_expired_tasks(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {}, timeout_seconds=0)
        delegator.assign_task(task.task_id, "agent1")
        delegator.start_task(task.task_id)
        import time
        time.sleep(0.1)
        expired = delegator.cleanup_expired_tasks()
        assert len(expired) == 1 and task.status == TaskStatus.PENDING

class TestTaskDelegatorStatistics:
    def test_get_statistics(self):
        delegator = TaskDelegator()
        delegator.create_task("test1", {})
        t2 = delegator.create_task("test2", {})
        delegator.assign_task(t2.task_id, "agent1")
        stats = delegator.get_statistics()
        assert stats["total_tasks"] == 2 and stats["pending"] == 1 and stats["assigned"] == 1

class TestTaskDelegatorEdgeCases:
    def test_start_nonexistent_task(self):
        delegator = TaskDelegator()
        result = delegator.start_task("fake_id")
        assert result is False
    
    def test_start_already_in_progress(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        delegator.start_task(task.task_id)
        result = delegator.start_task(task.task_id)
        assert result is False
    
    def test_complete_nonexistent_task(self):
        delegator = TaskDelegator()
        result = delegator.complete_task("fake_id", {})
        assert result is False
    
    def test_complete_pending_task(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        result = delegator.complete_task(task.task_id, {})
        assert result is False
    
    def test_fail_nonexistent_task(self):
        delegator = TaskDelegator()
        result = delegator.fail_task("fake_id", "error")
        assert result is False
    
    def test_fail_task_max_retries(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {}, timeout_seconds=0)
        delegator.assign_task(task.task_id, "agent1")
        for _ in range(4):
            delegator.fail_task(task.task_id, "error")
        assert task.retry_count == 4 and task.status == TaskStatus.FAILED
    
    def test_cancel_nonexistent_task(self):
        delegator = TaskDelegator()
        result = delegator.cancel_task("fake_id")
        assert result is False
    
    def test_get_nonexistent_task(self):
        delegator = TaskDelegator()
        task = delegator.get_task("fake_id")
        assert task is None
    
    def test_get_agent_tasks_no_tasks(self):
        delegator = TaskDelegator()
        tasks = delegator.get_agent_tasks("agent1")
        assert len(tasks) == 0
    
    def test_get_suitable_agents_nonexistent_task(self):
        delegator = TaskDelegator()
        agents = {"agent1": {"cap1"}}
        suitable = delegator.get_suitable_agents("fake_id", agents)
        assert len(suitable) == 0
    
    def test_cleanup_no_expired(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {}, timeout_seconds=300)
        delegator.assign_task(task.task_id, "agent1")
        delegator.start_task(task.task_id)
        expired = delegator.cleanup_expired_tasks()
        assert len(expired) == 0
    
    def test_pending_queue_after_assignment(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        pending = delegator.get_pending_tasks()
        assert len(pending) == 0
    
    def test_complete_from_in_progress(self):
        delegator = TaskDelegator()
        task = delegator.create_task("test", {})
        delegator.assign_task(task.task_id, "agent1")
        delegator.start_task(task.task_id)
        result = delegator.complete_task(task.task_id, {"status": "done"})
        assert result is True and task.result["status"] == "done"
