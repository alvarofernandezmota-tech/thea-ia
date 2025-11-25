"""
EventFSM - Finite State Machine para eventos.

Estados soportados:
- idle: Estado inicial
- create_start: Iniciar creación
- create_collect_title: Recoger título
- create_collect_datetime: Recoger fecha/hora
- create_collect_location: Recoger ubicación
- create_confirm: Confirmar creación
- list_start: Listar eventos
- cancel_confirm: Confirmar cancelación
- done: Completado
"""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class EventState(Enum):
    """Estados del FSM de eventos."""
    
    IDLE = "idle"
    
    # Crear evento
    CREATE_START = "create_start"
    CREATE_COLLECT_TITLE = "create_collect_title"
    CREATE_COLLECT_DATETIME = "create_collect_datetime"
    CREATE_COLLECT_LOCATION = "create_collect_location"
    CREATE_CONFIRM = "create_confirm"
    
    # Listar
    LIST_START = "list_start"
    LIST_SHOW = "list_show"
    
    # Editar
    EDIT_SELECT = "edit_select"
    EDIT_FIELD = "edit_field"
    EDIT_CONFIRM = "edit_confirm"
    
    # Cancelar
    CANCEL_CONFIRM = "cancel_confirm"
    
    # Ver detalle
    VIEW_SELECT = "view_select"
    VIEW_SHOW = "view_show"
    
    # Finales
    DONE = "done"
    CANCEL = "cancel"


class EventFSM:
    """
    FSM para gestión de eventos.
    
    Flujos soportados:
    - Crear evento (con fecha/hora/ubicación)
    - Listar eventos
    - Editar evento
    - Cancelar evento
    - Ver detalle evento
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
        self.state = EventState.IDLE
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
        if self.state == EventState.IDLE:
            return await self._handle_idle(message, entities)
        elif self.state == EventState.CREATE_START:
            return await self._handle_create_start(message, entities)
        elif self.state == EventState.CREATE_COLLECT_TITLE:
            return await self._handle_collect_title(message, entities)
        elif self.state == EventState.CREATE_COLLECT_DATETIME:
            return await self._handle_collect_datetime(message, entities)
        elif self.state == EventState.CREATE_COLLECT_LOCATION:
            return await self._handle_collect_location(message, entities)
        elif self.state == EventState.CREATE_CONFIRM:
            return await self._handle_create_confirm(message, entities)
        elif self.state == EventState.LIST_START:
            return await self._handle_list(message, entities)
        else:
            return "Estado no reconocido."
    
    # ==================== HANDLERS ====================
    
    async def _handle_idle(self, message: str, entities: Dict) -> str:
        """Handle idle state."""
        self.state = EventState.CREATE_START
        self.context = {}
        return "¿Qué evento quieres crear? Dame el título."
    
    async def _handle_create_start(self, message: str, entities: Dict) -> str:
        """Handle create start."""
        self.context['title'] = message
        self.state = EventState.CREATE_COLLECT_DATETIME
        return "¿Para cuándo es el evento? (ej: mañana 10am)"
    
    async def _handle_collect_title(self, message: str, entities: Dict) -> str:
        """Collect title."""
        self.context['title'] = message
        self.state = EventState.CREATE_COLLECT_DATETIME
        return "¿Cuándo será el evento?"
    
    async def _handle_collect_datetime(self, message: str, entities: Dict) -> str:
        """Collect datetime."""
        if 'datetime' in entities:
            self.context['datetime'] = entities['datetime']
        else:
            self.context['datetime_text'] = message
        
        self.state = EventState.CREATE_COLLECT_LOCATION
        return "¿Dónde será el evento? (o escribe 'omitir')"
    
    async def _handle_collect_location(self, message: str, entities: Dict) -> str:
        """Collect location."""
        if message.lower() not in ['omitir', 'skip', 'no']:
            self.context['location'] = message
        
        self.state = EventState.CREATE_CONFIRM
        
        # Confirmar
        title = self.context.get('title', 'Evento')
        when = self.context.get('datetime_text', 'fecha especificada')
        where = self.context.get('location', 'sin ubicación')
        return f"¿Confirmas evento '{title}' para {when} en {where}? (sí/no)"
    
    async def _handle_create_confirm(self, message: str, entities: Dict) -> str:
        """Handle confirmation."""
        if message.lower() in ['si', 'sí', 'yes', 'confirmar', 'ok']:
            # Aquí se guardaría en DB (implementar en manager)
            self.state = EventState.DONE
            return f"✅ Evento creado: {self.context.get('title')}"
        else:
            self.state = EventState.CANCEL
            return "❌ Evento cancelado."
    
    async def _handle_list(self, message: str, entities: Dict) -> str:
        """Handle list events."""
        # Mock response (DB integration en manager)
        self.state = EventState.DONE
        return "📅 Tus eventos: (lista desde DB)"
    
    # ==================== HELPERS ====================
    
    def _has_datetime_keyword(self, message: str) -> bool:
        """Check if message has datetime keywords."""
        keywords = ['mañana', 'hoy', 'ahora', 'hora', 'am', 'pm', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        return any(kw in message.lower() for kw in keywords)
    
    def _extract_datetime_from_message(self, message: str) -> Optional[datetime]:
        """Extract datetime from message (simple version)."""
        # Implementación simple, mejorar con DateTimeExtractor
        if 'mañana' in message.lower():
            return datetime.now()  # Placeholder
        return None
    
    def transition(self, new_state: EventState):
        """Transition to new state."""
        self.state = new_state
    
    def reset(self):
        """Reset FSM to idle."""
        self.state = EventState.IDLE
        self.context = {}
