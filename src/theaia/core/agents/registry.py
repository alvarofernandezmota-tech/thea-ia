"""
Agent Registry - H07.1
Central registry for agent registration and management
"""
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import logging
import threading
from .metadata import AgentMetadata, AgentStatus, AgentCapability

logger = logging.getLogger(__name__)


class RegistrationError(Exception):
    """Exception raised for registration errors"""
    pass


class AgentRegistry:
    """
    Central registry for managing agent registrations
    Thread-safe singleton implementation
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._agents: Dict[str, AgentMetadata] = {}
            self._agents_by_type: Dict[str, List[str]] = {}
            self._agents_by_capability: Dict[AgentCapability, List[str]] = {}
            self._lock = threading.RLock()
            self._heartbeat_timeout = 60  # seconds
            self._initialized = True
            logger.info("AgentRegistry initialized")
    
    def register(
        self,
        metadata: AgentMetadata,
        force: bool = False
    ) -> str:
        """
        Register an agent in the registry
        
        Args:
            metadata: Agent metadata
            force: Force registration even if agent exists
            
        Returns:
            agent_id of registered agent
            
        Raises:
            RegistrationError: If registration fails
        """
        with self._lock:
            if not force and metadata.agent_id in self._agents:
                raise RegistrationError(
                    f"Agent {metadata.agent_id} already registered. "
                    "Use force=True to override."
                )
            
            # Store agent metadata
            self._agents[metadata.agent_id] = metadata
            
            # Index by type
            if metadata.agent_type not in self._agents_by_type:
                self._agents_by_type[metadata.agent_type] = []
            if metadata.agent_id not in self._agents_by_type[metadata.agent_type]:
                self._agents_by_type[metadata.agent_type].append(metadata.agent_id)
            
            # Index by capabilities
            for capability in metadata.capabilities:
                if capability not in self._agents_by_capability:
                    self._agents_by_capability[capability] = []
                if metadata.agent_id not in self._agents_by_capability[capability]:
                    self._agents_by_capability[capability].append(metadata.agent_id)
            
            logger.info(
                f"Registered agent {metadata.agent_id} "
                f"({metadata.agent_type}) with capabilities: "
                f"{[c.value for c in metadata.capabilities]}"
            )
            
            return metadata.agent_id
    
    def unregister(self, agent_id: str) -> bool:
        """
        Unregister an agent from the registry
        
        Args:
            agent_id: ID of agent to unregister
            
        Returns:
            True if agent was unregistered, False if not found
        """
        with self._lock:
            if agent_id not in self._agents:
                logger.warning(f"Attempted to unregister unknown agent {agent_id}")
                return False
            
            metadata = self._agents[agent_id]
            
            # Remove from type index
            if metadata.agent_type in self._agents_by_type:
                if agent_id in self._agents_by_type[metadata.agent_type]:
                    self._agents_by_type[metadata.agent_type].remove(agent_id)
                if not self._agents_by_type[metadata.agent_type]:
                    del self._agents_by_type[metadata.agent_type]
            
            # Remove from capability index
            for capability in metadata.capabilities:
                if capability in self._agents_by_capability:
                    if agent_id in self._agents_by_capability[capability]:
                        self._agents_by_capability[capability].remove(agent_id)
                    if not self._agents_by_capability[capability]:
                        del self._agents_by_capability[capability]
            
            # Remove agent
            del self._agents[agent_id]
            
            logger.info(f"Unregistered agent {agent_id}")
            return True
    
    def get(self, agent_id: str) -> Optional[AgentMetadata]:
        """Get agent metadata by ID"""
        with self._lock:
            return self._agents.get(agent_id)
    
    def get_agent(self, agent_id: str) -> Optional[AgentMetadata]:
        """
        Get agent metadata by ID (alias for get method)
        
        Args:
            agent_id: ID of agent
            
        Returns:
            AgentMetadata if found, None otherwise
        """
        return self.get(agent_id)
    
    def get_all(self) -> List[AgentMetadata]:
        """Get all registered agents"""
        with self._lock:
            return list(self._agents.values())
    
    def get_by_type(self, agent_type: str) -> List[AgentMetadata]:
        """Get all agents of specific type"""
        with self._lock:
            agent_ids = self._agents_by_type.get(agent_type, [])
            return [self._agents[aid] for aid in agent_ids if aid in self._agents]
    
    def get_by_capability(
        self,
        capability: AgentCapability
    ) -> List[AgentMetadata]:
        """Get all agents with specific capability"""
        with self._lock:
            agent_ids = self._agents_by_capability.get(capability, [])
            return [self._agents[aid] for aid in agent_ids if aid in self._agents]
    
    def update_status(
        self,
        agent_id: str,
        status: AgentStatus
    ) -> bool:
        """Update agent status"""
        with self._lock:
            if agent_id not in self._agents:
                return False
            
            self._agents[agent_id].status = status
            logger.debug(f"Updated status for agent {agent_id}: {status.value}")
            return True
    
    def update_heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat"""
        with self._lock:
            if agent_id not in self._agents:
                return False
            
            self._agents[agent_id].update_heartbeat()
            return True
    
    def update_load(
        self,
        agent_id: str,
        increment: bool = True
    ) -> bool:
        """Update agent load"""
        with self._lock:
            if agent_id not in self._agents:
                return False
            
            if increment:
                self._agents[agent_id].increment_load()
            else:
                self._agents[agent_id].decrement_load()
            
            return True
    
    def increment_load(self, agent_id: str) -> bool:
        """
        Increment agent load (convenience method)
        
        Args:
            agent_id: ID of agent
            
        Returns:
            True if successful, False if agent not found
        """
        return self.update_load(agent_id, increment=True)
    
    def decrement_load(self, agent_id: str) -> bool:
        """
        Decrement agent load (convenience method)
        
        Args:
            agent_id: ID of agent
            
        Returns:
            True if successful, False if agent not found
        """
        return self.update_load(agent_id, increment=False)
    
    def get_healthy_agents(self) -> List[AgentMetadata]:
        """Get all healthy agents"""
        with self._lock:
            return [
                agent for agent in self._agents.values()
                if agent.status == AgentStatus.HEALTHY
            ]
    
    def get_available_agents(self) -> List[AgentMetadata]:
        """Get all available agents (healthy and not overloaded)"""
        with self._lock:
            return [
                agent for agent in self._agents.values()
                if agent.is_available
            ]
    
    def check_stale_heartbeats(self) -> List[str]:
        """
        Check for agents with stale heartbeats
        
        Returns:
            List of agent IDs with stale heartbeats
        """
        with self._lock:
            stale_agents = []
            cutoff = datetime.now() - timedelta(seconds=self._heartbeat_timeout)
            
            for agent_id, metadata in self._agents.items():
                if metadata.last_heartbeat < cutoff:
                    stale_agents.append(agent_id)
                    logger.warning(
                        f"Agent {agent_id} has stale heartbeat "
                        f"(last: {metadata.last_heartbeat})"
                    )
            
            return stale_agents
    
    def mark_stale_as_unavailable(self) -> int:
        """
        Mark agents with stale heartbeats as unavailable
        
        Returns:
            Number of agents marked as unavailable
        """
        stale_agents = self.check_stale_heartbeats()
        count = 0
        
        for agent_id in stale_agents:
            if self.update_status(agent_id, AgentStatus.UNAVAILABLE):
                count += 1
        
        return count
    
    def get_count(self) -> int:
        """Get total number of registered agents"""
        with self._lock:
            return len(self._agents)
    
    def get_count_by_status(self, status: AgentStatus) -> int:
        """Get count of agents with specific status"""
        with self._lock:
            return sum(
                1 for agent in self._agents.values()
                if agent.status == status
            )
    
    def clear(self):
        """Clear all registered agents (for testing)"""
        with self._lock:
            self._agents.clear()
            self._agents_by_type.clear()
            self._agents_by_capability.clear()
            logger.info("Registry cleared")
