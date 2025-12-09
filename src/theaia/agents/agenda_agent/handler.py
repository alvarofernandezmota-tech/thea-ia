"""
Handlers para AgendaAgent - Funciones auxiliares

Este módulo contiene helpers para procesar intents específicos:
- Extracción de entidades
- Validación de datos
- Acceso a repositorio (cuando esté disponible)
- Formateo de respuestas

Autor: Álvaro Fernández Mota
Fecha: 09 Dic 2025
"""

from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger(__name__)


class EventEntityExtractor:
    """Extrae entidades de evento del mensaje"""
    
    @staticmethod
    def extract_title(message: str) -> Optional[str]:
        """
        Extrae el título del evento del mensaje.
        
        Ejemplos:
            "agendar reunión de seguimiento" → "reunión de seguimiento"
            "crear evento llamado 'Sprint Planning'" → "Sprint Planning"
        
        TODO: Implementar en A.3
        """
        # Placeholder: por ahora retorna None
        return None
    
    
    @staticmethod
    def extract_date(message: str) -> Optional[datetime]:
        """
        Extrae la fecha del evento.
        
        Ejemplos:
            "mañana" → tomorrow
            "próximo lunes" → next Monday
            "el 15 de enero" → Jan 15
            "en 3 días" → today + 3 days
        
        TODO: Implementar en A.3 (usar DateTimeParser)
        """
        # Placeholder
        return None
    
    
    @staticmethod
    def extract_time(message: str) -> Optional[str]:
        """
        Extrae la hora del evento.
        
        Ejemplos:
            "a las 3pm" → "15:00"
            "las 3 de la tarde" → "15:00"
            "15:00" → "15:00"
        
        TODO: Implementar en A.3
        """
        # Placeholder
        return None
    
    
    @staticmethod
    def extract_participants(message: str) -> List[str]:
        """
        Extrae participantes del evento.
        
        Ejemplos:
            "con Juan y María" → ["Juan", "María"]
            "invitar a juan@email.com" → ["juan@email.com"]
        
        TODO: Implementar en A.3
        """
        # Placeholder: retorna lista vacía
        return []
    
    
    @staticmethod
    def extract_location(message: str) -> Optional[str]:
        """
        Extrae ubicación del evento.
        
        Ejemplos:
            "en sala 5" → "sala 5"
            "reunión online" → "online"
        
        TODO: Implementar en A.3
        """
        # Placeholder
        return None
    
    
    @staticmethod
    def extract_description(message: str) -> Optional[str]:
        """
        Extrae descripción del evento.
        
        TODO: Implementar en A.3
        """
        # Placeholder
        return None


class EventValidator:
    """Valida datos de evento"""
    
    @staticmethod
    def validate_event_data(
        title: Optional[str],
        date: Optional[datetime],
        time: Optional[str]
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida que el evento tenga datos mínimos requeridos.
        
        Retorna:
            Tuple (is_valid, error_message)
        """
        if not title or not title.strip():
            return False, "El evento necesita un título"
        
        if not date:
            return False, "Especifica cuándo quieres el evento"
        
        # TODO: Validar más campos cuando A.3 esté completo
        
        return True, None


class EventResponseFormatter:
    """Formatea respuestas del agente"""
    
    @staticmethod
    def format_event_created(
        event_title: str,
        event_date: Optional[datetime],
        event_time: Optional[str]
    ) -> str:
        """Formatea mensaje de evento creado"""
        msg = f"✅ Evento '{event_title}' creado"
        if event_date:
            msg += f" para {event_date.strftime('%d de %B')}"
        if event_time:
            msg += f" a las {event_time}"
        return msg
    
    
    @staticmethod
    def format_events_list(events: List[Dict]) -> str:
        """Formatea listado de eventos"""
        if not events:
            return "📅 No tienes eventos próximos"
        
        msg = "📅 Tus eventos:\n"
        for i, event in enumerate(events, 1):
            title = event.get("title", "Sin título")
            msg += f"{i}. {title}\n"
        
        return msg
    
    
    @staticmethod
    def format_event_updated(event_title: str) -> str:
        """Formatea mensaje de evento actualizado"""
        return f"✏️ Evento '{event_title}' actualizado"
    
    
    @staticmethod
    def format_event_deleted(event_title: str) -> str:
        """Formatea mensaje de evento eliminado"""
        return f"🗑️ Evento '{event_title}' cancelado"


class EventContextBuilder:
    """Construye contexto para el flujo de evento"""
    
    @staticmethod
    def build_create_context(
        message: str,
        entities: Optional[Dict] = None
    ) -> Dict:
        """
        Construye contexto para crear evento.
        
        Contiene:
        - Datos extraídos del mensaje
        - Estado actual
        - Siguiente paso esperado
        """
        entities = entities or {}
        
        context = {
            "action": "create_event",
            "state": "gathering_info",
            "extracted": {
                "title": entities.get("title"),
                "date": entities.get("date"),
                "time": entities.get("time"),
                "participants": entities.get("participants", []),
                "location": entities.get("location"),
            },
            "missing_fields": [],
            "message": message
        }
        
        # Identificar campos faltantes
        if not context["extracted"]["title"]:
            context["missing_fields"].append("title")
        if not context["extracted"]["date"]:
            context["missing_fields"].append("date")
        
        return context
    
    
    @staticmethod
    def build_query_context(
        message: str,
        filters: Optional[Dict] = None
    ) -> Dict:
        """Construye contexto para consultar eventos"""
        filters = filters or {}
        
        return {
            "action": "query_events",
            "state": "searching",
            "filters": {
                "date": filters.get("date"),
                "participant": filters.get("participant"),
                "location": filters.get("location"),
            },
            "message": message
        }
    
    
    @staticmethod
    def build_update_context(event_id: Optional[str] = None) -> Dict:
        """Construye contexto para actualizar evento"""
        return {
            "action": "update_event",
            "state": "identifying_event",
            "event_id": event_id,
            "updates": {}
        }


class EventRepository:
    """
    Interfaz para acceder a eventos en BD.
    
    TODO: Implementar cuando EventService esté disponible
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        # TODO: Conectar a BD real
    
    
    async def create_event(self, event_data: Dict) -> Optional[Dict]:
        """Crear evento en BD"""
        logger.info(f"Creating event for user {self.user_id}")
        # TODO: Implementar en A.5
        return None
    
    
    async def get_events(
        self,
        date_filter: Optional[datetime] = None
    ) -> List[Dict]:
        """Consultar eventos de usuario"""
        logger.info(f"Querying events for user {self.user_id}")
        # TODO: Implementar en A.5
        return []
    
    
    async def update_event(
        self,
        event_id: str,
        updates: Dict
    ) -> Optional[Dict]:
        """Actualizar evento"""
        logger.info(f"Updating event {event_id}")
        # TODO: Implementar en A.5
        return None
    
    
    async def delete_event(self, event_id: str) -> bool:
        """Eliminar evento"""
        logger.info(f"Deleting event {event_id}")
        # TODO: Implementar en A.5
        return True