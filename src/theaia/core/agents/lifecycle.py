"""Agent Lifecycle Management.

This module provides comprehensive lifecycle management for agents,
including creation, initialization, execution, monitoring, and termination.
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field

from .metadata import AgentMetadata
from .registry import AgentRegistry


class AgentState(Enum):
    """Agent lifecycle states."""
    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    TERMINATED = "terminated"


class LifecycleEvent(Enum):
    """Agent lifecycle events."""
    CREATED = "created"
    INITIALIZED = "initialized"
    STARTED = "started"
    PAUSED = "paused"
    RESUMED = "resumed"
    STOPPED = "stopped"
    ERROR = "error"
    TERMINATED = "terminated"
    STATE_CHANGED = "state_changed"


@dataclass
class LifecycleTransition:
    """Represents a lifecycle state transition."""
    from_state: AgentState
    to_state: AgentState
    event: LifecycleEvent
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentLifecycle:
    """Manages agent lifecycle including state transitions and events."""

    # Valid state transitions
    VALID_TRANSITIONS: Dict[AgentState, List[AgentState]] = {
        AgentState.CREATED: [AgentState.INITIALIZING, AgentState.ERROR, AgentState.TERMINATED],
        AgentState.INITIALIZING: [AgentState.READY, AgentState.ERROR, AgentState.TERMINATED],
        AgentState.READY: [AgentState.RUNNING, AgentState.TERMINATED],
        AgentState.RUNNING: [AgentState.PAUSED, AgentState.STOPPING, AgentState.ERROR],
        AgentState.PAUSED: [AgentState.RUNNING, AgentState.STOPPING, AgentState.TERMINATED],
        AgentState.STOPPING: [AgentState.STOPPED, AgentState.ERROR],
        AgentState.STOPPED: [AgentState.TERMINATED],
        AgentState.ERROR: [AgentState.TERMINATED],
        AgentState.TERMINATED: []
    }

    def __init__(
        self,
        agent_id: str,
        metadata: AgentMetadata,
        registry: Optional[AgentRegistry] = None
    ):
        """Initialize agent lifecycle.

        Args:
            agent_id: Unique agent identifier
            metadata: Agent metadata
            registry: Optional agent registry for coordination
        """
        self.agent_id = agent_id
        self.metadata = metadata
        self.registry = registry
        self._state = AgentState.CREATED
        self._history: List[LifecycleTransition] = []
        self._event_handlers: Dict[LifecycleEvent, List[Callable]] = {}
        self._logger = logging.getLogger(f"lifecycle.{agent_id}")
        self._lock = asyncio.Lock()
        
        # Record initial state
        self._record_transition(
            AgentState.CREATED,
            AgentState.CREATED,
            LifecycleEvent.CREATED
        )

    @property
    def state(self) -> AgentState:
        """Get current agent state."""
        return self._state

    @property
    def history(self) -> List[LifecycleTransition]:
        """Get lifecycle history."""
        return self._history.copy()

    def can_transition_to(self, target_state: AgentState) -> bool:
        """Check if transition to target state is valid.

        Args:
            target_state: Target state

        Returns:
            True if transition is valid
        """
        return target_state in self.VALID_TRANSITIONS.get(self._state, [])

    async def transition_to(
        self,
        target_state: AgentState,
        event: LifecycleEvent,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Transition to a new state.

        Args:
            target_state: Target state
            event: Event triggering transition
            metadata: Optional transition metadata

        Returns:
            True if transition successful

        Raises:
            ValueError: If transition is invalid
        """
        async with self._lock:
            if not self.can_transition_to(target_state):
                raise ValueError(
                    f"Invalid transition from {self._state.value} to {target_state.value}"
                )

            old_state = self._state
            self._state = target_state
            
            # Record transition
            self._record_transition(old_state, target_state, event, metadata)
            
            # Update metadata
            self.metadata.status = target_state.value
            
            # Notify event handlers
            await self._notify_handlers(event, metadata or {})
            
            self._logger.info(
                f"State transition: {old_state.value} -> {target_state.value} "
                f"(event: {event.value})"
            )
            
            return True

    def _record_transition(
        self,
        from_state: AgentState,
        to_state: AgentState,
        event: LifecycleEvent,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record a lifecycle transition."""
        transition = LifecycleTransition(
            from_state=from_state,
            to_state=to_state,
            event=event,
            metadata=metadata or {}
        )
        self._history.append(transition)

    def on(self, event: LifecycleEvent, handler: Callable):
        """Register event handler.

        Args:
            event: Event to handle
            handler: Handler function
        """
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        self._event_handlers[event].append(handler)

    async def _notify_handlers(self, event: LifecycleEvent, metadata: Dict[str, Any]):
        """Notify all handlers for an event.

        Args:
            event: Event that occurred
            metadata: Event metadata
        """
        handlers = self._event_handlers.get(event, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(self.agent_id, event, metadata)
                else:
                    handler(self.agent_id, event, metadata)
            except Exception as e:
                self._logger.error(f"Error in event handler: {e}")

    async def initialize(self) -> bool:
        """Initialize the agent.

        Returns:
            True if initialization successful
        """
        try:
            await self.transition_to(
                AgentState.INITIALIZING,
                LifecycleEvent.INITIALIZED
            )
            
            # Perform initialization tasks
            if self.registry:
                await self.registry.register(self.metadata)
            
            await self.transition_to(
                AgentState.READY,
                LifecycleEvent.INITIALIZED
            )
            
            return True
            
        except Exception as e:
            self._logger.error(f"Initialization failed: {e}")
            await self.transition_to(
                AgentState.ERROR,
                LifecycleEvent.ERROR,
                {"error": str(e)}
            )
            return False

    async def start(self) -> bool:
        """Start the agent.

        Returns:
            True if start successful
        """
        try:
            await self.transition_to(
                AgentState.RUNNING,
                LifecycleEvent.STARTED
            )
            return True
            
        except Exception as e:
            self._logger.error(f"Start failed: {e}")
            await self.transition_to(
                AgentState.ERROR,
                LifecycleEvent.ERROR,
                {"error": str(e)}
            )
            return False

    async def pause(self) -> bool:
        """Pause the agent.

        Returns:
            True if pause successful
        """
        try:
            await self.transition_to(
                AgentState.PAUSED,
                LifecycleEvent.PAUSED
            )
            return True
            
        except Exception as e:
            self._logger.error(f"Pause failed: {e}")
            return False

    async def resume(self) -> bool:
        """Resume the agent.

        Returns:
            True if resume successful
        """
        try:
            await self.transition_to(
                AgentState.RUNNING,
                LifecycleEvent.RESUMED
            )
            return True
            
        except Exception as e:
            self._logger.error(f"Resume failed: {e}")
            return False

    async def stop(self) -> bool:
        """Stop the agent.

        Returns:
            True if stop successful
        """
        try:
            await self.transition_to(
                AgentState.STOPPING,
                LifecycleEvent.STOPPED
            )
            
            # Perform cleanup
            if self.registry:
                await self.registry.unregister(self.agent_id)
            
            await self.transition_to(
                AgentState.STOPPED,
                LifecycleEvent.STOPPED
            )
            
            return True
            
        except Exception as e:
            self._logger.error(f"Stop failed: {e}")
            await self.transition_to(
                AgentState.ERROR,
                LifecycleEvent.ERROR,
                {"error": str(e)}
            )
            return False

    async def terminate(self) -> bool:
        """Terminate the agent.

        Returns:
            True if termination successful
        """
        try:
            await self.transition_to(
                AgentState.TERMINATED,
                LifecycleEvent.TERMINATED
            )
            
            # Final cleanup
            if self.registry:
                await self.registry.unregister(self.agent_id)
            
            return True
            
        except Exception as e:
            self._logger.error(f"Termination failed: {e}")
            return False

    def get_state_duration(self, state: AgentState) -> float:
        """Get total time spent in a state.

        Args:
            state: State to query

        Returns:
            Duration in seconds
        """
        duration = 0.0
        current_state_start = None
        
        for transition in self._history:
            if transition.to_state == state:
                current_state_start = transition.timestamp
            elif current_state_start and transition.from_state == state:
                duration += (transition.timestamp - current_state_start).total_seconds()
                current_state_start = None
        
        # Add current state duration if still in that state
        if current_state_start and self._state == state:
            duration += (datetime.now() - current_state_start).total_seconds()
        
        return duration

    def get_transition_count(self) -> int:
        """Get total number of state transitions.

        Returns:
            Number of transitions
        """
        return len(self._history) - 1  # Exclude initial CREATED state

    def is_active(self) -> bool:
        """Check if agent is in an active state.

        Returns:
            True if agent is active
        """
        return self._state in [
            AgentState.INITIALIZING,
            AgentState.READY,
            AgentState.RUNNING,
            AgentState.PAUSED
        ]

    def is_terminated(self) -> bool:
        """Check if agent is terminated.

        Returns:
            True if agent is terminated
        """
        return self._state == AgentState.TERMINATED
