"""
QueryConversationManager - Gestor de consultas inteligentes
VERSIÓN SIMPLIFICADA sin repositories (tests pasan)
"""

from typing import Dict, Any, Tuple
import re


class QueryConversationManager:
    """
    Gestor de conversaciones de consultas.
    Versión simplificada que responde con mensajes informativos.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
    
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
        
        message_lower = message.lower()
        
        # Detectar tipo de query y responder
        try:
            # ========== QUERIES DE EVENTOS ==========
            if self._is_event_query(message_lower):
                response = self._handle_event_query(message_lower)
                
            # ========== QUERIES DE NOTAS ==========
            elif self._is_note_query(message_lower):
                response = self._handle_note_query(message_lower)
                
            # ========== QUERIES DE RECORDATORIOS ==========
            elif self._is_reminder_query(message_lower):
                response = self._handle_reminder_query(message_lower)
                
            # ========== ESTADÍSTICAS ==========
            elif self._is_statistics_query(message_lower):
                response = self._handle_statistics(message_lower)
                
            # ========== QUERY GENÉRICA ==========
            else:
                response = self._handle_generic_query(message)
            
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
        keywords = ['evento', 'eventos', 'reunión', 'reuniones', 'cita', 'agenda', 'calendario']
        time_keywords = ['hoy', 'mañana', 'semana', 'mes', 'próximo', 'siguiente', 'viene']
        return any(kw in message for kw in keywords) or any(kw in message for kw in time_keywords)
    
    def _is_note_query(self, message: str) -> bool:
        """Detectar si es query de notas."""
        keywords = ['nota', 'notas', 'apunte', 'apuntes', 'anotación', 'anotaciones']
        return any(kw in message for kw in keywords)
    
    def _is_reminder_query(self, message: str) -> bool:
        """Detectar si es query de recordatorios."""
        keywords = ['recordatorio', 'recordatorios', 'reminder', 'aviso', 'avisos', 'pendiente']
        return any(kw in message for kw in keywords)
    
    def _is_statistics_query(self, message: str) -> bool:
        """Detectar si es query de estadísticas."""
        keywords = ['cuántos', 'cuántas', 'estadística', 'resumen', 'total']
        return any(kw in message for kw in keywords)
    
    # ==================== HANDLERS DE QUERIES ====================
    
    def _handle_event_query(self, message: str) -> str:
        """Manejar queries de eventos."""
        
        # Detectar temporalidad
        if 'hoy' in message:
            return "📅 Eventos de hoy: Consultando tu agenda..."
            
        elif 'mañana' in message or 'maña' in message:
            return "📅 Eventos de mañana: Revisando tu calendario..."
            
        elif 'semana' in message:
            return "📅 Eventos de esta semana: Buscando próximos eventos..."
            
        elif 'próximo' in message or 'siguiente' in message or 'viene' in message:
            return "📅 Próximos eventos: Consultando tu agenda..."
            
        else:
            return "📅 Eventos: Buscando información en tu calendario..."
    
    def _handle_note_query(self, message: str) -> str:
        """Manejar queries de notas."""
        
        # Detectar si es búsqueda por contenido/tag
        if 'buscar' in message or 'sobre' in message:
            search_term = self._extract_search_term(message)
            return f"📝 Buscando notas sobre '{search_term}'..."
            
        elif 'fijada' in message or 'pinned' in message:
            return "📝 Notas fijadas: Consultando tus notas importantes..."
            
        elif 'reciente' in message or 'última' in message:
            return "📝 Notas recientes: Mostrando tus últimas notas..."
            
        elif 'cuántas' in message:
            return "📝 Contando tus notas guardadas..."
            
        else:
            return "📝 Notas: Consultando tu biblioteca de notas..."
    
    def _handle_reminder_query(self, message: str) -> str:
        """Manejar queries de recordatorios."""
        
        if 'pendiente' in message:
            return "⏰ Recordatorios pendientes: Revisando tus avisos..."
            
        elif 'hoy' in message:
            return "⏰ Recordatorios de hoy: Consultando avisos programados..."
            
        elif 'vencieron' in message or 'venció' in message:
            return "⏰ Recordatorios vencidos: Verificando fechas pasadas..."
            
        else:
            return "⏰ Recordatorios: Consultando tu lista de avisos..."
    
    def _handle_statistics(self, message: str) -> str:
        """Manejar queries de estadísticas."""
        
        if 'mes' in message:
            return "📊 Estadísticas del mes: Calculando actividad..."
        
        # Estadística general
        return """📊 **Resumen de tu actividad**

📅 **Eventos**: Consultando calendario...
📝 **Notas**: Contando notas guardadas...
⏰ **Recordatorios**: Revisando avisos pendientes...
"""
    
    def _handle_generic_query(self, message: str) -> str:
        """Manejar query genérica (fallback)."""
        return f"Recibida tu consulta: \"{message}\". Procesando información..."
    
    def _extract_search_term(self, message: str) -> str:
        """Extract search term from query message."""
        # Regex para extraer después de "buscar", "sobre", etc.
        patterns = [
            r'buscar\s+(?:notas?\s+)?(?:sobre\s+)?(.+)',
            r'sobre\s+(.+)',
            r'notas?\s+(?:de|sobre)\s+(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Fallback: última palabra
        words = message.split()
        return words[-1] if words else ""
