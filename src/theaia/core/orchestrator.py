"""
Core Orchestrator - Coordinador maestro del ecosistema THEA IA
Orquesta todos los agentes y gestiona el flujo completo de conversación.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass
import logging
from datetime import datetime

from .intent_parser import CoreIntentParser, IntentMatch
from .nlp_engine import CoreNLPEngine, NLPResult
from .conversation_manager import CoreConversationManager, ConversationContext
from .response_formatter import CoreResponseFormatter


logger = logging.getLogger(__name__)


@dataclass
class AgentRegistry:
    """Registro de agentes disponibles."""
    name: str
    agent_class: Type
    intents: List[str]
    description: str
    priority: int = 0


@dataclass
class OrchestratorResponse:
    """Respuesta del orchestrator."""
    message: str
    conversation_id: str
    state: str
    active_agent: Optional[str]
    intent: str
    confidence: float
    context: Dict[str, Any]
    metadata: Dict[str, Any]


class CoreOrchestrator:
    """
    Orchestrator maestro que coordina todo el ecosistema THEA IA.
    
    Responsabilidades:
    - Detectar intenciones con NLP centralizado
    - Delegar a agentes especializados
    - Gestionar contexto conversacional multi-turno
    - Coordinar respuestas formateadas
    - Manejar errores y fallbacks
    - Gestionar registro de agentes
    """
    
    def __init__(
        self,
        language: str = "es",
        session_timeout_minutes: int = 30
    ):
        """
        Inicializa el orchestrator.
        
        Args:
            language: Idioma por defecto
            session_timeout_minutes: Timeout de sesiones
        """
        self.language = language
        
        # Componentes core
        self.intent_parser = CoreIntentParser()
        self.nlp_engine = CoreNLPEngine(default_language=language)
        self.conversation_manager = CoreConversationManager(
            session_timeout_minutes=session_timeout_minutes
        )
        self.response_formatter = CoreResponseFormatter(language=language)
        
        # Registro de agentes
        self._agent_registry: Dict[str, AgentRegistry] = {}
        self._intent_to_agent: Dict[str, str] = {}
        
        # Stats y monitoring
        self._stats = {
            "total_messages": 0,
            "successful_delegations": 0,
            "failed_delegations": 0,
            "fallbacks": 0,
        }
        
        logger.info("CoreOrchestrator initialized")
    
    
    def register_agent(
        self,
        name: str,
        agent_class: Type,
        intents: List[str],
        description: str,
        priority: int = 0
    ) -> None:
        """
        Registra un agente en el ecosistema.
        
        Args:
            name: Nombre del agente
            agent_class: Clase del agente
            intents: Lista de intents que maneja
            description: Descripción del agente
            priority: Prioridad (mayor = más prioritario)
        """
        registry = AgentRegistry(
            name=name,
            agent_class=agent_class,
            intents=intents,
            description=description,
            priority=priority
        )
        
        self._agent_registry[name] = registry
        
        # Mapear intents a agente
        for intent in intents:
            self._intent_to_agent[intent] = name
        
        logger.info(f"Agent registered: {name} (intents: {intents})")
    
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> OrchestratorResponse:
        """
        Procesa un mensaje del usuario - Punto de entrada principal.
        
        Args:
            user_id: ID del usuario
            message: Mensaje del usuario
            metadata: Metadata adicional (plataforma, etc.)
            
        Returns:
            OrchestratorResponse con la respuesta completa
        """
        self._stats["total_messages"] += 1
        
        try:
            # 1. Obtener o crear conversación
            conversation = await self.conversation_manager.get_or_create_conversation(
                user_id=user_id
            )
            
            # 2. Procesar con NLP
            nlp_result = await self.nlp_engine.process_message(
                message=message,
                context=conversation.data
            )
            
            # 3. Decidir flujo según estado de conversación
            if conversation.active_agent:
                # Continuar con agente activo
                response = await self._continue_with_active_agent(
                    conversation=conversation,
                    message=message,
                    nlp_result=nlp_result
                )
            else:
                # Nueva delegación
                response = await self._delegate_to_agent(
                    conversation=conversation,
                    message=message,
                    nlp_result=nlp_result
                )
            
            # 4. Añadir turno al historial
            await self.conversation_manager.add_turn(
                conversation_id=conversation.conversation_id,
                user_message=message,
                bot_response=response.message,
                intent=nlp_result.intent,
                entities=nlp_result.entities
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return await self._handle_error(user_id, str(e), metadata)
    
    
    async def _delegate_to_agent(
        self,
        conversation: ConversationContext,
        message: str,
        nlp_result: NLPResult
    ) -> OrchestratorResponse:
        """
        Delega el mensaje a un agente especializado.
        
        Args:
            conversation: Contexto de conversación
            message: Mensaje del usuario
            nlp_result: Resultado del NLP
            
        Returns:
            OrchestratorResponse
        """
        intent = nlp_result.intent
        
        # Buscar agente para el intent
        agent_name = self._intent_to_agent.get(intent)
        
        if not agent_name:
            # Fallback
            logger.warning(f"No agent found for intent: {intent}")
            return await self._handle_fallback(conversation, message, nlp_result)
        
        # Obtener agente del registry
        agent_registry = self._agent_registry.get(agent_name)
        if not agent_registry:
            logger.error(f"Agent {agent_name} not in registry")
            return await self._handle_fallback(conversation, message, nlp_result)
        
        try:
            # Instanciar agente
            agent_instance = agent_registry.agent_class(
                user_id=conversation.user_id
            )
            
            # Delegar mensaje
            agent_response = await agent_instance.process_message(
                message=message,
                context=conversation.data
            )
            
            # Actualizar conversación
            await self.conversation_manager.set_active_agent(
                conversation_id=conversation.conversation_id,
                agent_name=agent_name
            )
            
            await self.conversation_manager.update_context(
                conversation_id=conversation.conversation_id,
                updates=agent_response.get("context", {})
            )
            
            self._stats["successful_delegations"] += 1
            
            return OrchestratorResponse(
                message=agent_response.get("message", ""),
                conversation_id=conversation.conversation_id,
                state=agent_response.get("state", "active"),
                active_agent=agent_name,
                intent=intent,
                confidence=nlp_result.confidence,
                context=conversation.data,
                metadata={
                    "agent": agent_name,
                    "processing_time_ms": nlp_result.processing_time_ms
                }
            )
            
        except Exception as e:
            logger.error(f"Error delegating to agent {agent_name}: {e}", exc_info=True)
            self._stats["failed_delegations"] += 1
            return await self._handle_fallback(conversation, message, nlp_result)
    
    
    async def _continue_with_active_agent(
        self,
        conversation: ConversationContext,
        message: str,
        nlp_result: NLPResult
    ) -> OrchestratorResponse:
        """
        Continúa la conversación con el agente activo.
        
        Args:
            conversation: Contexto de conversación
            message: Mensaje del usuario
            nlp_result: Resultado del NLP
            
        Returns:
            OrchestratorResponse
        """
        agent_name = conversation.active_agent
        agent_registry = self._agent_registry.get(agent_name)
        
        if not agent_registry:
            logger.error(f"Active agent {agent_name} not found in registry")
            return await self._handle_fallback(conversation, message, nlp_result)
        
        try:
            # Instanciar agente
            agent_instance = agent_registry.agent_class(
                user_id=conversation.user_id
            )
            
            # Continuar conversación
            agent_response = await agent_instance.process_message(
                message=message,
                context=conversation.data
            )
            
            # Actualizar contexto
            await self.conversation_manager.update_context(
                conversation_id=conversation.conversation_id,
                updates=agent_response.get("context", {})
            )
            
            # Verificar si el agente terminó
            if agent_response.get("state") in ["completed", "cancelled"]:
                # Liberar agente
                await self.conversation_manager.set_active_agent(
                    conversation_id=conversation.conversation_id,
                    agent_name=None
                )
            
            return OrchestratorResponse(
                message=agent_response.get("message", ""),
                conversation_id=conversation.conversation_id,
                state=agent_response.get("state", "active"),
                active_agent=agent_name if agent_response.get("state") not in ["completed", "cancelled"] else None,
                intent=nlp_result.intent,
                confidence=nlp_result.confidence,
                context=conversation.data,
                metadata={
                    "agent": agent_name,
                    "processing_time_ms": nlp_result.processing_time_ms
                }
            )
            
        except Exception as e:
            logger.error(f"Error continuing with agent {agent_name}: {e}", exc_info=True)
            return await self._handle_fallback(conversation, message, nlp_result)
    
    
    async def _handle_fallback(
        self,
        conversation: ConversationContext,
        message: str,
        nlp_result: NLPResult
    ) -> OrchestratorResponse:
        """
        Maneja casos donde no se puede procesar el mensaje.
        
        Args:
            conversation: Contexto de conversación
            message: Mensaje del usuario
            nlp_result: Resultado del NLP
            
        Returns:
            OrchestratorResponse con mensaje de fallback
        """
        self._stats["fallbacks"] += 1
        
        fallback_message = self.response_formatter.format_info(
            "No he entendido tu solicitud. ¿Podrías reformularla?",
            items=[
                "Crea eventos de agenda",
                "Guarda notas",
                "Configura recordatorios",
                "Busca información"
            ]
        )
        
        return OrchestratorResponse(
            message=fallback_message,
            conversation_id=conversation.conversation_id,
            state="fallback",
            active_agent=None,
            intent="unknown",
            confidence=0.0,
            context=conversation.data,
            metadata={"fallback": True}
        )
    
    
    async def _handle_error(
        self,
        user_id: str,
        error_message: str,
        metadata: Optional[Dict]
    ) -> OrchestratorResponse:
        """
        Maneja errores globales.
        
        Args:
            user_id: ID del usuario
            error_message: Mensaje de error
            metadata: Metadata adicional
            
        Returns:
            OrchestratorResponse con mensaje de error
        """
        error_response = self.response_formatter.format_error(
            error_message=error_message,
            error_type="general"
        )
        
        return OrchestratorResponse(
            message=error_response,
            conversation_id="error",
            state="error",
            active_agent=None,
            intent="error",
            confidence=0.0,
            context={},
            metadata={"error": error_message}
        )
    
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """
        Obtiene lista de agentes disponibles.
        
        Returns:
            Lista de agentes con info
        """
        return [
            {
                "name": registry.name,
                "description": registry.description,
                "intents": registry.intents,
                "priority": registry.priority
            }
            for registry in sorted(
                self._agent_registry.values(),
                key=lambda x: x.priority,
                reverse=True
            )
        ]
    
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del orchestrator.
        
        Returns:
            Dict con stats
        """
        return {
            **self._stats,
            "registered_agents": len(self._agent_registry),
            "active_conversations": len(self.conversation_manager._conversations)
        }
