"""
Task Delegation System for Multi-Agent Architecture
Manages task assignment, load balancing, and lifecycle tracking.


Author: Álvaro Fernández Mota
Date: 11 December 2025
Version: 1.0.0
"""


from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging
import asyncio
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
        # Try direct lookup
        return AgentCapability(capability_str)
    except ValueError:
        # Try uppercase conversion
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
        metadata: Additional task metadata
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

    def increment_retry(self) -> None:
        """Increment retry counter"""
        self.retry_count += 1
        self.status = TaskStatus.PENDING
        self.assigned_agent_id = None
        self.assigned_at = None


class TaskDelegator:
    """
    Manages task delegation and lifecycle in multi-agent system.
    
    Features:
    - Intelligent agent selection based on capabilities and load
    - Dynamic load balancing
    - Timeout detection and handling
    - Retry logic with exponential backoff
    - Task lifecycle tracking
    - Priority-based assignment
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
        discovery_service: DiscoveryService,
        message_broker: MessageBroker,
        enable_auto_reassignment: bool = True,
    ):
        """
        Initialize task delegator.
        
        Args:
            agent_registry: Registry of available agents
            discovery_service: Service for agent discovery
            message_broker: Broker for agent communication
            enable_auto_reassignment: Enable automatic reassignment on timeout/failure
        """
        self.agent_registry = agent_registry
        self.discovery_service = discovery_service
        self.message_broker = message_broker
        self.enable_auto_reassignment = enable_auto_reassignment

        # Task tracking
        self.tasks: Dict[str, Task] = {}
        self.agent_tasks: Dict[str, List[str]] = {}  # agent_id -> task_ids

        # Statistics
        self.stats = {
            "total_assigned": 0,
            "total_completed": 0,
            "total_failed": 0,
            "total_timeout": 0,
            "total_retries": 0,
        }

        # Monitoring task
        self._monitor_task: Optional[asyncio.Task] = None
        self._monitoring_interval = 10  # seconds

    async def start_monitoring(self) -> None:
        """Start background monitoring for timeouts"""
        if self._monitor_task is None:
            self._monitor_task = asyncio.create_task(self._monitor_timeouts())
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

    async def _monitor_timeouts(self) -> None:
        """Background task to monitor and handle timeouts"""
        while True:
            try:
                await asyncio.sleep(self._monitoring_interval)
                await self._check_timeouts()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in timeout monitoring: {e}")

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

    async def _handle_timeout(self, task: Task) -> None:
        """
        Handle task timeout.
        
        Args:
            task: The timed-out task
        """
        task.mark_timeout()
        self.stats["total_timeout"] += 1

        # Remove from agent's task list
        if task.assigned_agent_id and task.assigned_agent_id in self.agent_tasks:
            self.agent_tasks[task.assigned_agent_id].remove(task.task_id)

        # Attempt reassignment if enabled and retries available
        if self.enable_auto_reassignment and task.can_retry():
            logger.info(f"Attempting to reassign task {task.task_id} (retry {task.retry_count + 1}/{task.max_retries})")
            task.increment_retry()
            self.stats["total_retries"] += 1
            await self.delegate_task(task)
        else:
            logger.error(f"Task {task.task_id} failed permanently (max retries exceeded)")
            task.mark_failed("Maximum retries exceeded after timeout")
            self.stats["total_failed"] += 1

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
        Create a new task.
        
        Args:
            task_type: Type/category of task
            payload: Task data
            priority: Task priority level
            timeout_seconds: Maximum execution time
            max_retries: Maximum retry attempts
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
            metadata=metadata or {},
        )

        self.tasks[task.task_id] = task
        logger.info(f"Created task {task.task_id} (type: {task_type}, priority: {priority.name})")
        
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

        # Assign task to agent
        agent_id = agent_metadata.agent_id
        task.mark_assigned(agent_id)

        # Track assignment
        if agent_id not in self.agent_tasks:
            self.agent_tasks[agent_id] = []
        self.agent_tasks[agent_id].append(task.task_id)

        # Increment agent load
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
            # Specific agent requested
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
            # Auto-select best agent
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
        Mark task as failed.
        
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
            logger.info(
                f"Task {task_id} failed, attempting retry "
                f"({task.retry_count + 1}/{task.max_retries})"
            )
            task.increment_retry()
            self.stats["total_retries"] += 1
            await self.delegate_task(task)
        else:
            task.mark_failed(error)
            self.stats["total_failed"] += 1
            logger.error(f"Task {task_id} failed permanently: {error}")

        return True

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

    def get_statistics(self) -> Dict[str, Any]:
        """Get delegation statistics"""
        pending = len(self.get_tasks_by_status(TaskStatus.PENDING))
        assigned = len(self.get_tasks_by_status(TaskStatus.ASSIGNED))
        in_progress = len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS))
        completed = len(self.get_tasks_by_status(TaskStatus.COMPLETED))
        failed = len(self.get_tasks_by_status(TaskStatus.FAILED))
        timeout = len(self.get_tasks_by_status(TaskStatus.TIMEOUT))

        return {
            **self.stats,
            "current_pending": pending,
            "current_assigned": assigned,
            "current_in_progress": in_progress,
            "current_completed": completed,
            "current_failed": failed,
            "current_timeout": timeout,
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
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.TIMEOUT]:
                if task.completed_at and task.completed_at < cutoff_time:
                    to_remove.append(task_id)

        for task_id in to_remove:
            del self.tasks[task_id]

        logger.info(f"Cleared {len(to_remove)} completed tasks")
        return len(to_remove)

    def __repr__(self):
        return f"TaskDelegator(tasks={len(self.tasks)}, stats={self.stats})"
