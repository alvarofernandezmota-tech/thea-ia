"""
Tests for Discovery Service - H07.1
"""
import pytest
from src.theaia.core.multi_agent.discovery_service import (
    DiscoveryService,
    DiscoveryQuery,
    LoadBalancingStrategy
)
from src.theaia.core.multi_agent.agent_registry import AgentRegistry
from src.theaia.core.multi_agent.agent_metadata import (
    AgentMetadata,
    AgentCapability,
    AgentStatus
)


@pytest.fixture
def registry():
    """Fixture that provides a fresh registry"""
    reg = AgentRegistry()
    reg.clear()
    return reg


@pytest.fixture
def discovery_service(registry):
    """Fixture that provides discovery service with fresh registry"""
    return DiscoveryService(registry)


@pytest.fixture
def populated_registry(registry):
    """Fixture that provides registry with sample agents"""
    # Agent 1: Agenda agent, healthy, low load
    agent1 = AgentMetadata(
        agent_type="AgendaAgent",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT, AgentCapability.EVENT_CREATION},
        status=AgentStatus.HEALTHY,
        current_load=10,
        max_capacity=100,
        priority=5
    )
    
    # Agent 2: Agenda agent, healthy, high load
    agent2 = AgentMetadata(
        agent_type="AgendaAgent",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT, AgentCapability.EVENT_CREATION},
        status=AgentStatus.HEALTHY,
        current_load=80,
        max_capacity=100,
        priority=3
    )
    
    # Agent 3: Note agent, healthy
    agent3 = AgentMetadata(
        agent_type="NoteAgent",
        capabilities={AgentCapability.NOTE_MANAGEMENT},
        status=AgentStatus.HEALTHY,
        current_load=20,
        max_capacity=100,
        priority=4
    )
    
    # Agent 4: Unavailable agent
    agent4 = AgentMetadata(
        agent_type="AgendaAgent",
        capabilities={AgentCapability.CALENDAR_MANAGEMENT},
        status=AgentStatus.UNAVAILABLE,
        current_load=0,
        max_capacity=100
    )
    
    registry.register(agent1)
    registry.register(agent2)
    registry.register(agent3)
    registry.register(agent4)
    
    return registry


class TestBasicDiscovery:
    """Test basic discovery functionality"""
    
    def test_discover_all_agents(self, discovery_service, populated_registry):
        """Test discovering all available agents"""
        query = DiscoveryQuery()
        
        results = discovery_service.discover(query)
        
        # Should return 3 (excluding unavailable agent)
        assert len(results) == 3
    
    def test_discover_by_capability(self, discovery_service, populated_registry):
        """Test discovering agents by capability"""
        query = DiscoveryQuery(
            capabilities={AgentCapability.CALENDAR_MANAGEMENT}
        )
        
        results = discovery_service.discover(query)
        
        assert len(results) == 2
        assert all(
            a.has_capability(AgentCapability.CALENDAR_MANAGEMENT)
            for a in results
        )
    
    def test_discover_by_multiple_capabilities(self, discovery_service, populated_registry):
        """Test discovering agents with multiple capabilities"""
        query = DiscoveryQuery(
            capabilities={
                AgentCapability.CALENDAR_MANAGEMENT,
                AgentCapability.EVENT_CREATION
            }
        )
        
        results = discovery_service.discover(query)
        
        assert len(results) == 2
        assert all(
            a.has_capability(AgentCapability.CALENDAR_MANAGEMENT) and
            a.has_capability(AgentCapability.EVENT_CREATION)
            for a in results
        )
    
    def test_discover_by_agent_type(self, discovery_service, populated_registry):
        """Test discovering agents by type"""
        query = DiscoveryQuery(agent_type="NoteAgent")
        
        results = discovery_service.discover(query)
        
        assert len(results) == 1
        assert results[0].agent_type == "NoteAgent"
    
    def test_discover_by_status(self, discovery_service, populated_registry):
        """Test discovering agents by status"""
        query = DiscoveryQuery(status=AgentStatus.UNAVAILABLE)
        
        results = discovery_service.discover(query)
        
        assert len(results) == 1
        assert results[0].status == AgentStatus.UNAVAILABLE
    
    def test_discover_with_min_capacity(self, discovery_service, populated_registry):
        """Test discovering agents with minimum capacity"""
        query = DiscoveryQuery(min_available_capacity=50)
        
        results = discovery_service.discover(query)
        
        # Only agent1 (90 available) and agent3 (80 available) meet criteria
        assert len(results) == 2
        assert all(a.available_capacity >= 50 for a in results)
    
    def test_discover_with_max_results(self, discovery_service, populated_registry):
        """Test limiting discovery results"""
        query = DiscoveryQuery(max_results=2)
        
        results = discovery_service.discover(query)
        
        assert len(results) == 2
    
    def test_discover_by_capability_convenience(self, discovery_service, populated_registry):
        """Test convenience method for discovering by capability"""
        results = discovery_service.discover_by_capability(
            AgentCapability.NOTE_MANAGEMENT
        )
        
        assert len(results) == 1
        assert results[0].agent_type == "NoteAgent"
    
    def test_discover_best_agent(self, discovery_service, populated_registry):
        """Test discovering single best agent"""
        query = DiscoveryQuery(
            capabilities={AgentCapability.CALENDAR_MANAGEMENT}
        )
        
        best = discovery_service.discover_best_agent(query)
        
        assert best is not None
        assert best.has_capability(AgentCapability.CALENDAR_MANAGEMENT)


