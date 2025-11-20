"""
Agent Registry for THEA-IA.

Dynamic agent registration and management system.
Provides centralized agent discovery and instantiation.

Version: v0.16.0 (H03)
Author: Álvaro Fernández Mota
Date: 20 Nov 2025
"""

from typing import Dict, List, Optional, Type, Any
import logging
from .base_agent import BaseAgent
from .agent_config import AgentConfig, DEFAULT_AGENT_CONFIGS


logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Central registry for agent management.
    
    Handles agent registration, discovery, and instantiation
    with configuration validation and error handling.
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._agents: Dict[str, Type[BaseAgent]] = {}
        self._configs: Dict[str, AgentConfig] = {}
        self._instances: Dict[str, BaseAgent] = {}
        logger.info("AgentRegistry initialized")
    
    def register(
        self,
        agent_class: Type[BaseAgent],
        config: Optional[AgentConfig] = None
    ) -> None:
        """
        Register an agent class with optional config.
        
        Args:
            agent_class: Agent class to register (subclass of BaseAgent)
            config: Optional configuration (uses default if None)
            
        Raises:
            ValueError: If agent_class is not BaseAgent subclass
            TypeError: If agent_class is not a class
        """
        if not isinstance(agent_class, type):
            raise TypeError(f"agent_class must be a class, got {type(agent_class)}")
        
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(f"{agent_class.__name__} must inherit from BaseAgent")
        
        agent_name = agent_class.__name__.replace("Agent", "").lower()
        
        # Use provided config or default
        if config is None:
            config = DEFAULT_AGENT_CONFIGS.get(agent_name)
            if config is None:
                logger.warning(f"No default config for {agent_name}, creating minimal config")
                config = AgentConfig(
                    name=agent_name,
                    display_name=agent_class.__name__,
                    description=agent_class.__doc__ or "No description",
                    intents=[agent_name]
                )
        
        self._agents[agent_name] = agent_class
        self._configs[agent_name] = config
        
        logger.info(f"Registered agent: {agent_name} ({agent_class.__name__})")
    
    def unregister(self, agent_name: str) -> None:
        """
        Unregister an agent.
        
        Args:
            agent_name: Agent identifier to remove
        """
        agent_name = agent_name.lower()
        
        if agent_name in self._agents:
            del self._agents[agent_name]
            logger.info(f"Unregistered agent: {agent_name}")
        
        if agent_name in self._configs:
            del self._configs[agent_name]
        
        if agent_name in self._instances:
            del self._instances[agent_name]
    
    def get_agent_class(self, agent_name: str) -> Optional[Type[BaseAgent]]:
        """
        Get registered agent class by name.
        
        Args:
            agent_name: Agent identifier (case-insensitive)
            
        Returns:
            Agent class if registered, None otherwise
        """
        return self._agents.get(agent_name.lower())
    
    def get_config(self, agent_name: str) -> Optional[AgentConfig]:
        """
        Get agent configuration.
        
        Args:
            agent_name: Agent identifier (case-insensitive)
            
        Returns:
            AgentConfig if found, None otherwise
        """
        return self._configs.get(agent_name.lower())
    
    def create_instance(
        self,
        agent_name: str,
        **kwargs: Any
    ) -> Optional[BaseAgent]:
        """
        Create new agent instance.
        
        Args:
            agent_name: Agent identifier
            **kwargs: Additional arguments for agent constructor
            
        Returns:
            Agent instance if successful, None otherwise
        """
        agent_name = agent_name.lower()
        agent_class = self.get_agent_class(agent_name)
        
        if agent_class is None:
            logger.error(f"Agent not registered: {agent_name}")
            return None
        
        try:
            instance = agent_class(**kwargs)
            logger.info(f"Created instance of {agent_name}")
            return instance
        except Exception as e:
            logger.error(f"Failed to create {agent_name} instance: {e}")
            return None
    
    def get_or_create_instance(
        self,
        agent_name: str,
        **kwargs: Any
    ) -> Optional[BaseAgent]:
        """
        Get cached instance or create new one.
        
        Args:
            agent_name: Agent identifier
            **kwargs: Additional arguments for agent constructor
            
        Returns:
            Agent instance (cached or new)
        """
        agent_name = agent_name.lower()
        
        if agent_name in self._instances:
            return self._instances[agent_name]
        
        instance = self.create_instance(agent_name, **kwargs)
        if instance:
            self._instances[agent_name] = instance
        
        return instance
    
    def list_agents(self) -> List[str]:
        """
        Get list of registered agent names.
        
        Returns:
            List of agent identifiers
        """
        return list(self._agents.keys())
    
    def list_enabled_agents(self) -> List[str]:
        """
        Get list of enabled agents.
        
        Returns:
            List of enabled agent identifiers
        """
        return [
            name for name, config in self._configs.items()
            if config.enabled
        ]
    
    def get_agent_for_intent(self, intent: str) -> Optional[str]:
        """
        Find agent that handles given intent.
        
        Args:
            intent: Intent string to match
            
        Returns:
            Agent name if found, None otherwise
        """
        intent_lower = intent.lower()
        
        # Find all matching agents
        matches = []
        for name, config in self._configs.items():
            if config.enabled and config.handles_intent(intent_lower):
                matches.append((name, config.priority.value))
        
        if not matches:
            return None
        
        # Return highest priority agent
        return max(matches, key=lambda x: x[1])[0]
    
    def is_registered(self, agent_name: str) -> bool:
        """Check if agent is registered."""
        return agent_name.lower() in self._agents
    
    def clear_instances(self) -> None:
        """Clear all cached instances."""
        self._instances.clear()
        logger.info("Cleared all agent instances")
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics.
        
        Returns:
            Dictionary with registry stats
        """
        return {
            'total_registered': len(self._agents),
            'total_enabled': len(self.list_enabled_agents()),
            'total_instances': len(self._instances),
            'agents': self.list_agents(),
            'enabled_agents': self.list_enabled_agents()
        }


# ==================== GLOBAL REGISTRY INSTANCE ====================

# Singleton global registry
_global_registry: Optional[AgentRegistry] = None


def get_global_registry() -> AgentRegistry:
    """
    Get or create global agent registry.
    
    Returns:
        Global AgentRegistry instance
    """
    global _global_registry
    
    if _global_registry is None:
        _global_registry = AgentRegistry()
        logger.info("Created global agent registry")
    
    return _global_registry


def register_agent(
    agent_class: Type[BaseAgent],
    config: Optional[AgentConfig] = None
) -> None:
    """
    Register agent in global registry.
    
    Args:
        agent_class: Agent class to register
        config: Optional configuration
    """
    registry = get_global_registry()
    registry.register(agent_class, config)


def get_agent(agent_name: str, **kwargs: Any) -> Optional[BaseAgent]:
    """
    Get agent instance from global registry.
    
    Args:
        agent_name: Agent identifier
        **kwargs: Additional constructor arguments
        
    Returns:
        Agent instance if found
    """
    registry = get_global_registry()
    return registry.get_or_create_instance(agent_name, **kwargs)


def list_all_agents() -> List[str]:
    """Get list of all registered agents."""
    registry = get_global_registry()
    return registry.list_agents()


def reset_global_registry() -> None:
    """Reset global registry (useful for testing)."""
    global _global_registry
    _global_registry = None
    logger.info("Reset global agent registry")
