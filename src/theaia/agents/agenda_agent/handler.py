"""
AgendaAgent Handler - Main Entry Point

Handles user messages and orchestrates the complete agenda management flow.
Integrates all components: parsing, orchestration, conversation management, and formatting.
"""

from typing import Dict, Any, Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from .orchestrator import AgendaOrchestrator
from .conversation_manager import ConversationManager
from .response_formatter import ResponseFormatter
from .services.event_service import EventService
from .tools.event_tools import EventTools
from ...database.repositories.event_repository import EventRepository


logger = logging.getLogger(__name__)


class AgendaAgent:
    """
    Main AgendaAgent handler.
    
    Entry point for all agenda-related user messages.
    Orchestrates the complete flow from message to response.
    """
    
    def __init__(
        self,
        session: AsyncSession,
        timezone: str = "UTC",
        language: str = "es"
    ):
        """
        Initialize AgendaAgent with all required components.
        
        Args:
            session: SQLAlchemy async session
            timezone: User's timezone (default: UTC)
            language: Response language ("es" or "en")
        """
        self.session = session
        self.timezone = timezone
        self.language = language
        
        # Initialize repositories
        self.event_repository = EventRepository(session)
        
        # Initialize services
        self.event_service = EventService(self.event_repository)
        
        # Initialize tools
        self.event_tools = EventTools(session)
        
        # Initialize orchestrator
        self.orchestrator = AgendaOrchestrator(
            event_service=self.event_service,
            event_tools=self.event_tools,
            timezone=timezone
        )
        
        # Initialize conversation manager
        self.conversation_manager = ConversationManager()
        
        # Initialize response formatter
        self.response_formatter = ResponseFormatter(language=language)
        
        # FSM instances (for multi-user support)
        self.fsm_instances: Dict[int, Dict[str, Any]] = {}
        
        logger.info(f"AgendaAgent initialized with timezone={timezone}, language={language}")
    
    async def handle_message(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Main entry point for handling user messages.
        
        Args:
            message: User's natural language message
            context: Context dictionary containing:
                - user_id: int
                - tenant_id: str
                - conversation_id: str (optional, for multi-turn)
                
        Returns:
            Formatted response string
        """
        user_id = context.get("user_id")
        tenant_id = context.get("tenant_id")
        conversation_id = context.get("conversation_id")
        
        if not user_id or not tenant_id:
            logger.error("Missing user_id or tenant_id in context")
            return self.response_formatter.format_error(
                "Error de configuración: falta información de usuario",
                error_type="general"
            )
        
        logger.info(f"Processing message from user {user_id}: {message[:50]}...")
        
        try:
            # Check if this is part of an ongoing conversation
            if conversation_id:
                return await self._handle_conversation_turn(
                    message,
                    conversation_id,
                    context
                )
            
            # New message - process through orchestrator
            result = await self.orchestrator.process_message(message, context)
            
            # Check if we need to start a conversation for missing info
            if not result["success"] and result.get("missing_fields"):
                return await self._start_conversation(result, context)
            
            # Return the response (already formatted by orchestrator/tools)
            return result["response"]
            
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}", exc_info=True)
            return self.response_formatter.format_error(
                f"Error procesando mensaje: {str(e)}",
                error_type="general"
            )
    
    async def _start_conversation(
        self,
        incomplete_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """
        Start a new multi-turn conversation for incomplete request.
        
        Args:
            incomplete_result: Result from orchestrator with missing fields
            context: User context
            
        Returns:
            Prompt for next missing field
        """
        user_id = context["user_id"]
        intent = incomplete_result["intent"]
        partial_entities = incomplete_result.get("partial_entities", {})
        missing_fields = incomplete_result["missing_fields"]
        
        # Start conversation
        conversation_id = self.conversation_manager.start_conversation(
            user_id=user_id,
            intent=intent,
            partial_entities=partial_entities,
            missing_fields=missing_fields
        )
        
        # Store conversation_id in context for next turn
        context["conversation_id"] = conversation_id
        
        # Generate prompt for first missing field
        prompt = self.conversation_manager.generate_prompt(conversation_id)
        
        logger.info(f"Started conversation {conversation_id} for user {user_id}")
        
        return prompt
    
    async def _handle_conversation_turn(
        self,
        message: str,
        conversation_id: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Handle a turn in an ongoing multi-turn conversation.
        
        Args:
            message: User's message (providing missing info)
            conversation_id: Active conversation ID
            context: User context
            
        Returns:
            Response (next prompt or completion message)
        """
        conversation = self.conversation_manager.get_conversation(conversation_id)
        
        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            return self.response_formatter.format_error(
                "Conversación no encontrada. Por favor inicia una nueva solicitud.",
                error_type="not_found"
            )
        
        # Parse the message to extract the missing field value
        intent = conversation["intent"]
        missing_fields = conversation["missing_fields"]
        
        if not missing_fields:
            # Conversation already complete
            self.conversation_manager.end_conversation(conversation_id)
            return "✅ Información completa. Procesando..."
        
        # Assume user is providing the first missing field
        next_field = missing_fields[0]
        
        # Update conversation with new value
        new_entities = {next_field: message}
        self.conversation_manager.update_conversation(
            conversation_id,
            new_entities=new_entities
        )
        
        # Check if conversation is now complete
        if self.conversation_manager.is_conversation_complete(conversation_id):
            # Execute the action with complete information
            return await self._complete_conversation(conversation_id, context)
        
        # Still missing fields - ask for next one
        prompt = self.conversation_manager.generate_prompt(conversation_id)
        return prompt
    
    async def _complete_conversation(
        self,
        conversation_id: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Complete conversation and execute the action.
        
        Args:
            conversation_id: Conversation ID
            context: User context
            
        Returns:
            Result message
        """
        conversation = self.conversation_manager.get_conversation(conversation_id)
        
        if not conversation:
            return self.response_formatter.format_error(
                "Error: Conversación no encontrada",
                error_type="not_found"
            )
        
        # Build complete message from collected entities
        entities = conversation["partial_entities"]
        intent = conversation["intent"]
        
        # Create a synthetic message for orchestrator
        # (In production, you'd reconstruct from entities)
        synthetic_message = self._reconstruct_message(intent, entities)
        
        # Process through orchestrator
        result = await self.orchestrator.process_message(synthetic_message, context)
        
        # End conversation
        self.conversation_manager.end_conversation(conversation_id)
        context.pop("conversation_id", None)
        
        logger.info(f"Completed conversation {conversation_id}")
        
        return result["response"]
    
    def _reconstruct_message(self, intent: str, entities: Dict[str, Any]) -> str:
        """
        Reconstruct a message from intent and entities.
        
        Args:
            intent: Intent type
            entities: Collected entities
            
        Returns:
            Synthetic message string
        """
        # This is a simplified reconstruction
        # In production, you'd have a more sophisticated approach
        
        if intent == "create_event":
            title = entities.get("title", "")
            datetime_str = entities.get("datetime_str", "")
            location = entities.get("location", "")
            
            msg = f"crear evento {title}"
            if datetime_str:
                msg += f" {datetime_str}"
            if location:
                msg += f" en {location}"
            
            return msg
        
        elif intent == "update_event":
            event_id = entities.get("event_id", "")
            return f"modificar evento #{event_id}"
        
        elif intent == "delete_event":
            event_id = entities.get("event_id", "")
            return f"eliminar evento #{event_id}"
        
        else:
            return ""
    
    async def get_user_events(
        self,
        user_id: int,
        tenant_id: str,
        hours: int = 24
    ) -> str:
        """
        Get user's upcoming events (convenience method).
        
        Args:
            user_id: User ID
            tenant_id: Tenant ID
            hours: Hours ahead to look (default: 24)
            
        Returns:
            Formatted events list
        """
        try:
            events = await self.event_service.get_upcoming_events(
                user_id=user_id,
                tenant_id=tenant_id,
                hours=hours
            )
            
            return self.response_formatter.format_event_list(events)
            
        except Exception as e:
            logger.error(f"Error getting events: {str(e)}", exc_info=True)
            return self.response_formatter.format_error(
                f"Error obteniendo eventos: {str(e)}",
                error_type="general"
            )
    
    async def cleanup(self):
        """Cleanup resources (call on shutdown)."""
        # Cleanup old conversations
        self.conversation_manager.cleanup_old_conversations(max_age_minutes=30)
        logger.info("AgendaAgent cleanup completed")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get agent statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "active_conversations": len(self.conversation_manager.conversations),
            "timezone": self.timezone,
            "language": self.language,
        }
