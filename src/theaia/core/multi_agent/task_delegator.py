"""
Task Delegation System for Multi-Agent Architecture
Manages task assignment, load balancing, and lifecycle tracking.

Author: Álvaro Fernández Mota
Date: 12 December 2025
Version: 2.0.0 - Complete with 6 Advanced Features
"""

from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging
import asyncio
import random
from uuid import uuid4

from theaia.core.multi_agent.agent_registry import AgentRegistry
from theaia.core.multi_agent.agent_metadata import AgentCapability
from theaia.core.multi_agent.discovery_service import (
    DiscoveryService,
    LoadBalancingStrategy,
)
from theaia.core.multi_agent.message.broker import MessageBroker
from theaia.core.multi_agent.message.types import Message, MessageType, MessagePriority

logger = logging.getLogger(__name__)


def _capability_from_string(capability_str: str) -> Optional[AgentCapability]:
    """
    Convert string to AgentCapability enum.
    
    Args:
        capability_str: Capability string (e.g., "calendar_management")
        
    Returns:
        AgentCapability enum or None if invalid
    """
    try:
        return AgentCapability(capability_str)
    except ValueError:
        try:
            return AgentCapability[capability_str.upper()]
        except KeyError:
            logger.warning(f"Unknown capability: {capability_str}")
            return None


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


