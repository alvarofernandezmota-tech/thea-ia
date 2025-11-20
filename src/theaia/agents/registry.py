"""
Agent Registry System - H03 Advanced Agent Management
Dynamic agent loading con decorators integration.

H03 FASE 1 - BLOQUE 1.3 - TAREA 1.3.2
"""

import pkgutil
import importlib
import logging
from typing import Dict, List, Optional, Type, Any
from pathlib import Path

from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.decorators import get_registered_agents, get_agent_by_name, get_agents_by_intent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Registry centralizado de agents con dynamic loading.
    
    H03 Features:
    - Lazy loading de agents
    - Integration con decorators
    - Agent discovery automático
    - Priority-based routing
    - Dependency injection
    """
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._agent_classes: Dict[str, Type[BaseAgent]] = {}
        self._loaded = False
    
    def load_agents(self):
        """
        Escanea y carga agents dinámicamente.
        Busca en src/theaia/agents/*/handler.py
        """
        if self._loaded:
            logger.debug("[AgentRegistry] Agents already loaded")
            return
        
        logger.info("[AgentRegistry] Starting agent discovery...")
        
        try:
            package = importlib.import_module("src.theaia.agents")
        except ModuleNotFoundError:
            logger.error("[AgentRegistry] Cannot import agents package")
            return
        
        # Iterar sobre subdirectorios de agents
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            if not is_pkg:
                continue
            
            try:
                # Intentar importar handler.py de cada agent
                module = importlib.import_module(f"src.theaia.agents.{name}.handler")
                
                # Buscar clases que hereden de BaseAgent
                for attr in dir(module):
                    cls = getattr(module, attr)
                    
                    if (
                        isinstance(cls, type) and
                        issubclass(cls, BaseAgent) and
                        cls is not BaseAgent
                    ):
                        # Registrar clase (lazy instantiation)
                        intent = getattr(cls, 'INTENT', name)
                        self._agent_classes[intent] = cls
                        logger.info(f"[AgentRegistry] Discovered agent: {intent} ({cls.__name__})")
            
            except ModuleNotFoundError:
                logger.debug(f"[AgentRegistry] No handler.py in {name}")
                continue
            except Exception as e:
                logger.error(f"[AgentRegistry] Error loading agent {name}: {e}")
                continue
        
        # Cargar agents desde decorators registry
        self._load_from_decorators()
        
        self._loaded = True
        logger.info(f"[AgentRegistry] Loaded {len(self._agent_classes)} agent classes")
    
    def _load_from_decorators(self):
        """Carga agents registrados vía decorators."""
        decorated_agents = get_registered_agents()
        
        for name, metadata in decorated_agents.items():
            agent_class = metadata.get("class")
            if agent_class and name not in self._agent_classes:
                self._agent_classes[name] = agent_class
                logger.info(f"[AgentRegistry] Loaded from decorator: {name}")
    
    def get_agent(self, intent: str) -> Optional[BaseAgent]:
        """
        Retorna agent instanciado para el intent.
        Lazy instantiation: crea instancia solo cuando se pide.
        
        Args:
            intent: Intent del agent
            
        Returns:
            Agent instance o None
        """
        if not self._loaded:
            self.load_agents()
        
        # Si ya existe instancia, retornarla
        if intent in self._agents:
            return self._agents[intent]
        
        # Si existe clase, instanciarla
        if intent in self._agent_classes:
            try:
                self._agents[intent] = self._agent_classes[intent]()
                logger.debug(f"[AgentRegistry] Instantiated agent: {intent}")
                return self._agents[intent]
            except Exception as e:
                logger.error(f"[AgentRegistry] Error instantiating {intent}: {e}")
                return None
        
        logger.warning(f"[AgentRegistry] Agent not found: {intent}")
        return None
    
    def get_agents_by_intent(self, intent: str) -> List[BaseAgent]:
        """
        Retorna todos los agents que manejan un intent.
        
        Args:
            intent: Intent a buscar
            
        Returns:
            Lista de agents
        """
        if not self._loaded:
            self.load_agents()
        
        # Buscar en decorators registry
        decorated = get_agents_by_intent(intent)
        agents = []
        
        for metadata in decorated:
            agent_name = metadata["name"]
            agent = self.get_agent(agent_name)
            if agent:
                agents.append(agent)
        
        # Ordenar por prioridad (mayor primero)
        agents.sort(
            key=lambda a: getattr(a, '_metadata', {}).get('priority', 5),
            reverse=True
        )
        
        return agents
    
    def get_all_agents(self) -> Dict[str, BaseAgent]:
        """Retorna todos los agents cargados."""
        if not self._loaded:
            self.load_agents()
        
        # Instanciar todos los agents
        for intent in self._agent_classes:
            self.get_agent(intent)
        
        return self._agents.copy()
    
    def list_intents(self) -> List[str]:
        """Lista todos los intents disponibles."""
        if not self._loaded:
            self.load_agents()
        
        return list(self._agent_classes.keys())
    
    def reload_agents(self):
        """Recarga agents (útil para hot-reload)."""
        self._agents.clear()
        self._agent_classes.clear()
        self._loaded = False
        self.load_agents()
        logger.info("[AgentRegistry] Agents reloaded")
    
    def register_agent(self, intent: str, agent_class: Type[BaseAgent]):
        """
        Registra agent manualmente.
        
        Args:
            intent: Intent del agent
            agent_class: Clase del agent
        """
        self._agent_classes[intent] = agent_class
        logger.info(f"[AgentRegistry] Manually registered: {intent}")
    
    def get_agent_metadata(self, intent: str) -> Optional[Dict[str, Any]]:
        """
        Retorna metadata del agent.
        
        Args:
            intent: Intent del agent
            
        Returns:
            Metadata dict o None
        """
        # Intentar desde decorators
        metadata = get_agent_by_name(intent)
        if metadata:
            return metadata
        
        # Fallback: metadata básico
        if intent in self._agent_classes:
            return {
                "name": intent,
                "class": self._agent_classes[intent],
                "intents": [intent]
            }
        
        return None


# ==================== GLOBAL REGISTRY INSTANCE ====================

# Singleton registry instance
_registry = AgentRegistry()

# Legacy compatibility
agent_registry: Dict[str, BaseAgent] = _registry._agents


def load_agents():
    """Legacy function - carga agents."""
    _registry.load_agents()


def get_agent(intent: str) -> Optional[BaseAgent]:
    """Retorna agent por intent."""
    return _registry.get_agent(intent)


def get_all_agents() -> Dict[str, BaseAgent]:
    """Retorna todos los agents."""
    return _registry.get_all_agents()


def list_intents() -> List[str]:
    """Lista intents disponibles."""
    return _registry.list_intents()


def reload_agents():
    """Recarga agents."""
    _registry.reload_agents()


# Auto-load al importar módulo
load_agents()
