"""
ReminderConversationManager - Gestor de conversaciones de recordatorios.

Coordina FSM, ML entity extraction y DB operations para recordatorios.
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime

from src.theaia.agents.reminder_agent.model.reminder_fsm import ReminderFSM, ReminderState


class ReminderConversationManager:
    """
    Gestor de conversaciones para recordatorios.
    
    Responsabilidades:
    - Gestionar FSM per-user instances
    - Integrar ML entity extraction (datetime, location)
    - Coordinar con DB (ReminderRepository)
    - Formatear respuestas user-friendly
    """
    
    def __init__(self, user_id: str):
        """
        Initialize manager.
        
        Args:
            user_id: User ID
        """
        self.user_id = user_id
        self.fsm_instances: Dict[str, ReminderFSM] = {}
        
        # ML extractors (importar cuando estén disponibles)
        # from src.theaia.ml.entity_extractor import DateTimeExtractor
        # self.datetime_extractor = DateTimeExtractor()
    
    async def handle_message(
        self, 
        user_id: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Handle reminder message.
        
        Args:
            user_id: User ID
            message: User message
            context: Conversation context
            
        Returns:
            Tuple[str, str, Dict]: (response, state, updated_context)
        """
        tenant_id = self._get_tenant_id(context)
        
        # Get or create FSM instance
        fsm = self._get_or_create_fsm(user_id, tenant_id)
        
        # Extract entities (ML)
        entities = self._extract_entities(message)
        
        # FSM handle
        try:
            response = await fsm.handle(message, entities, context)
            
            # Update context
            context['fsm_state'] = fsm.state.value
            context['reminder_context'] = fsm.context
            
            # Determine response state
            if fsm.state == ReminderState.DONE:
                new_state = "completed"
            elif fsm.state == ReminderState.CANCEL:
                new_state = "cancelled"
            else:
                new_state = "in_progress"
            
        except Exception as e:
            response = f"Error procesando recordatorio: {str(e)}"
            new_state = "error"
        
        return response, new_state, context
    
    def _get_or_create_fsm(self, user_id: str, tenant_id: str) -> ReminderFSM:
        """
        Get or create FSM instance for user.
        
        Args:
            user_id: User ID
            tenant_id: Tenant ID
            
        Returns:
            ReminderFSM: FSM instance
        """
        if user_id not in self.fsm_instances:
            self.fsm_instances[user_id] = ReminderFSM(user_id, tenant_id)
        return self.fsm_instances[user_id]
    
    def _get_tenant_id(self, context: Dict[str, Any]) -> str:
        """
        Extract tenant_id from context.
        
        Args:
            context: Context dict
            
        Returns:
            str: Tenant ID
        """
        return context.get('tenant_id') or context.get('user', {}).get('tenant_id', 'default')
    
    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """
        Extract entities from message using ML.
        
        Args:
            message: User message
            
        Returns:
            Dict: Extracted entities (datetime, location, etc.)
        """
        entities = {}
        
        # TODO: Integrar DateTimeExtractor cuando esté disponible
        # entities['datetime'] = self.datetime_extractor.extract(message)
        
        # TODO: Integrar LocationExtractor si es necesario
        # entities['location'] = self.location_extractor.extract(message)
        
        return entities
    
    def cleanup_fsm(self, user_id: str):
        """
        Cleanup FSM instance for user (memory management).
        
        Args:
            user_id: User ID
        """
        if user_id in self.fsm_instances:
            del self.fsm_instances[user_id]
