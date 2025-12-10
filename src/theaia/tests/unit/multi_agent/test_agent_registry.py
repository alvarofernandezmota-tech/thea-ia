"""
Tests for Agent Registry - H07.1
"""
import pytest
import time
from datetime import datetime, timedelta
from src.theaia.core.multi_agent.agent_registry import (
    AgentRegistry,
    RegistrationError
)
from src.theaia.core.multi_agent.agent_metadata import (
    AgentMetadata,
    AgentCapability,
    AgentStatus
)


@pytest.fixture
def registry():
    """Fixture that provides a fresh registry for each test"""
    reg = AgentRegistry()
    reg.clear()  # Clear any existing registrations
    return reg


@pytest.fixture
def sample_metadata():
    """Fixture that provides sample agent metadata"""
    return AgentMetadata(
        agent_type="TestAgent",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT}
    )


class TestAgentRegistration:
    """Test agent registration functionality"""
    
    def test_register_agent(self, registry, sample_metadata):
        """Test basic agent registration"""
        agent_id = registry.register(sample_metadata)
        
        assert agent_id == sample_metadata.agent_id
        assert registry.get(agent_id) is not None
    
    def test_register_returns_agent_id(self, registry, sample_metadata):
        """Test that register returns the agent ID"""
        agent_id = registry.register(sample_metadata)
        
        assert isinstance(agent_id, str)
        assert len(agent_id) > 0
    
    def test_register_stores_metadata(self, registry, sample_metadata):
        """Test that registration stores complete metadata"""
        agent_id = registry.register(sample_metadata)
        
        stored = registry.get(agent_id)
        assert stored.agent_type == sample_metadata.agent_type
        assert stored.capabilities == sample_metadata.capabilities
    
    def test_register_duplicate_raises_error(self, registry, sample_metadata):
        """Test that registering duplicate agent raises error"""
        registry.register(sample_metadata)
        
        with pytest.raises(RegistrationError, match="already registered"):
            registry.register(sample_metadata)
    
    def test_register_duplicate_with_force(self, registry, sample_metadata):
        """Test that force=True allows re-registration"""
        agent_id = registry.register(sample_metadata)
        
        # Modify metadata
        sample_metadata.max_capacity = 200
        
        # Re-register with force
        new_id = registry.register(sample_metadata, force=True)
        
        assert new_id == agent_id
        assert registry.get(agent_id).max_capacity == 200
    
    def test_register_multiple_agents(self, registry):
        """Test registering multiple agents"""
        metadata1 = AgentMetadata(agent_type="Agent1")
        metadata2 = AgentMetadata(agent_type="Agent2")
        
        id1 = registry.register(metadata1)
        id2 = registry.register(metadata2)
        
        assert id1 != id2
        assert registry.get_count() == 2
    
    def test_register_indexes_by_type(self, registry):
        """Test that agents are indexed by type"""
        metadata1 = AgentMetadata(agent_type="AgendaAgent")
        metadata2 = AgentMetadata(agent_type="AgendaAgent")
        metadata3 = AgentMetadata(agent_type="NoteAgent")
        
        registry.register(metadata1)
        registry.register(metadata2)
        registry.register(metadata3)
        
        agenda_agents = registry.get_by_type("AgendaAgent")
        assert len(agenda_agents) == 2
        
        note_agents = registry.get_by_type("NoteAgent")
        assert len(note_agents) == 1
    
    def test_register_indexes_by_capability(self, registry):
        """Test that agents are indexed by capability"""
        metadata1 = AgentMetadata(
            agent_type="Agent1",
            capabilities={AgentCapability.CALENDAR_MANAGEMENT}
        )
        metadata2 = AgentMetadata(
            agent_type="Agent2",
            capabilities={AgentCapability.CALENDAR_MANAGEMENT, AgentCapability.NOTE_MANAGEMENT}
        )
        
        registry.register(metadata1)
        registry.register(metadata2)
        
        cal_agents = registry.get_by_capability(AgentCapability.CALENDAR_MANAGEMENT)
        assert len(cal_agents) == 2
        
        note_agents = registry.get_by_capability(AgentCapability.NOTE_MANAGEMENT)
        assert len(note_agents) == 1