class TaskStatus(Enum):
    """Task lifecycle states"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class RetryPolicy:
    """
    Retry policy configuration with exponential backoff.
    
    Attributes:
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        multiplier: Exponential multiplier
        jitter: Random jitter (0.0-1.0)
    """
    base_delay: float = 1.0
    max_delay: float = 60.0
    multiplier: float = 2.0
    jitter: float = 0.1
    
    def calculate_delay(self, retry_count: int) -> float:
        """
        Calculate delay for given retry attempt with exponential backoff.
        
        Formula: delay = min(base * (multiplier ^ retry_count), max_delay) + jitter
        
        Args:
            retry_count: Current retry attempt (0-indexed)
            
        Returns:
            Delay in seconds with exponential backoff and jitter
        
        Examples:
            >>> policy = RetryPolicy(base_delay=1.0, multiplier=2.0)
            >>> policy.calculate_delay(0)  # 1s
            >>> policy.calculate_delay(1)  # 2s
            >>> policy.calculate_delay(2)  # 4s
            >>> policy.calculate_delay(3)  # 8s
        """
        # Exponential backoff: base * (multiplier ^ retry_count)
        delay = self.base_delay * (self.multiplier ** retry_count)
        
        # Cap at max_delay
        delay = min(delay, self.max_delay)
        
        # Add random jitter to avoid thundering herd
        if self.jitter > 0:
            jitter_amount = delay * self.jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
        
        return max(0, delay)  # Never negative


@dataclass
class Task:
    """
    Represents a task to be delegated to an agent.
    
    Attributes:
        task_id: Unique identifier
        task_type: Type/category of task
        payload: Task data
        priority: Task priority level
        status: Current task status
        assigned_agent_id: Agent currently handling task
        created_at: Task creation timestamp
        assigned_at: Task assignment timestamp
        completed_at: Task completion timestamp
        timeout_seconds: Maximum execution time
        max_retries: Maximum retry attempts
        retry_count: Current retry attempt
        retry_delay: Current retry delay in seconds
        progress_percent: Task progress (0-100)
        progress_message: Human-readable progress message
        depends_on: List of task IDs this task depends on
        metadata: Additional task metadata
        result: Task result (when completed)
        error: Error message (when failed)
    """
    task_id: str = field(default_factory=lambda: str(uuid4()))
    task_type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    timeout_seconds: int = 300  # 5 minutes default
    max_retries: int = 3
    retry_count: int = 0
    retry_delay: float = 0.0
    progress_percent: int = 0
    progress_message: str = ""
    depends_on: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None

    def is_timed_out(self) -> bool:
        """Check if task has exceeded timeout"""
        if self.assigned_at is None:
            return False
        
        elapsed = (datetime.now() - self.assigned_at).total_seconds()
        return elapsed > self.timeout_seconds

    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries

    def mark_assigned(self, agent_id: str) -> None:
        """Mark task as assigned to agent"""
        self.status = TaskStatus.ASSIGNED
        self.assigned_agent_id = agent_id
        self.assigned_at = datetime.now()

    def mark_in_progress(self) -> None:
        """Mark task as in progress"""
        self.status = TaskStatus.IN_PROGRESS

    def mark_completed(self, result: Any) -> None:
        """Mark task as completed with result"""
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.progress_percent = 100
        self.completed_at = datetime.now()

    def mark_failed(self, error: str) -> None:
        """Mark task as failed with error"""
        self.status = TaskStatus.FAILED
        self.error = error
        self.completed_at = datetime.now()

    def mark_timeout(self) -> None:
        """Mark task as timed out"""
        self.status = TaskStatus.TIMEOUT
        self.completed_at = datetime.now()

    def mark_cancelled(self, reason: str = "Cancelled by user") -> None:
        """Mark task as cancelled"""
        self.status = TaskStatus.CANCELLED
        self.error = reason
        self.completed_at = datetime.now()

    def increment_retry(self, delay: float = 0.0) -> None:
        """Increment retry counter with optional delay"""
        self.retry_count += 1
        self.retry_delay = delay
        self.status = TaskStatus.PENDING
        self.assigned_agent_id = None
        self.assigned_at = None

    def update_progress(self, percent: int, message: str = "") -> None:
        """Update task progress"""
        self.progress_percent = max(0, min(100, percent))
        self.progress_message = message


class TaskDelegator:
    """
    Manages task delegation and lifecycle in multi-agent system.
    
    Features:
    - Intelligent agent selection based on capabilities and load
    - Dynamic load balancing with multiple strategies
    - Timeout detection and automatic handling
    - Retry logic with exponential backoff
    - Task cancellation with resource cleanup
    - Batch delegation for efficiency
    - Progress tracking with callbacks
    - Task dependency management
    - Dead Letter Queue for permanently failed tasks
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
        discovery_service: DiscoveryService,
        message_broker: MessageBroker,
        enable_auto_reassignment: bool = True,
        retry_policy: Optional[RetryPolicy] = None,
    ):
        """
        Initialize task delegator.
        
        Args:
            agent_registry: Registry of available agents
            discovery_service: Service for agent discovery
            message_broker: Broker for agent communication
            enable_auto_reassignment: Enable automatic reassignment on timeout/failure
            retry_policy: Retry policy configuration (default: exponential backoff)
        """
        self.agent_registry = agent_registry
        self.discovery_service = discovery_service
        self.message_broker = message_broker
        self.enable_auto_reassignment = enable_auto_reassignment
        self.retry_policy = retry_policy or RetryPolicy()

        # Task tracking
        self.tasks: Dict[str, Task] = {}
        self.agent_tasks: Dict[str, List[str]] = {}  # agent_id -> task_ids
        self.dead_letter_queue: Dict[str, Task] = {}  # task_id -> failed task

        # Progress callbacks
        self.progress_callbacks: Dict[str, List[Callable]] = {}  # task_id -> callbacks

        # Statistics
        self.stats = {
            "total_assigned": 0,
            "total_completed": 0,
            "total_failed": 0,
            "total_timeout": 0,
            "total_retries": 0,
            "total_cancelled": 0,
            "total_dlq": 0,
        }

        # Monitoring task
        self._monitor_task: Optional[asyncio.Task] = None
        self._monitoring_interval = 10  # seconds

    async def start_monitoring(self) -> None:
        """Start background monitoring for timeouts and dependencies"""
        if self._monitor_task is None:
            self._monitor_task = asyncio.create_task(self._monitor_loop())
            logger.info("Task monitoring started")

    async def stop_monitoring(self) -> None:
        """Stop background monitoring"""
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None
            logger.info("Task monitoring stopped")

    async def _monitor_loop(self) -> None:
        """Background monitoring loop"""
        while True:
            try:
                await asyncio.sleep(self._monitoring_interval)
                await self._check_timeouts()
                await self._check_dependencies()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

    async def _check_timeouts(self) -> None:
        """Check all in-progress tasks for timeouts"""
        timed_out_tasks = []

        for task in self.tasks.values():
            if task.status in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]:
                if task.is_timed_out():
                    timed_out_tasks.append(task)

        for task in timed_out_tasks:
            logger.warning(
                f"Task {task.task_id} timed out (agent: {task.assigned_agent_id})"
            )
            await self._handle_timeout(task)

    async def _check_dependencies(self) -> None:
        """Check pending tasks for satisfied dependencies"""
        for task in list(self.tasks.values()):
            if task.status == TaskStatus.PENDING and task.depends_on:
                if self.check_dependencies_completed(task.task_id):
                    logger.info(f"Dependencies satisfied for task {task.task_id}, auto-delegating")
                    await self.delegate_task(task)

    async def _handle_timeout(self, task: Task) -> None:
        """Handle task timeout with retry logic"""
        task.mark_timeout()
        self.stats["total_timeout"] += 1

        # Remove from agent's task list
        if task.assigned_agent_id and task.assigned_agent_id in self.agent_tasks:
            self.agent_tasks[task.assigned_agent_id].remove(task.task_id)
            self.agent_registry.decrement_load(task.assigned_agent_id)

        # Attempt reassignment if enabled and retries available
        if self.enable_auto_reassignment and task.can_retry():
            delay = self.retry_policy.calculate_delay(task.retry_count)
            logger.info(
                f"Attempting to reassign task {task.task_id} "
                f"(retry {task.retry_count + 1}/{task.max_retries}) "
                f"after {delay:.2f}s delay"
            )
            task.increment_retry(delay)
            self.stats["total_retries"] += 1
            
            # Schedule retry with exponential backoff
            await asyncio.sleep(delay)
            await self.delegate_task(task)
        else:
            logger.error(f"Task {task.task_id} failed permanently (max retries exceeded)")
            await self._move_to_dlq(task, "Maximum retries exceeded after timeout")

    def create_task(
        self,
        task_type: str,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout_seconds: int = 300,
        max_retries: int = 3,
        depends_on: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Task:
        """
        Create a new task.
        
        Args:
            task_type: Type/category of task
            payload: Task data
            priority: Task priority level
            timeout_seconds: Maximum execution time
            max_retries: Maximum retry attempts
            depends_on: List of task IDs this task depends on
            metadata: Additional task metadata
            
        Returns:
            Created task
        """
        task = Task(
            task_type=task_type,
            payload=payload,
            priority=priority,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            depends_on=depends_on or [],
            metadata=metadata or {},
        )

        self.tasks[task.task_id] = task
        logger.info(
            f"Created task {task.task_id} (type: {task_type}, "
            f"priority: {priority.name}, depends_on: {depends_on or []})"
        )
        
        return task

    async def delegate_task(
        self,
        task: Task,
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
    ) -> bool:
        """
        Delegate task to best available agent.
        
        Args:
            task: Task to delegate
            strategy: Load balancing strategy
            
        Returns:
            True if task was successfully assigned
        """
        # Check dependencies first
        if task.depends_on and not self.check_dependencies_completed(task.task_id):
            logger.warning(f"Task {task.task_id} has unsatisfied dependencies, skipping delegation")
            return False

        # Convert task_type string to AgentCapability
        capability = _capability_from_string(task.task_type)
        if not capability:
            logger.error(f"Invalid task type: {task.task_type}")
            return False

        # Find best agent for this task type
        agents = self.discovery_service.discover_by_capability(
            capability,
            max_results=1,
            strategy=strategy,
        )

        if not agents:
            logger.warning(f"No agent available for task type: {task.task_type}")
            return False

        agent_metadata = agents[0]
        agent_id = agent_metadata.agent_id
        task.mark_assigned(agent_id)

        # Track assignment
        if agent_id not in self.agent_tasks:
            self.agent_tasks[agent_id] = []
        self.agent_tasks[agent_id].append(task.task_id)
        self.agent_registry.increment_load(agent_id)

        # Send message to agent
        message = Message(
            message_id=str(uuid4()),
            message_type=MessageType.REQUEST,
            sender_id="task_delegator",
            recipient_id=agent_id,
            priority=self._map_priority(task.priority),
            payload={
                "task_id": task.task_id,
                "task_type": task.task_type,
                "payload": task.payload,
                "metadata": task.metadata,
            },
        )

        await self.message_broker.send(message)

        self.stats["total_assigned"] += 1
        logger.info(
            f"Delegated task {task.task_id} to agent {agent_id} "
            f"(strategy: {strategy.name})"
        )

        return True

    async def delegate_tasks_batch(
        self,
        tasks: List[Task],
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
    ) -> Dict[str, bool]:
        """
        Delegate multiple tasks in parallel for efficiency.
        
        Args:
            tasks: List of tasks to delegate
            strategy: Load balancing strategy
            
        Returns:
            Dictionary mapping task_id to success status
        """
        logger.info(f"Batch delegating {len(tasks)} tasks")
        
        # Delegate all tasks in parallel
        results = await asyncio.gather(
            *[self.delegate_task(task, strategy) for task in tasks],
            return_exceptions=True
        )
        
        # Map results
        batch_results = {}
        for task, result in zip(tasks, results):
            if isinstance(result, Exception):
                logger.error(f"Error delegating task {task.task_id}: {result}")
                batch_results[task.task_id] = False
            else:
                batch_results[task.task_id] = result
        
        successful = sum(1 for success in batch_results.values() if success)
        logger.info(f"Batch delegation complete: {successful}/{len(tasks)} successful")
        
        return batch_results

    def _map_priority(self, task_priority: TaskPriority) -> MessagePriority:
        """Map task priority to message priority"""
        mapping = {
            TaskPriority.LOW: MessagePriority.LOW,
            TaskPriority.NORMAL: MessagePriority.NORMAL,
            TaskPriority.HIGH: MessagePriority.HIGH,
            TaskPriority.URGENT: MessagePriority.CRITICAL,
        }
        return mapping.get(task_priority, MessagePriority.NORMAL)

    async def delegate_to_best_agent(
        self,
        task_type: str,
        payload: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL,
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
    ) -> Optional[str]:
        """
        Create and delegate task in one call.
        
        Args:
            task_type: Type/category of task
            payload: Task data
            priority: Task priority level
            strategy: Load balancing strategy
            
        Returns:
            Task ID if successful, None otherwise
        """
        task = self.create_task(task_type, payload, priority)
        success = await self.delegate_task(task, strategy)
        
        return task.task_id if success else None

    async def cancel_task(
        self,
        task_id: str,
        reason: str = "Cancelled by user",
    ) -> bool:
        """
        Cancel a task and cleanup resources.
        
        Args:
            task_id: ID of task to cancel
            reason: Cancellation reason
            
        Returns:
            True if task was cancelled
        """
        task = self.tasks.get(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return False

        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            logger.warning(f"Task {task_id} already in terminal state: {task.status}")
            return False

        # Remove from agent's task list
        if task.assigned_agent_id:
            if task.assigned_agent_id in self.agent_tasks:
                self.agent_tasks[task.assigned_agent_id].remove(task_id)
            self.agent_registry.decrement_load(task.assigned_agent_id)

            # Send cancellation message to agent
            message = Message(
                message_id=str(uuid4()),
                message_type=MessageType.COMMAND,
                sender_id="task_delegator",
                recipient_id=task.assigned_agent_id,
                priority=MessagePriority.HIGH,
                payload={
                    "command": "cancel_task",
                    "task_id": task_id,
                    "reason": reason,
                },
            )
            await self.message_broker.send(message)

        task.mark_cancelled(reason)
        self.stats["total_cancelled"] += 1
        logger.info(f"Task {task_id} cancelled: {reason}")
        
        return True

    async def update_task_progress(
        self,
        task_id: str,
        percent: int,
        message: str = "",
        agent_id: Optional[str] = None,
    ) -> bool:
        """
        Update task progress with optional callbacks.
        
        Args:
            task_id: ID of task
            percent: Progress percentage (0-100)
            message: Human-readable progress message
            agent_id: Agent reporting progress (for validation)
            
        Returns:
            True if progress was updated
        """
        task = self.tasks.get(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return False

        # Validate agent if provided
        if agent_id and task.assigned_agent_id != agent_id:
            logger.warning(
                f"Agent {agent_id} tried to update progress for task {task_id} "
                f"assigned to {task.assigned_agent_id}"
            )
            return False

        task.update_progress(percent, message)
        logger.debug(f"Task {task_id} progress: {percent}% - {message}")

        # Trigger callbacks
        if task_id in self.progress_callbacks:
            for callback in self.progress_callbacks[task_id]:
                try:
                    callback(task_id, percent, message)
                except Exception as e:
                    logger.error(f"Error in progress callback: {e}")

        return True

    def register_progress_callback(
        self,
        task_id: str,
        callback: Callable[[str, int, str], None],
    ) -> bool:
        """
        Register callback for task progress updates.
        
        Args:
            task_id: Task to monitor
            callback: Function(task_id, percent, message)
            
        Returns:
            True if callback was registered
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return False

        if task_id not in self.progress_callbacks:
            self.progress_callbacks[task_id] = []
        
        self.progress_callbacks[task_id].append(callback)
        logger.debug(f"Registered progress callback for task {task_id}")
        
        return True

    def check_dependencies_completed(self, task_id: str) -> bool:
        """
        Check if all dependencies for a task are completed.
        
        Args:
            task_id: Task to check
            
        Returns:
            True if all dependencies are completed
        """
        task = self.tasks.get(task_id)
        if not task or not task.depends_on:
            return True

        for dep_id in task.depends_on:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False

        return True

    async def reassign_task(
        self,
        task_id: str,
        new_agent_id: Optional[str] = None,
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
    ) -> bool:
        """
        Reassign task to different agent.
        
        Args:
            task_id: ID of task to reassign
            new_agent_id: Specific agent to assign to (None for auto-selection)
            strategy: Load balancing strategy if auto-selecting
            
        Returns:
            True if reassignment successful
        """
        task = self.tasks.get(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return False

        # Remove from old agent
        old_agent_id = task.assigned_agent_id
        if old_agent_id:
            if old_agent_id in self.agent_tasks:
                self.agent_tasks[old_agent_id].remove(task_id)
            self.agent_registry.decrement_load(old_agent_id)

        # Reset task status
        task.status = TaskStatus.PENDING
        task.assigned_agent_id = None
        task.assigned_at = None

        # Assign to new agent
        if new_agent_id:
            agent_metadata = self.agent_registry.get_agent(new_agent_id)
            if not agent_metadata:
                logger.error(f"Agent {new_agent_id} not found")
                return False
            
            task.mark_assigned(new_agent_id)
            if new_agent_id not in self.agent_tasks:
                self.agent_tasks[new_agent_id] = []
            self.agent_tasks[new_agent_id].append(task_id)
            self.agent_registry.increment_load(new_agent_id)
        else:
            return await self.delegate_task(task, strategy)

        logger.info(f"Reassigned task {task_id} from {old_agent_id} to {new_agent_id or 'auto'}")
        return True

    async def complete_task(
        self,
        task_id: str,
        result: Any,
        agent_id: str,
    ) -> bool:
        """
        Mark task as completed.
        
        Args:
            task_id: ID of completed task
            result: Task result
            agent_id: Agent that completed task
            
        Returns:
            True if task was found and marked completed
        """
        task = self.tasks.get(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return False

        if task.assigned_agent_id != agent_id:
            logger.warning(
                f"Agent {agent_id} tried to complete task {task_id} "
                f"assigned to {task.assigned_agent_id}"
            )
            return False

        task.mark_completed(result)
        self.stats["total_completed"] += 1

        # Decrement agent load
        self.agent_registry.decrement_load(agent_id)

        # Remove from agent's task list
        if agent_id in self.agent_tasks:
            self.agent_tasks[agent_id].remove(task_id)

        logger.info(f"Task {task_id} completed by agent {agent_id}")
        return True

    async def fail_task(
        self,
        task_id: str,
        error: str,
        agent_id: str,
    ) -> bool:
        """
        Mark task as failed with retry logic.
        
        Args:
            task_id: ID of failed task
            error: Error description
            agent_id: Agent that failed task
            
        Returns:
            True if task was found and processed
        """
        task = self.tasks.get(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return False

        if task.assigned_agent_id != agent_id:
            logger.warning(
                f"Agent {agent_id} tried to fail task {task_id} "
                f"assigned to {task.assigned_agent_id}"
            )
            return False

        # Decrement agent load
        self.agent_registry.decrement_load(agent_id)

        # Remove from agent's task list
        if agent_id in self.agent_tasks:
            self.agent_tasks[agent_id].remove(task_id)

        # Attempt retry if available
        if self.enable_auto_reassignment and task.can_retry():
            delay = self.retry_policy.calculate_delay(task.retry_count)
            logger.info(
                f"Task {task_id} failed, attempting retry "
                f"({task.retry_count + 1}/{task.max_retries}) "
                f"after {delay:.2f}s delay"
            )
            task.increment_retry(delay)
            self.stats["total_retries"] += 1
            
            # Schedule retry with exponential backoff
            await asyncio.sleep(delay)
            await self.delegate_task(task)
        else:
            await self._move_to_dlq(task, error)

        return True

    async def _move_to_dlq(self, task: Task, reason: str) -> None:
        """Move task to Dead Letter Queue"""
        task.mark_failed(reason)
        self.dead_letter_queue[task.task_id] = task
        self.stats["total_failed"] += 1
        self.stats["total_dlq"] += 1
        logger.error(f"Task {task.task_id} moved to DLQ: {reason}")

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)

    def get_agent_tasks(self, agent_id: str) -> List[Task]:
        """Get all tasks assigned to agent"""
        task_ids = self.agent_tasks.get(agent_id, [])
        return [self.tasks[tid] for tid in task_ids if tid in self.tasks]

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with specific status"""
        return [task for task in self.tasks.values() if task.status == status]

    def get_dlq_tasks(self) -> List[Task]:
        """Get all tasks in Dead Letter Queue"""
        return list(self.dead_letter_queue.values())

    def clear_dlq(self) -> int:
        """Clear Dead Letter Queue and return count"""
        count = len(self.dead_letter_queue)
        self.dead_letter_queue.clear()
        logger.info(f"Cleared {count} tasks from DLQ")
        return count

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive delegation statistics"""
        pending = len(self.get_tasks_by_status(TaskStatus.PENDING))
        assigned = len(self.get_tasks_by_status(TaskStatus.ASSIGNED))
        in_progress = len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS))
        completed = len(self.get_tasks_by_status(TaskStatus.COMPLETED))
        failed = len(self.get_tasks_by_status(TaskStatus.FAILED))
        timeout = len(self.get_tasks_by_status(TaskStatus.TIMEOUT))
        cancelled = len(self.get_tasks_by_status(TaskStatus.CANCELLED))

        return {
            **self.stats,
            "current_pending": pending,
            "current_assigned": assigned,
            "current_in_progress": in_progress,
            "current_completed": completed,
            "current_failed": failed,
            "current_timeout": timeout,
            "current_cancelled": cancelled,
            "current_dlq": len(self.dead_letter_queue),
            "total_tasks": len(self.tasks),
        }

    def clear_completed_tasks(self, older_than_minutes: int = 60) -> int:
        """
        Clear completed tasks older than specified time.
        
        Args:
            older_than_minutes: Clear tasks completed before this many minutes ago
            
        Returns:
            Number of tasks cleared
        """
        cutoff_time = datetime.now() - timedelta(minutes=older_than_minutes)
        to_remove = []

        for task_id, task in self.tasks.items():
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.TIMEOUT, TaskStatus.CANCELLED]:
                if task.completed_at and task.completed_at < cutoff_time:
                    to_remove.append(task_id)

        for task_id in to_remove:
            del self.tasks[task_id]

        logger.info(f"Cleared {len(to_remove)} completed tasks")
        return len(to_remove)

    def __repr__(self):
        return (
            f"TaskDelegator("
            f"tasks={len(self.tasks)}, "
            f"dlq={len(self.dead_letter_queue)}, "
            f"stats={self.stats})"
        )
