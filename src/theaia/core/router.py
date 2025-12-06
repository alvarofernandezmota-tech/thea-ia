"""
TheaRouter v2.0 - Powered by CoreOrchestrator
Orquestador multiagente central de Thea IA con arquitectura escalable.

Mejoras v2.0:
- Integración con CoreOrchestrator para gestión centralizada
- Registro dinámico de agentes
- Conversación multi-turno robusta
- NLP centralizado
- Response formatting consistente
- 100% compatible con tests legacy (CoreRouter alias)

Autor: Álvaro Fernández Mota
Fecha: 6 Diciembre 2025
Versión: 2.0 (TheaRouter con CoreOrchestrator)
Arquitectura: Multi-agente escalable
"""

from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
import asyncio
import logging

logger = logging.getLogger(__name__)

try:
    from src.theaia.core.orchestrator import CoreOrchestrator
except ImportError:
    logger.warning("CoreOrchestrator not available - running in stub mode")
    CoreOrchestrator = None


# ==================== DATACLASSES H03 COMPATIBLES ====================


@dataclass
class Message:
    """Mensaje entrante del usuario (H03 compatible)."""
    text: str
    user_id: str
    tenant_id: str = "default"
    session_id: str = ""
    timestamp: datetime = None
    metadata: Optional[Dict] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        if not self.session_id:
            self.session_id = self.user_id


@dataclass
class ProcessedMessage:
    """Resultado del procesamiento completo (H03 compatible)."""
    intent: str
    entities: Dict
    confidence: float
    agent_target: str
    processing_time_ms: int = 0
    original_text: str = ""
    fsm_state: str = "idle"
    status: str = "ok"


# ==================== HELPER FUNCTIONS ====================


def preprocess_text(text: str) -> str:
    """
    Limpia y normaliza texto de entrada.
    
    Args:
        text: Texto crudo
        
    Returns:
        Texto limpio y normalizado
    """
    if not text or not isinstance(text, str):
        return ""
    
    text = text.lower().strip()
    text = " ".join(text.split())
    
    return text


# ==================== THEA ROUTER V2 ====================


