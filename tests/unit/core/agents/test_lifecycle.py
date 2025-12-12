"""Tests for agent lifecycle management."""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from src.core.agents.lifecycle import (
    AgentLifecycle,
    AgentState,
    LifecycleEvent,
    LifecycleTransition
)
from src.core.agents.metadata import AgentMetadata
from src.core.agents.registry import AgentRegistry


@pytest.fixture
def agent_metadata():
    """Create test agent metadata."""
    return AgentMetadata(
        agent_id="test_agent",
        agent_type="test",
        version="1.0.0"
    )


@pytest.fixture
def mock_registry():
    """Create mock registry."""
    registry = AsyncMock(spec=AgentRegistry)
    registry.register = AsyncMock()
    registry.unregister = AsyncMock()
    return registry


@pytest.fixture
def lifecycle(agent_metadata, mock_registry):
    """Create test lifecycle."""
    return AgentLifecycle("test_agent", agent_metadata, mock_registry)


class TestAgentLifecycle:
    """Test AgentLifecycle class."""

    def test_initialization(self, lifecycle, agent_metadata):
        """Test lifecycle initialization."""
        assert lifecycle.agent_id == "test_agent"
        assert lifecycle.metadata == agent_metadata
        assert lifecycle.state == AgentState.CREATED
        assert len(lifecycle.history) == 1
        assert lifecycle.history[0].to_state == AgentState.CREATED

    def test_state_property(self, lifecycle):
        """Test state property."""
        assert lifecycle.state == AgentState.CREATED
        assert isinstance(lifecycle.state, AgentState)

    def test_history_property(self, lifecycle):
        """Test history property returns copy."""
        history1 = lifecycle.history
        history2 = lifecycle.history
        assert history1 == history2
        assert history1 is not history2

    def test_can_transition_to_valid(self, lifecycle):
        """Test valid transition check."""
        assert lifecycle.can_transition_to(AgentState.INITIALIZING)
        assert lifecycle.can_transition_to(AgentState.ERROR)
        assert lifecycle.can_transition_to(AgentState.TERMINATED)

    def test_can_transition_to_invalid(self, lifecycle):
        """Test invalid transition check."""
        assert not lifecycle.can_transition_to(AgentState.RUNNING)
        assert not lifecycle.can_transition_to(AgentState.PAUSED)
        assert not lifecycle.can_transition_to(AgentState.STOPPED)

    @pytest.mark.asyncio
    async def test_transition_to_valid(self, lifecycle):
        """Test valid state transition."""
        result = await lifecycle.transition_to(
            AgentState.INITIALIZING,
            LifecycleEvent.INITIALIZED
        )
        
        assert result is True
        assert lifecycle.state == AgentState.INITIALIZING
        assert len(lifecycle.history) == 2
        assert lifecycle.metadata.status == "initializing"

    @pytest.mark.asyncio
    async def test_transition_to_invalid(self, lifecycle):
        """Test invalid state transition."""
        with pytest.raises(ValueError, match="Invalid transition"):
            await lifecycle.transition_to(
                AgentState.RUNNING,
                LifecycleEvent.STARTED
            )

    @pytest.mark.asyncio
    async def test_transition_with_metadata(self, lifecycle):
        """Test transition with metadata."""
        metadata = {"reason": "test"}
        await lifecycle.transition_to(
            AgentState.INITIALIZING,
            LifecycleEvent.INITIALIZED,
            metadata
        )
        
        assert lifecycle.history[-1].metadata == metadata

    @pytest.mark.asyncio
    async def test_event_handler_registration(self, lifecycle):
        """Test event handler registration."""
        handler = Mock()
        lifecycle.on(LifecycleEvent.INITIALIZED, handler)
        
        await lifecycle.transition_to(
            AgentState.INITIALIZING,
            LifecycleEvent.INITIALIZED
        )
        
        handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_event_handler(self, lifecycle):
        """Test async event handler."""
        handler = AsyncMock()
        lifecycle.on(LifecycleEvent.INITIALIZED, handler)
        
        await lifecycle.transition_to(
            AgentState.INITIALIZING,
            LifecycleEvent.INITIALIZED
        )
        
        handler.assert_called_once_with(
            "test_agent",
            LifecycleEvent.INITIALIZED,
            {}
        )

    @pytest.mark.asyncio
    async def test_multiple_event_handlers(self, lifecycle):
        """Test multiple event handlers."""
        handler1 = Mock()
        handler2 = Mock()
        
        lifecycle.on(LifecycleEvent.INITIALIZED, handler1)
        lifecycle.on(LifecycleEvent.INITIALIZED, handler2)
        
        await lifecycle.transition_to(
            AgentState.INITIALIZING,
            LifecycleEvent.INITIALIZED
        )
        
        handler1.assert_called_once()
        handler2.assert_called_once()

    @pytest.mark.asyncio
    async def test_event_handler_error_handling(self, lifecycle):
        """Test event handler error doesn't break transition."""
        def failing_handler(*args):
            raise Exception("Handler error")
        
        lifecycle.on(LifecycleEvent.INITIALIZED, failing_handler)
        
        # Should not raise
        await lifecycle.transition_to(
            AgentState.INITIALIZING,
            LifecycleEvent.INITIALIZED
        )
        
        assert lifecycle.state == AgentState.INITIALIZING

    @pytest.mark.asyncio
    async def test_initialize_success(self, lifecycle, mock_registry):
        """Test successful initialization."""
        result = await lifecycle.initialize()
        
        assert result is True
        assert lifecycle.state == AgentState.READY
        mock_registry.register.assert_called_once_with(lifecycle.metadata)

    @pytest.mark.asyncio
    async def test_initialize_without_registry(self, agent_metadata):
        """Test initialization without registry."""
        lifecycle = AgentLifecycle("test_agent", agent_metadata, None)
        result = await lifecycle.initialize()
        
        assert result is True
        assert lifecycle.state == AgentState.READY

    @pytest.mark.asyncio
    async def test_initialize_failure(self, lifecycle, mock_registry):
        """Test initialization failure."""
        mock_registry.register.side_effect = Exception("Registry error")
        
        result = await lifecycle.initialize()
        
        assert result is False
        assert lifecycle.state == AgentState.ERROR

    @pytest.mark.asyncio
    async def test_start_success(self, lifecycle):
        """Test successful start."""
        await lifecycle.initialize()
        result = await lifecycle.start()
        
        assert result is True
        assert lifecycle.state == AgentState.RUNNING

    @pytest.mark.asyncio
    async def test_start_from_invalid_state(self, lifecycle):
        """Test start from invalid state."""
        # Start returns False instead of raising when in invalid state
        result = await lifecycle.start()
        assert result is False

    @pytest.mark.asyncio
    async def test_pause_success(self, lifecycle):
        """Test successful pause."""
        await lifecycle.initialize()
        await lifecycle.start()
        
        result = await lifecycle.pause()
        
        assert result is True
        assert lifecycle.state == AgentState.PAUSED

    @pytest.mark.asyncio
    async def test_pause_from_invalid_state(self, lifecycle):
        """Test pause from invalid state."""
        result = await lifecycle.pause()
        assert result is False

    @pytest.mark.asyncio
    async def test_resume_success(self, lifecycle):
        """Test successful resume."""
        await lifecycle.initialize()
        await lifecycle.start()
        await lifecycle.pause()
        
        result = await lifecycle.resume()
        
        assert result is True
        assert lifecycle.state == AgentState.RUNNING

    @pytest.mark.asyncio
    async def test_resume_from_invalid_state(self, lifecycle):
        """Test resume from invalid state."""
        result = await lifecycle.resume()
        assert result is False

    @pytest.mark.asyncio
    async def test_stop_success(self, lifecycle, mock_registry):
        """Test successful stop."""
        await lifecycle.initialize()
        await lifecycle.start()
        
        result = await lifecycle.stop()
        
        assert result is True
        assert lifecycle.state == AgentState.STOPPED
        mock_registry.unregister.assert_called_once_with("test_agent")

    @pytest.mark.asyncio
    async def test_stop_without_registry(self, agent_metadata):
        """Test stop without registry."""
        lifecycle = AgentLifecycle("test_agent", agent_metadata, None)
        await lifecycle.initialize()
        await lifecycle.start()
        
        result = await lifecycle.stop()
        
        assert result is True
        assert lifecycle.state == AgentState.STOPPED

    @pytest.mark.asyncio
    async def test_stop_failure(self, lifecycle, mock_registry):
        """Test stop failure."""
        await lifecycle.initialize()
        await lifecycle.start()
        
        mock_registry.unregister.side_effect = Exception("Unregister error")
        
        result = await lifecycle.stop()
        
        assert result is False
        assert lifecycle.state == AgentState.ERROR

    @pytest.mark.asyncio
    async def test_terminate_success(self, lifecycle, mock_registry):
        """Test successful termination."""
        await lifecycle.initialize()
        
        result = await lifecycle.terminate()
        
        assert result is True
        assert lifecycle.state == AgentState.TERMINATED
        mock_registry.unregister.assert_called_once_with("test_agent")

    @pytest.mark.asyncio
    async def test_terminate_from_any_state(self, lifecycle):
        """Test termination is possible from most states."""
        # From CREATED
        await lifecycle.terminate()
        assert lifecycle.is_terminated()

    @pytest.mark.asyncio
    async def test_get_state_duration(self, lifecycle):
        """Test state duration calculation."""
        await lifecycle.transition_to(AgentState.INITIALIZING, LifecycleEvent.INITIALIZED)
        await asyncio.sleep(0.1)
        await lifecycle.transition_to(AgentState.READY, LifecycleEvent.INITIALIZED)
        
        duration = lifecycle.get_state_duration(AgentState.INITIALIZING)
        assert duration >= 0.1
        assert duration < 1.0

    @pytest.mark.asyncio
    async def test_get_state_duration_current_state(self, lifecycle):
        """Test duration calculation for current state."""
        await lifecycle.transition_to(AgentState.INITIALIZING, LifecycleEvent.INITIALIZED)
        await asyncio.sleep(0.1)
        
        duration = lifecycle.get_state_duration(AgentState.INITIALIZING)
        assert duration >= 0.1

    def test_get_state_duration_never_entered(self, lifecycle):
        """Test duration for state never entered."""
        duration = lifecycle.get_state_duration(AgentState.RUNNING)
        assert duration == 0.0

    @pytest.mark.asyncio
    async def test_get_transition_count(self, lifecycle):
        """Test transition count."""
        assert lifecycle.get_transition_count() == 0
        
        await lifecycle.transition_to(AgentState.INITIALIZING, LifecycleEvent.INITIALIZED)
        assert lifecycle.get_transition_count() == 1
        
        await lifecycle.transition_to(AgentState.READY, LifecycleEvent.INITIALIZED)
        assert lifecycle.get_transition_count() == 2

    def test_is_active_created(self, lifecycle):
        """Test is_active for CREATED state."""
        assert not lifecycle.is_active()

    @pytest.mark.asyncio
    async def test_is_active_initializing(self, lifecycle):
        """Test is_active for INITIALIZING state."""
        await lifecycle.transition_to(AgentState.INITIALIZING, LifecycleEvent.INITIALIZED)
        assert lifecycle.is_active()

    @pytest.mark.asyncio
    async def test_is_active_ready(self, lifecycle):
        """Test is_active for READY state."""
        await lifecycle.transition_to(AgentState.INITIALIZING, LifecycleEvent.INITIALIZED)
        await lifecycle.transition_to(AgentState.READY, LifecycleEvent.INITIALIZED)
        assert lifecycle.is_active()

    @pytest.mark.asyncio
    async def test_is_active_running(self, lifecycle):
        """Test is_active for RUNNING state."""
        await lifecycle.initialize()
        await lifecycle.start()
        assert lifecycle.is_active()

    @pytest.mark.asyncio
    async def test_is_active_paused(self, lifecycle):
        """Test is_active for PAUSED state."""
        await lifecycle.initialize()
        await lifecycle.start()
        await lifecycle.pause()
        assert lifecycle.is_active()

    @pytest.mark.asyncio
    async def test_is_active_stopped(self, lifecycle):
        """Test is_active for STOPPED state."""
        await lifecycle.initialize()
        await lifecycle.start()
        await lifecycle.stop()
        assert not lifecycle.is_active()

    def test_is_terminated_initial(self, lifecycle):
        """Test is_terminated initially."""
        assert not lifecycle.is_terminated()

    @pytest.mark.asyncio
    async def test_is_terminated_after_termination(self, lifecycle):
        """Test is_terminated after termination."""
        await lifecycle.terminate()
        assert lifecycle.is_terminated()

    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, lifecycle):
        """Test concurrent transition attempts."""
        # Only one should succeed due to lock
        tasks = [
            lifecycle.transition_to(AgentState.INITIALIZING, LifecycleEvent.INITIALIZED),
            lifecycle.transition_to(AgentState.ERROR, LifecycleEvent.ERROR),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # One should succeed, one may fail
        assert lifecycle.state in [AgentState.INITIALIZING, AgentState.ERROR]

    @pytest.mark.asyncio
    async def test_full_lifecycle(self, lifecycle, mock_registry):
        """Test complete lifecycle flow."""
        # Initialize
        assert await lifecycle.initialize()
        assert lifecycle.state == AgentState.READY
        
        # Start
        assert await lifecycle.start()
        assert lifecycle.state == AgentState.RUNNING
        
        # Pause
        assert await lifecycle.pause()
        assert lifecycle.state == AgentState.PAUSED
        
        # Resume
        assert await lifecycle.resume()
        assert lifecycle.state == AgentState.RUNNING
        
        # Stop
        assert await lifecycle.stop()
        assert lifecycle.state == AgentState.STOPPED
        
        # Terminate
        assert await lifecycle.terminate()
        assert lifecycle.state == AgentState.TERMINATED
        
        # Verify history
        assert lifecycle.get_transition_count() >= 6

    @pytest.mark.asyncio
    async def test_error_recovery_path(self, lifecycle):
        """Test error state can transition to terminated."""
        await lifecycle.transition_to(AgentState.ERROR, LifecycleEvent.ERROR)
        assert lifecycle.state == AgentState.ERROR
        
        await lifecycle.terminate()
        assert lifecycle.state == AgentState.TERMINATED


class TestLifecycleTransition:
    """Test LifecycleTransition dataclass."""
    def test_transition_creation(self):
        """Test transition creation."""
        transition = LifecycleTransition(
            from_state=AgentState.CREATED,
            to_state=AgentState.INITIALIZING,
            event=LifecycleEvent.INITIALIZED,
            metadata={"test": "data"}
        )
        
        assert transition.from_state == AgentState.CREATED
        assert transition.to_state == AgentState.INITIALIZING
        assert transition.event == LifecycleEvent.INITIALIZED
        assert transition.metadata == {"test": "data"}
        assert isinstance(transition.timestamp, datetime)

    def test_transition_default_timestamp(self):
        """Test transition default timestamp."""
        transition = LifecycleTransition(
            from_state=AgentState.CREATED,
            to_state=AgentState.INITIALIZING,
            event=LifecycleEvent.INITIALIZED
        )
        
        assert (datetime.now() - transition.timestamp).total_seconds() < 1.0

    def test_transition_default_metadata(self):
        """Test transition default metadata."""
        transition = LifecycleTransition(
            from_state=AgentState.CREATED,
            to_state=AgentState.INITIALIZING,
            event=LifecycleEvent.INITIALIZED
        )
        
        assert transition.metadata == {}


class TestAgentStateEnum:
    """Test AgentState enum."""

    def test_all_states_defined(self):
        """Test all expected states are defined."""
        expected_states = [
            "CREATED", "INITIALIZING", "READY", "RUNNING",
            "PAUSED", "STOPPING", "STOPPED", "ERROR", "TERMINATED"
        ]
        
        for state_name in expected_states:
            assert hasattr(AgentState, state_name)

    def test_state_values(self):
        """Test state values are lowercase strings."""
        assert AgentState.CREATED.value == "created"
        assert AgentState.RUNNING.value == "running"
        assert AgentState.TERMINATED.value == "terminated"


class TestLifecycleEventEnum:
    """Test LifecycleEvent enum."""

    def test_all_events_defined(self):
        """Test all expected events are defined."""
        expected_events = [
            "CREATED", "INITIALIZED", "STARTED", "PAUSED",
            "RESUMED", "STOPPED", "ERROR", "TERMINATED", "STATE_CHANGED"
        ]
        
        for event_name in expected_events:
            assert hasattr(LifecycleEvent, event_name)

    def test_event_values(self):
        """Test event values are lowercase strings."""
        assert LifecycleEvent.CREATED.value == "created"
        assert LifecycleEvent.STARTED.value == "started"
        assert LifecycleEvent.TERMINATED.value == "terminated"


class TestValidTransitions:
    """Test valid state transitions mapping."""

    def test_valid_transitions_completeness(self):
        """Test all states have transition rules."""
        for state in AgentState:
            assert state in AgentLifecycle.VALID_TRANSITIONS

    def test_created_transitions(self):
        """Test CREATED state transitions."""
        valid = AgentLifecycle.VALID_TRANSITIONS[AgentState.CREATED]
        assert AgentState.INITIALIZING in valid
        assert AgentState.ERROR in valid
        assert AgentState.TERMINATED in valid

    def test_terminated_no_transitions(self):
        """Test TERMINATED state has no outgoing transitions."""
        valid = AgentLifecycle.VALID_TRANSITIONS[AgentState.TERMINATED]
        assert len(valid) == 0

    def test_error_only_to_terminated(self):
        """Test ERROR state can only go to TERMINATED."""
        valid = AgentLifecycle.VALID_TRANSITIONS[AgentState.ERROR]
        assert valid == [AgentState.TERMINATED]

    def test_running_cannot_skip_to_stopped(self):
        """Test RUNNING cannot directly transition to STOPPED."""
        valid = AgentLifecycle.VALID_TRANSITIONS[AgentState.RUNNING]
        assert AgentState.STOPPED not in valid
        assert AgentState.STOPPING in valid
