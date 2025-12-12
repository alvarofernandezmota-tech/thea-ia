import pytest
from datetime import datetime, timedelta
from src.theaia.core.multi_agent.agent_metadata import (
    AgentMetadata,
    AgentStatus,
    AgentCapability,
    PerformanceMetrics
)

# ==================== PerformanceMetrics Tests ====================
class TestPerformanceMetrics:
    def test_default_initialization(self):
        metrics = PerformanceMetrics()
        assert metrics.average_response_time == 0.0
        assert metrics.total_requests == 0
        assert metrics.successful_requests == 0
        assert metrics.failed_requests == 0
        assert metrics.last_request_time is None

    def test_success_rate_zero_requests(self):
        metrics = PerformanceMetrics()
        assert metrics.success_rate == 0.0

    def test_success_rate_all_successful(self):
        metrics = PerformanceMetrics(total_requests=10, successful_requests=10)
        assert metrics.success_rate == 1.0

    def test_success_rate_partial(self):
        metrics = PerformanceMetrics(total_requests=10, successful_requests=7)
        assert metrics.success_rate == 0.7

    def test_error_rate_zero_requests(self):
        metrics = PerformanceMetrics()
        assert metrics.error_rate == 1.0

    def test_error_rate_all_successful(self):
        metrics = PerformanceMetrics(total_requests=10, successful_requests=10)
        assert metrics.error_rate == 0.0

    def test_error_rate_partial(self):
        metrics = PerformanceMetrics(total_requests=10, successful_requests=7)
        assert abs(metrics.error_rate - 0.3) < 0.0001

    def test_with_last_request_time(self):
        now = datetime.now()
        metrics = PerformanceMetrics(last_request_time=now)
        assert metrics.last_request_time == now

# ==================== AgentMetadata Basic Tests ====================
class TestAgentMetadataBasic:
    def test_default_initialization(self):
        metadata = AgentMetadata(agent_type="TestAgent")
        assert metadata.agent_type == "TestAgent"
        assert metadata.version == "1.0.0"
        assert isinstance(metadata.capabilities, set)
        assert metadata.status == AgentStatus.HEALTHY
        assert metadata.current_load == 0
        assert metadata.max_capacity == 100
        assert isinstance(metadata.metrics, PerformanceMetrics)
        assert metadata.priority == 0

    def test_agent_id_generated(self):
        metadata = AgentMetadata(agent_type="TestAgent")
        assert metadata.agent_id is not None
        assert isinstance(metadata.agent_id, str)
        assert len(metadata.agent_id) > 0

    def test_unique_agent_ids(self):
        metadata1 = AgentMetadata(agent_type="TestAgent1")
        metadata2 = AgentMetadata(agent_type="TestAgent2")
        assert metadata1.agent_id != metadata2.agent_id

    def test_with_capabilities(self):
        caps = {AgentCapability.CALENDAR_MANAGEMENT, AgentCapability.EVENT_CREATION}
        metadata = AgentMetadata(agent_type="CalendarAgent", capabilities=caps)
        assert metadata.capabilities == caps
        assert AgentCapability.CALENDAR_MANAGEMENT in metadata.capabilities

    def test_timestamps_set(self):
        metadata = AgentMetadata(agent_type="TestAgent")
        assert isinstance(metadata.registered_at, datetime)
        assert isinstance(metadata.last_heartbeat, datetime)

# ==================== AgentMetadata Validation Tests ====================
class TestAgentMetadataValidation:
    def test_missing_agent_type_raises_error(self):
        with pytest.raises(ValueError, match="agent_type is required"):
            AgentMetadata(agent_type="")

    def test_negative_max_capacity_raises_error(self):
        with pytest.raises(ValueError, match="max_capacity must be positive"):
            AgentMetadata(agent_type="TestAgent", max_capacity=-1)

    def test_zero_max_capacity_raises_error(self):
        with pytest.raises(ValueError, match="max_capacity must be positive"):
            AgentMetadata(agent_type="TestAgent", max_capacity=0)

    def test_negative_current_load_raises_error(self):
        with pytest.raises(ValueError, match="current_load cannot be negative"):
            AgentMetadata(agent_type="TestAgent", current_load=-5)

# ==================== AgentMetadata Load Tests ====================
class TestAgentMetadataLoad:
    def test_load_percentage_zero_load(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=0, max_capacity=100)
        assert metadata.load_percentage == 0.0

    def test_load_percentage_full_load(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=100, max_capacity=100)
        assert metadata.load_percentage == 100.0

    def test_load_percentage_partial_load(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=50, max_capacity=100)
        assert metadata.load_percentage == 50.0

    def test_load_percentage_over_capacity(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=150, max_capacity=100)
        assert metadata.load_percentage == 150.0

    def test_load_percentage_zero_max_capacity(self):
        # This should be caught by validation, but test the property logic
        metadata = AgentMetadata.__new__(AgentMetadata)
        metadata.current_load = 10
        metadata.max_capacity = 0
        assert metadata.load_percentage == 100.0

# ==================== AgentMetadata Status Tests ====================
class TestAgentMetadataStatus:
    def test_healthy_status(self):
        metadata = AgentMetadata(agent_type="TestAgent", status=AgentStatus.HEALTHY)
        assert metadata.status == AgentStatus.HEALTHY

    def test_degraded_status(self):
        metadata = AgentMetadata(agent_type="TestAgent", status=AgentStatus.DEGRADED)
        assert metadata.status == AgentStatus.DEGRADED

    def test_unavailable_status(self):
        metadata = AgentMetadata(agent_type="TestAgent", status=AgentStatus.UNAVAILABLE)
        assert metadata.status == AgentStatus.UNAVAILABLE

    def test_maintenance_status(self):
        metadata = AgentMetadata(agent_type="TestAgent", status=AgentStatus.MAINTENANCE)
        assert metadata.status == AgentStatus.MAINTENANCE

