"""
QueryConversationManager - Gestor de consultas inteligentes
Coordina búsquedas en eventos, notas, recordatorios
"""

from typing import Dict, Any, Tuple, List
from datetime import datetime, timedelta
import re

# Repositories (ajusta imports según tu estructura)
try:
    from src.theaia.database.repositories.event_repository import EventRepository
    from src.theaia.database.repositories.note_repository import NoteRepository
    # from src.theaia.database.repositories.reminder_repository import ReminderRepository
except ImportError:
    # Fallback si no existen aún
    EventRepository = None
    NoteRepository = None


class QueryConversationManager:
    """
    Gestor de conversaciones de consultas.
    Maneja búsquedas sin FSM complejo (stateless queries).
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        
        # Initialize repositories si existen
        self.event_repo = EventRepository() if EventRepository else None
        self.note_repo = NoteRepository() if NoteRepository else None
        # self.reminder_repo = ReminderRepository() if ReminderRepository else None
    
    def handle_message(
        self, 
        user_id: str, 
        message: str, 
        context: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Handle query message y ejecutar búsqueda correspondiente.
        
        Args:
            user_id: User ID
            message: User query
            context: Conversation context
            
        Returns:
            (response, new_state, updated_context)
        """
        
        tenant_id = context.get('tenant_id', 'default')
        message_lower = message.lower()
        
        # Detectar tipo de query y ejecutar
        try:
            # ========== QUERIES DE EVENTOS ==========
            if self._is_event_query(message_lower):
                response = self._handle_event_query(message_lower, user_id, tenant_id)
                
            # ========== QUERIES DE NOTAS ==========
            elif self._is_note_query(message_lower):
                response = self._handle_note_query(message_lower, user_id, tenant_id)
                
            # ========== QUERIES DE RECORDATORIOS ==========
            elif self._is_reminder_query(message_lower):
                response = self._handle_reminder_query(message_lower, user_id, tenant_id)
                
            # ========== ESTADÍSTICAS ==========
            elif self._is_statistics_query(message_lower):
                response = self._handle_statistics(message_lower, user_id, tenant_id)
                
            # ========== QUERY GENÉRICA ==========
            else:
                response = self._handle_generic_query(message, user_id, tenant_id)
            
            new_state = "completed"
            context["last_query"] = message
            context["fsm_state"] = "completed"
            
        except Exception as e:
            response = f"Error procesando tu consulta: {str(e)}"
            new_state = "error"
        
        return response, new_state, context
    
    # ==================== DETECCIÓN DE QUERIES ====================
    
    def _is_event_query(self, message: str) -> bool:
        """Detectar si es query de eventos."""
        keywords = ['evento', 'eventos', 'reunión', 'cita', 'agenda', 'calendario']
        time_keywords = ['hoy', 'mañana', 'semana', 'mes', 'próximo', 'siguiente']
        return any(kw in message for kw in keywords) or any(kw in message for kw in time_keywords)
    
    def _is_note_query(self, message: str) -> bool:
        """Detectar si es query de notas."""
        keywords = ['nota', 'notas', 'apunte', 'apuntes', 'anotación']
        return any(kw in message for kw in keywords)
    
    def _is_reminder_query(self, message: str) -> bool:
        """Detectar si es query de recordatorios."""
        keywords = ['recordatorio', 'recordatorios', 'reminder', 'aviso']
        return any(kw in message for kw in keywords)
    
    def _is_statistics_query(self, message: str) -> bool:
        """Detectar si es query de estadísticas."""
        keywords = ['cuántos', 'cuántas', 'estadística', 'resumen', 'total']
        return any(kw in message for kw in keywords)
    
    # ==================== HANDLERS DE QUERIES ====================
    
    def _handle_event_query(self, message: str, user_id: str, tenant_id: str) -> str:
        """Manejar queries de eventos."""
        
        if not self.event_repo:
            return "⚠️ Sistema de eventos no disponible temporalmente."
        
        try:
            # Detectar temporalidad
            if 'hoy' in message:
                events = self._get_events_today(user_id, tenant_id)
                return self._format_events_response(events, "hoy")
                
            elif 'mañana' in message or 'maña' in message:
                events = self._get_events_tomorrow(user_id, tenant_id)
                return self._format_events_response(events, "mañana")
                
            elif 'semana' in message:
                events = self._get_events_week(user_id, tenant_id)
                return self._format_events_response(events, "esta semana")
                
            elif 'próximo' in message or 'siguiente' in message or 'viene' in message:
                events = self._get_events_upcoming(user_id, tenant_id, limit=5)
                return self._format_events_response(events, "próximamente")
                
            else:
                # Query genérica de eventos
                events = self._get_events_upcoming(user_id, tenant_id, limit=10)
                return self._format_events_response(events, "")
                
        except Exception as e:
            return f"Error buscando eventos: {str(e)}"
    
    def _handle_note_query(self, message: str, user_id: str, tenant_id: str) -> str:
        """Manejar queries de notas."""
        
        if not self.note_repo:
            return "⚠️ Sistema de notas no disponible temporalmente."
        
        try:
            # Detectar si es búsqueda por contenido
            if 'buscar' in message or 'sobre' in message:
                # Extraer término de búsqueda
                search_term = self._extract_search_term(message)
                notes = self._search_notes(search_term, user_id, tenant_id)
                return self._format_notes_response(notes, f"sobre '{search_term}'")
                
            elif 'reciente' in message or 'última' in message:
                notes = self._get_notes_recent(user_id, tenant_id, limit=5)
                return self._format_notes_response(notes, "recientes")
                
            elif 'cuántas' in message:
                count = self._count_notes(user_id, tenant_id)
                return f"📝 Tienes {count} nota{'s' if count != 1 else ''} guardada{'s' if count != 1 else ''}."
                
            else:
                # Listar notas generales
                notes = self._get_notes_recent(user_id, tenant_id, limit=10)
                return self._format_notes_response(notes, "")
                
        except Exception as e:
            return f"Error buscando notas: {str(e)}"
    
    def _handle_reminder_query(self, message: str, user_id: str, tenant_id: str) -> str:
        """Manejar queries de recordatorios."""
        
        # Por ahora mock (hasta que ReminderRepository exista)
        if 'pendiente' in message:
            return "⏰ No tienes recordatorios pendientes."
        elif 'hoy' in message:
            return "⏰ No tienes recordatorios programados para hoy."
        elif 'vencieron' in message or 'venció' in message:
            return "⏰ No tienes recordatorios vencidos."
        else:
            return "⏰ Sistema de recordatorios (próximamente disponible)."
    
    def _handle_statistics(self, message: str, user_id: str, tenant_id: str) -> str:
        """Manejar queries de estadísticas."""
        
        try:
            stats = {
                'events': self._count_events(user_id, tenant_id) if self.event_repo else 0,
                'events_today': self._count_events_today(user_id, tenant_id) if self.event_repo else 0,
                'notes': self._count_notes(user_id, tenant_id) if self.note_repo else 0,
                'reminders': 0  # Placeholder
            }
            
            if 'mes' in message:
                events_month = self._count_events_month(user_id, tenant_id) if self.event_repo else 0
                return f"📊 Este mes tienes {events_month} eventos programados."
            
            # Estadística general
            response = f"""📊 **Resumen de tu actividad**

📅 **Eventos**: {stats['events']} total ({stats['events_today']} hoy)
📝 **Notas**: {stats['notes']} guardadas
⏰ **Recordatorios**: {stats['reminders']} pendientes
"""
            return response
            
        except Exception as e:
            return f"Error calculando estadísticas: {str(e)}"
    
    def _handle_generic_query(self, message: str, user_id: str, tenant_id: str) -> str:
        """Manejar query genérica (fallback)."""
        return f"Recibida tu consulta: \"{message}\". Buscaré la información correspondiente."
    
    # ==================== HELPERS DE EVENTOS ====================
    
    def _get_events_today(self, user_id: str, tenant_id: str) -> List:
        """Get events for today."""
        if not self.event_repo:
            return []
        today = datetime.now().date()
        # Ajusta según tu API de EventRepository
        return []  # self.event_repo.get_by_date(today, tenant_id, user_id)
    
    def _get_events_tomorrow(self, user_id: str, tenant_id: str) -> List:
        """Get events for tomorrow."""
        if not self.event_repo:
            return []
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        return []  # self.event_repo.get_by_date(tomorrow, tenant_id, user_id)
    
    def _get_events_week(self, user_id: str, tenant_id: str) -> List:
        """Get events for this week."""
        if not self.event_repo:
            return []
        # Implementar según tu repo
        return []
    
    def _get_events_upcoming(self, user_id: str, tenant_id: str, limit: int = 10) -> List:
        """Get upcoming events."""
        if not self.event_repo:
            return []
        # Implementar según tu repo
        return []
    
    def _count_events(self, user_id: str, tenant_id: str) -> int:
        """Count total events."""
        if not self.event_repo:
            return 0
        return 0  # self.event_repo.count(tenant_id, user_id)
    
    def _count_events_today(self, user_id: str, tenant_id: str) -> int:
        """Count events today."""
        return len(self._get_events_today(user_id, tenant_id))
    
    def _count_events_month(self, user_id: str, tenant_id: str) -> int:
        """Count events this month."""
        if not self.event_repo:
            return 0
        return 0  # Implementar
    
    # ==================== HELPERS DE NOTAS ====================
    
    def _get_notes_recent(self, user_id: str, tenant_id: str, limit: int = 10) -> List:
        """Get recent notes."""
        if not self.note_repo:
            return []
        return []  # self.note_repo.get_recent(tenant_id, user_id, limit)
    
    def _search_notes(self, query: str, user_id: str, tenant_id: str) -> List:
        """Search notes by content."""
        if not self.note_repo:
            return []
        return []  # self.note_repo.search(query, tenant_id, user_id)
    
    def _count_notes(self, user_id: str, tenant_id: str) -> int:
        """Count total notes."""
        if not self.note_repo:
            return 0
        return 0  # self.note_repo.count(tenant_id, user_id)
    
    # ==================== FORMATTERS ====================
    
    def _format_events_response(self, events: List, timeframe: str) -> str:
        """Format events list as user response."""
        if not events:
            return f"📅 No tienes eventos {timeframe}." if timeframe else "📅 No tienes eventos."
        
        response = f"📅 **Eventos {timeframe}**:\n\n" if timeframe else "📅 **Tus eventos**:\n\n"
        for event in events[:10]:  # Limit to 10
            # Ajusta según tu modelo Event
            title = getattr(event, 'title', 'Sin título')
            date = getattr(event, 'date', datetime.now())
            response += f"• {title} - {date}\n"
        
        if len(events) > 10:
            response += f"\n... y {len(events) - 10} más."
        
        return response
    
    def _format_notes_response(self, notes: List, context: str) -> str:
        """Format notes list as user response."""
        if not notes:
            return f"📝 No encontré notas {context}." if context else "📝 No tienes notas."
        
        response = f"📝 **Notas {context}**:\n\n" if context else "📝 **Tus notas**:\n\n"
        for note in notes[:10]:  # Limit to 10
            title = getattr(note, 'title', 'Sin título')
            content = getattr(note, 'content', '')
            preview = content[:50] + "..." if len(content) > 50 else content
            response += f"• **{title}**: {preview}\n"
        
        if len(notes) > 10:
            response += f"\n... y {len(notes) - 10} más."
        
        return response
    
    def _extract_search_term(self, message: str) -> str:
        """Extract search term from query message."""
        # Regex para extraer después de "buscar", "sobre", etc.
        patterns = [
            r'buscar\s+(?:notas?\s+)?(?:sobre\s+)?(.+)',
            r'sobre\s+(.+)',
            r'notas?\s+de\s+(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Fallback: última palabra
        words = message.split()
        return words[-1] if words else ""