class TestAgentUnregistration:
    """Test agent unregistration functionality"""
    
    def test_unregister_agent(self, registry, sample_metadata):
        """Test basic agent unregistration"""
        agent_id = registry.register(sample_metadata)
        
        result = registry.unregister(agent_id)
        
        assert result is True
        assert registry.get(agent_id) is None
    
    def test_unregister_removes_from_type_index(self, registry):
        """Test that unregister removes from type index"""
        metadata = AgentMetadata(agent_type="TestAgent")
        agent_id = registry.register(metadata)
        
        registry.unregister(agent_id)
        
        agents = registry.get_by_type("TestAgent")
        assert len(agents) == 0
    
    def test_unregister_removes_from_capability_index(self, registry):
        """Test that unregister removes from capability index"""
        metadata = AgentMetadata(
            agent_type="TestAgent",
            capabilities={AgentCapability.CALENDAR_MANAGEMENT}
        )
        agent_id = registry.register(metadata)
        
        registry.unregister(agent_id)
        
        agents = registry.get_by_capability(AgentCapability.CALENDAR_MANAGEMENT)
        assert len(agents) == 0
    
    def test_unregister_nonexistent_returns_false(self, registry):
        """Test that unregistering nonexistent agent returns False"""
        result = registry.unregister("nonexistent-id")
        
        assert result is False
    
    def test_unregister_decreases_count(self, registry):
        """Test that unregister decreases agent count"""
        metadata1 = AgentMetadata(agent_type="Agent1")
        metadata2 = AgentMetadata(agent_type="Agent2")
        
        id1 = registry.register(metadata1)
        registry.register(metadata2)
        
        assert registry.get_count() == 2
        
        registry.unregister(id1)
        
        assert registry.get_count() == 1


class TestAgentRetrieval:
    """Test agent retrieval methods"""
    
    def test_get_agent_by_id(self, registry, sample_metadata):
        """Test retrieving agent by ID"""
        agent_id = registry.register(sample_metadata)
        
        retrieved = registry.get(agent_id)
        
        assert retrieved is not None
        assert retrieved.agent_id == agent_id
    
    def test_get_nonexistent_returns_none(self, registry):
        """Test that getting nonexistent agent returns None"""
        result = registry.get("nonexistent-id")
        
        assert result is None
    
    def test_get_all_agents(self, registry):
        """Test retrieving all agents"""
        metadata1 = AgentMetadata(agent_type="Agent1")
        metadata2 = AgentMetadata(agent_type="Agent2")
        
        registry.register(metadata1)
        registry.register(metadata2)
        
        all_agents = registry.get_all()
        
        assert len(all_agents) == 2
    
    def test_get_by_type(self, registry):
        """Test retrieving agents by type"""
        metadata1 = AgentMetadata(agent_type="AgendaAgent")
        metadata2 = AgentMetadata(agent_type="AgendaAgent")
        metadata3 = AgentMetadata(agent_type="NoteAgent")
        
        registry.register(metadata1)
        registry.register(metadata2)
        registry.register(metadata3)
        
        agenda_agents = registry.get_by_type("AgendaAgent")
        
        assert len(agenda_agents) == 2
        assert all(a.agent_type == "AgendaAgent" for a in agenda_agents)
    
    def test_get_by_capability(self, registry):
        """Test retrieving agents by capability"""
        metadata1 = AgentMetadata(
            agent_type="Agent1",
            capabilities={AgentCapability.EVENT_CREATION}
        )
        metadata2 = AgentMetadata(
            agent_type="Agent2",
            capabilities={AgentCapability.EVENT_CREATION}
        )
        
        registry.register(metadata1)
        registry.register(metadata2)
        
        agents = registry.get_by_capability(AgentCapability.EVENT_CREATION)
        
        assert len(agents) == 2
        assert all(a.has_capability(AgentCapability.EVENT_CREATION) for a in agents)
    
    def test_get_healthy_agents(self, registry):
        """Test retrieving only healthy agents"""
        metadata1 = AgentMetadata(agent_type="Agent1", status=AgentStatus.HEALTHY)
        metadata2 = AgentMetadata(agent_type="Agent2", status=AgentStatus.UNAVAILABLE)
        
        registry.register(metadata1)
        registry.register(metadata2)
        
        healthy = registry.get_healthy_agents()
        
        assert len(healthy) == 1
        assert healthy[0].status == AgentStatus.HEALTHY
    
    def test_get_available_agents(self, registry):
        """Test retrieving available agents"""
        metadata1 = AgentMetadata(
            agent_type="Agent1",
            status=AgentStatus.HEALTHY,
            current_load=50,
            max_capacity=100
        )
        metadata2 = AgentMetadata(
            agent_type="Agent2",
            status=AgentStatus.HEALTHY,
            current_load=100,
            max_capacity=100
        )
        
        registry.register(metadata1)
        registry.register(metadata2)
        
        available = registry.get_available_agents()
        
        assert len(available) == 1
        assert available[0].agent_id == metadata1.agent_id