# ==================== AgentMetadata Additional Fields Tests ====================
class TestAgentMetadataAdditionalFields:
    def test_with_tags(self):
        tags = {"environment": "production", "region": "us-east"}
        metadata = AgentMetadata(agent_type="TestAgent", tags=tags)
        assert metadata.tags == tags

    def test_with_priority(self):
        metadata = AgentMetadata(agent_type="TestAgent", priority=10)
        assert metadata.priority == 10

    def test_health_check_intervals(self):
        metadata = AgentMetadata(
            agent_type="TestAgent",
            health_check_interval=60,
            health_check_timeout=10
        )
        assert metadata.health_check_interval == 60
        assert metadata.health_check_timeout == 10

    def test_with_version(self):
        metadata = AgentMetadata(agent_type="TestAgent", version="2.0.0")
        assert metadata.version == "2.0.0"

# ==================== AgentCapability Enum Tests ====================
class TestAgentCapabilityEnum:
    def test_calendar_management(self):
        assert AgentCapability.CALENDAR_MANAGEMENT.value == "calendar_management"

    def test_event_creation(self):
        assert AgentCapability.EVENT_CREATION.value == "event_creation"

    def test_event_query(self):
        assert AgentCapability.EVENT_QUERY.value == "event_query"

    def test_note_management(self):
        assert AgentCapability.NOTE_MANAGEMENT.value == "note_management"

    def test_reminder_management(self):
        assert AgentCapability.REMINDER_MANAGEMENT.value == "reminder_management"

# ==================== AgentStatus Enum Tests ====================
class TestAgentStatusEnum:
    def test_healthy(self):
        assert AgentStatus.HEALTHY.value == "healthy"

    def test_degraded(self):
        assert AgentStatus.DEGRADED.value == "degraded"

    def test_unavailable(self):
        assert AgentStatus.UNAVAILABLE.value == "unavailable"

    def test_maintenance(self):
        assert AgentStatus.MAINTENANCE.value == "maintenance"

# ==================== Integration Tests ====================
class TestAgentMetadataIntegration:
    def test_full_agent_lifecycle(self):
        # Create agent
        metadata = AgentMetadata(
            agent_type="LifecycleAgent",
            capabilities={AgentCapability.CALENDAR_MANAGEMENT},
            max_capacity=50
        )
        
        # Verify initial state
        assert metadata.status == AgentStatus.HEALTHY
        assert metadata.current_load == 0
        assert metadata.load_percentage == 0.0
        
        # Simulate load increase
        metadata.current_load = 25
        assert metadata.load_percentage == 50.0
        
        # Check metrics
        assert metadata.metrics.success_rate == 0.0

    def test_multiple_capabilities(self):
        caps = {
            AgentCapability.EVENT_CREATION,
            AgentCapability.EVENT_QUERY,
            AgentCapability.CALENDAR_MANAGEMENT
        }
        metadata = AgentMetadata(agent_type="MultiAgent", capabilities=caps)
        assert len(metadata.capabilities) == 3
        assert all(cap in metadata.capabilities for cap in caps)



# ==================== AgentMetadata Methods Tests ====================
class TestAgentMetadataMethods:
    def test_available_capacity(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=30, max_capacity=100)
        assert metadata.available_capacity == 70

    def test_available_capacity_zero(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=100, max_capacity=100)
        assert metadata.available_capacity == 0

    def test_is_overloaded_false(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=50, max_capacity=100)
        assert metadata.is_overloaded is False

    def test_is_overloaded_true(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=100, max_capacity=100)
        assert metadata.is_overloaded is True

    def test_has_capability_true(self):
        metadata = AgentMetadata(
            agent_type="TestAgent",
            capabilities={AgentCapability.CALENDAR_MANAGEMENT}
        )
        assert metadata.has_capability(AgentCapability.CALENDAR_MANAGEMENT) is True

    def test_has_capability_false(self):
        metadata = AgentMetadata(agent_type="TestAgent")
        assert metadata.has_capability(AgentCapability.CALENDAR_MANAGEMENT) is False

    def test_add_capability(self):
        metadata = AgentMetadata(agent_type="TestAgent")
        metadata.add_capability(AgentCapability.NOTE_MANAGEMENT)
        assert AgentCapability.NOTE_MANAGEMENT in metadata.capabilities

    def test_remove_capability(self):
        metadata = AgentMetadata(
            agent_type="TestAgent",
            capabilities={AgentCapability.NOTE_MANAGEMENT}
        )
        metadata.remove_capability(AgentCapability.NOTE_MANAGEMENT)
        assert AgentCapability.NOTE_MANAGEMENT not in metadata.capabilities

    def test_update_heartbeat_method(self):
        metadata = AgentMetadata(agent_type="TestAgent")
        original = metadata.last_heartbeat
        import time
        time.sleep(0.01)
        metadata.update_heartbeat()
        assert metadata.last_heartbeat > original

    def test_increment_load_method(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=5)
        metadata.increment_load()
        assert metadata.current_load == 6

    def test_increment_load_at_max(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=100, max_capacity=100)
        metadata.increment_load()
        assert metadata.current_load == 100  # Should not exceed max

    def test_decrement_load_method(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=5)
        metadata.decrement_load()
        assert metadata.current_load == 4

    def test_decrement_load_at_zero(self):
        metadata = AgentMetadata(agent_type="TestAgent", current_load=0)
        metadata.decrement_load()
        assert metadata.current_load == 0  # Should not go below zero

    

