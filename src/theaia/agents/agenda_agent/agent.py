"""
AgendaAgent - Agente especializado en gestión de eventos y calendario

Responsabilidades:
- Procesar intents relacionados con agenda (create, query, update, delete)
- Acceder a EventRepository para operaciones de BD
- Extraer entidades del mensaje (fechas, participantes, etc)
- Generar respuestas formateadas y contextuales

Autor: Álvaro Fernández Mota
Fecha: 09 Dic 2025
Arquitectura: THEA IA - H05 BLOQUE 1.5
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Respuesta estándar del agente"""
    message: str
    state: str  # "active", "completed", "cancelled", "error"
    context: Dict[str, Any]
    entities: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AgendaAgent:
    """
    Agente especializado en gestión de eventos de calendario.
    
    Intents soportados:
    - create_event: crear nuevo evento
    - query_events: listar/buscar eventos
    - update_event: modificar evento existente
    - delete_event: eliminar evento
    
    Flujo:
    1. Recibe message + context del Orchestrator
    2. Extrae intent (ya detectado por NLP)
    3. Delega a handler específico
    4. Retorna AgentResponse
    """
    
    def __init__(self, user_id: str):
        """
        Inicializa el AgendaAgent.
        
        Args:
            user_id: ID del usuario propietario del agente
        """
        self.user_id = user_id
        self.logger = logging.getLogger(f"{__name__}.{user_id}")
        
        # TODO: Inicializar EventRepository cuando esté implementado
        # self.event_repository = EventRepository(user_id=user_id)
        
        self.logger.info(f"AgendaAgent initialized for user {user_id}")
    
    
    async def process_message(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Procesa un mensaje recibido del Orchestrator.
        
        Args:
            message: Mensaje del usuario
            context: Contexto de conversación (incluye intent detectado por NLP)
            
        Returns:
            AgentResponse con resultado procesado
            
        Nota:
            El contexto contiene:
            - intent: str (detectado por NLP)
            - confidence: float (score del NLP)
            - entities: Dict (extraídas por NLP)
            - last_messages: List (historial conversacional)
        """
        try:
            context = context or {}
            intent = context.get("intent", "unknown")
            
            self.logger.debug(f"Processing message: {message[:50]}... | Intent: {intent}")
            
            # Delegar a handler específico según el intent
            if intent == "create_event":
                response = await self._handle_create_event(message, context)
            elif intent == "query_events":
                response = await self._handle_query_events(message, context)
            elif intent == "update_event":
                response = await self._handle_update_event(message, context)
            elif intent == "delete_event":
                response = await self._handle_delete_event(message, context)
            else:
                response = await self._handle_unknown_intent(message, context)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}", exc_info=True)
            return AgentResponse(
                message=f"❌ Error procesando tu solicitud: {str(e)}",
                state="error",
                context=context or {},
                metadata={"error": str(e)}
            )
    
    
    async def _handle_create_event(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Handler para crear nuevo evento.
        
        Ejemplo:
            "Quiero agendar una reunión mañana a las 3pm"
            
        TODO:
        - Extraer title, date, time, participants del mensaje
        - Validar datos
        - Crear evento en BD
        - Retornar confirmación
        """
        self.logger.info(f"Creating event for user {self.user_id}")
        
        # Placeholder response (será implementado en A.5)
        return AgentResponse(
            message="✅ Evento creado exitosamente",
            state="completed",
            context=context,
            entities=context.get("entities", {}),
            metadata={"action": "create_event"}
        )
    
    
    async def _handle_query_events(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Handler para listar/buscar eventos.
        
        Ejemplo:
            "Muéstrame mis eventos de mañana"
            "¿Qué reuniones tengo el lunes?"
            
        TODO:
        - Extraer criterios de búsqueda (fecha, participantes, etc)
        - Consultar BD
        - Formatear resultados
        """
        self.logger.info(f"Querying events for user {self.user_id}")
        
        # Placeholder response
        return AgentResponse(
            message="📅 Tienes los siguientes eventos",
            state="completed",
            context=context,
            entities=context.get("entities", {}),
            metadata={"action": "query_events"}
        )
    
    
    async def _handle_update_event(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Handler para modificar evento existente.
        
        Ejemplo:
            "Cambiar la reunión de las 3 a las 4"
            "Modificar el título de mi evento de mañana"
            
        TODO:
        - Identificar evento a modificar
        - Extraer cambios solicitados
        - Actualizar en BD
        - Retornar confirmación
        """
        self.logger.info(f"Updating event for user {self.user_id}")
        
        # Placeholder response
        return AgentResponse(
            message="✏️ Evento actualizado",
            state="completed",
            context=context,
            entities=context.get("entities", {}),
            metadata={"action": "update_event"}
        )
    
    
    async def _handle_delete_event(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Handler para eliminar evento.
        
        Ejemplo:
            "Cancela mi reunión de mañana"
            "Elimina el evento de las 3pm"
            
        TODO:
        - Identificar evento a eliminar
        - Solicitar confirmación (opcional)
        - Eliminar de BD
        - Retornar confirmación
        """
        self.logger.info(f"Deleting event for user {self.user_id}")
        
        # Placeholder response
        return AgentResponse(
            message="🗑️ Evento eliminado",
            state="completed",
            context=context,
            entities=context.get("entities", {}),
            metadata={"action": "delete_event"}
        )
    
    
    async def _handle_unknown_intent(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> AgentResponse:
        """
        Handler para intents no reconocidos.
        """
        self.logger.warning(f"Unknown intent for user {self.user_id}: {message}")
        
        return AgentResponse(
            message="❓ No he entendido tu solicitud. ¿Puedes reformularla?\n\n"
                    "Puedo ayudarte con:\n"
                    "• Crear eventos\n"
                    "• Listar tus eventos\n"
                    "• Modificar eventos\n"
                    "• Cancelar eventos",
            state="active",
            context=context,
            metadata={"action": "unknown_intent"}
        )
    
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna información del agente"""
        return {
            "name": "AgendaAgent",
            "user_id": self.user_id,
            "intents": ["create_event", "query_events", "update_event", "delete_event"],
            "status": "active",
            "version": "1.0.0"
        }