"""
AgendaAgent Orchestrator Adapter

Adapta AgendaAgent para funcionar con CoreOrchestrator.
Maneja la inicialización de sesión de DB y conversión de formatos.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

from typing import Dict, Any
import logging

from .handler import AgendaAgent
from ...database.session import get_db


logger = logging.getLogger(__name__)


class AgendaAgentAdapter:
    """
    Adapter para AgendaAgent compatible con CoreOrchestrator.
    
    Responsabilidades:
    - Gestión de sesiones de DB
    - Conversión de formatos entrada/salida
    - Compatibilidad con interface de CoreOrchestrator
    """
    
    def __init__(self, user_id: str):
        """
        Inicializa el adapter.
        
        Args:
            user_id: ID del usuario
        """
        self.user_id = user_id
        self._agenda_agent = None
        
        logger.info(f"AgendaAgentAdapter initialized for user {user_id}")
    
    
    async def _get_agenda_agent(self) -> AgendaAgent:
        """
        Obtiene o crea instancia de AgendaAgent con sesión de DB.
        
        Returns:
            AgendaAgent instance
        """
        if self._agenda_agent is None:
            # Obtener sesión async de DB
            async for session in get_db():
                self._agenda_agent = AgendaAgent(
                    session=session,
                    timezone="UTC",
                    language="es"
                )
                break
        
        return self._agenda_agent
    
    
    async def process_message(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje (compatible con CoreOrchestrator).
        
        Args:
            message: Mensaje del usuario
            context: Contexto de conversación
            
        Returns:
            Dict con formato CoreOrchestrator:
            {
                "message": str,
                "state": str,
                "context": Dict
            }
        """
        try:
            # Asegurar que context tiene campos requeridos
            if "user_id" not in context:
                # Convertir user_id de string a int si es necesario
                try:
                    context["user_id"] = int(self.user_id)
                except ValueError:
                    context["user_id"] = 1  # Default
            
            if "tenant_id" not in context:
                context["tenant_id"] = "default"
            
            # Obtener AgendaAgent
            agent = await self._get_agenda_agent()
            
            # Procesar mensaje
            response = await agent.handle_message(message, context)
            
            # Determinar estado
            state = self._determine_state(context)
            
            return {
                "message": response,
                "state": state,
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Error in AgendaAgentAdapter: {e}", exc_info=True)
            return {
                "message": f"Error procesando solicitud de agenda: {str(e)}",
                "state": "error",
                "context": context
            }
    
    
    def _determine_state(self, context: Dict[str, Any]) -> str:
        """
        Determina el estado de la conversación.
        
        Args:
            context: Contexto actual
            
        Returns:
            Estado: "active", "completed", "cancelled"
        """
        if "conversation_id" in context:
            return "active"
        
        # Por ahora, asumimos completado si no hay conversación activa
        return "completed"
    
    
    async def cleanup(self):
        """Limpia recursos del adapter."""
        if self._agenda_agent:
            await self._agenda_agent.cleanup()
            self._agenda_agent = None
        
        logger.info(f"AgendaAgentAdapter cleanup completed for user {self.user_id}")
