"""
THEA IA Core - Sistema central de orquestación
Exporta todos los componentes core del ecosistema.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

from .orchestrator import CoreOrchestrator, OrchestratorResponse, AgentRegistry
from .conversation_manager import (
    CoreConversationManager,
    ConversationContext,
    ConversationTurn
)
from .intent_parser import CoreIntentParser, IntentMatch
from .nlp_engine import CoreNLPEngine, NLPResult
from .response_formatter import CoreResponseFormatter


__all__ = [
    # Orchestrator
    "CoreOrchestrator",
    "OrchestratorResponse",
    "AgentRegistry",
    
    # Conversation Manager
    "CoreConversationManager",
    "ConversationContext",
    "ConversationTurn",
    
    # Intent Parser
    "CoreIntentParser",
    "IntentMatch",
    
    # NLP Engine
    "CoreNLPEngine",
    "NLPResult",
    
    # Response Formatter
    "CoreResponseFormatter",
]


__version__ = "1.0.0"
__author__ = "Álvaro Fernández Mota"
