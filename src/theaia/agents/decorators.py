"""
Agent Decorators System - H03 Advanced Agent Management
Decoradores para auto-registration y metadata.

H03 FASE 1 - BLOQUE 1.3 - TAREA 1.3.1
"""

from functools import wraps
from typing import Callable, List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Registry global de agents decorados
_REGISTERED_AGENTS: Dict[str, Dict[str, Any]] = {}


def agent_handler(
    name: str,
    intents: List[str],
    priority: int = 5,
    requires_auth: bool = False,
    description: Optional[str] = None
):
    """
    Decorator para registrar agent handlers automáticamente.
    
    Args:
        name: Nombre del agent
        intents: Lista de intents que maneja
        priority: Prioridad (1-10, mayor = más prioritario)
        requires_auth: Si requiere autenticación
        description: Descripción del agent
        
    Usage:
        @agent_handler(
            name="agenda_agent",
            intents=["calendar", "schedule", "appointment"],
            priority=8
        )
        class AgendaAgent(BaseAgent):
            pass
    """
    def decorator(cls):
        # Extraer metadata
        metadata = {
            "name": name,
            "intents": intents,
            "priority": priority,
            "requires_auth": requires_auth,
            "description": description or cls.__doc__ or f"{name} agent",
            "class": cls
        }
        
        # Registrar en registry global
        _REGISTERED_AGENTS[name] = metadata
        
        logger.info(f"[AgentDecorator] Registered agent '{name}' with intents: {intents}")
        
        # Añadir metadata al class
        cls._agent_metadata = metadata
        
        @wraps(cls)
        def wrapper(*args, **kwargs):
            instance = cls(*args, **kwargs)
            instance._metadata = metadata
            return instance
        
        # Preservar metadata en wrapper
        wrapper._agent_metadata = metadata
        wrapper.__name__ = cls.__name__
        wrapper.__doc__ = cls.__doc__
        
        return wrapper
    
    return decorator


def get_registered_agents() -> Dict[str, Dict[str, Any]]:
    """Retorna todos los agents registrados."""
    return _REGISTERED_AGENTS.copy()


def get_agent_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Retorna metadata de agent por nombre."""
    return _REGISTERED_AGENTS.get(name)


def get_agents_by_intent(intent: str) -> List[Dict[str, Any]]:
    """Retorna agents que manejan el intent especificado."""
    return [
        metadata for metadata in _REGISTERED_AGENTS.values()
        if intent in metadata["intents"]
    ]


def clear_registry():
    """Limpia registry (útil para tests)."""
    _REGISTERED_AGENTS.clear()
    logger.debug("[AgentDecorator] Registry cleared")


# ==================== VALIDATION DECORATORS ====================

def validate_input(validator: Callable):
    """
    Decorator para validar input de agent.
    
    Args:
        validator: Función validadora que recibe user_input y retorna bool
    """
    def decorator(method):
        @wraps(method)
        async def wrapper(self, user_input: str, *args, **kwargs):
            if not validator(user_input):
                logger.warning(f"[{self.__class__.__name__}] Input validation failed")
                return {"error": "Invalid input", "input": user_input}
            return await method(self, user_input, *args, **kwargs)
        return wrapper
    return decorator


def require_context_keys(*required_keys: str):
    """
    Decorator que valida presencia de keys en context.
    
    Args:
        required_keys: Keys requeridas en context
    """
    def decorator(method):
        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            context = kwargs.get("context", {})
            missing = [key for key in required_keys if key not in context]
            
            if missing:
                logger.error(f"[{self.__class__.__name__}] Missing context keys: {missing}")
                return {"error": "Missing context keys", "missing": missing}
            
            return await method(self, *args, **kwargs)
        return wrapper
    return decorator


def log_execution(log_level: str = "INFO"):
    """
    Decorator para loggear ejecución de métodos.
    
    Args:
        log_level: Nivel de log (DEBUG, INFO, WARNING, ERROR)
    """
    def decorator(method):
        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            log_func = getattr(logger, log_level.lower())
            log_func(f"[{self.__class__.__name__}] Executing {method.__name__}")
            
            result = await method(self, *args, **kwargs)
            
            log_func(f"[{self.__class__.__name__}] Completed {method.__name__}")
            return result
        return wrapper
    return decorator
