"""
Response Formatter for AgendaAgent

Formats responses with emojis, structure, and Telegram-friendly markup.
Creates beautiful, user-friendly messages.
"""

from typing import List, Optional
from datetime import datetime

from ...database.models.event import Event


class ResponseFormatter:
    """
    Formats responses for AgendaAgent.
    
    Supports:
    - Rich formatting with emojis
    - Telegram markdown
    - Structured layouts
    - Multiple languages (Spanish/English)
    """
    
    def __init__(self, language: str = "es"):
        """
        Initialize formatter.
        
        Args:
            language: Language code ("es" or "en")
        """
        self.language = language
    
    def format_event_created(self, event: Event) -> str:
        """
        Format successful event creation message.
        
        Args:
            event: Created event object
            
        Returns:
            Formatted success message
        """
        if self.language == "es":
            msg = f"""✅ **Evento creado exitosamente**

📝 **Título:** {event.title}
📅 **Fecha:** {self._format_datetime(event.start_time)}"""
            
            if event.location:
                msg += f"\n📍 **Ubicación:** {event.location}"
            
            if event.participants:
                participants_str = ", ".join(event.participants)
                msg += f"\n👥 **Participantes:** {participants_str}"
            
            msg += f"\n🆔 **ID del evento:** #{event.id}"
            
        else:  # English
            msg = f"""✅ **Event created successfully**

📝 **Title:** {event.title}
📅 **Date:** {self._format_datetime(event.start_time)}"""
            
            if event.location:
                msg += f"\n📍 **Location:** {event.location}"
            
            if event.participants:
                participants_str = ", ".join(event.participants)
                msg += f"\n👥 **Participants:** {participants_str}"
            
            msg += f"\n🆔 **Event ID:** #{event.id}"
        
        return msg
    
    def format_event_updated(self, event: Event) -> str:
        """
        Format successful event update message.
        
        Args:
            event: Updated event object
            
        Returns:
            Formatted success message
        """
        if self.language == "es":
            msg = f"""✅ **Evento actualizado**

🆔 **ID:** #{event.id}
📝 **Título:** {event.title}
📅 **Fecha:** {self._format_datetime(event.start_time)}"""
            
            if event.location:
                msg += f"\n📍 **Ubicación:** {event.location}"
        
        else:  # English
            msg = f"""✅ **Event updated**

🆔 **ID:** #{event.id}
📝 **Title:** {event.title}
📅 **Date:** {self._format_datetime(event.start_time)}"""
            
            if event.location:
                msg += f"\n📍 **Location:** {event.location}"
        
        return msg
    
    def format_event_deleted(self, event_id: int, title: Optional[str] = None) -> str:
        """
        Format successful event deletion message.
        
        Args:
            event_id: Deleted event ID
            title: Event title (if available)
            
        Returns:
            Formatted success message
        """
        if self.language == "es":
            msg = f"✅ **Evento #{event_id} eliminado correctamente**"
            if title:
                msg += f"\n📝 {title}"
        else:
            msg = f"✅ **Event #{event_id} deleted successfully**"
            if title:
                msg += f"\n📝 {title}"
        
        return msg
    
    def format_event_completed(self, event_id: int, title: str) -> str:
        """
        Format event marked as completed message.
        
        Args:
            event_id: Event ID
            title: Event title
            
        Returns:
            Formatted success message
        """
        if self.language == "es":
            return f"✅ **Evento #{event_id} '{title}' marcado como completado**"
        else:
            return f"✅ **Event #{event_id} '{title}' marked as completed**"
    
    def format_event_list(self, events: List[Event], title: Optional[str] = None) -> str:
        """
        Format list of events.
        
        Args:
            events: List of events
            title: Optional title for the list
            
        Returns:
            Formatted events list
        """
        if not events:
            if self.language == "es":
                return "📅 No tienes eventos próximos"
            else:
                return "📅 You don't have any upcoming events"
        
        if self.language == "es":
            header = title or f"📅 **Tus próximos eventos** ({len(events)})"
        else:
            header = title or f"📅 **Your upcoming events** ({len(events)})"
        
        msg = header + "\n\n"
        
        for i, event in enumerate(events, 1):
            msg += self._format_event_item(event, index=i)
            if i < len(events):
                msg += "\n" + "─" * 30 + "\n"
        
        return msg
    
    def _format_event_item(self, event: Event, index: Optional[int] = None) -> str:
        """
        Format a single event item for list display.
        
        Args:
            event: Event object
            index: Optional index number
            
        Returns:
            Formatted event item
        """
        prefix = f"{index}. " if index else ""
        
        item = f"{prefix}**{event.title}**\n"
        item += f"   🆔 #{event.id}\n"
        item += f"   📅 {self._format_datetime(event.start_time)}\n"
        
        if event.location:
            item += f"   📍 {event.location}\n"
        
        if event.participants:
            participants_str = ", ".join(event.participants[:3])
            if len(event.participants) > 3:
                participants_str += f" +{len(event.participants) - 3} más"
            item += f"   👥 {participants_str}\n"
        
        # Status indicator
        if event.status == "completed":
            item += "   ✅ Completado\n"
        elif event.status == "cancelled":
            item += "   ❌ Cancelado\n"
        elif event.status == "pending":
            item += "   ⏳ Pendiente\n"
        
        return item.rstrip()
    
    def format_error(self, error_message: str, error_type: str = "general") -> str:
        """
        Format error message.
        
        Args:
            error_message: Error description
            error_type: Type of error (general, validation, not_found, etc.)
            
        Returns:
            Formatted error message
        """
        emoji_map = {
            "general": "❌",
            "validation": "⚠️",
            "not_found": "🔍",
            "permission": "🔒",
            "timeout": "⏱️",
        }
        
        emoji = emoji_map.get(error_type, "❌")
        
        if self.language == "es":
            return f"{emoji} **Error:** {error_message}"
        else:
            return f"{emoji} **Error:** {error_message}"
    
    def format_missing_info_prompt(self, missing_fields: List[str], intent: str) -> str:
        """
        Format prompt for missing information.
        
        Args:
            missing_fields: List of missing field names
            intent: Intent type
            
        Returns:
            Formatted prompt
        """
        if self.language == "es":
            header = "❓ **Necesito más información:**\n\n"
        else:
            header = "❓ **I need more information:**\n\n"
        
        prompts = self._get_field_prompts(intent)
        
        msg = header
        for field in missing_fields:
            prompt = prompts.get(field, field)
            msg += f"• {prompt}\n"
        
        return msg
    
    def format_confirmation_request(self, event_data: dict) -> str:
        """
        Format confirmation request before creating/updating event.
        
        Args:
            event_data: Event data to confirm
            
        Returns:
            Formatted confirmation message
        """
        if self.language == "es":
            msg = "🔍 **Por favor confirma:**\n\n"
            msg += f"📝 **Título:** {event_data.get('title', 'N/A')}\n"
            
            if event_data.get('start_time'):
                msg += f"📅 **Fecha:** {self._format_datetime(event_data['start_time'])}\n"
            
            if event_data.get('location'):
                msg += f"📍 **Ubicación:** {event_data['location']}\n"
            
            if event_data.get('participants'):
                participants_str = ", ".join(event_data['participants'])
                msg += f"👥 **Participantes:** {participants_str}\n"
            
            msg += "\n¿Es correcto? (Responde 'sí' o 'no')"
        
        else:  # English
            msg = "🔍 **Please confirm:**\n\n"
            msg += f"📝 **Title:** {event_data.get('title', 'N/A')}\n"
            
            if event_data.get('start_time'):
                msg += f"📅 **Date:** {self._format_datetime(event_data['start_time'])}\n"
            
            if event_data.get('location'):
                msg += f"📍 **Location:** {event_data['location']}\n"
            
            if event_data.get('participants'):
                participants_str = ", ".join(event_data['participants'])
                msg += f"👥 **Participants:** {participants_str}\n"
            
            msg += "\n Is this correct? (Reply 'yes' or 'no')"
        
        return msg
    
    def _format_datetime(self, dt: Optional[datetime]) -> str:
        """
        Format datetime in user-friendly format.
        
        Args:
            dt: Datetime object
            
        Returns:
            Formatted datetime string
        """
        if not dt:
            return "N/A"
        
        if self.language == "es":
            # Spanish format: "Miércoles, 04 de Diciembre de 2025 a las 15:30"
            days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            
            day_name = days[dt.weekday()]
            month_name = months[dt.month - 1]
            
            return f"{day_name}, {dt.day:02d} de {month_name} de {dt.year} a las {dt.hour:02d}:{dt.minute:02d}"
        
        else:  # English
            # English format: "Wednesday, December 04, 2025 at 15:30"
            return dt.strftime("%A, %B %d, %Y at %H:%M")
    
    def _get_field_prompts(self, intent: str) -> dict:
        """Get prompts for missing fields based on intent."""
        if self.language == "es":
            prompts = {
                "create_event": {
                    "title": "📝 ¿Cuál es el título del evento?",
                    "datetime_str": "📅 ¿Cuándo será? (ej: mañana a las 3pm)",
                    "location": "📍 ¿Dónde será? (opcional)",
                    "participants": "👥 ¿Quién participará? (opcional)",
                },
                "update_event": {
                    "event_id": "🔍 ¿Qué evento quieres modificar? (usa #ID)",
                },
                "delete_event": {
                    "event_id": "🔍 ¿Qué evento quieres eliminar? (usa #ID)",
                },
            }
        else:
            prompts = {
                "create_event": {
                    "title": "📝 What's the event title?",
                    "datetime_str": "📅 When will it be? (e.g: tomorrow at 3pm)",
                    "location": "📍 Where will it be? (optional)",
                    "participants": "👥 Who will participate? (optional)",
                },
                "update_event": {
                    "event_id": "🔍 Which event do you want to modify? (use #ID)",
                },
                "delete_event": {
                    "event_id": "🔍 Which event do you want to delete? (use #ID)",
                },
            }
        
        return prompts.get(intent, {})