class TheaRouter:
    """
    Router v2.0 con CoreOrchestrator integrado.
    
    Características principales:
    - Orquestación centralizada con CoreOrchestrator
    - Registro dinámico de agentes
    - Conversación multi-turno robusta
    - NLP avanzado (spaCy, intent detection)
    - Response formatting consistente
    - Compatible con tests legacy (via CoreRouter alias)
    
    Arquitectura:
    User Message → Preprocess → CoreOrchestrator → Agent Selection → Response
    
    Agentes soportados:
    - AgendaAgent: Gestión de eventos y calendario
    - NoteAgent: Gestión de notas (próximo)
    - QueryAgent: Consultas generales (próximo)
    - HelpAgent: Ayuda y documentación (próximo)
    """
    
    def __init__(self):
        """Inicializa router con orchestrator."""
        
        self.message_count = 0
        self.agents = {}
        
        # Core orchestrator (si está disponible)
        self.orchestrator = None
        if CoreOrchestrator:
            self.orchestrator = CoreOrchestrator(
                language="es",
                session_timeout_minutes=30
            )
            self._register_agents()
            logger.info("[TheaRouter v2.0] Initialized with CoreOrchestrator")
        else:
            logger.warning("[TheaRouter v2.0] CoreOrchestrator not available - running in compatibility mode")
    
    
    def _register_agents(self):
        """Registra todos los agentes disponibles en el orchestrator."""
        
        if not self.orchestrator:
            return
        
        # AgendaAgent - Completamente implementado con adapter
        try:
            from src.theaia.agents.agenda_agent.handler import AgendaAgentHandler
            
            agenda_handler = AgendaAgentHandler()
            self.orchestrator.register_agent(
                name="agenda_agent",
                agent_instance=agenda_handler,
                intents=[
                    "create_event",
                    "query_events",
                    "update_event",
                    "delete_event",
                    "mark_complete"
                ],
                description="Gestión completa de eventos de calendario",
                priority=10
            )
            
            self.agents["agenda_agent"] = agenda_handler
            logger.info("[TheaRouter v2.0] ✅ AgendaAgent registered successfully")
            
        except ImportError as e:
            logger.warning(f"[TheaRouter v2.0] ⚠️  AgendaAgent not available: {e}")
        except Exception as e:
            logger.error(f"[TheaRouter v2.0] ❌ Error registering AgendaAgent: {e}")
    
    
    def handle(self, user_id: str, message: str) -> Dict:
        """
        Pipeline principal de procesamiento (SYNC version).
        
        Compatible con código legacy - devuelve mismo formato.
        
        Args:
            user_id: ID del usuario
            message: Mensaje de texto
            
        Returns:
            Dict con status, message, state, context, etc.
        """
        self.message_count += 1
        
        try:
            # Preprocess
            cleaned_message = preprocess_text(message)
            
            if not cleaned_message:
                return {
                    "status": "error",
                    "message": "Empty message after preprocessing",
                    "state": "error",
                    "intent": "unknown",
                    "confidence": 0.0,
                    "agent": "fallback",
                    "original_text": message,
                    "cleaned_text": cleaned_message,
                }
            
            # Procesar con orchestrator si está disponible
            if self.orchestrator:
                loop = self._get_event_loop()
                orchestrator_response = loop.run_until_complete(
                    self.orchestrator.process_message(
                        user_id=user_id,
                        message=cleaned_message,
                        metadata={"original_text": message}
                    )
                )
                
                return {
                    "status": "ok" if orchestrator_response.state != "error" else "error",
                    "message": orchestrator_response.message,
                    "state": orchestrator_response.state,
                    "context": orchestrator_response.context,
                    "intent": orchestrator_response.intent,
                    "confidence": orchestrator_response.confidence,
                    "agent": orchestrator_response.active_agent or "fallback",
                    "entities": orchestrator_response.context.get("entities", {}),
                    "processing_time_ms": orchestrator_response.metadata.get("processing_time_ms", 0),
                    "original_text": message,
                    "cleaned_text": cleaned_message,
                }
            else:
                # Fallback: respuesta simple si orchestrator no está disponible
                return {
                    "status": "ok",
                    "message": f"Echo: {cleaned_message}",
                    "state": "idle",
                    "intent": "unknown",
                    "confidence": 0.0,
                    "agent": "fallback",
                    "original_text": message,
                    "cleaned_text": cleaned_message,
                }
                
        except Exception as e:
            logger.error(f"Error in handle(): {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "state": "error",
                "intent": "unknown",
                "confidence": 0.0,
                "agent": "fallback",
                "original_text": message,
            }
    
    
    async def process(self, message: Message) -> ProcessedMessage:
        """
        Método ASYNC compatible con tests H03.
        
        Pipeline:
        1. Validate message
        2. Preprocess text
        3. Route through orchestrator
        4. Format response
        
        Args:
            message: Message dataclass
            
        Returns:
            ProcessedMessage dataclass
        """
        self.message_count += 1
        
        try:
            # Validate
            if not message or not message.text:
                return ProcessedMessage(
                    intent="unknown",
                    entities={},
                    confidence=0.0,
                    agent_target="fallback",
                    processing_time_ms=0,
                    original_text=message.text if message else "",
                    fsm_state="error",
                    status="error"
                )
            
            # Preprocess
            cleaned_text = preprocess_text(message.text)
            
            if not cleaned_text:
                return ProcessedMessage(
                    intent="unknown",
                    entities={},
                    confidence=0.0,
                    agent_target="fallback",
                    processing_time_ms=0,
                    original_text=message.text,
                    fsm_state="error",
                    status="error"
                )
            
            # Process with orchestrator
            if self.orchestrator:
                orchestrator_response = await self.orchestrator.process_message(
                    user_id=message.user_id,
                    message=cleaned_text,
                    metadata={
                        "tenant_id": message.tenant_id,
                        "session_id": message.session_id
                    }
                )
                
                return ProcessedMessage(
                    intent=orchestrator_response.intent,
                    entities=orchestrator_response.context.get("entities", {}),
                    confidence=orchestrator_response.confidence,
                    agent_target=orchestrator_response.active_agent or "fallback",
                    processing_time_ms=orchestrator_response.metadata.get("processing_time_ms", 0),
                    original_text=message.text,
                    fsm_state=orchestrator_response.state,
                    status="ok" if orchestrator_response.state != "error" else "error"
                )
            else:
                # Fallback
                return ProcessedMessage(
                    intent="unknown",
                    entities={},
                    confidence=0.0,
                    agent_target="fallback",
                    processing_time_ms=0,
                    original_text=message.text,
                    fsm_state="idle",
                    status="ok"
                )
                
        except Exception as e:
            logger.error(f"Error in process(): {e}", exc_info=True)
            return ProcessedMessage(
                intent="unknown",
                entities={},
                confidence=0.0,
                agent_target="fallback",
                processing_time_ms=0,
                original_text=message.text,
                fsm_state="error",
                status="error"
            )
    
    
    def reset_session(self, user_id: str = None):
        """
        Resetea la sesión de un usuario.
        
        Args:
            user_id: ID del usuario (opcional)
        """
        if self.orchestrator:
            loop = self._get_event_loop()
            loop.run_until_complete(
                self.orchestrator.reset_session(user_id) if user_id else 
                self.orchestrator.reset_all_sessions()
            )
        
        logger.info(f"[TheaRouter v2.0] Session reset for user {user_id or 'all'}")
    
    
    def get_stats(self) -> Dict:
        """
        Obtiene estadísticas del router.
        
        Returns:
            Dict con estadísticas
        """
        stats = {
            "message_count": self.message_count,
            "version": "2.0",
            "router_type": "TheaRouter",
            "agents_available": list(self.agents.keys()) if self.agents else [],
            "orchestrator_available": bool(self.orchestrator),
        }
        
        if self.orchestrator:
            orchestrator_stats = self.orchestrator.get_stats()
            stats.update(orchestrator_stats)
        
        return stats
    
    
    def get_available_agents(self) -> List[str]:
        """
        Lista agentes disponibles.
        
        Returns:
            Lista de nombres de agentes registrados
        """
        agents = list(self.agents.keys())
        
        if self.orchestrator:
            orchestrator_agents = self.orchestrator.get_available_agents()
            agents.extend(orchestrator_agents)
        
        return list(set(agents))
    
    
    @staticmethod
    def _get_event_loop() -> asyncio.AbstractEventLoop:
        """
        Obtiene o crea event loop de forma segura.
        
        Compatible con Windows + Linux.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            if asyncio.sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop


# ==================== ALIAS DE COMPATIBILIDAD TESTING ====================
# Exporta CoreRouter para que todos los tests legacy importen correctamente.
# CoreRouter = TheaRouter  (uncomment cuando H03 tests estén listos)

# Por ahora, ambas clases existen:
CoreRouter = TheaRouter


__all__ = [
    "TheaRouter",
    "CoreRouter",
    "Message",
    "ProcessedMessage",
    "preprocess_text",
]