"""
Core Response Formatter - Formateador centralizado de respuestas
Genera respuestas bonitas con emojis para todos los agentes.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class CoreResponseFormatter:
    """
    Formateador de respuestas centralizado para todo el ecosistema.
    
    Genera mensajes consistentes con emojis y formato bonito.
    Soporta múltiples tipos de respuesta por agente.
    """
    
    def __init__(self, language: str = "es"):
        """
        Inicializa el formatter.
        
        Args:
            language: Idioma de las respuestas ("es" o "en")
        """
        self.language = language
        
        # Emojis por tipo de mensaje
        self.emojis = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "question": "❓",
            "calendar": "📅",
            "clock": "🕐",
            "note": "📝",
            "reminder": "⏰",
            "search": "🔍",
            "help": "💡",
            "location": "📍",
            "user": "👤",
            "id": "🆔",
        }
        
        # Mensajes de error por idioma
        self.error_messages = {
            "es": {
                "general": "Ha ocurrido un error inesperado.",
                "missing_info": "Falta información necesaria.",
                "not_found": "No se encontró lo que buscas.",
                "validation": "Los datos no son válidos.",
                "timeout": "La operación ha tardado demasiado.",
            },
            "en": {
                "general": "An unexpected error occurred.",
                "missing_info": "Missing required information.",
                "not_found": "Could not find what you're looking for.",
                "validation": "The data is not valid.",
                "timeout": "The operation took too long.",
            }
        }
    
    
    def format_success(self, message: str, details: Optional[Dict] = None) -> str:
        """
        Formatea un mensaje de éxito.
        
        Args:
            message: Mensaje principal
            details: Detalles opcionales
            
        Returns:
            Mensaje formateado con emoji
        """
        response = f"{self.emojis['success']} {message}"
        
        if details:
            response += "\n\n"
            for key, value in details.items():
                emoji = self._get_emoji_for_field(key)
                response += f"{emoji} **{key.title()}:** {value}\n"
        
        return response
    
    
    def format_error(
        self, 
        error_message: str, 
        error_type: str = "general"
    ) -> str:
        """
        Formatea un mensaje de error.
        
        Args:
            error_message: Mensaje de error específico
            error_type: Tipo de error (general, missing_info, etc.)
            
        Returns:
            Mensaje de error formateado
        """
        base_message = self.error_messages.get(
            self.language, 
            self.error_messages["es"]
        ).get(error_type, self.error_messages["es"]["general"])
        
        return f"{self.emojis['error']} {base_message}\n\n{error_message}"
    
    
    def format_info(self, message: str, items: Optional[List[str]] = None) -> str:
        """
        Formatea un mensaje informativo.
        
        Args:
            message: Mensaje principal
            items: Lista de items opcional
            
        Returns:
            Mensaje formateado
        """
        response = f"{self.emojis['info']} {message}"
        
        if items:
            response += "\n\n"
            for item in items:
                response += f"• {item}\n"
        
        return response
    
    
    def format_question(
        self, 
        question: str, 
        options: Optional[List[str]] = None
    ) -> str:
        """
        Formatea una pregunta al usuario.
        
        Args:
            question: Pregunta a hacer
            options: Opciones disponibles
            
        returns:
            Pregunta formateada
        """
        response = f"{self.emojis['question']} {question}"
        
        if options:
            response += "\n\n"
            for i, option in enumerate(options, 1):
                response += f"{i}. {option}\n"
        
        return response
    
    
    def format_event(self, event: Dict[str, Any]) -> str:
        """
        Formatea un evento de agenda.
        
        Args:
            event: Dict con datos del evento
            
        Returns:
            Evento formateado
        """
        response = f"{self.emojis['calendar']} **Evento**\n\n"
        
        if "title" in event:
            response += f"📝 **Título:** {event['title']}\n"
        
        if "datetime" in event or "date" in event:
            dt = event.get("datetime") or event.get("date")
            response += f"📅 **Fecha:** {self._format_datetime(dt)}\n"
        
        if "time" in event:
            response += f"🕐 **Hora:** {event['time']}\n"
        
        if "location" in event:
            response += f"📍 **Lugar:** {event['location']}\n"
        
        if "participants" in event:
            response += f"👤 **Participantes:** {', '.join(event['participants'])}\n"
        
        if "id" in event:
            response += f"\n🆔 ID: #{event['id']}"
        
        return response
    
    
    def format_event_list(self, events: List[Dict[str, Any]]) -> str:
        """
        Formatea una lista de eventos.
        
        Args:
            events: Lista de eventos
            
        Returns:
            Lista formateada
        """
        if not events:
            return f"{self.emojis['info']} No hay eventos para mostrar."
        
        response = f"{self.emojis['calendar']} **Eventos ({len(events)})**\n\n"
        
        for i, event in enumerate(events, 1):
            title = event.get("title", "Sin título")
            dt = event.get("datetime") or event.get("date", "")
            event_id = event.get("id", "")
            
            response += f"{i}. **{title}**\n"
            if dt:
                response += f"   📅 {self._format_datetime(dt)}\n"
            if event_id:
                response += f"   🆔 #{event_id}\n"
            response += "\n"
        
        return response
    
    
    def format_note(self, note: Dict[str, Any]) -> str:
        """
        Formatea una nota.
        
        Args:
            note: Dict con datos de la nota
            
        Returns:
            Nota formateada
        """
        response = f"{self.emojis['note']} **Nota**\n\n"
        
        if "title" in note:
            response += f"📝 **Título:** {note['title']}\n"
        
        if "content" in note:
            response += f"\n{note['content']}\n"
        
        if "created_at" in note:
            response += f"\n📅 Creada: {self._format_datetime(note['created_at'])}\n"
        
        if "id" in note:
            response += f"🆔 ID: #{note['id']}"
        
        return response
    
    
    def format_reminder(self, reminder: Dict[str, Any]) -> str:
        """
        Formatea un recordatorio.
        
        Args:
            reminder: Dict con datos del recordatorio
            
        Returns:
            Recordatorio formateado
        """
        response = f"{self.emojis['reminder']} **Recordatorio**\n\n"
        
        if "message" in reminder:
            response += f"📝 {reminder['message']}\n"
        
        if "datetime" in reminder:
            response += f"\n⏰ {self._format_datetime(reminder['datetime'])}\n"
        
        if "id" in reminder:
            response += f"🆔 ID: #{reminder['id']}"
        
        return response
    
    
    def format_missing_info_prompt(
        self, 
        missing_fields: List[str], 
        context_type: str = "event"
    ) -> str:
        """
        Genera prompt pidiendo información faltante.
        
        Args:
            missing_fields: Campos que faltan
            context_type: Tipo de contexto (event, note, reminder)
            
        Returns:
            Prompt formateado
        """
        if self.language == "es":
            field_names = {
                "title": "título",
                "datetime": "fecha y hora",
                "date": "fecha",
                "time": "hora",
                "location": "ubicación",
                "content": "contenido",
                "description": "descripción",
            }
            
            intro = "Para completar, necesito:"
        else:
            field_names = {
                "title": "title",
                "datetime": "date and time",
                "date": "date",
                "time": "time",
                "location": "location",
                "content": "content",
                "description": "description",
            }
            
            intro = "To complete, I need:"
        
        response = f"{self.emojis['question']} {intro}\n\n"
        
        for field in missing_fields:
            field_name = field_names.get(field, field)
            emoji = self._get_emoji_for_field(field)
            response += f"{emoji} {field_name.title()}\n"
        
        return response
    
    
    def format_help(self, commands: List[Dict[str, str]]) -> str:
        """
        Formatea mensaje de ayuda con comandos disponibles.
        
        Args:
            commands: Lista de comandos con descripción
            
        Returns:
            Mensaje de ayuda formateado
        """
        response = f"{self.emojis['help']} **Comandos disponibles**\n\n"
        
        for cmd in commands:
            name = cmd.get("name", "")
            desc = cmd.get("description", "")
            example = cmd.get("example", "")
            
            response += f"• **{name}**\n"
            response += f"  {desc}\n"
            if example:
                response += f"  _Ejemplo: {example}_\n"
            response += "\n"
        
        return response
    
    
    def _format_datetime(self, dt: Any) -> str:
        """
        Formatea fecha/hora de manera legible.
        
        Args:
            dt: Datetime object o string
            
        Returns:
            String formateado
        """
        if isinstance(dt, datetime):
            if self.language == "es":
                return dt.strftime("%d/%m/%Y %H:%M")
            else:
                return dt.strftime("%m/%d/%Y %I:%M %p")
        
        return str(dt)
    
    
    def _get_emoji_for_field(self, field: str) -> str:
        """
        Obtiene emoji apropiado para un campo.
        
        Args:
            field: Nombre del campo
            
        Returns:
            Emoji correspondiente
        """
        field_emojis = {
            "title": "📝",
            "datetime": "📅",
            "date": "📅",
            "time": "🕐",
            "location": "📍",
            "participants": "👤",
            "id": "🆔",
            "content": "📝",
            "description": "📝",
        }
        
        return field_emojis.get(field.lower(), self.emojis["info"])
