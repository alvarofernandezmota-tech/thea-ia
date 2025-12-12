"""
Task Delegation System
Gestión de delegación de tareas entre agentes con balanceo de carga.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import uuid


class TaskStatus(Enum):
    """Estados de una tarea"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Prioridad de tareas"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Tarea delegable entre agentes"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    required_capabilities: Set[str] = field(default_factory=set)
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 300
    
    def is_expired(self) -> bool:
        """Check if task has exceeded timeout"""
        if self.assigned_at is None:
            return False
        age = (datetime.utcnow() - self.assigned_at).total_seconds()
        return age > self.timeout_seconds
    
    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries
    
    def mark_assigned(self, agent_id: str) -> None:
        """Mark task as assigned to agent"""
        self.assigned_agent_id = agent_id
        self.assigned_at = datetime.utcnow()
        self.status = TaskStatus.ASSIGNED
    
    def mark_in_progress(self) -> None:
        """Mark task as in progress"""
        self.status = TaskStatus.IN_PROGRESS
    
    def mark_completed(self, result: Dict[str, Any]) -> None:
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.result = result
    
    def mark_failed(self, error: str) -> None:
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.error = error
        self.retry_count += 1


class TaskDelegator:
    """Sistema de delegación de tareas entre agentes"""
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._agent_tasks: Dict[str, List[str]] = {}  # agent_id -> task_ids
        self._pending_queue: List[str] = []  # task_ids ordenados por prioridad
    
    def create_task(
        self,
        task_type: str,
        payload: Dict[str, Any],
        required_capabilities: Optional[Set[str]] = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout_seconds: int = 300
    ) -> Task:
        """Crear nueva tarea"""
        task = Task(
            task_type=task_type,
            payload=payload,
            required_capabilities=required_capabilities or set(),
            priority=priority,
            timeout_seconds=timeout_seconds
        )
        self._tasks[task.task_id] = task
        self._pending_queue.append(task.task_id)
        self._sort_pending_queue()
        return task
    
    def _sort_pending_queue(self) -> None:
        """Ordenar cola por prioridad (mayor primero)"""
        self._pending_queue.sort(
            key=lambda tid: self._tasks[tid].priority.value,
            reverse=True
        )
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Asignar tarea a agente"""
        if task_id not in self._tasks:
            return False
        
        task = self._tasks[task_id]
        if task.status != TaskStatus.PENDING:
            return False
        
        task.mark_assigned(agent_id)
        
        if agent_id not in self._agent_tasks:
            self._agent_tasks[agent_id] = []
        self._agent_tasks[agent_id].append(task_id)
        
        if task_id in self._pending_queue:
            self._pending_queue.remove(task_id)
        
        return True
    
    def get_suitable_agents(
        self,
        task_id: str,
        available_agents: Dict[str, Set[str]]  # agent_id -> capabilities
    ) -> List[str]:
        """Obtener agentes adecuados para una tarea"""
        if task_id not in self._tasks:
            return []
        
        task = self._tasks[task_id]
        suitable = []
        
        for agent_id, capabilities in available_agents.items():
            if task.required_capabilities.issubset(capabilities):
                suitable.append(agent_id)
        
        return suitable
    
    def delegate_to_best_agent(
        self,
        task_id: str,
        available_agents: Dict[str, Set[str]],
        agent_loads: Dict[str, int]  # agent_id -> current_load
    ) -> Optional[str]:
        """Delegar tarea al mejor agente disponible"""
        suitable = self.get_suitable_agents(task_id, available_agents)
        if not suitable:
            return None
        
        # Seleccionar agente con menor carga
        best_agent = min(suitable, key=lambda aid: agent_loads.get(aid, 0))
        
        if self.assign_task(task_id, best_agent):
            return best_agent
        return None
    
    def start_task(self, task_id: str) -> bool:
        """Marcar tarea como iniciada"""
        if task_id not in self._tasks:
            return False
        
        task = self._tasks[task_id]
        if task.status != TaskStatus.ASSIGNED:
            return False
        
        task.mark_in_progress()
        return True
    
    def complete_task(self, task_id: str, result: Dict[str, Any]) -> bool:
        """Completar tarea"""
        if task_id not in self._tasks:
            return False
        
        task = self._tasks[task_id]
        if task.status not in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]:
            return False
        
        task.mark_completed(result)
        return True
    
    def fail_task(self, task_id: str, error: str) -> bool:
        """Marcar tarea como fallida"""
        if task_id not in self._tasks:
            return False
        
        task = self._tasks[task_id]
        task.mark_failed(error)
        
        # Re-agregar a cola si puede reintentarse
        if task.can_retry() and task_id not in self._pending_queue:
            task.status = TaskStatus.PENDING
            task.assigned_agent_id = None
            task.assigned_at = None
            self._pending_queue.append(task_id)
            self._sort_pending_queue()
        
        return True
    
    def get_pending_tasks(self) -> List[Task]:
        """Obtener tareas pendientes"""
        return [self._tasks[tid] for tid in self._pending_queue]
    
    def get_agent_tasks(self, agent_id: str) -> List[Task]:
        """Obtener tareas asignadas a un agente"""
        task_ids = self._agent_tasks.get(agent_id, [])
        return [self._tasks[tid] for tid in task_ids if tid in self._tasks]
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Obtener tarea por ID"""
        return self._tasks.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancelar tarea"""
        if task_id not in self._tasks:
            return False
        
        task = self._tasks[task_id]
        if task.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return False
        
        task.status = TaskStatus.CANCELLED
        
        if task_id in self._pending_queue:
            self._pending_queue.remove(task_id)
        
        return True
    
    def cleanup_expired_tasks(self) -> List[str]:
        """Limpiar tareas expiradas"""
        expired = []
        for task_id, task in self._tasks.items():
            if task.status == TaskStatus.IN_PROGRESS and task.is_expired():
                self.fail_task(task_id, "Task timeout exceeded")
                expired.append(task_id)
        return expired
    
    def get_statistics(self) -> Dict[str, int]:
        """Obtener estadísticas del delegador"""
        stats = {
            "total_tasks": len(self._tasks),
            "pending": 0,
            "assigned": 0,
            "in_progress": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0
        }
        
        for task in self._tasks.values():
            stats[task.status.value] += 1
        
        return stats
