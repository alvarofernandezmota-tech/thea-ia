"""
ReminderFSM - Finite State Machine para recordatorios.

Estados soportados:
- idle: Estado inicial
- create_start: Iniciar creación
- create_collect_title: Recoger título
- create_collect_datetime: Recoger fecha/hora
- create_confirm: Confirmar creación
- list_start: Listar recordatorios
- complete_confirm: Confirmar completado
- delete_confirm: Confirmar eliminación
- done: Completado
"""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class ReminderState(Enum):
    """Estados del FSM de recordatorios."""
    
    IDLE = "idle"
    
    # Crear recordatorio
    CREATE_START = "create_start"
    CREATE_COLLECT_TITLE = "create_collect_title"
    CREATE_COLLECT_DATETIME = "create_collect_datetime"
    CREATE_COLLECT_LOCATION = "create_collect_location"  # Opcional
    CREATE_CONFIRM = "create_confirm"
    
    # Listar
    LIST_START = "list_start"
    LIST_SHOW = "list_show"
    
    # Editar
    EDIT_SELECT = "edit_select"
    EDIT_FIELD = "edit_field"
    EDIT_CONFIRM = "edit_confirm"
    
    # Completar/Eliminar
    COMPLETE_CONFIRM = "complete_confirm"
    DELETE_CONFIRM = "delete_confirm"
    
    # Finales
    DONE = "done"
    CANCEL = "cancel"


class ReminderFSM:
    """
    FSM para gestión de recordatorios.
    
    Flujos soportados:
    - Crear recordatorio (con fecha/hora/ubicación)
    - Listar recordatorios
    - Editar recordatorio
    - Completar recordatorio
    - Eliminar recordatorio
    """
    
    def __init__(self, user_id: str, tenant_id: str):
        """
        Initialize FSM.
        
        Args:
            user_id: User ID
            tenant_id: Tenant ID
        """
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.state = ReminderState.IDLE
        self.context: Dict[str, Any] = {}
    
    async def handle(
        self, 
        message: str, 
        entities: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> str:
        """
        Handle message según estado actual.
        
        Args:
            message: User message
            entities: Extracted entities (datetime, location, etc.)
            context: Conversation context
            
        Returns:
            str: Response message
        """
        # Auto-extract datetime si no viene
        if 'datetime' not in entities and self._has_datetime_keyword(message):
            entities['datetime'] = self._extract_datetime_from_message(message)
        
        # Route por estado
        if self.state == ReminderState.IDLE:
            return await self._handle_idle(message, entities)
        elif self.state == ReminderState.CREATE_START:
            return await self._handle_create_start(message, entities)
        elif self.state == ReminderState.CREATE_COLLECT_TITLE:
            return await self._handle_collect_title(message, entities)
        elif self.state == ReminderState.CREATE_COLLECT_DATETIME:
            return await self._handle_collect_datetime(message, entities)
        elif self.state == ReminderState.CREATE_CONFIRM:
            return await self._handle_create_confirm(message, entities)
        elif self.state == ReminderState.LIST_START:
            return await self._handle_list(message, entities)
        else:
            return "Estado no reconocido."
    
    # ==================== HANDLERS ====================
    
    async def _handle_idle(self, message: str, entities: Dict) -> str:
        """Handle idle state."""
        self.state = ReminderState.CREATE_START
        self.context = {}
        return "¿Qué recordatorio quieres crear? Dame el título."
    
    async def _handle_create_start(self, message: str, entities: Dict) -> str:
        """Handle create start."""
        self.context['title'] = message
        self.state = ReminderState.CREATE_COLLECT_DATETIME
        return "¿Para cuándo es el recordatorio? (ej: mañana 10am)"
    
    async def _handle_collect_title(self, message: str, entities: Dict) -> str:
        """Collect title."""
        self.context['title'] = message
        self.state = ReminderState.CREATE_COLLECT_DATETIME
        return "¿Cuándo quieres que te lo recuerde?"
    
    async def _handle_collect_datetime(self, message: str, entities: Dict) -> str:
        """Collect datetime."""
        if 'datetime' in entities:
            self.context['datetime'] = entities['datetime']
        else:
            self.context['datetime_text'] = message
        
        self.state = ReminderState.CREATE_CONFIRM
        
        # Confirmar
        title = self.context.get('title', 'Recordatorio')
        when = self.context.get('datetime_text', message)
        return f"¿Confirmas recordatorio '{title}' para {when}? (sí/no)"
    
    async def _handle_create_confirm(self, message: str, entities: Dict) -> str:
        """Handle confirmation."""
        if message.lower() in ['si', 'sí', 'yes', 'confirmar', 'ok']:
            # Aquí se guardaría en DB
            self.state = ReminderState.DONE
            return f"✅ Recordatorio creado: {self.context.get('title')}"
        else:
            self.state = ReminderState.CANCEL
            return "❌ Recordatorio cancelado."
    
    async def _handle_list(self, message: str, entities: Dict) -> str:
        """Handle list reminders."""
        # Mock response (DB integration en H05)
        self.state = ReminderState.DONE
        return "📋 Tus recordatorios: (pendiente implementar lista real)"
    
    # ==================== HELPERS ====================
    
    def _has_datetime_keyword(self, message: str) -> bool:
        """Check if message has datetime keywords."""
        keywords = ['mañana', 'hoy', 'ahora', 'hora', 'am', 'pm', 'lunes', 'martes']
        return any(kw in message.lower() for kw in keywords)
    
    def _extract_datetime_from_message(self, message: str) -> Optional[datetime]:
        """Extract datetime from message (simple version)."""
        # Implementación simple, mejorar con DateTimeExtractor
        if 'mañana' in message.lower():
            return datetime.now()  # Placeholder
        return None
    
    def transition(self, new_state: ReminderState):
        """Transition to new state."""
        self.state = new_state
    
    def reset(self):
        """Reset FSM to idle."""
        self.state = ReminderState.IDLE
        self.context = {}