class TestLoadBalancing:
    """Test load balancing strategies"""
    
    def test_least_loaded_strategy(self, discovery_service, populated_registry):
        """Test least loaded load balancing"""
        query = DiscoveryQuery(
            agent_type="AgendaAgent",
            load_balancing=LoadBalancingStrategy.LEAST_LOADED
        )
        
        results = discovery_service.discover(query)
        
        # Should return in order of increasing load
        assert results[0].current_load < results[1].current_load
    
    def test_priority_strategy(self, discovery_service, populated_registry):
        """Test priority-based load balancing"""
        query = DiscoveryQuery(
            agent_type="AgendaAgent",
            load_balancing=LoadBalancingStrategy.PRIORITY
        )
        
        results = discovery_service.discover(query)
        
        # Should return highest priority first
        assert results[0].priority >= results[1].priority
    
    def test_round_robin_strategy(self, discovery_service, populated_registry):
        """Test round-robin load balancing"""
        query = DiscoveryQuery(
            agent_type="AgendaAgent",
            load_balancing=LoadBalancingStrategy.ROUND_ROBIN
        )
        
        results1 = discovery_service.discover(query)
        results2 = discovery_service.discover(query)
        
        # Second call should rotate the list
        assert results1[0].agent_id != results2[0].agent_id
    
    def test_random_strategy(self, discovery_service, populated_registry):
        """Test random load balancing"""
        query = DiscoveryQuery(
            agent_type="AgendaAgent",
            load_balancing=LoadBalancingStrategy.RANDOM
        )
        
        results = discovery_service.discover(query)
        
        # Just verify we get results (order is random)
        assert len(results) == 2


class TestDiscoveryFilters:
    """Test discovery filter combinations"""
    
    def test_filter_by_capability_and_type(self, discovery_service, populated_registry):
        """Test filtering by capability and type"""
        query = DiscoveryQuery(
            capabilities={AgentCapability.CALENDAR_MANAGEMENT},
            agent_type="AgendaAgent"
        )
        
        results = discovery_service.discover(query)
        
        assert len(results) == 2
        assert all(a.agent_type == "AgendaAgent" for a in results)
    
    def test_filter_excludes_unavailable_by_default(self, discovery_service, populated_registry):
        """Test that unavailable agents are excluded by default"""
        query = DiscoveryQuery(
            capabilities={AgentCapability.CALENDAR_MANAGEMENT}
        )
        
        results = discovery_service.discover(query)
        
        assert all(a.is_available for a in results)
    
    def test_filter_with_tags(self, discovery_service, registry):
        """Test filtering by tags"""
        agent1 = AgentMetadata(
            agent_type="TestAgent",
            tags={"environment": "production", "region": "us-east"}
        )
        agent2 = AgentMetadata(
            agent_type="TestAgent",
            tags={"environment": "staging", "region": "us-west"}
        )
        
        registry.register(agent1)
        registry.register(agent2)
        
        query = DiscoveryQuery(
            tags={"environment": "production"}
        )
        
        results = discovery_service.discover(query)
        
        assert len(results) == 1
        assert results[0].tags["environment"] == "production"
    
    def test_no_results_when_no_match(self, discovery_service, populated_registry):
        """Test that empty list returned when no agents match"""
        query = DiscoveryQuery(
            capabilities={AgentCapability.USER_MANAGEMENT}  # No agent has this
        )
        
        results = discovery_service.discover(query)
        
        assert len(results) == 0
    
    def test_discover_best_returns_none_when_no_match(self, discovery_service, populated_registry):
        """Test that discover_best returns None when no match"""
        query = DiscoveryQuery(
            capabilities={AgentCapability.USER_MANAGEMENT}
        )
        
        best = discovery_service.discover_best_agent(query)
        
        assert best is None


class TestAgentSummary:
    """Test agent summary statistics"""
    
    def test_get_agent_summary(self, discovery_service, populated_registry):
        """Test getting agent summary"""
        summary = discovery_service.get_agent_summary()
        
        assert summary["total_agents"] == 4
        assert summary["healthy_agents"] == 3
        assert summary["available_agents"] == 3
        assert summary["overloaded_agents"] == 0
        assert summary["total_capacity"] == 400
        assert summary["used_capacity"] == 110
    
    def test_summary_includes_capabilities(self, discovery_service, populated_registry):
        """Test that summary includes capability counts"""
        summary = discovery_service.get_agent_summary()
        
        assert "capabilities" in summary
        assert summary["capabilities"][AgentCapability.CALENDAR_MANAGEMENT.value] == 3
        assert summary["capabilities"][AgentCapability.NOTE_MANAGEMENT.value] == 1
    
    def test_summary_calculates_average_load(self, discovery_service, populated_registry):
        """Test that summary includes average load"""
        summary = discovery_service.get_agent_summary()
        
        # (10 + 80 + 20 + 0) / 400 = 27.5%
        assert summary["average_load_percentage"] == 27.5
    
    def test_summary_with_empty_registry(self, discovery_service, registry):
        """Test summary with no registered agents"""
        summary = discovery_service.get_agent_summary()
        
        assert summary["total_agents"] == 0
        assert summary["total_capacity"] == 0
        assert summary["average_load_percentage"] == 0
