"""
Event Tools - Herramientas para AgendaAgent
Tools que el agente usa para interactuar con eventos

UPGRADE v1.0 → v1.1 (04 DIC 2025):
- ✅ user_id y tenant_id ahora son opcionales en __init__
- ✅ Se pueden configurar después vía set_context()
- ✅ Backward compatible con uso directo

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025 (H03 PHASE 1 - Updated H04)
Hito: H03 - AgendaAgent Tools
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.theaia.agents.agenda_agent.services.event_service import EventService
from src.theaia.agents.agenda_agent.schemas.event_schema import (
    EventCreate,
    EventUpdate,
    EventResponse
)

# Logger
logger = logging.getLogger(__name__)


class EventTools:
    """
    Herramientas para que AgendaAgent gestione eventos.
    
    v1.1: user_id y tenant_id son opcionales en __init__.
    Se pueden configurar después con set_context().
    
    Cada método es una herramienta (tool) que el agente puede invocar.
    Los métodos reciben parámetros en formato dict (como los manda el LLM)
    y retornan respuestas en formato dict/string (para el LLM).
    
    Example uso directo:
        tools = EventTools(session, user_id=1, tenant_id="default")
        result = await tools.create_event({
            "title": "Reunión",
            "start_datetime": "2025-12-05T10:00:00Z"
        })
    
    Example uso lazy (desde handler):
        tools = EventTools(session)  # Sin user_id/tenant_id
        tools.set_context(user_id=1, tenant_id="default")  # Configurar después
        result = await tools.create_event({"title": "Reunión", ...})
    """
    
    def __init__(
        self,
        session: AsyncSession,
        user_id: Optional[int] = None,
        tenant_id: Optional[str] = None
    ):
        """
        Inicializa EventTools.
        
        v1.1: user_id y tenant_id ahora son opcionales.
        Si no se proveen en __init__, deben configurarse con set_context()
        antes de usar las herramientas.
        
        Args:
            session: AsyncSession de SQLAlchemy
            user_id: ID del usuario actual (opcional)
            tenant_id: ID del tenant actual (opcional)
        """
        self.service = EventService(session)
        self.user_id = user_id
        self.tenant_id = tenant_id
        
        if user_id and tenant_id:
            logger.debug(
                f"EventTools initialized for user_id={user_id}, tenant_id={tenant_id}"
            )
        else:
            logger.debug(
                "EventTools initialized without context (use set_context() before calling tools)"
            )
    
    def set_context(self, user_id: int, tenant_id: str) -> None:
        """
        Configura el contexto de usuario/tenant después de __init__.
        
        Útil cuando EventTools se inicializa en el handler sin conocer
        el user_id/tenant_id aún.
        
        Args:
            user_id: ID del usuario actual
            tenant_id: ID del tenant actual
        
        Example:
            tools = EventTools(session)
            tools.set_context(user_id=1, tenant_id="default")
        """
        self.user_id = user_id
        self.tenant_id = tenant_id
        logger.debug(
            f"EventTools context set: user_id={user_id}, tenant_id={tenant_id}"
        )
    
    def _ensure_context(self) -> None:
        """
        Valida que user_id y tenant_id estén configurados.
        
        Raises:
            RuntimeError: Si falta user_id o tenant_id
        """
        if self.user_id is None or self.tenant_id is None:
            raise RuntimeError(
                "EventTools context not set. Call set_context(user_id, tenant_id) first."
            )
    
    async def create_event(self, params: Dict[str, Any]) -> str:
        """
        Tool: Crear un nuevo evento.
        
        Args:
            params: Diccionario con datos del evento
                - title (str): Título del evento
                - start_datetime (str): Fecha/hora inicio (ISO 8601)
                - description (str, opcional): Descripción
                - end_datetime (str, opcional): Fecha/hora fin
                - location (str, opcional): Ubicación
                - participants (list[str], opcional): Lista de participantes
                - event_type (str, opcional): Tipo de evento
        
        Returns:
            String con confirmación y detalles del evento creado
        
        Example:
            result = await tools.create_event({
                "title": "Reunión con cliente",
                "start_datetime": "2025-12-05T10:00:00Z",
                "location": "Oficina central",
                "participants": ["Juan", "María"]
            })
        """
        try:
            self._ensure_context()  # Validar contexto
            logger.info(f"Creating event with params: {params}")
            
            # Convertir start_datetime string a datetime
            start_dt = datetime.fromisoformat(
                params['start_datetime'].replace('Z', '+00:00')
            )
            
            # Convertir end_datetime si existe
            end_dt = None
            if 'end_datetime' in params and params['end_datetime']:
                end_dt = datetime.fromisoformat(
                    params['end_datetime'].replace('Z', '+00:00')
                )
            
            # Crear EventCreate schema
            event_data = EventCreate(
                title=params['title'],
                start_datetime=start_dt,
                end_datetime=end_dt,
                description=params.get('description'),
                location=params.get('location'),
                participants=params.get('participants', []),
                event_type=params.get('event_type', 'personal'),
                status='pending'
            )
            
            # Crear en BD
            event = await self.service.create_event(
                user_id=self.user_id,
                tenant_id=self.tenant_id,
                event_data=event_data
            )
            
            # Formatear respuesta para el LLM
            return (
                f"✅ Evento creado exitosamente:\n"
                f"- ID: {event.id}\n"
                f"- Título: {event.title}\n"
                f"- Fecha: {event.start_datetime.strftime('%d/%m/%Y %H:%M')}\n"
                f"- Ubicación: {event.location or 'No especificada'}\n"
                f"- Participantes: {', '.join(event.participants) if event.participants else 'Ninguno'}"
            )
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error creating event: {e}", exc_info=True)
            return f"❌ Error al crear evento: {str(e)}"
    
    async def get_event(self, params: Dict[str, Any]) -> str:
        """
        Tool: Obtener detalles de un evento.
        
        Args:
            params: Diccionario con:
                - event_id (int): ID del evento
        
        Returns:
            String con detalles del evento o mensaje de error
        
        Example:
            result = await tools.get_event({"event_id": 5})
        """
        try:
            self._ensure_context()
            event_id = params['event_id']
            logger.info(f"Getting event: id={event_id}")
            
            event = await self.service.get_event(event_id, self.tenant_id)
            
            if not event:
                return f"❌ Evento {event_id} no encontrado"
            
            # Formatear respuesta
            return (
                f"📅 Evento #{event.id}:\n"
                f"- Título: {event.title}\n"
                f"- Descripción: {event.description or 'Sin descripción'}\n"
                f"- Fecha inicio: {event.start_datetime.strftime('%d/%m/%Y %H:%M')}\n"
                f"- Fecha fin: {event.end_datetime.strftime('%d/%m/%Y %H:%M') if event.end_datetime else 'No especificada'}\n"
                f"- Ubicación: {event.location or 'No especificada'}\n"
                f"- Participantes: {', '.join(event.participants) if event.participants else 'Ninguno'}\n"
                f"- Tipo: {event.event_type}\n"
                f"- Estado: {event.status}"
            )
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error getting event: {e}", exc_info=True)
            return f"❌ Error al obtener evento: {str(e)}"
    
    async def update_event(self, params: Dict[str, Any]) -> str:
        """
        Tool: Actualizar un evento existente.
        
        Args:
            params: Diccionario con:
                - event_id (int): ID del evento
                - Campos a actualizar (opcionales)
        
        Returns:
            String con confirmación de actualización
        
        Example:
            result = await tools.update_event({
                "event_id": 5,
                "title": "Reunión CANCELADA",
                "status": "cancelled"
            })
        """
        try:
            self._ensure_context()
            event_id = params.pop('event_id')
            logger.info(f"Updating event: id={event_id}, params={params}")
            
            # Convertir datetimes si existen
            if 'start_datetime' in params:
                params['start_datetime'] = datetime.fromisoformat(
                    params['start_datetime'].replace('Z', '+00:00')
                )
            
            if 'end_datetime' in params:
                params['end_datetime'] = datetime.fromisoformat(
                    params['end_datetime'].replace('Z', '+00:00')
                )
            
            # Crear EventUpdate schema
            update_data = EventUpdate(**params)
            
            # Actualizar en BD
            event = await self.service.update_event(
                event_id=event_id,
                tenant_id=self.tenant_id,
                event_data=update_data
            )
            
            if not event:
                return f"❌ Evento {event_id} no encontrado"
            
            return (
                f"✅ Evento #{event_id} actualizado exitosamente:\n"
                f"- Título: {event.title}\n"
                f"- Estado: {event.status}"
            )
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error updating event: {e}", exc_info=True)
            return f"❌ Error al actualizar evento: {str(e)}"
    
    async def delete_event(self, params: Dict[str, Any]) -> str:
        """
        Tool: Eliminar un evento.
        
        Args:
            params: Diccionario con:
                - event_id (int): ID del evento
        
        Returns:
            String con confirmación de eliminación
        
        Example:
            result = await tools.delete_event({"event_id": 5})
        """
        try:
            self._ensure_context()
            event_id = params['event_id']
            logger.info(f"Deleting event: id={event_id}")
            
            deleted = await self.service.delete_event(event_id, self.tenant_id)
            
            if deleted:
                return f"✅ Evento #{event_id} eliminado exitosamente"
            else:
                return f"❌ Evento {event_id} no encontrado"
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error deleting event: {e}", exc_info=True)
            return f"❌ Error al eliminar evento: {str(e)}"
    
    async def list_upcoming_events(self, params: Dict[str, Any]) -> str:
        """
        Tool: Listar eventos próximos.
        
        Args:
            params: Diccionario con:
                - hours (int, opcional): Horas hacia adelante (default 24)
        
        Returns:
            String con lista de eventos próximos
        
        Example:
            result = await tools.list_upcoming_events({"hours": 48})
        """
        try:
            self._ensure_context()
            hours = params.get('hours', 24)
            logger.info(f"Listing upcoming events: hours={hours}")
            
            events = await self.service.get_upcoming_events(
                user_id=self.user_id,
                tenant_id=self.tenant_id,
                hours=hours
            )
            
            if not events:
                return f"📅 No tienes eventos próximos en las próximas {hours} horas"
            
            # Formatear lista
            result = f"📅 Próximos eventos ({len(events)}) en las próximas {hours}h:\n\n"
            
            for event in events:
                result += (
                    f"• #{event.id}: {event.title}\n"
                    f"  Fecha: {event.start_datetime.strftime('%d/%m/%Y %H:%M')}\n"
                    f"  Ubicación: {event.location or 'No especificada'}\n\n"
                )
            
            return result
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error listing upcoming events: {e}", exc_info=True)
            return f"❌ Error al listar eventos: {str(e)}"
    
    async def list_today_events(self, params: Dict[str, Any]) -> str:
        """
        Tool: Listar eventos de hoy.
        
        Args:
            params: Diccionario vacío (no requiere parámetros)
        
        Returns:
            String con lista de eventos de hoy
        
        Example:
            result = await tools.list_today_events({})
        """
        try:
            self._ensure_context()
            logger.info("Listing today events")
            
            events = await self.service.get_today_events(
                user_id=self.user_id,
                tenant_id=self.tenant_id
            )
            
            if not events:
                return "📅 No tienes eventos para hoy"
            
            # Formatear lista
            result = f"📅 Eventos de hoy ({len(events)}):\n\n"
            
            for event in events:
                result += (
                    f"• #{event.id}: {event.title}\n"
                    f"  Hora: {event.start_datetime.strftime('%H:%M')}\n"
                    f"  Ubicación: {event.location or 'No especificada'}\n"
                    f"  Estado: {event.status}\n\n"
                )
            
            return result
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error listing today events: {e}", exc_info=True)
            return f"❌ Error al listar eventos de hoy: {str(e)}"
    
    async def mark_completed(self, params: Dict[str, Any]) -> str:
        """
        Tool: Marcar evento como completado.
        
        Args:
            params: Diccionario con:
                - event_id (int): ID del evento
        
        Returns:
            String con confirmación
        
        Example:
            result = await tools.mark_completed({"event_id": 5})
        """
        try:
            self._ensure_context()
            event_id = params['event_id']
            logger.info(f"Marking event {event_id} as completed")
            
            event = await self.service.mark_event_completed(event_id, self.tenant_id)
            
            if not event:
                return f"❌ Evento {event_id} no encontrado"
            
            return f"✅ Evento #{event_id} '{event.title}' marcado como completado"
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error marking event completed: {e}", exc_info=True)
            return f"❌ Error al marcar evento: {str(e)}"
    
    async def mark_cancelled(self, params: Dict[str, Any]) -> str:
        """
        Tool: Marcar evento como cancelado.
        
        Args:
            params: Diccionario con:
                - event_id (int): ID del evento
        
        Returns:
            String con confirmación
        
        Example:
            result = await tools.mark_cancelled({"event_id": 5})
        """
        try:
            self._ensure_context()
            event_id = params['event_id']
            logger.info(f"Marking event {event_id} as cancelled")
            
            event = await self.service.mark_event_cancelled(event_id, self.tenant_id)
            
            if not event:
                return f"❌ Evento {event_id} no encontrado"
            
            return f"✅ Evento #{event_id} '{event.title}' marcado como cancelado"
        
        except RuntimeError as re:
            logger.error(f"Context error: {re}")
            return f"❌ Error de contexto: {str(re)}"
        except Exception as e:
            logger.error(f"Error marking event cancelled: {e}", exc_info=True)
            return f"❌ Error al marcar evento: {str(e)}"
