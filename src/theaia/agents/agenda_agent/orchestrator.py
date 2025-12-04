"""
Orchestrator for AgendaAgent


Orchestrates the complete message processing flow.
Coordinates all components: parsing, validation, execution, formatting.
Integrates NLP engine for better intent detection.
"""


from typing import Dict, Optional, Any
from datetime import datetime
import logging


from .intent_parser import AgendaIntentParser
from .datetime_parser import DateTimeParser
from .nlp_engine import SimpleNLPEngine
from .services.event_service import EventService
from .tools.event_tools import EventTools
from .schemas.event_schema import EventCreate, EventUpdate


logger = logging.getLogger(__name__)


class AgendaOrchestrator:
    """
    Orchestrates the complete message processing workflow.
    
    Flow:
    1. Parse intent using NLP engine
    2. Extract entities
    3. Validate extracted entities
    4. Parse datetime if present
    5. Execute appropriate action
    6. Return structured result
    """
    
    def __init__(
        self,
        event_service: EventService,
        event_tools: EventTools,
        timezone: str = "UTC"
    ):
        """
        Initialize orchestrator with required services.
        
        Args:
            event_service: Service for event operations
            event_tools: CrewAI tools for events
            timezone: Timezone for datetime parsing
        """
        self.intent_parser = AgendaIntentParser()
        self.nlp_engine = SimpleNLPEngine()  # Simple NLP with dictionary
        self.datetime_parser = DateTimeParser(timezone=timezone)
        self.event_service = event_service
        self.event_tools = event_tools
        self.timezone = timezone
    
    async def process_message(
        self, 
        message: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process user message through complete workflow.
        
        Args:
            message: User's natural language message
            context: Context dictionary with user_id, tenant_id, etc.
            
        Returns:
            Dictionary with:
            - success: bool
            - intent: str
            - response: str
            - data: dict (optional, contains created/updated event)
            - missing_fields: list (if incomplete request)
        """
        logger.info(f"Processing message: {message[:50]}...")
        
        try:
            # Step 1: Detect intent using NLP engine (primary) with fallback to regex
            intent = await self.nlp_engine.detect_intent(message)
            
            # Fallback to regex-based parser if NLP returns unknown
            if intent == "unknown":
                intent = await self.intent_parser.detect_intent(message)
            
            logger.info(f"Detected intent: {intent}")
            
            if intent == "unknown":
                return {
                    "success": False,
                    "intent": "unknown",
                    "response": "❓ No entendí tu solicitud. ¿Puedes reformularla? Por ejemplo: 'crear reunión mañana a las 3pm'",
                    "data": None,
                    "missing_fields": []
                }
            
            # Step 2: Extract entities using intent parser
            entities = self.nlp_engine.extract_entities(message, intent)
            
            # Step 2.5: Get entity hints from NLP engine
            entity_hints = self.nlp_engine.extract_entities_hints(message)
            logger.debug(f"Entity hints from NLP: {entity_hints}")
            
            logger.info(f"Extracted entities: {entities}")
            
            # Step 3: Parse datetime if present
            if entities.get("datetime_str"):
                parsed_dt = self.datetime_parser.parse(entities["datetime_str"])
                if parsed_dt:
                    entities["datetime"] = parsed_dt
                    logger.info(f"Parsed datetime: {parsed_dt}")
                else:
                    logger.warning(f"Failed to parse datetime: {entities['datetime_str']}")
            
            # Step 4: Validate entities
            is_valid, missing = self.intent_parser.validate_entities(entities, intent)
            
            if not is_valid:
                logger.info(f"Incomplete request. Missing: {missing}")
                
                # Get NLP suggestion for missing info
                suggestion = self.nlp_engine.suggest_missing_info(intent, entities)
                
                return {
                    "success": False,
                    "intent": intent,
                    "response": self._generate_missing_fields_prompt(intent, missing, suggestion),
                    "data": None,
                    "missing_fields": missing,
                    "partial_entities": entities
                }
            
            # Step 5: Execute action based on intent
            result = await self._execute_action(intent, entities, context)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return {
                "success": False,
                "intent": "error",
                "response": f"❌ Ocurrió un error procesando tu solicitud: {str(e)}",
                "data": None,
                "missing_fields": []
            }
    
    async def _execute_action(
        self,
        intent: str,
        entities: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the appropriate action based on intent.
        
        Args:
            intent: Detected intent
            entities: Extracted and validated entities
            context: User context
            
        Returns:
            Result dictionary
        """
        user_id = context.get("user_id")
        tenant_id = context.get("tenant_id")
        
        if not user_id or not tenant_id:
            return {
                "success": False,
                "intent": intent,
                "response": "❌ Error: Falta información de usuario o tenant",
                "data": None,
                "missing_fields": []
            }
        
        try:
            if intent == "create_event":
                return await self._handle_create_event(entities, user_id, tenant_id)
            
            elif intent == "update_event":
                return await self._handle_update_event(entities, user_id, tenant_id)
            
            elif intent == "delete_event":
                return await self._handle_delete_event(entities, user_id, tenant_id)
            
            elif intent == "query_events":
                return await self._handle_query_events(entities, user_id, tenant_id)
            
            elif intent == "mark_complete":
                return await self._handle_mark_complete(entities, user_id, tenant_id)
            
            else:
                return {
                    "success": False,
                    "intent": intent,
                    "response": f"❌ Intent '{intent}' no está implementado todavía",
                    "data": None,
                    "missing_fields": []
                }
                
        except Exception as e:
            logger.error(f"Error executing action {intent}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "intent": intent,
                "response": f"❌ Error ejecutando acción: {str(e)}",
                "data": None,
                "missing_fields": []
            }
    
    async def _handle_create_event(
        self,
        entities: Dict[str, Any],
        user_id: int,
        tenant_id: str
    ) -> Dict[str, Any]:
        """
        Handle create event action.
        
        ✅ FIXED: Removed duplicate event creation.
        Now only uses EventTools which internally calls EventService.
        """
        
        # Prepare event data
        event_data = {
            "title": entities.get("title"),
            "start_datetime": entities.get("datetime"),
            "location": entities.get("location"),
            "participants": entities.get("participants", []),
        }
        
        # Use EventTools to create event (formats response nicely)
        self.event_tools.set_context(user_id=user_id, tenant_id=tenant_id)
        response = await self.event_tools.create_event(event_data)
        
        return {
            "success": True,
            "intent": "create_event",
            "response": response,
            "data": None,  # EventTools response is already formatted
            "missing_fields": []
        }
    
    async def _handle_update_event(
        self,
        entities: Dict[str, Any],
        user_id: int,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Handle update event action."""
        
        event_id = entities.get("event_id")
        
        if not event_id:
            return {
                "success": False,
                "intent": "update_event",
                "response": "❌ No especificaste qué evento modificar. Usa el número del evento, ej: 'modificar evento #123'",
                "data": None,
                "missing_fields": ["event_id"]
            }
        
        # Prepare update data
        update_data = {}
        if entities.get("title"):
            update_data["title"] = entities["title"]
        if entities.get("datetime"):
            update_data["start_datetime"] = entities["datetime"]
        if entities.get("location"):
            update_data["location"] = entities["location"]
        if entities.get("participants"):
            update_data["participants"] = entities["participants"]
        
        # Use EventTools
        self.event_tools.set_context(user_id=user_id, tenant_id=tenant_id)
        update_data["event_id"] = event_id
        response = await self.event_tools.update_event(update_data)
        
        return {
            "success": True,
            "intent": "update_event",
            "response": response,
            "data": {"event_id": event_id},
            "missing_fields": []
        }
    
    async def _handle_delete_event(
        self,
        entities: Dict[str, Any],
        user_id: int,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Handle delete event action."""
        
        event_id = entities.get("event_id")
        
        if not event_id:
            return {
                "success": False,
                "intent": "delete_event",
                "response": "❌ No especificaste qué evento eliminar. Usa el número del evento, ej: 'eliminar evento #123'",
                "data": None,
                "missing_fields": ["event_id"]
            }
        
        # Use EventTools
        self.event_tools.set_context(user_id=user_id, tenant_id=tenant_id)
        response = await self.event_tools.delete_event({"event_id": event_id})
        
        return {
            "success": True,
            "intent": "delete_event",
            "response": response,
            "data": {"event_id": event_id},
            "missing_fields": []
        }
    
    async def _handle_query_events(
        self,
        entities: Dict[str, Any],
        user_id: int,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Handle query events action."""
        
        # Use EventTools to list events
        self.event_tools.set_context(user_id=user_id, tenant_id=tenant_id)
        
        # If datetime specified, filter by that date
        query_params = {}
        if entities.get("datetime"):
            query_params["start_date"] = entities["datetime"]
        
        response = await self.event_tools.list_upcoming_events(query_params)
        
        return {
            "success": True,
            "intent": "query_events",
            "response": response,
            "data": None,
            "missing_fields": []
        }
    
    async def _handle_mark_complete(
        self,
        entities: Dict[str, Any],
        user_id: int,
        tenant_id: str
    ) -> Dict[str, Any]:
        """Handle mark event as complete action."""
        
        event_id = entities.get("event_id")
        
        if not event_id:
            return {
                "success": False,
                "intent": "mark_complete",
                "response": "❌ No especificaste qué evento marcar como completado. Usa el número del evento.",
                "data": None,
                "missing_fields": ["event_id"]
            }
        
        # Use EventTools
        self.event_tools.set_context(user_id=user_id, tenant_id=tenant_id)
        response = await self.event_tools.mark_completed({"event_id": event_id})
        
        return {
            "success": True,
            "intent": "mark_complete",
            "response": response,
            "data": {"event_id": event_id},
            "missing_fields": []
        }
    
    def _generate_missing_fields_prompt(
        self,
        intent: str,
        missing: list,
        nlp_suggestion: Optional[str] = None
    ) -> str:
        """Generate helpful prompt for missing information."""
        
        # Use NLP suggestion if available
        if nlp_suggestion:
            return f"❓ {nlp_suggestion}"
        
        # Fallback to manual prompts
        prompts = {
            "create_event": {
                "title": "¿Cuál es el título del evento?",
                "datetime_str": "¿Cuándo será el evento? (ej: mañana a las 3pm, el viernes)",
            },
            "update_event": {
                "event_id": "¿Qué evento quieres modificar? Usa el número del evento (ej: #123)",
            },
            "delete_event": {
                "event_id": "¿Qué evento quieres eliminar? Usa el número del evento (ej: #123)",
            },
            "mark_complete": {
                "event_id": "¿Qué evento quieres marcar como completado? Usa el número del evento (ej: #123)",
            }
        }
        
        intent_prompts = prompts.get(intent, {})
        missing_prompts = [intent_prompts.get(field, f"Falta: {field}") for field in missing]
        
        return "❓ Me falta información:\n" + "\n".join(f"• {p}" for p in missing_prompts)
