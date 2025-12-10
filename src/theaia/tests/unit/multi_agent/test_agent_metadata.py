"""
Tests for Agent Metadata - H07.1
"""
import pytest
from datetime import datetime, timedelta
from src.theaia.core.multi_agent.agent_metadata import (
    AgentMetadata,
    AgentCapability,
    AgentStatus,
    PerformanceMetrics
)


class TestAgentMetadataCreation:
    """Test agent metadata creation"""
    
    def test_create_minimal_metadata(self):
        """Test creating metadata with minimal info"""
        metadata = AgentMetadata(agent_type="TestAgent")
        
        assert metadata.agent_id
        assert metadata.agent_type == "TestAgent"
        assert metadata.version == "1.0.0"
        assert metadata.status == AgentStatus.HEALTHY
        assert metadata.current_load == 0
        assert metadata.max_capacity == 100
    
    def test_create_with_capabilities(self):
        """Test creating metadata with capabilities"""
        capabilities = {
            AgentCapability.CALENDAR_MANAGEMENT,
            AgentCapability.EVENT_CREATION
        }
        metadata = AgentMetadata(
            agent_type="AgendaAgent",
            capabilities=capabilities
        )
        
        assert metadata.capabilities == capabilities
        assert metadata.has_capability(AgentCapability.CALENDAR_MANAGEMENT)
        assert metadata.has_capability(AgentCapability.EVENT_CREATION)
        assert not metadata.has_capability(AgentCapability.NOTE_MANAGEMENT)
    
    def test_create_with_custom_capacity(self):
        """Test creating metadata with custom capacity"""
        metadata = AgentMetadata(
            agent_type="TestAgent",
            max_capacity=50
        )
        
        assert metadata.max_capacity == 50
    
    def test_agent_id_is_unique(self):
        """Test that each agent gets unique ID"""
        metadata1 = AgentMetadata(agent_type="Agent1")
        metadata2 = AgentMetadata(agent_type="Agent2")
        
        assert metadata1.agent_id != metadata2.agent_id
    
    def test_validation_requires_agent_type(self):
        """Test that agent_type is required"""
        with pytest.raises(ValueError, match="agent_type is required"):
            AgentMetadata()
    
    def test_validation_positive_capacity(self):
        """Test that max_capacity must be positive"""
        with pytest.raises(ValueError, match="max_capacity must be positive"):
            AgentMetadata(agent_type="Test", max_capacity=0)
    
    def test_validation_non_negative_load(self):
        """Test that current_load cannot be negative"""
        with pytest.raises(ValueError, match="current_load cannot be negative"):
            AgentMetadata(agent_type="Test", current_load=-1)


class TestAgentMetadataProperties:
    """Test agent metadata computed properties"""
    
    def test_load_percentage_calculation(self):
        """Test load percentage calculation"""
        metadata = AgentMetadata(
            agent_type="Test",
            current_load=25,
            max_capacity=100
        )
        
        assert metadata.load_percentage == 25.0
    
    def test_load_percentage_full(self):
        """Test load percentage at full capacity"""
        metadata = AgentMetadata(
            agent_type="Test",
            current_load=100,
            max_capacity=100
        )
        
        assert metadata.load_percentage == 100.0
    
    def test_available_capacity(self):
        """Test available capacity calculation"""
        metadata = AgentMetadata(
            agent_type="Test",
            current_load=30,
            max_capacity=100
        )
        
        assert metadata.available_capacity == 70
    
    def test_is_available_when_healthy_and_not_full(self):
        """Test is_available when agent is healthy and has capacity"""
        metadata = AgentMetadata(
            agent_type="Test",
            current_load=50,
            max_capacity=100
        )
        
        assert metadata.is_available
    
    def test_is_not_available_when_full(self):
        """Test is_available returns False when at capacity"""
        metadata = AgentMetadata(
            agent_type="Test",
            current_load=100,
            max_capacity=100
        )
        
        assert not metadata.is_available
    
    def test_is_not_available_when_unavailable_status(self):
        """Test is_available returns False when status is unavailable"""
        metadata = AgentMetadata(
            agent_type="Test",
            status=AgentStatus.UNAVAILABLE,
            current_load=0
        )
        
        assert not metadata.is_available
    
    def test_is_overloaded(self):
        """Test is_overloaded property"""
        metadata = AgentMetadata(
            agent_type="Test",
            current_load=100,
            max_capacity=100
        )
        
        assert metadata.is_overloaded


