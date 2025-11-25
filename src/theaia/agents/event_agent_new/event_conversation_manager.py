"""
EventConversationManager - Gestor de conversaciones de eventos.

Coordina FSM, ML entity extraction y DB operations para eventos.
✅ INTEGRACIÓN REAL CON EventRepository (ASYNC + COMMIT)
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime

from src.theaia.agents.event_agent_new.model.event_fsm import EventFSM, EventState
from src.theaia.database.repositories.event_repository import EventRepository
from src.theaia.database.session import get_db


class EventConversationManager:
    """
    Gestor de conversaciones para eventos.
    
    Responsabilidades:
    - Gestionar FSM per-user instances
    - Integrar ML entity extraction (datetime, location)
    - Coordinar con DB via EventRepository ✅
    - Formatear respuestas user-friendly
    """
    
    def __init__(self, user_id: str):
        """
        Initialize manager.
        
        Args:
            user_id: User ID
        """
        self.user_id = user_id
        self.fsm_instances: Dict[str, EventFSM] = {}
    
    async def handle_message(
        self, 
        user_id: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Handle event message.
        
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
            
            # ✅ INTERCEPT CREATE_CONFIRM for DB save
            if fsm.state == EventState.DONE and 'title' in fsm.context:
                # Save to DB
                event = await self._save_event_to_db(fsm.context, user_id, tenant_id)
                response = f"✅ Evento #{event.id} creado: {event.title}"
            
            # ✅ INTERCEPT LIST for DB query
            if fsm.state == EventState.LIST_START:
                events = await self._get_events_from_db(user_id, tenant_id)
                response = self._format_events(events)
            
            # Update context
            context['fsm_state'] = fsm.state.value
            context['event_context'] = fsm.context
            
            # Determine response state
            if fsm.state == EventState.DONE:
                new_state = "completed"
            elif fsm.state == EventState.CANCEL:
                new_state = "cancelled"
            else:
                new_state = "in_progress"
            
        except Exception as e:
            response = f"Error procesando evento: {str(e)}"
            new_state = "error"
        
        return response, new_state, context
    
    async def _save_event_to_db(
        self, 
        event_data: Dict[str, Any], 
        user_id: str, 
        tenant_id: str
    ):
        """
        Save event to database via EventRepository.
        
        Args:
            event_data: Event data from FSM context
            user_id: User ID
            tenant_id: Tenant ID
            
        Returns:
            Event: Created event object
        """
        async for session in get_db():
            event_repo = EventRepository(session)
            
            # Prepare data
            data = {
                'title': event_data.get('title'),
                'start_datetime': event_data.get('datetime') or datetime.now(),
                'end_datetime': event_data.get('end_datetime'),
                'location': event_data.get('location'),
                'event_type': 'personal',
                'status': 'pending',
                'user_id': user_id,
                'tenant_id': tenant_id
            }
            
            # Create in DB
            event = await event_repo.create(**data)
            await session.commit()        # ✅ COMMIT transaction
            await session.refresh(event)  # ✅ REFRESH to load ID
            return event
    
    async def _get_events_from_db(self, user_id: str, tenant_id: str):
        """
        Get events from database.
        
        Args:
            user_id: User ID
            tenant_id: Tenant ID
            
        Returns:
            List[Event]: List of events
        """
        async for session in get_db():
            event_repo = EventRepository(session)
            events = await event_repo.get_by_user(user_id, tenant_id)
            return events
    
    def _format_events(self, events) -> str:
        """
        Format events list for user display.
        
        Args:
            events: List of Event objects
            
        Returns:
            str: Formatted response
        """
        if not events:
            return "📅 No tienes eventos programados."
        
        response = "📅 Tus eventos:\n"
        for event in events:
            date_str = event.start_datetime.strftime("%d/%m/%Y %H:%M") if event.start_datetime else "Sin fecha"
            location_str = f" - {event.location}" if event.location else ""
            response += f"\n• {event.title} ({date_str}){location_str}"
        
        return response
    
    def _get_or_create_fsm(self, user_id: str, tenant_id: str) -> EventFSM:
        """
        Get or create FSM instance for user.
        
        Args:
            user_id: User ID
            tenant_id: Tenant ID
            
        Returns:
            EventFSM: FSM instance
        """
        if user_id not in self.fsm_instances:
            self.fsm_instances[user_id] = EventFSM(user_id, tenant_id)
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
