"""
Tests for Agent Registry - H07.1  
Coverage target: >85%
"""
import pytest
from src.theaia.core.multi_agent.agent_metadata import AgentMetadata, AgentStatus, AgentCapability
from src.theaia.core.multi_agent.agent_registry import AgentRegistry


@pytest.fixture
def registry():
    reg = AgentRegistry()
    reg.clear()
    return reg


class TestAgentRegistryBasic:
    def test_registry_initialization(self, registry):
        assert registry is not None
        assert registry.get_count() == 0
    
    def test_register_simple(self, registry):
        agent = AgentMetadata(agent_type="TestAgent")
        result = registry.register(agent)
        assert result is not None
        assert registry.get_count() == 1
    
    def test_register_with_capabilities(self, registry):
        agent = AgentMetadata(agent_type="CalendarAgent", capabilities={AgentCapability.CALENDAR_MANAGEMENT})
        result = registry.register(agent)
        assert result is not None
    
    def test_get_all_empty(self, registry):
        agents = registry.get_all()
        assert isinstance(agents, (dict, list))
    
    def test_register_and_retrieve(self, registry):
        agent = AgentMetadata(agent_type="TestAgent")
        agent_id = registry.register(agent)
        retrieved = registry.get(agent_id)
        assert retrieved is not None
    
    def test_multiple_agents(self, registry):
        agent1 = AgentMetadata(agent_type="Agent1")
        agent2 = AgentMetadata(agent_type="Agent2")
        id1 = registry.register(agent1)
        id2 = registry.register(agent2)
        assert id1 != id2
        assert registry.get_count() == 2


class TestAgentRegistryUnregister:
    def test_unregister_agent(self, registry):
        agent = AgentMetadata(agent_type="TestAgent")
        agent_id = registry.register(agent)
        assert registry.get_count() == 1
        registry.unregister(agent_id)
        assert registry.get_count() == 0


class TestAgentRegistryCapabilities:
    def test_get_by_capability_empty(self, registry):
        agents = registry.get_by_capability(AgentCapability.NOTE_MANAGEMENT)
        assert isinstance(agents, list)
        assert len(agents) == 0
    
    def test_get_by_capability_single(self, registry):
        agent = AgentMetadata(agent_type="CalendarAgent", capabilities={AgentCapability.CALENDAR_MANAGEMENT})
        registry.register(agent)
        agents = registry.get_by_capability(AgentCapability.CALENDAR_MANAGEMENT)
        assert len(agents) == 1
    
    def test_get_by_capability_multiple(self, registry):
        agent1 = AgentMetadata(agent_type="Calendar1", capabilities={AgentCapability.EVENT_CREATION})
        agent2 = AgentMetadata(agent_type="Calendar2", capabilities={AgentCapability.EVENT_CREATION})
        registry.register(agent1)
        registry.register(agent2)
        agents = registry.get_by_capability(AgentCapability.EVENT_CREATION)
        assert len(agents) == 2


class TestAgentRegistryStatus:
    def test_update_status(self, registry):
        agent = AgentMetadata(agent_type="TestAgent")
        agent_id = registry.register(agent)
        registry.update_status(agent_id, AgentStatus.MAINTENANCE)
        updated = registry.get(agent_id)
        assert updated.status == AgentStatus.MAINTENANCE
    
    def test_get_healthy_agents(self, registry):
        healthy = AgentMetadata(agent_type="HealthyAgent")
        degraded = AgentMetadata(agent_type="DegradedAgent", status=AgentStatus.DEGRADED)
        registry.register(healthy)
        registry.register(degraded)
        healthy_agents = registry.get_healthy_agents()
        assert len(healthy_agents) == 1


class TestAgentRegistryAvailability:
    def test_get_available_agents_empty(self, registry):
        available = registry.get_available_agents()
        assert isinstance(available, list)
        assert len(available) == 0
    
    def test_get_available_agents_healthy(self, registry):
        agent = AgentMetadata(agent_type="AvailableAgent")
        registry.register(agent)
        available = registry.get_available_agents()
        assert len(available) == 1


class TestAgentRegistryLoad:
    def test_increment_load(self, registry):
        agent = AgentMetadata(agent_type="TestAgent")
        agent_id = registry.register(agent)
        original_load = registry.get(agent_id).current_load
        registry.increment_load(agent_id)
        new_load = registry.get(agent_id).current_load
        assert new_load == original_load + 1
    
    def test_decrement_load(self, registry):
        agent = AgentMetadata(agent_type="TestAgent", current_load=5)
        agent_id = registry.register(agent)
        registry.decrement_load(agent_id)
        new_load = registry.get(agent_id).current_load
        assert new_load == 4


class TestAgentRegistryHeartbeat:
    def test_update_heartbeat(self, registry):
        agent = AgentMetadata(agent_type="TestAgent")
        agent_id = registry.register(agent)
        original_heartbeat = registry.get(agent_id).last_heartbeat
        import time
        time.sleep(0.01)
        registry.update_heartbeat(agent_id)
        new_heartbeat = registry.get(agent_id).last_heartbeat
        assert new_heartbeat > original_heartbeat


class TestAgentRegistryStats:
    def test_get_count_empty(self, registry):
        count = registry.get_count()
        assert count == 0
    
    def test_get_count_with_agents(self, registry):
        registry.register(AgentMetadata(agent_type="Agent0"))
        registry.register(AgentMetadata(agent_type="Agent1"))
        registry.register(AgentMetadata(agent_type="Agent2"))
        count = registry.get_count()
        assert count == 3
    
    def test_get_count_by_status(self, registry):
        registry.register(AgentMetadata(agent_type="Healthy"))
        registry.register(AgentMetadata(agent_type="Degraded", status=AgentStatus.DEGRADED))
        healthy_count = registry.get_count_by_status(AgentStatus.HEALTHY)
        assert healthy_count == 1
        degraded_count = registry.get_count_by_status(AgentStatus.DEGRADED)
        assert degraded_count == 1


class TestAgentRegistryByType:
    def test_get_by_type(self, registry):
        agent1 = AgentMetadata(agent_type="TypeA")
        agent2 = AgentMetadata(agent_type="TypeA")
        agent3 = AgentMetadata(agent_type="TypeB")
        registry.register(agent1)
        registry.register(agent2)
        registry.register(agent3)
        type_a_agents = registry.get_by_type("TypeA")
        assert len(type_a_agents) == 2
