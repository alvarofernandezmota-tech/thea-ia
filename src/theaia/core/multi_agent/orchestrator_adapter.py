"""
Orchestrator Adapter - Bridge between CoreOrchestrator and TaskDelegator
Translates orchestrator requests to task delegation system.

Author: Álvaro Fernández Mota
Date: 12 December 2025
Version: 1.0.0
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
import logging
from datetime import datetime

from .task_delegator import TaskDelegator, Task, TaskPriority, TaskStatus
from .agent_metadata import AgentCapability
from ..nlp_engine import NLPResult


logger = logging.getLogger(__name__)


@dataclass
class TaskRequest:
    """Request to create a task from orchestrator."""
    intent: str
    message: str
    user_id: str
    conversation_id: str
    context: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class TaskResponse:
    """Response from task execution."""
    task_id: str
    status: TaskStatus
    message: str
    result: Optional[Dict[str, Any]] = None
    progress: int = 0
    error: Optional[str] = None


class OrchestratorAdapter:
    """
    Adapter that bridges CoreOrchestrator and TaskDelegator.
    
    Responsibilities:
    - Convert intents to tasks
    - Manage task lifecycle from orchestrator perspective
    - Handle progress callbacks
    - Translate task results to orchestrator responses
    """
    
    def __init__(self, task_delegator: TaskDelegator):
        """
        Initialize adapter.
        
        Args:
            task_delegator: TaskDelegator instance
        """
        self.task_delegator = task_delegator
        
        # Map intents to task types (capabilities)
        self._intent_to_capability = {
            "create_event": AgentCapability.EVENT_CREATION,
            "list_events": AgentCapability.CALENDAR_MANAGEMENT,
            "update_event": AgentCapability.EVENT_CREATION,
            "delete_event": AgentCapability.CALENDAR_MANAGEMENT,
            "create_note": AgentCapability.NOTE_MANAGEMENT,
            "search_notes": AgentCapability.NOTE_MANAGEMENT,
            "create_reminder": AgentCapability.REMINDER_MANAGEMENT,
            "web_search": AgentCapability.NATURAL_LANGUAGE_PROCESSING,
            "general_query": AgentCapability.FALLBACK,
        }
        
        # Progress callbacks per conversation
        self._progress_callbacks: Dict[str, List[Callable]] = {}
        
        logger.info("OrchestratorAdapter initialized")
    
    
    def register_intent_capability(
        self,
        intent: str,
        capability: AgentCapability
    ) -> None:
        """
        Register custom intent to capability mapping.
        
        Args:
            intent: Intent name
            capability: AgentCapability to map to
        """
        self._intent_to_capability[intent] = capability
        logger.debug(f"Registered intent mapping: {intent} -> {capability.value}")
    
    
    async def create_task_from_intent(
        self,
        task_request: TaskRequest
    ) -> Task:
        """
        Create a task from an orchestrator intent request.
        
        Args:
            task_request: TaskRequest with intent and context
            
        Returns:
            Created Task instance
            
        Raises:
            ValueError: If intent cannot be mapped to capability
        """
        # Map intent to capability
        capability = self._intent_to_capability.get(task_request.intent)
        
        if not capability:
            logger.warning(f"Unknown intent: {task_request.intent}, using GENERAL_ASSISTANCE")
            capability = AgentCapability.FALLBACK
        
        # Build task payload
        payload = {
            "message": task_request.message,
            "user_id": task_request.user_id,
            "conversation_id": task_request.conversation_id,
            "intent": task_request.intent,
            "context": task_request.context,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Create task
        task = self.task_delegator.create_task(
            task_type=capability.value,
            payload=payload,
            priority=task_request.priority,
            metadata=task_request.metadata or {},
        )
        
        logger.info(
            f"Created task {task.task_id} for intent {task_request.intent} "
            f"(conversation: {task_request.conversation_id})"
        )
        
        return task
    
    
    async def delegate_task_async(
        self,
        task_request: TaskRequest,
        progress_callback: Optional[Callable[[str, int, str], None]] = None
    ) -> TaskResponse:
        """
        Create and delegate task asynchronously.
        
        Args:
            task_request: TaskRequest with intent and context
            progress_callback: Optional callback for progress updates
            
        Returns:
            TaskResponse with task info
        """
        # Create task
        task = await self.create_task_from_intent(task_request)
        
        # Register progress callback if provided
        if progress_callback:
            self.register_progress_callback(
                conversation_id=task_request.conversation_id,
                callback=progress_callback
            )
            
            # Also register on task delegator
            self.task_delegator.register_progress_callback(
                task.task_id,
                progress_callback
            )
        
        # Delegate task
        success = await self.task_delegator.delegate_task(task)
        
        if not success:
            logger.error(f"Failed to delegate task {task.task_id}")
            return TaskResponse(
                task_id=task.task_id,
                status=TaskStatus.FAILED,
                message="No se pudo asignar la tarea a un agente disponible",
                error="No available agents"
            )
        
        # Return initial response
        return TaskResponse(
            task_id=task.task_id,
            status=task.status,
            message=f"Tarea asignada al agente {task.assigned_agent_id}",
            progress=0
        )
    
    
    async def get_task_response(self, task_id: str) -> Optional[TaskResponse]:
        """
        Get current task status and result.
        
        Args:
            task_id: Task ID
            
        Returns:
            TaskResponse or None if not found
        """
        task = self.task_delegator.get_task(task_id)
        
        if not task:
            logger.warning(f"Task {task_id} not found")
            return None
        
        # Build response based on task status
        if task.status == TaskStatus.COMPLETED:
            message = "Tarea completada exitosamente"
            result = task.result
        elif task.status == TaskStatus.FAILED:
            message = f"Tarea falló: {task.error}"
            result = None
        elif task.status == TaskStatus.ASSIGNED:
            message = f"Tarea en progreso ({task.progress_percent}%)"
            result = None
        elif task.status == TaskStatus.CANCELLED:
            message = "Tarea cancelada"
            result = None
        else:
            message = "Tarea pendiente"
            result = None
        
        return TaskResponse(
            task_id=task.task_id,
            status=task.status,
            message=message,
            result=result,
            progress=task.progress_percent,
            error=task.error
        )
    
    
    async def cancel_task(
        self,
        task_id: str,
        reason: str = "User requested cancellation"
    ) -> bool:
        """
        Cancel a task.
        
        Args:
            task_id: Task ID
            reason: Cancellation reason
            
        Returns:
            True if cancelled successfully
        """
        success = await self.task_delegator.cancel_task(task_id, reason)
        
        if success:
            logger.info(f"Task {task_id} cancelled: {reason}")
        else:
            logger.warning(f"Failed to cancel task {task_id}")
        
        return success
    
    
    def register_progress_callback(
        self,
        conversation_id: str,
        callback: Callable[[str, int, str], None]
    ) -> None:
        """
        Register progress callback for a conversation.
        
        Args:
            conversation_id: Conversation ID
            callback: Callback function (task_id, progress, message)
        """
        if conversation_id not in self._progress_callbacks:
            self._progress_callbacks[conversation_id] = []
        
        self._progress_callbacks[conversation_id].append(callback)
        logger.debug(f"Registered progress callback for conversation {conversation_id}")
    
    
    def get_conversation_tasks(self, conversation_id: str) -> List[Task]:
        """
        Get all tasks for a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of tasks
        """
        all_tasks = self.task_delegator.tasks.values()
        
        conversation_tasks = [
            task for task in all_tasks
            if task.payload.get("conversation_id") == conversation_id
        ]
        
        return conversation_tasks
    
    
    def get_user_active_tasks(self, user_id: str) -> List[Task]:
        """
        Get active tasks for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of active tasks
        """
        all_tasks = self.task_delegator.tasks.values()
        
        active_tasks = [
            task for task in all_tasks
            if task.payload.get("user_id") == user_id
            and task.status in [TaskStatus.PENDING, TaskStatus.ASSIGNED]
        ]
        
        return active_tasks
    
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get adapter statistics.
        
        Returns:
            Dict with stats
        """
        stats = self.task_delegator.get_statistics()
        
        return {
            **stats,
            "registered_intents": len(self._intent_to_capability),
            "active_callbacks": len(self._progress_callbacks),
        }
