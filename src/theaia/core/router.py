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
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timezone

from .orchestrator import CoreOrchestrator


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
    processing_time_ms: int
    original_text: str
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
    if not text:
        return ""
    
    text = text.lower().strip()
    text = " ".join(text.split())
    
    return text


# ==================== THEA ROUTER V2 ====================

class TheaRouter:
    """
    Router v2.0 con CoreOrchestrator integrado.
    
    Características:
    - Orquestación centralizada con CoreOrchestrator
    - Registro dinámico de agentes
    - Conversación multi-turno
    - NLP avanzado
    - Compatible con tests legacy
    """
    
    def __init__(self):
        """Inicializa router con orchestrator."""
        
        # Core orchestrator
        self.orchestrator = CoreOrchestrator(
            language="es",
            session_timeout_minutes=30
        )
        
        # Registrar agentes
        self._register_agents()
        
        print("[TheaRouter v2.0] Initialized with CoreOrchestrator")
        print(f"[TheaRouter v2.0] Registered agents: {len(self.orchestrator.get_available_agents())}")
    
    
    def _register_agents(self):
        """Registra todos los agentes disponibles en el orchestrator."""
        
        # AgendaAgent - Completamente implementado con adapter
        try:
            from src.theaia.agents.agenda_agent.orchestrator_adapter import AgendaAgentAdapter
            
            self.orchestrator.register_agent(
                name="agenda_agent",
                agent_class=AgendaAgentAdapter,
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
            
            print("[TheaRouter v2.0] ✅ AgendaAgent registered successfully")
            
        except ImportError as e:
            print(f"[TheaRouter v2.0] ⚠️  AgendaAgent not available: {e}")
        
        # TODO: Registrar más agentes cuando estén listos
        # Ejemplo estructura para futuros agentes:
        #
        # try:
        #     from src.theaia.agents.note_agent.adapter import NoteAgentAdapter
        #     
        #     self.orchestrator.register_agent(
        #         name="note_agent",
        #         agent_class=NoteAgentAdapter,
        #         intents=["create_note", "query_notes", "update_note", "delete_note"],
        #         description="Gestión de notas y apuntes",
        #         priority=8
        #     )
        #     
        #     print("[TheaRouter v2.0] ✅ NoteAgent registered")
        # except ImportError:
        #     print("[TheaRouter v2.0] ⚠️  NoteAgent not available")
    
    
    def handle(self, user_id: str, message: str) -> Dict:
        """
        Pipeline principal de procesamiento.
        
        Compatible con código legacy - devuelve mismo formato.
        
        Args:
            user_id: ID del usuario
            message: Mensaje de texto
            
        Returns:
            Dict con status, message, state, context, etc.
        """
        # Preprocess
        cleaned_message = preprocess_text(message)
        
        # Procesar con orchestrator (sync wrapper)
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        orchestrator_response = loop.run_until_complete(
            self.orchestrator.process_message(
                user_id=user_id,
                message=cleaned_message,
                metadata={"original_text": message}
            )
        )
        
        # Convertir a formato legacy para compatibilidad
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
    
    
    async def process(self, message: Message) -> ProcessedMessage:
        """
        Método async compatible con tests H03.
        
        Args:
            message: Message dataclass
            
        Returns:
            ProcessedMessage dataclass
        """
        # Procesar con orchestrator
        orchestrator_response = await self.orchestrator.process_message(
            user_id=message.user_id,
            message=message.text,
            metadata={"tenant_id": message.tenant_id}
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
    
    
    def reset_session(self, user_id: str):
        """
        Resetea la sesión de un usuario.
        
        Args:
            user_id: ID del usuario
        """
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Buscar conversación activa y limpiarla
        for conv_id, conv in self.orchestrator.conversation_manager._conversations.items():
            if conv.user_id == user_id:
                loop.run_until_complete(
                    self.orchestrator.conversation_manager.clear_conversation(conv_id)
                )
                break
        
        print(f"[TheaRouter v2.0] Session reset for user {user_id}")
    
    
    def get_stats(self) -> Dict:
        """
        Obtiene estadísticas del router.
        
        Returns:
            Dict con stats del orchestrator
        """
        stats = self.orchestrator.get_stats()
        stats["router_version"] = "2.0"
        return stats
    
    
    def get_available_agents(self) -> list:
        """
        Lista agentes disponibles.
        
        Returns:
            Lista de agentes registrados
        """
        return self.orchestrator.get_available_agents()


# ==================== ALIAS DE COMPATIBILIDAD TESTING ====================
# Exporta CoreRouter para que todos los tests legacy importen correctamente.
CoreRouter = TheaRouter
