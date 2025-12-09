"""
Workflow Orchestration System
Allows complex multi-step workflows with dependencies and rollback.

Author: Álvaro Fernández Mota
Date: 09 December 2025
Version: 1.0.0
"""

from typing import Optional, List, Dict, Set, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
import logging
import asyncio

logger = logging.getLogger(__name__)


class StepStatus(Enum):
    """Status of a workflow step"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    SKIPPED = "skipped"


class WorkflowStatus(Enum):
    """Status of entire workflow"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class WorkflowStep:
    """
    Represents a single step in a workflow.
    
    Attributes:
        name: Unique step identifier
        action: Async function to execute
        rollback_action: Optional rollback function
        depends_on: List of step names this depends on
        parallel: Whether this can run in parallel with siblings
        pre_condition: Optional validation before execution
        post_condition: Optional validation after execution
        metadata: Additional step metadata
    
    Example:
        >>> async def create_event(ctx):
        ...     return {"event_id": 123}
        >>> 
        >>> async def rollback_event(ctx, result):
        ...     await delete_event(result["event_id"])
        >>> 
        >>> step = WorkflowStep(
        ...     name="create_event",
        ...     action=create_event,
        ...     rollback_action=rollback_event
        ... )
    """
    name: str
    action: Callable[[Dict[str, Any]], Awaitable[Any]]
    rollback_action: Optional[Callable[[Dict[str, Any], Any], Awaitable[None]]] = None
    depends_on: List[str] = field(default_factory=list)
    parallel: bool = False
    pre_condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    post_condition: Optional[Callable[[Dict[str, Any], Any], bool]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Runtime state
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None
    
    def __hash__(self):
        """Make hashable for use in sets"""
        return hash(self.name)
    
    def __eq__(self, other):
        """Equality based on name"""
        if not isinstance(other, WorkflowStep):
            return False
        return self.name == other.name


class Workflow:
    """
    Orchestrates complex multi-step workflows with dependencies.
    
    Features:
        - Sequential and parallel execution
        - Automatic dependency resolution
        - Rollback on failure
        - Pre/post condition validation
        - Context sharing between steps
    
    Example:
        >>> workflow = Workflow("onboarding")
        >>> workflow.add_step("create_profile", create_profile_fn)
        >>> workflow.add_step("send_email", send_email_fn, depends_on=["create_profile"])
        >>> result = await workflow.execute({"user_id": 123})
    """
    
    def __init__(self, name: str, auto_rollback: bool = True):
        """
        Initialize workflow.
        
        Args:
            name: Workflow name
            auto_rollback: Whether to automatically rollback on failure
        """
        self.name = name
        self.auto_rollback = auto_rollback
        self.steps: Dict[str, WorkflowStep] = {}
        self.execution_order: List[str] = []
        self.status = WorkflowStatus.PENDING
        self.context: Dict[str, Any] = {}
        self.completed_steps: List[str] = []
        self.failed_step: Optional[str] = None
        
        logger.info(f"Workflow '{name}' initialized")
    
    def add_step(
        self,
        name: str,
        action: Callable[[Dict[str, Any]], Awaitable[Any]],
        rollback_action: Optional[Callable[[Dict[str, Any], Any], Awaitable[None]]] = None,
        depends_on: Optional[List[str]] = None,
        parallel: bool = False,
        pre_condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
        post_condition: Optional[Callable[[Dict[str, Any], Any], bool]] = None,
        **metadata
    ) -> None:
        """
        Add a step to the workflow.
        
        Args:
            name: Step name
            action: Async function to execute
            rollback_action: Optional rollback function
            depends_on: List of step names this depends on
            parallel: Whether step can run in parallel
            pre_condition: Validation before execution
            post_condition: Validation after execution
            **metadata: Additional metadata
            
        Raises:
            ValueError: If step already exists or dependency not found
        """
        if name in self.steps:
            raise ValueError(f"Step '{name}' already exists in workflow")
        
        # Validate dependencies exist
        depends_on = depends_on or []
        for dep in depends_on:
            if dep not in self.steps:
                raise ValueError(f"Dependency '{dep}' not found for step '{name}'")
        
        step = WorkflowStep(
            name=name,
            action=action,
            rollback_action=rollback_action,
            depends_on=depends_on,
            parallel=parallel,
            pre_condition=pre_condition,
            post_condition=post_condition,
            metadata=metadata
        )
        
        self.steps[name] = step
        logger.debug(f"Added step '{name}' to workflow '{self.name}'")
    
    def _build_execution_order(self) -> List[List[str]]:
        """
        Build execution order respecting dependencies.
        Uses topological sort to determine order.
        Groups parallel steps together.
        
        Returns:
            List of execution batches (each batch can run in parallel)
            
        Raises:
            ValueError: If circular dependency detected
        """
        # Calculate in-degree for each step
        in_degree = {name: len(step.depends_on) for name, step in self.steps.items()}
        
        # Find steps with no dependencies (in-degree 0)
        ready = [name for name, degree in in_degree.items() if degree == 0]
        
        execution_batches = []
        processed = set()
        
        while ready:
            # Current batch (can be executed in parallel)
            current_batch = ready.copy()
            execution_batches.append(current_batch)
            
            # Mark as processed
            for step_name in current_batch:
                processed.add(step_name)
            
            # Find next ready steps
            ready = []
            for name, step in self.steps.items():
                if name in processed:
                    continue
                
                # Check if all dependencies are processed
                if all(dep in processed for dep in step.depends_on):
                    ready.append(name)
        
        # Verify all steps processed (no circular dependencies)
        if len(processed) != len(self.steps):
            unprocessed = set(self.steps.keys()) - processed
            raise ValueError(f"Circular dependency detected. Unprocessed steps: {unprocessed}")
        
        return execution_batches
    
    async def _execute_step(self, step: WorkflowStep) -> Any:
        """
        Execute a single workflow step.
        
        Args:
            step: Step to execute
            
        Returns:
            Step result
            
        Raises:
            Exception: If step execution fails
        """
        step.status = StepStatus.RUNNING
        logger.info(f"Executing step '{step.name}' in workflow '{self.name}'")
        
        try:
            # Pre-condition check
            if step.pre_condition and not step.pre_condition(self.context):
                step.status = StepStatus.SKIPPED
                logger.warning(f"Step '{step.name}' pre-condition failed, skipping")
                return None
            
            # Execute action
            result = await step.action(self.context)
            
            # Post-condition check
            if step.post_condition and not step.post_condition(self.context, result):
                raise ValueError(f"Post-condition failed for step '{step.name}'")
            
            step.result = result
            step.status = StepStatus.COMPLETED
            self.completed_steps.append(step.name)
            
            # Store result in context
            self.context[f"{step.name}_result"] = result
            
            logger.info(f"Step '{step.name}' completed successfully")
            return result
            
        except Exception as e:
            step.status = StepStatus.FAILED
            step.error = e
            self.failed_step = step.name
            logger.error(f"Step '{step.name}' failed: {e}")
            raise
    
    async def _rollback_step(self, step: WorkflowStep) -> None:
        """
        Rollback a completed step.
        
        Args:
            step: Step to rollback
        """
        if not step.rollback_action:
            logger.warning(f"No rollback action for step '{step.name}'")
            return
        
        if step.status != StepStatus.COMPLETED:
            logger.debug(f"Step '{step.name}' not completed, skipping rollback")
            return
        
        try:
            logger.info(f"Rolling back step '{step.name}'")
            await step.rollback_action(self.context, step.result)
            step.status = StepStatus.ROLLED_BACK
            logger.info(f"Step '{step.name}' rolled back successfully")
            
        except Exception as e:
            logger.error(f"Rollback failed for step '{step.name}': {e}")
            # Continue rolling back other steps even if one fails
    
    async def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the complete workflow.
        
        Args:
            initial_context: Initial context data
            
        Returns:
            Dictionary with:
                - status: Final workflow status
                - results: Results from all completed steps
                - failed_step: Name of failed step (if any)
                - error: Error message (if any)
                
        Raises:
            ValueError: If workflow validation fails
        """
        self.status = WorkflowStatus.RUNNING
        self.context = initial_context or {}
        self.completed_steps = []
        self.failed_step = None
        
        logger.info(f"Starting workflow '{self.name}'")
        
        try:
            # Build execution order
            execution_batches = self._build_execution_order()
            
            # Execute batches sequentially, steps within batch in parallel
            for batch in execution_batches:
                # Execute batch (parallel if multiple steps)
                if len(batch) == 1:
                    step = self.steps[batch[0]]
                    await self._execute_step(step)
                else:
                    # Parallel execution
                    tasks = [self._execute_step(self.steps[name]) for name in batch]
                    await asyncio.gather(*tasks)
            
            self.status = WorkflowStatus.COMPLETED
            logger.info(f"Workflow '{self.name}' completed successfully")
            
            return {
                "status": "completed",
                "results": {name: step.result for name, step in self.steps.items()},
                "completed_steps": self.completed_steps,
                "failed_step": None,
                "error": None
            }
            
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            logger.error(f"Workflow '{self.name}' failed: {e}")
            
            # Auto-rollback if enabled
            if self.auto_rollback:
                await self._rollback()
            
            return {
                "status": "failed",
                "results": {name: step.result for name, step in self.steps.items() if step.result},
                "completed_steps": self.completed_steps,
                "failed_step": self.failed_step,
                "error": str(e)
            }
    
    async def _rollback(self) -> None:
        """Rollback all completed steps in reverse order"""
        logger.info(f"Starting rollback for workflow '{self.name}'")
        
        # Rollback in reverse order of completion
        for step_name in reversed(self.completed_steps):
            step = self.steps[step_name]
            await self._rollback_step(step)
        
        self.status = WorkflowStatus.ROLLED_BACK
        logger.info(f"Workflow '{self.name}' rolled back")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current workflow status.
        
        Returns:
            Dictionary with workflow status details
        """
        return {
            "name": self.name,
            "status": self.status.value,
            "total_steps": len(self.steps),
            "completed_steps": len(self.completed_steps),
            "failed_step": self.failed_step,
            "steps": {
                name: {
                    "status": step.status.value,
                    "has_result": step.result is not None,
                    "error": str(step.error) if step.error else None
                }
                for name, step in self.steps.items()
            }
        }
    
    def reset(self) -> None:
        """Reset workflow to initial state"""
        self.status = WorkflowStatus.PENDING
        self.context.clear()
        self.completed_steps.clear()
        self.failed_step = None
        
        for step in self.steps.values():
            step.status = StepStatus.PENDING
            step.result = None
            step.error = None
        
        logger.info(f"Workflow '{self.name}' reset")