class TestAgentUpdates:
    """Test agent update methods"""
    
    def test_update_status(self, registry, sample_metadata):
        """Test updating agent status"""
        agent_id = registry.register(sample_metadata)
        
        result = registry.update_status(agent_id, AgentStatus.DEGRADED)
        
        assert result is True
        assert registry.get(agent_id).status == AgentStatus.DEGRADED
    
    def test_update_status_nonexistent_returns_false(self, registry):
        """Test updating status of nonexistent agent"""
        result = registry.update_status("nonexistent", AgentStatus.HEALTHY)
        
        assert result is False
    
    def test_update_heartbeat(self, registry, sample_metadata):
        """Test updating agent heartbeat"""
        agent_id = registry.register(sample_metadata)
        old_heartbeat = registry.get(agent_id).last_heartbeat
        
        time.sleep(0.01)
        
        result = registry.update_heartbeat(agent_id)
        
        assert result is True
        assert registry.get(agent_id).last_heartbeat > old_heartbeat
    
    def test_update_heartbeat_nonexistent_returns_false(self, registry):
        """Test updating heartbeat of nonexistent agent"""
        result = registry.update_heartbeat("nonexistent")
        
        assert result is False
    
    def test_update_load_increment(self, registry, sample_metadata):
        """Test incrementing agent load"""
        agent_id = registry.register(sample_metadata)
        
        result = registry.update_load(agent_id, increment=True)
        
        assert result is True
        assert registry.get(agent_id).current_load == 1
    
    def test_update_load_decrement(self, registry):
        """Test decrementing agent load"""
        metadata = AgentMetadata(agent_type="Test", current_load=5)
        agent_id = registry.register(metadata)
        
        result = registry.update_load(agent_id, increment=False)
        
        assert result is True
        assert registry.get(agent_id).current_load == 4
    
    def test_update_load_nonexistent_returns_false(self, registry):
        """Test updating load of nonexistent agent"""
        result = registry.update_load("nonexistent", increment=True)
        
        assert result is False


class TestHeartbeatMonitoring:
    """Test heartbeat monitoring functionality"""
    
    def test_check_stale_heartbeats(self, registry):
        """Test checking for stale heartbeats"""
        metadata = AgentMetadata(agent_type="TestAgent")
        agent_id = registry.register(metadata)
        
        # Manually set old heartbeat
        registry.get(agent_id).last_heartbeat = (
            datetime.now() - timedelta(seconds=120)
        )
        
        stale = registry.check_stale_heartbeats()
        
        assert agent_id in stale
    
    def test_check_stale_heartbeats_empty_when_fresh(self, registry, sample_metadata):
        """Test that fresh heartbeats are not considered stale"""
        registry.register(sample_metadata)
        
        stale = registry.check_stale_heartbeats()
        
        assert len(stale) == 0
    
    def test_mark_stale_as_unavailable(self, registry):
        """Test marking stale agents as unavailable"""
        metadata = AgentMetadata(agent_type="TestAgent", status=AgentStatus.HEALTHY)
        agent_id = registry.register(metadata)
        
        # Make heartbeat stale
        registry.get(agent_id).last_heartbeat = (
            datetime.now() - timedelta(seconds=120)
        )
        
        count = registry.mark_stale_as_unavailable()
        
        assert count == 1
        assert registry.get(agent_id).status == AgentStatus.UNAVAILABLE


class TestRegistryStatistics:
    """Test registry statistics methods"""
    
    def test_get_count(self, registry):
        """Test getting total agent count"""
        metadata1 = AgentMetadata(agent_type="Agent1")
        metadata2 = AgentMetadata(agent_type="Agent2")
        
        registry.register(metadata1)
        registry.register(metadata2)
        
        assert registry.get_count() == 2
    
    def test_get_count_by_status(self, registry):
        """Test getting count by status"""
        metadata1 = AgentMetadata(agent_type="Agent1", status=AgentStatus.HEALTHY)
        metadata2 = AgentMetadata(agent_type="Agent2", status=AgentStatus.HEALTHY)
        metadata3 = AgentMetadata(agent_type="Agent3", status=AgentStatus.DEGRADED)
        
        registry.register(metadata1)
        registry.register(metadata2)
        registry.register(metadata3)
        
        healthy_count = registry.get_count_by_status(AgentStatus.HEALTHY)
        degraded_count = registry.get_count_by_status(AgentStatus.DEGRADED)
        
        assert healthy_count == 2
        assert degraded_count == 1
    
    def test_clear_registry(self, registry):
        """Test clearing the registry"""
        metadata1 = AgentMetadata(agent_type="Agent1")
        metadata2 = AgentMetadata(agent_type="Agent2")
        
        registry.register(metadata1)
        registry.register(metadata2)
        
        registry.clear()
        
        assert registry.get_count() == 0
