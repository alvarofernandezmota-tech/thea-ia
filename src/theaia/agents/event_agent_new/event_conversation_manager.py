"""
EventConversationManager - Gestión de conversaciones para eventos
Versión: 1.0.0
Fecha: 25 Noviembre 2025
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime

from src.theaia.agents.event_agent_new.model.event_fsm import EventFSM
from src.theaia.ml.entity_extractor.date_parser import DateTimeExtractor
from src.theaia.ml.entity_extractor.location_extractor import LocationExtractor


class EventConversationManager:
    """
    Gestiona conversaciones para la creación, edición y gestión de eventos.
    
    Responsabilidades:
    - Orquestar FSM para flujos de eventos
    - Extraer entidades (fechas, ubicaciones, participantes)
    - Mantener contexto de conversación
    - Validar datos de eventos
    """
    
    def __init__(self, user_id: str):
        """
        Inicializa el conversation manager para un usuario.
        
        Args:
            user_id: ID único del usuario
        """
        self.user_id = user_id
        self.fsm = EventFSM()
        self.datetime_extractor = DateTimeExtractor()
        self.location_extractor = LocationExtractor()
        self.context: Dict[str, Any] = {}
    
    async def handle_message(
        self,
        user_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Procesa un mensaje del usuario en el contexto de eventos.
        
        Args:
            user_id: ID del usuario
            message: Mensaje del usuario
            context: Contexto actual de la conversación
            
        Returns:
            Tuple[str, str, Dict]: (respuesta, nuevo_estado, nuevo_contexto)
        """
        # Actualizar contexto
        if context:
            self.context.update(context)
        
        current_state = self.context.get("state", "idle")
        
        # Extraer entidades del mensaje
        entities = await self._extract_entities(message)
        self.context.update(entities)
        
        # Procesar según el estado actual
        if current_state == "idle":
            return await self._handle_idle_state(message)
        elif current_state == "awaiting_event_title":
            return await self._handle_awaiting_title(message)
        elif current_state == "awaiting_event_datetime":
            return await self._handle_awaiting_datetime(message, entities)
        elif current_state == "awaiting_event_location":
            return await self._handle_awaiting_location(message, entities)
        elif current_state == "awaiting_event_description":
            return await self._handle_awaiting_description(message)
        elif current_state == "awaiting_confirmation":
            return await self._handle_confirmation(message)
        else:
            return await self._handle_unknown_state()
    
    async def _extract_entities(self, message: str) -> Dict[str, Any]:
        """Extrae entidades relevantes del mensaje."""
        entities = {}
        
        # Extraer fecha/hora
        datetime_info = self.datetime_extractor.extract(message)
        if datetime_info:
            entities["datetime"] = datetime_info
        
        # Extraer ubicación
        location_info = self.location_extractor.extract(message)
        if location_info:
            entities["location"] = location_info
        
        return entities
    
    async def _handle_idle_state(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja el estado inicial."""
        # Transicionar a solicitar título
        new_state = "awaiting_event_title"
        self.context["state"] = new_state
        
        response = "¿Cuál es el título del evento que quieres crear?"
        return response, new_state, self.context
    
    async def _handle_awaiting_title(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja la captura del título del evento."""
        # Guardar título
        self.context["event_title"] = message.strip()
        
        # Transicionar a solicitar fecha/hora
        new_state = "awaiting_event_datetime"
        self.context["state"] = new_state
        
        response = f"Perfecto, '{message.strip()}'. ¿Cuándo será el evento? (fecha y hora)"
        return response, new_state, self.context
    
    async def _handle_awaiting_datetime(
        self,
        message: str,
        entities: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja la captura de fecha/hora."""
        if "datetime" in entities:
            # Guardar fecha/hora
            self.context["event_datetime"] = entities["datetime"]
            
            # Transicionar a solicitar ubicación
            new_state = "awaiting_event_location"
            self.context["state"] = new_state
            
            response = "¿Dónde será el evento? (opcional, puedes decir 'ninguna' o 'online')"
            return response, new_state, self.context
        else:
            # No se pudo extraer fecha, pedir de nuevo
            response = "No pude entender la fecha. Por favor, indícala de nuevo (ej: 'mañana a las 15:00' o '25 de diciembre a las 18:30')"
            return response, "awaiting_event_datetime", self.context
    
    async def _handle_awaiting_location(
        self,
        message: str,
        entities: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja la captura de ubicación."""
        if "location" in entities:
            self.context["event_location"] = entities["location"]
        elif message.lower() in ["ninguna", "online", "virtual", "no"]:
            self.context["event_location"] = "Virtual"
        else:
            self.context["event_location"] = message.strip()
        
        # Transicionar a solicitar descripción
        new_state = "awaiting_event_description"
        self.context["state"] = new_state
        
        response = "¿Quieres agregar una descripción del evento? (opcional, puedes decir 'no' o 'ninguna')"
        return response, new_state, self.context
    
    async def _handle_awaiting_description(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja la captura de descripción."""
        if message.lower() not in ["no", "ninguna", "nada", "skip"]:
            self.context["event_description"] = message.strip()
        else:
            self.context["event_description"] = ""
        
        # Transicionar a confirmación
        new_state = "awaiting_confirmation"
        self.context["state"] = new_state
        
        # Construir resumen
        summary = self._build_event_summary()
        response = f"{summary}\n\n¿Es correcto? (sí/no)"
        return response, new_state, self.context
    
    async def _handle_confirmation(self, message: str) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja la confirmación del evento."""
        if message.lower() in ["sí", "si", "yes", "ok", "confirmar", "correcto"]:
            # Evento confirmado
            new_state = "event_confirmed"
            self.context["state"] = new_state
            self.context["event_confirmed"] = True
            
            response = "✅ Evento creado exitosamente. ¿Quieres crear otro evento?"
            return response, new_state, self.context
        else:
            # Cancelar y reiniciar
            new_state = "idle"
            self.context.clear()
            self.context["state"] = new_state
            
            response = "Evento cancelado. ¿Quieres crear un evento nuevo?"
            return response, new_state, self.context
    
    async def _handle_unknown_state(self) -> Tuple[str, str, Dict[str, Any]]:
        """Maneja estados desconocidos."""
        new_state = "idle"
        self.context["state"] = new_state
        
        response = "Lo siento, algo salió mal. Empecemos de nuevo. ¿Quieres crear un evento?"
        return response, new_state, self.context
    
    def _build_event_summary(self) -> str:
        """Construye un resumen del evento para confirmación."""
        title = self.context.get("event_title", "Sin título")
        datetime_info = self.context.get("event_datetime", "Sin fecha")
        location = self.context.get("event_location", "Sin ubicación")
        description = self.context.get("event_description", "")
        
        summary = f"""
📅 **Resumen del Evento:**

**Título:** {title}
**Fecha/Hora:** {datetime_info}
**Ubicación:** {location}
"""
        
        if description:
            summary += f"**Descripción:** {description}\n"
        
        return summary.strip()
    
    def reset(self):
        """Reinicia el contexto de conversación."""
        self.context.clear()
        self.context["state"] = "idle"
    
    def get_context(self) -> Dict[str, Any]:
        """Obtiene el contexto actual."""
        return self.context.copy()
    
    def set_context(self, context: Dict[str, Any]):
        """Establece el contexto."""
        self.context = context.copy()
