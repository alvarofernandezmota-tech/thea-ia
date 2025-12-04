"""
Conversation Manager for AgendaAgent

Manages multi-turn conversations and FSM state when user requests are incomplete.
Maintains conversation context and guides users through information gathering.
Integrates with FSM Machine for robust state management.
"""

from typing import Dict, Optional, Any, List
from datetime import datetime
import logging

from .model.agent_states import AgentState
from .fsm_machine import AgendaFSM, FSMManager


logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manages multi-turn conversations for incomplete requests.
    
    Handles FSM state transitions and conversation context.
    Guides users through providing missing information.
    Uses FSM Machine for state management.
    """
    
    def __init__(self):
        """Initialize conversation manager with FSM manager."""
        # In-memory conversation storage (will be replaced with DB/Redis in production)
        self.conversations: Dict[str, Dict[str, Any]] = {}
        
        # FSM Manager for state machines
        self.fsm_manager = FSMManager()
    
    def start_conversation(
        self,
        user_id: int,
        intent: str,
        partial_entities: Dict[str, Any],
        missing_fields: List[str]
    ) -> str:
        """
        Start a new conversation for an incomplete request.
        
        Args:
            user_id: User ID
            intent: Detected intent
            partial_entities: Entities already extracted
            missing_fields: List of missing required fields
            
        Returns:
            Conversation ID (unique identifier)
        """
        conversation_id = f"{user_id}_{intent}_{int(datetime.now().timestamp())}"
        
        # Create FSM for this conversation
        fsm = self.fsm_manager.get_or_create(conversation_id)
        
        # Determine initial FSM state based on intent
        initial_state = self._get_initial_state(intent, missing_fields)
        
        # Trigger appropriate FSM transition
        self._trigger_fsm_start(fsm, intent)
        
        # Update FSM context with partial entities
        for key, value in partial_entities.items():
            fsm.update_context(key, value)
        
        self.conversations[conversation_id] = {
            "user_id": user_id,
            "intent": intent,
            "state": fsm.get_current_state(),
            "partial_entities": partial_entities,
            "missing_fields": missing_fields,
            "created_at": datetime.now(),
            "last_interaction": datetime.now(),
            "turn_count": 0
        }
        
        logger.info(f"Started conversation {conversation_id} for user {user_id}, intent={intent}, fsm_state={fsm.get_current_state().value}")
        
        return conversation_id
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation by ID."""
        return self.conversations.get(conversation_id)
    
    def update_conversation(
        self,
        conversation_id: str,
        new_entities: Dict[str, Any] = None,
        new_state: AgentState = None
    ) -> bool:
        """
        Update conversation with new information.
        
        Args:
            conversation_id: Conversation ID
            new_entities: New entities to merge
            new_state: New FSM state (optional, FSM manages this)
            
        Returns:
            True if updated successfully
        """
        conversation = self.conversations.get(conversation_id)
        
        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            return False
        
        # Get FSM
        fsm = self.fsm_manager.get(conversation_id)
        if not fsm:
            logger.error(f"FSM not found for conversation {conversation_id}")
            return False
        
        # Merge new entities into conversation
        if new_entities:
            conversation["partial_entities"].update(new_entities)
            
            # Also update FSM context
            for key, value in new_entities.items():
                fsm.update_context(key, value)
            
            logger.info(f"Updated conversation {conversation_id} with entities: {new_entities}")
            
            # Trigger FSM transitions based on what was provided
            self._trigger_fsm_update(fsm, new_entities)
        
        # Update state from FSM
        conversation["state"] = fsm.get_current_state()
        
        # Update metadata
        conversation["last_interaction"] = datetime.now()
        conversation["turn_count"] += 1
        
        # Update missing fields
        conversation["missing_fields"] = [
            field for field in conversation["missing_fields"]
            if not conversation["partial_entities"].get(field)
        ]
        
        return True
    
    def end_conversation(self, conversation_id: str) -> bool:
        """
        End and cleanup conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            True if deleted successfully
        """
        # Remove conversation
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Ended conversation {conversation_id}")
        
        # Remove FSM
        self.fsm_manager.remove(conversation_id)
        
        return True
    
    def is_conversation_complete(self, conversation_id: str) -> bool:
        """
        Check if conversation has all required information.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            True if all required fields are filled
        """
        conversation = self.conversations.get(conversation_id)
        
        if not conversation:
            return False
        
        return len(conversation["missing_fields"]) == 0
    
    def generate_prompt(
        self,
        conversation_id: str
    ) -> str:
        """
        Generate prompt for next missing field.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Prompt string to ask user for missing information
        """
        conversation = self.conversations.get(conversation_id)
        
        if not conversation:
            return "❌ Error: Conversación no encontrada"
        
        missing = conversation["missing_fields"]
        
        if not missing:
            return "✅ Ya tengo toda la información necesaria"
        
        # Get next missing field
        next_field = missing[0]
        intent = conversation["intent"]
        
        # Get FSM state for context
        fsm = self.fsm_manager.get(conversation_id)
        state = fsm.get_current_state() if fsm else AgentState.IDLE
        
        # Generate contextual prompt based on intent and state
        prompts = self._get_field_prompts(intent)
        
        return prompts.get(next_field, f"Por favor proporciona: {next_field}")
    
    def _get_initial_state(
        self,
        intent: str,
        missing_fields: List[str]
    ) -> AgentState:
        """
        Determine initial FSM state based on intent and missing fields.
        
        Args:
            intent: Detected intent
            missing_fields: List of missing fields
            
        Returns:
            Initial AgentState
        """
        if intent == "create_event":
            if "title" in missing_fields:
                return AgentState.AWAITING_EVENT_DETAILS
            elif "datetime_str" in missing_fields:
                return AgentState.AWAITING_TIME
            else:
                return AgentState.AWAITING_CONFIRMATION
        
        elif intent == "update_event":
            if "event_id" in missing_fields:
                return AgentState.AWAITING_EVENT_SELECTION
            else:
                return AgentState.AWAITING_EVENT_DETAILS
        
        elif intent == "query_events":
            return AgentState.AWAITING_TIME  # Optional time filter
        
        else:
            return AgentState.IDLE
    
    def _trigger_fsm_start(self, fsm: AgendaFSM, intent: str):
        """Trigger initial FSM transition based on intent."""
        try:
            if intent == "create_event":
                fsm.start_create_event()
            elif intent == "update_event":
                fsm.start_update_event()
            elif intent == "query_events":
                fsm.start_query()
        except Exception as e:
            logger.warning(f"Could not trigger FSM start: {e}")
    
    def _trigger_fsm_update(self, fsm: AgendaFSM, new_entities: Dict[str, Any]):
        """Trigger FSM transitions based on provided entities."""
        try:
            # Check what was provided and trigger appropriate transitions
            if "title" in new_entities:
                if fsm.can_trigger("provide_details"):
                    fsm.provide_details()
            
            if "datetime" in new_entities or "datetime_str" in new_entities:
                if fsm.can_trigger("provide_time"):
                    fsm.provide_time()
                elif fsm.can_trigger("provide_complete_info"):
                    fsm.provide_complete_info()
            
            if "event_id" in new_entities:
                if fsm.can_trigger("select_event"):
                    fsm.select_event()
                elif fsm.can_trigger("select_and_confirm"):
                    fsm.select_and_confirm()
        
        except Exception as e:
            logger.warning(f"Could not trigger FSM update: {e}")
    
    def _get_field_prompts(self, intent: str) -> Dict[str, str]:
        """
        Get contextual prompts for each field type.
        
        Args:
            intent: Intent type
            
        Returns:
            Dictionary mapping fields to prompts
        """
        if intent == "create_event":
            return {
                "title": "📝 ¿Cuál es el título o descripción del evento?",
                "datetime_str": "📅 ¿Cuándo será el evento?\nPuedes decir: 'mañana a las 3pm', 'el viernes', 'en 2 horas', etc.",
                "location": "📍 ¿Dónde será el evento? (opcional, presiona Enter para omitir)",
                "participants": "👥 ¿Quién participará? (opcional, puedes listar nombres separados por comas)",
            }
        
        elif intent == "update_event":
            return {
                "event_id": "🔍 ¿Qué evento quieres modificar?\nUsa el número del evento (ej: #123)\nPuedes ver tus eventos con: 'mostrar mis eventos'",
                "title": "📝 ¿Cuál será el nuevo título?",
                "datetime_str": "📅 ¿Cuándo será ahora el evento?",
                "location": "📍 ¿Cuál será la nueva ubicación?",
            }
        
        elif intent == "delete_event":
            return {
                "event_id": "🔍 ¿Qué evento quieres eliminar?\nUsa el número del evento (ej: #123)\nPuedes ver tus eventos con: 'mostrar mis eventos'",
            }
        
        elif intent == "mark_complete":
            return {
                "event_id": "🔍 ¿Qué evento quieres marcar como completado?\nUsa el número del evento (ej: #123)",
            }
        
        else:
            return {}
    
    def cleanup_old_conversations(self, max_age_minutes: int = 30):
        """
        Clean up conversations older than max_age_minutes.
        
        Args:
            max_age_minutes: Maximum age in minutes
        """
        now = datetime.now()
        to_delete = []
        
        for conv_id, conversation in self.conversations.items():
            age = (now - conversation["last_interaction"]).total_seconds() / 60
            if age > max_age_minutes:
                to_delete.append(conv_id)
        
        for conv_id in to_delete:
            self.end_conversation(conv_id)
        
        # Also cleanup FSMs in final state
        self.fsm_manager.cleanup_final_states()
        
        if to_delete:
            logger.info(f"Cleaned up {len(to_delete)} old conversations")
    
    def get_active_conversations_count(self, user_id: int) -> int:
        """
        Get count of active conversations for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of active conversations
        """
        return sum(
            1 for conv in self.conversations.values()
            if conv["user_id"] == user_id
        )
    
    def get_conversation_summary(self, conversation_id: str) -> Optional[str]:
        """
        Get human-readable summary of conversation state.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Summary string or None if not found
        """
        conversation = self.conversations.get(conversation_id)
        
        if not conversation:
            return None
        
        intent = conversation["intent"]
        state = conversation["state"]
        entities = conversation["partial_entities"]
        missing = conversation["missing_fields"]
        turns = conversation["turn_count"]
        
        # Get FSM info
        fsm = self.fsm_manager.get(conversation_id)
        fsm_info = ""
        if fsm:
            possible_actions = fsm.get_possible_triggers()
            fsm_info = f"\n- Acciones posibles: {', '.join(possible_actions)}"
        
        summary = f"""
🔄 **Conversación activa**
- Intent: {intent}
- Estado FSM: {state.value}
- Turnos: {turns}
- Información recopilada: {list(entities.keys())}
- Falta: {missing}{fsm_info}
        """.strip()
        
        return summary
    
    def get_fsm_stats(self) -> Dict[str, Any]:
        """Get statistics about FSMs."""
        return self.fsm_manager.get_stats()
