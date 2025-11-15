# Archivo: src/theaia/agents/base_agent.py

"""
Base agent class for THEA-IA agents.
Provides common interface and functionality for all agents.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class AgentConfig:
    """
    Configuration for an agent instance.
    
    Attributes:
        name: Agent name
        enabled: Whether the agent is enabled
        max_retries: Maximum retry attempts for failed operations
        timeout: Operation timeout in seconds
        log_level: Logging level for this agent
    """
    name: str
    enabled: bool = True
    max_retries: int = 3
    timeout: int = 30
    log_level: str = "INFO"
    custom_config: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Abstract base class for all THEA-IA agents.
    
    All agents must inherit from this class and implement the required methods.
    Provides common functionality like logging, error handling, and lifecycle management.
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize the base agent.
        
        Args:
            config: Agent configuration (optional)
        """
        self.config = config or AgentConfig(name=self.__class__.__name__)
        self.logger = self._setup_logging()
        self._is_initialized = False
        self.logger.info(f"{self.config.name} initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """
        Setup logging for the agent.
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(self.config.name)
        logger.setLevel(getattr(logging, self.config.log_level))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'[%(asctime)s] [{self.config.name}] %(levelname)s: %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    @abstractmethod
    def get_supported_intents(self) -> List[str]:
        """
        Get list of intents this agent can handle.
        
        Returns:
            List of supported intent strings
        """
        raise NotImplementedError("Agents must implement get_supported_intents()")
    
    def can_handle(self, intent: str) -> bool:
        """
        Check if the agent can handle the given intent.
        
        Args:
            intent: Intent string to check
            
        Returns:
            True if agent can handle the intent, False otherwise
        """
        if not self.config.enabled:
            self.logger.warning(f"Agent {self.config.name} is disabled")
            return False
        
        return intent.lower() in [i.lower() for i in self.get_supported_intents()]
    
    def handle(self, user_id: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user message and return response.
        
        This is a wrapper that provides error handling and logging.
        Subclasses should override _process_message() instead.
        
        Args:
            user_id: User identifier
            message: User message text
            context: Optional conversation context
            
        Returns:
            Response dictionary with status, message, and context
        """
        context = context or {}
        
        self.logger.info(f"Handling message from user {user_id}: {message[:50]}...")
        
        try:
            # Call the agent-specific implementation
            response = self._process_message(user_id, message, context)
            
            self.logger.info(f"Successfully handled message from user {user_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error handling message: {e}", exc_info=True)
            return self._handle_error(user_id, message, context, e)
    
    def _process_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the user message (to be overridden by subclasses).
        
        Args:
            user_id: User identifier
            message: User message text
            context: Conversation context
            
        Returns:
            Response dictionary
        """
        # Default implementation
        context["unrecognized_message"] = message
        return {
            "status": "ok",
            "message": f"El agente {self.config.name} recibió el mensaje pero no pudo procesarlo completamente.",
            "context": context,
        }
    
    def _handle_error(self, user_id: str, message: str, context: Dict[str, Any], error: Exception) -> Dict[str, Any]:
        """
        Handle errors that occur during message processing.
        
        Args:
            user_id: User identifier
            message: Original message
            context: Conversation context
            error: The exception that occurred
            
        Returns:
            Error response dictionary
        """
        context["error"] = str(error)
        context["error_type"] = type(error).__name__
        
        return {
            "status": "error",
            "message": "Lo siento, ocurrió un error al procesar tu mensaje. Por favor, intenta de nuevo.",
            "context": context,
        }
    
    def initialize(self) -> bool:
        """
        Initialize the agent (called before first use).
        
        Subclasses can override this to perform setup tasks.
        
        Returns:
            True if initialization successful, False otherwise
        """
        if self._is_initialized:
            self.logger.warning(f"Agent {self.config.name} already initialized")
            return True
        
        try:
            self.logger.info(f"Initializing agent {self.config.name}")
            self._is_initialized = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {e}", exc_info=True)
            return False
    
    def cleanup(self) -> None:
        """
        Cleanup agent resources (called when shutting down).
        
        Subclasses can override this to perform cleanup tasks.
        """
        self.logger.info(f"Cleaning up agent {self.config.name}")
        self._is_initialized = False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the agent.
        
        Returns:
            Status dictionary with agent information
        """
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "initialized": self._is_initialized,
            "supported_intents": self.get_supported_intents(),
        }
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"<{self.__class__.__name__}(name={self.config.name}, enabled={self.config.enabled})>"
