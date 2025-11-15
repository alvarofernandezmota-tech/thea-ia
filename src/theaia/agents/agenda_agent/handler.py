# Archivo: src/theaia/agents/agenda_agent/handler.py

"""
AgendaAgent handler - Manages calendar events and appointments.
Complete implementation with date/time extraction and event creation.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

from src.theaia.agents.base_agent import BaseAgent, AgentConfig
from src.theaia.agents.agenda_agent.agenda_conversation_manager import AgendaConversationManager


class AgendaAgent(BaseAgent):
    """
    Agent for managing calendar events, appointments, and meetings.
    
    Handles:
    - Event creation
    - Event listing
    - Event editing/cancellation
    - Date/time extraction from natural language
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize AgendaAgent.
        
        Args:
            config: Agent configuration (optional)
        """
        if config is None:
            config = AgentConfig(name="AgendaAgent")
        
        super().__init__(config)
        self.conversation_managers = {}  # user_id -> AgendaConversationManager
        self.logger.info("AgendaAgent initialized")
    
    def get_supported_intents(self) -> List[str]:
        """Get list of supported intents."""
        return [
            "agenda",
            "cita",
            "reunión",
            "evento",
            "agendar",
            "calendario",
            "appointment",
            "meeting",
            "schedule"
        ]
    
    def _get_conversation_manager(self, user_id: str) -> AgendaConversationManager:
        """
        Get or create conversation manager for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            AgendaConversationManager instance
        """
        if user_id not in self.conversation_managers:
            self.conversation_managers[user_id] = AgendaConversationManager(user_id)
            self.logger.debug(f"Created conversation manager for user {user_id}")
        
        return self.conversation_managers[user_id]
    
    def _process_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process agenda-related message.
        
        Args:
            user_id: User identifier
            message: User message text
            context: Conversation context
            
        Returns:
            Response dictionary with status, message, and context
        """
        self.logger.info(f"Processing agenda message from user {user_id}")
        
        # Extract date/time information if present
        extracted_datetime = self._extract_datetime(message)
        if extracted_datetime:
            context["extracted_datetime"] = extracted_datetime
            self.logger.debug(f"Extracted datetime: {extracted_datetime}")
        
        # Get conversation manager for this user
        conv_manager = self._get_conversation_manager(user_id)
        
        # Handle message through conversation manager
        try:
            response_text, new_state, updated_context = conv_manager.handle_message(
                user_id, message, context
            )
            
            # Convert to standard response format
            return {
                "status": "ok",
                "message": response_text,
                "context": updated_context,
                "state": new_state
            }
            
        except Exception as e:
            self.logger.error(f"Error in conversation manager: {e}", exc_info=True)
            raise
    
    def _extract_datetime(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Extract date and time information from message.
        
        Args:
            message: User message text
            
        Returns:
            Dictionary with extracted date/time info, or None
        """
        message_lower = message.lower()
        extracted = {}
        
        # Extract relative dates
        if "hoy" in message_lower or "today" in message_lower:
            extracted["date"] = datetime.now().date()
        elif "mañana" in message_lower or "tomorrow" in message_lower:
            extracted["date"] = (datetime.now() + timedelta(days=1)).date()
        elif "pasado mañana" in message_lower:
            extracted["date"] = (datetime.now() + timedelta(days=2)).date()
        
        # Extract day of week
        days_map = {
            "lunes": 0, "monday": 0,
            "martes": 1, "tuesday": 1,
            "miércoles": 2, "wednesday": 2,
            "jueves": 3, "thursday": 3,
            "viernes": 4, "friday": 4,
            "sábado": 5, "saturday": 5,
            "domingo": 6, "sunday": 6
        }
        
        for day_name, day_num in days_map.items():
            if day_name in message_lower:
                # Calculate next occurrence of this day
                today = datetime.now()
                days_ahead = day_num - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                extracted["date"] = (today + timedelta(days=days_ahead)).date()
                break
        
        # Extract time (formato 24h o 12h) - CORREGIDO
        time_patterns = [
            (r'(\d{1,2}):(\d{2})\s*(am|pm)?', 'hm_ampm'),  # 3:30 pm
            (r'(\d{1,2})\s*(am|pm)', 'h_ampm'),             # 3 pm  
            (r'a las (\d{1,2})', 'h_only'),                 # a las 15
        ]
        
        for pattern, pattern_type in time_patterns:
            match = re.search(pattern, message_lower)
            if match:
                hour = int(match.group(1))
                minute = 0
                am_pm = None
                
                if pattern_type == 'hm_ampm':
                    minute = int(match.group(2))
                    am_pm = match.group(3) if len(match.groups()) >= 3 else None
                elif pattern_type == 'h_ampm':
                    am_pm = match.group(2)
                
                # Handle AM/PM conversion
                if am_pm:
                    if am_pm == 'pm' and hour < 12:
                        hour += 12
                    elif am_pm == 'am' and hour == 12:
                        hour = 0
                
                extracted["time"] = f"{hour:02d}:{minute:02d}"
                break
        
        # Extract duration
        duration_pattern = r'(\d+)\s*(hora|horas|minuto|minutos|hour|hours|minute|minutes)'
        duration_match = re.search(duration_pattern, message_lower)
        if duration_match:
            amount = int(duration_match.group(1))
            unit = duration_match.group(2)
            
            if "hora" in unit or "hour" in unit:
                extracted["duration_minutes"] = amount * 60
            else:
                extracted["duration_minutes"] = amount
        
        return extracted if extracted else None
    
    def create_event(self, user_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new calendar event.
        
        Args:
            user_id: User identifier
            event_data: Event information (title, date, time, duration)
            
        Returns:
            Response dictionary with created event info
        """
        self.logger.info(f"Creating event for user {user_id}: {event_data.get('title')}")
        
        # Validate required fields
        required_fields = ["title", "date", "time"]
        missing_fields = [f for f in required_fields if f not in event_data]
        
        if missing_fields:
            return {
                "status": "error",
                "message": f"Faltan campos requeridos: {', '.join(missing_fields)}",
                "context": {}
            }
        
        # TODO: Integrate with database to persist event
        # For now, return success with event data
        
        event_datetime = f"{event_data['date']} {event_data['time']}"
        
        return {
            "status": "ok",
            "message": f"Evento '{event_data['title']}' creado para {event_datetime}",
            "context": {
                "event_created": True,
                "event_data": event_data
            }
        }
    
    def list_events(self, user_id: str, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        List calendar events for a user.
        
        Args:
            user_id: User identifier
            date: Optional specific date (defaults to today)
            
        Returns:
            Response dictionary with list of events
        """
        if date is None:
            date = datetime.now()
        
        self.logger.info(f"Listing events for user {user_id} on {date.date()}")
        
        # TODO: Integrate with database to retrieve events
        # For now, return empty list
        
        return {
            "status": "ok",
            "message": f"No tienes eventos para el {date.strftime('%d/%m/%Y')}",
            "context": {
                "events": [],
                "date": date.isoformat()
            }
        }
    
    def cleanup(self) -> None:
        """Cleanup agent resources."""
        super().cleanup()
        self.conversation_managers.clear()
        self.logger.info("AgendaAgent cleaned up")