class TestAgentMetadataMethods:
    """Test agent metadata methods"""
    
    def test_add_capability(self):
        """Test adding capability"""
        metadata = AgentMetadata(agent_type="Test")
        
        metadata.add_capability(AgentCapability.NOTE_MANAGEMENT)
        
        assert metadata.has_capability(AgentCapability.NOTE_MANAGEMENT)
    
    def test_remove_capability(self):
        """Test removing capability"""
        metadata = AgentMetadata(
            agent_type="Test",
            capabilities={AgentCapability.NOTE_MANAGEMENT}
        )
        
        metadata.remove_capability(AgentCapability.NOTE_MANAGEMENT)
        
        assert not metadata.has_capability(AgentCapability.NOTE_MANAGEMENT)
    
    def test_update_heartbeat(self):
        """Test updating heartbeat"""
        metadata = AgentMetadata(agent_type="Test")
        old_heartbeat = metadata.last_heartbeat
        
        # Wait a bit
        import time
        time.sleep(0.01)
        
        metadata.update_heartbeat()
        
        assert metadata.last_heartbeat > old_heartbeat
    
    def test_increment_load(self):
        """Test incrementing load"""
        metadata = AgentMetadata(agent_type="Test", current_load=0)
        
        metadata.increment_load()
        
        assert metadata.current_load == 1
    
    def test_increment_load_respects_capacity(self):
        """Test that increment doesn't exceed capacity"""
        metadata = AgentMetadata(
            agent_type="Test",
            current_load=100,
            max_capacity=100
        )
        
        metadata.increment_load()
        
        assert metadata.current_load == 100
    
    def test_decrement_load(self):
        """Test decrementing load"""
        metadata = AgentMetadata(agent_type="Test", current_load=5)
        
        metadata.decrement_load()
        
        assert metadata.current_load == 4
    
    def test_decrement_load_stops_at_zero(self):
        """Test that decrement doesn't go below zero"""
        metadata = AgentMetadata(agent_type="Test", current_load=0)
        
        metadata.decrement_load()
        
        assert metadata.current_load == 0
    
    def test_update_metrics_success(self):
        """Test updating metrics with successful request"""
        metadata = AgentMetadata(agent_type="Test")
        
        metadata.update_metrics(response_time=0.5, success=True)
        
        assert metadata.metrics.total_requests == 1
        assert metadata.metrics.successful_requests == 1
        assert metadata.metrics.failed_requests == 0
        assert metadata.metrics.average_response_time == 0.5
    
    def test_update_metrics_failure(self):
        """Test updating metrics with failed request"""
        metadata = AgentMetadata(agent_type="Test")
        
        metadata.update_metrics(response_time=1.0, success=False)
        
        assert metadata.metrics.total_requests == 1
        assert metadata.metrics.successful_requests == 0
        assert metadata.metrics.failed_requests == 1
    
    def test_update_metrics_moving_average(self):
        """Test that average response time uses moving average"""
        metadata = AgentMetadata(agent_type="Test")
        
        metadata.update_metrics(response_time=0.5, success=True)
        metadata.update_metrics(response_time=1.5, success=True)
        
        assert metadata.metrics.average_response_time == 1.0


class TestPerformanceMetrics:
    """Test performance metrics calculations"""
    
    def test_success_rate(self):
        """Test success rate calculation"""
        metrics = PerformanceMetrics(
            total_requests=100,
            successful_requests=90,
            failed_requests=10
        )
        
        assert metrics.success_rate == 0.9
    
    def test_error_rate(self):
        """Test error rate calculation"""
        metrics = PerformanceMetrics(
            total_requests=100,
            successful_requests=90,
            failed_requests=10
        )
        
        assert metrics.error_rate == pytest.approx(0.1)
    
    def test_rates_with_zero_requests(self):
        """Test rates when no requests have been made"""
        metrics = PerformanceMetrics()
        
        assert metrics.success_rate == 0.0
        assert metrics.error_rate == 1.0
