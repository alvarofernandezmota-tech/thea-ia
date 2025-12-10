"""
Discovery Service - H07.1
Service for discovering agents based on queries
"""
from dataclasses import dataclass
from typing import List, Optional, Set, Dict, Any
from enum import Enum
import logging
from .agent_metadata import AgentMetadata, AgentCapability, AgentStatus
from .agent_registry import AgentRegistry

logger = logging.getLogger(__name__)


class LoadBalancingStrategy(Enum):
    """Load balancing strategies"""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    RANDOM = "random"
    PRIORITY = "priority"


@dataclass
class DiscoveryQuery:
    """Query for discovering agents"""
    capabilities: Optional[Set[AgentCapability]] = None
    agent_type: Optional[str] = None
    min_available_capacity: int = 1
    status: Optional[AgentStatus] = None
    tags: Optional[Dict[str, str]] = None
    max_results: Optional[int] = None
    load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED


class DiscoveryService:
    """
    Service for discovering agents in the registry
    """
    
    def __init__(self, registry: Optional[AgentRegistry] = None):
        self.registry = registry or AgentRegistry()
        self._round_robin_index: Dict[str, int] = {}
        logger.info("DiscoveryService initialized")
    
    def discover(
        self,
        query: DiscoveryQuery
    ) -> List[AgentMetadata]:
        """
        Discover agents matching the query
        
        Args:
            query: Discovery query with filters
            
        Returns:
            List of matching agents, sorted by load balancing strategy
        """
        # Start with all agents
        candidates = self.registry.get_all()
        
        # Apply filters
        candidates = self._apply_filters(candidates, query)
        
        # Apply load balancing strategy
        candidates = self._apply_load_balancing(candidates, query.load_balancing)
        
        # Limit results
        if query.max_results:
            candidates = candidates[:query.max_results]
        
        logger.debug(
            f"Discovery query returned {len(candidates)} agents "
            f"with strategy {query.load_balancing.value}"
        )
        
        return candidates
    
    def discover_by_capability(
        self,
        capability: AgentCapability,
        max_results: Optional[int] = None
    ) -> List[AgentMetadata]:
        """
        Discover agents by capability (convenience method)
        
        Args:
            capability: Required capability
            max_results: Maximum number of results
            
        Returns:
            List of matching agents
        """
        query = DiscoveryQuery(
            capabilities={capability},
            max_results=max_results
        )
        return self.discover(query)
    
    def discover_best_agent(
        self,
        query: DiscoveryQuery
    ) -> Optional[AgentMetadata]:
        """
        Discover the single best agent for the query
        
        Args:
            query: Discovery query
            
        Returns:
            Best matching agent or None
        """
        query.max_results = 1
        results = self.discover(query)
        return results[0] if results else None
    
    def _apply_filters(
        self,
        agents: List[AgentMetadata],
        query: DiscoveryQuery
    ) -> List[AgentMetadata]:
        """Apply query filters to agent list"""
        filtered = agents
        
        # Filter by capabilities
        if query.capabilities:
            filtered = [
                agent for agent in filtered
                if all(agent.has_capability(cap) for cap in query.capabilities)
            ]
        
        # Filter by agent type
        if query.agent_type:
            filtered = [
                agent for agent in filtered
                if agent.agent_type == query.agent_type
            ]
        
        # Filter by status
        if query.status:
            filtered = [
                agent for agent in filtered
                if agent.status == query.status
            ]
        else:
            # By default, only return available agents
            filtered = [agent for agent in filtered if agent.is_available]
        
        # Filter by available capacity
        filtered = [
            agent for agent in filtered
            if agent.available_capacity >= query.min_available_capacity
        ]
        
        # Filter by tags
        if query.tags:
            filtered = [
                agent for agent in filtered
                if all(
                    agent.tags.get(k) == v
                    for k, v in query.tags.items()
                )
            ]
        
        return filtered
    
    def _apply_load_balancing(
        self,
        agents: List[AgentMetadata],
        strategy: LoadBalancingStrategy
    ) -> List[AgentMetadata]:
        """Apply load balancing strategy to sort agents"""
        if not agents:
            return agents
        
        if strategy == LoadBalancingStrategy.LEAST_LOADED:
            return sorted(agents, key=lambda a: a.load_percentage)
        
        elif strategy == LoadBalancingStrategy.PRIORITY:
            return sorted(
                agents,
                key=lambda a: (-a.priority, a.load_percentage)
            )
        
        elif strategy == LoadBalancingStrategy.ROUND_ROBIN:
            # Group by agent type for round robin
            agent_type = agents[0].agent_type if agents else "default"
            index = self._round_robin_index.get(agent_type, 0)
            
            # Rotate list
            result = agents[index:] + agents[:index]
            
            # Update index
            self._round_robin_index[agent_type] = (index + 1) % len(agents)
            
            return result
        
        elif strategy == LoadBalancingStrategy.RANDOM:
            import random
            result = agents.copy()
            random.shuffle(result)
            return result
        
        return agents
    
    def get_agent_summary(self) -> Dict[str, Any]:
        """
        Get summary of registered agents
        
        Returns:
            Dictionary with agent statistics
        """
        agents = self.registry.get_all()
        
        total = len(agents)
        healthy = sum(1 for a in agents if a.status == AgentStatus.HEALTHY)
        available = sum(1 for a in agents if a.is_available)
        overloaded = sum(1 for a in agents if a.is_overloaded)
        
        total_capacity = sum(a.max_capacity for a in agents)
        used_capacity = sum(a.current_load for a in agents)
        
        avg_load = (
            used_capacity / total_capacity * 100
            if total_capacity > 0 else 0
        )
        
        capabilities_count = {}
        for agent in agents:
            for cap in agent.capabilities:
                capabilities_count[cap.value] = capabilities_count.get(cap.value, 0) + 1
        
        return {
            "total_agents": total,
            "healthy_agents": healthy,
            "available_agents": available,
            "overloaded_agents": overloaded,
            "total_capacity": total_capacity,
            "used_capacity": used_capacity,
            "average_load_percentage": round(avg_load, 2),
            "capabilities": capabilities_count,
        }
