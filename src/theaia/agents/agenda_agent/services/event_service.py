"""
Event Service - Lógica de negocio para eventos
Capa de servicio entre AgendaAgent y EventRepository

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025 (H03 PHASE 1)
Hito: H03 - AgendaAgent Service Layer
"""

from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.theaia.database.repositories.event_repository import EventRepository
from src.theaia.database.models.event import Event
from src.theaia.agents.agenda_agent.schemas.event_schema import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventListResponse
)

# Logger
logger = logging.getLogger(__name__)


class EventService:
    """
    Service para lógica de negocio de eventos.
    
    Capa intermedia entre AgendaAgent y EventRepository.
    Maneja:
    - Validación de datos
    - Conversión entre schemas y modelos ORM
    - Lógica de negocio específica
    - Logging de operaciones
    
    NO maneja:
    - ❌ Búsquedas complejas (QueryAgent)
    - ❌ Recordatorios (ReminderAgent)
    
    Example:
        async with get_db() as session:
            service = EventService(session)
            
            # Crear evento
            event_data = EventCreate(
                title="Reunión",
                start_datetime=datetime.now(timezone.utc)
            )
            event = await service.create_event(
                user_id=1,
                tenant_id="default",
                event_data=event_data
            )
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa EventService.
        
        Args:
            session: AsyncSession de SQLAlchemy
        """
        self.repository = EventRepository(session)
        logger.debug("EventService initialized")
    
    async def create_event(
        self,
        user_id: int,
        tenant_id: str,
        event_data: EventCreate
    ) -> EventResponse:
        """
        Crea un nuevo evento.
        
        Args:
            user_id: ID del usuario propietario
            tenant_id: ID del tenant
            event_data: Datos del evento (EventCreate schema)
        
        Returns:
            EventResponse con el evento creado
        
        Raises:
            ValueError: Si los datos son inválidos
        
        Example:
            event_data = EventCreate(
                title="Reunión con cliente",
                start_datetime=datetime(2025, 12, 5, 10, 0, tzinfo=timezone.utc)
            )
            event = await service.create_event(1, "default", event_data)
        """
        logger.info(f"Creating event for user_id={user_id}, tenant_id={tenant_id}")
        
        # Convertir schema a dict
        event_dict = event_data.model_dump()
        
        # Agregar user_id y tenant_id
        event_dict['user_id'] = user_id
        event_dict['tenant_id'] = tenant_id
        
        # Crear en BD
        event = await self.repository.create(**event_dict)
        
        logger.info(f"Event created: id={event.id}, title='{event.title}'")
        
        # Convertir a EventResponse
        return EventResponse.model_validate(event)
    
    async def get_event(
        self,
        event_id: int,
        tenant_id: str
    ) -> Optional[EventResponse]:
        """
        Obtiene un evento por ID.
        
        Args:
            event_id: ID del evento
            tenant_id: ID del tenant
        
        Returns:
            EventResponse o None si no existe
        
        Example:
            event = await service.get_event(5, "default")
        """
        logger.debug(f"Getting event: id={event_id}, tenant_id={tenant_id}")
        
        event = await self.repository.get_by_id(event_id, tenant_id)
        
        if not event:
            logger.warning(f"Event {event_id} not found in tenant {tenant_id}")
            return None
        
        return EventResponse.model_validate(event)
    
    async def update_event(
        self,
        event_id: int,
        tenant_id: str,
        event_data: EventUpdate
    ) -> Optional[EventResponse]:
        """
        Actualiza un evento existente.
        
        Args:
            event_id: ID del evento
            tenant_id: ID del tenant
            event_data: Datos a actualizar (EventUpdate schema)
        
        Returns:
            EventResponse actualizado o None si no existe
        
        Example:
            update_data = EventUpdate(status="completed")
            event = await service.update_event(5, "default", update_data)
        """
        logger.info(f"Updating event: id={event_id}, tenant_id={tenant_id}")
        
        # Convertir schema a dict (solo campos no-None)
        update_dict = event_data.model_dump(exclude_unset=True)
        
        if not update_dict:
            logger.warning("No fields to update")
            return await self.get_event(event_id, tenant_id)
        
        # Actualizar en BD
        event = await self.repository.update(event_id, tenant_id, **update_dict)
        
        if not event:
            logger.warning(f"Event {event_id} not found for update")
            return None
        
        logger.info(f"Event {event_id} updated successfully")
        return EventResponse.model_validate(event)
    
    async def delete_event(
        self,
        event_id: int,
        tenant_id: str
    ) -> bool:
        """
        Elimina un evento.
        
        Args:
            event_id: ID del evento
            tenant_id: ID del tenant
        
        Returns:
            True si se eliminó, False si no existía
        
        Example:
            deleted = await service.delete_event(5, "default")
        """
        logger.info(f"Deleting event: id={event_id}, tenant_id={tenant_id}")
        
        result = await self.repository.delete(event_id, tenant_id)
        
        if result:
            logger.info(f"Event {event_id} deleted successfully")
        else:
            logger.warning(f"Event {event_id} not found for deletion")
        
        return result
    
    async def get_user_events(
        self,
        user_id: int,
        tenant_id: str,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> EventListResponse:
        """
        Obtiene eventos de un usuario con paginación.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            status: Filtro por estado (opcional)
            page: Número de página (1-indexed)
            page_size: Tamaño de página (máx 100)
        
        Returns:
            EventListResponse con eventos paginados
        
        Example:
            # Primera página de eventos pendientes
            result = await service.get_user_events(
                user_id=1,
                tenant_id="default",
                status="pending",
                page=1,
                page_size=10
            )
        """
        logger.debug(
            f"Getting user events: user_id={user_id}, tenant_id={tenant_id}, "
            f"status={status}, page={page}, page_size={page_size}"
        )
        
        # Validar page_size
        page_size = min(page_size, 100)
        skip = (page - 1) * page_size
        
        # Obtener eventos
        events = await self.repository.get_by_user(
            user_id=user_id,
            tenant_id=tenant_id,
            status=status,
            skip=skip,
            limit=page_size
        )
        
        # Contar total (sin paginación)
        total = await self.repository.count_by_status(
            user_id=user_id,
            tenant_id=tenant_id,
            status=status or "pending"
        ) if status else len(events)
        
        # Calcular total_pages
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        
        logger.info(
            f"Retrieved {len(events)} events for user_id={user_id}, "
            f"page={page}/{total_pages}"
        )
        
        # Convertir a EventResponse
        event_responses = [EventResponse.model_validate(e) for e in events]
        
        return EventListResponse(
            events=event_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    async def get_upcoming_events(
        self,
        user_id: int,
        tenant_id: str,
        hours: int = 24
    ) -> List[EventResponse]:
        """
        Obtiene eventos próximos en X horas.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            hours: Horas hacia adelante (default 24)
        
        Returns:
            Lista de EventResponse ordenados por fecha
        
        Example:
            # Próximos eventos en 24h
            upcoming = await service.get_upcoming_events(1, "default", hours=24)
        """
        logger.debug(
            f"Getting upcoming events: user_id={user_id}, tenant_id={tenant_id}, "
            f"hours={hours}"
        )
        
        events = await self.repository.get_upcoming(
            user_id=user_id,
            tenant_id=tenant_id,
            hours=hours
        )
        
        logger.info(
            f"Retrieved {len(events)} upcoming events for user_id={user_id}, "
            f"next {hours}h"
        )
        
        return [EventResponse.model_validate(e) for e in events]
    
    async def get_today_events(
        self,
        user_id: int,
        tenant_id: str
    ) -> List[EventResponse]:
        """
        Obtiene eventos de hoy.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Lista de EventResponse de hoy
        
        Example:
            today = await service.get_today_events(1, "default")
        """
        logger.debug(f"Getting today events: user_id={user_id}, tenant_id={tenant_id}")
        
        events = await self.repository.get_today(
            user_id=user_id,
            tenant_id=tenant_id
        )
        
        logger.info(f"Retrieved {len(events)} events for today, user_id={user_id}")
        
        return [EventResponse.model_validate(e) for e in events]
    
    async def mark_event_completed(
        self,
        event_id: int,
        tenant_id: str
    ) -> Optional[EventResponse]:
        """
        Marca evento como completado.
        
        Args:
            event_id: ID del evento
            tenant_id: ID del tenant
        
        Returns:
            EventResponse actualizado o None
        
        Example:
            event = await service.mark_event_completed(5, "default")
        """
        logger.info(f"Marking event {event_id} as completed")
        
        event = await self.repository.mark_completed(event_id, tenant_id)
        
        if not event:
            logger.warning(f"Event {event_id} not found")
            return None
        
        return EventResponse.model_validate(event)
    
    async def mark_event_cancelled(
        self,
        event_id: int,
        tenant_id: str
    ) -> Optional[EventResponse]:
        """
        Marca evento como cancelado.
        
        Args:
            event_id: ID del evento
            tenant_id: ID del tenant
        
        Returns:
            EventResponse actualizado o None
        
        Example:
            event = await service.mark_event_cancelled(5, "default")
        """
        logger.info(f"Marking event {event_id} as cancelled")
        
        event = await self.repository.mark_cancelled(event_id, tenant_id)
        
        if not event:
            logger.warning(f"Event {event_id} not found")
            return None
        
        return EventResponse.model_validate(event)
