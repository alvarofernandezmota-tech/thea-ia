"""
Event Repository para THEA IA
Gestión de eventos con multi-tenant y logging

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025 (H03 PHASE 1)
Hito: H03 - EventAgent Database Layer
"""

from typing import Optional, List
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.event import Event

# Logger
logger = logging.getLogger(__name__)


class EventRepository(BaseRepository[Event]):
    """
    Repository para operaciones CRUD de eventos/recordatorios.
    
    Responsabilidades:
    - CRUD básico de eventos (heredado de BaseRepository)
    - get_by_user(): Eventos de un usuario con filtros
    - get_upcoming(): Próximos eventos en X horas
    - get_by_date_range(): Eventos en rango de fechas
    - get_today(): Eventos de hoy
    - mark_completed(): Marcar evento como completado
    - mark_cancelled(): Marcar evento como cancelado
    - count_by_status(): Contar eventos por estado
    
    NO incluye:
    - ❌ get_pending_reminders() → ReminderAgent se encarga
    - ❌ Búsquedas complejas → QueryAgent se encarga
    
    Example:
        async with get_db() as session:
            event_repo = EventRepository(session)
            upcoming = await event_repo.get_upcoming(
                user_id=1, 
                tenant_id="default", 
                hours=24
            )
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa EventRepository.
        
        Args:
            session: AsyncSession de SQLAlchemy
        """
        super().__init__(Event, session)
        logger.debug("EventRepository initialized")
    
    async def get_by_user(
        self,
        user_id: int,
        tenant_id: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Event]:
        """
        Obtiene eventos de un usuario con filtro opcional de estado.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            status: Filtro por estado (pending|completed|cancelled)
            skip: Registros a saltar (paginación)
            limit: Máximo de registros (máx 100)
        
        Returns:
            Lista de eventos del usuario ordenados por fecha descendente
        
        Example:
            # Todos los eventos
            events = await event_repo.get_by_user(1, "default")
            
            # Solo pendientes
            pending = await event_repo.get_by_user(1, "default", status="pending")
        """
        logger.debug(
            f"get_by_user: user_id={user_id}, tenant_id={tenant_id}, "
            f"status={status}, skip={skip}, limit={limit}"
        )
        
        stmt = select(Event).where(
            Event.user_id == user_id,
            Event.tenant_id == tenant_id
        )
        
        if status:
            stmt = stmt.where(Event.status == status)
        
        stmt = stmt.order_by(Event.start_datetime.desc()).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        events = list(result.scalars().all())
        
        logger.info(
            f"Retrieved {len(events)} events for user_id={user_id}, "
            f"tenant_id={tenant_id}, status={status}"
        )
        return events
    
    async def get_upcoming(
        self,
        user_id: int,
        tenant_id: str,
        hours: int = 24
    ) -> List[Event]:
        """
        Obtiene eventos próximos del usuario en las próximas X horas.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            hours: Horas hacia adelante (default 24h)
        
        Returns:
            Lista de eventos próximos ordenados por fecha ascendente
        
        Example:
            # Próximos eventos en 24h
            upcoming = await event_repo.get_upcoming(1, "default", hours=24)
            
            # Próxima semana
            week = await event_repo.get_upcoming(1, "default", hours=168)
        """
        logger.debug(
            f"get_upcoming: user_id={user_id}, tenant_id={tenant_id}, hours={hours}"
        )
        
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(hours=hours)
        
        stmt = select(Event).where(
            and_(
                Event.user_id == user_id,
                Event.tenant_id == tenant_id,
                Event.start_datetime >= now,
                Event.start_datetime <= end_time,
                Event.status != "cancelled"
            )
        ).order_by(Event.start_datetime.asc())
        
        result = await self.session.execute(stmt)
        events = list(result.scalars().all())
        
        logger.info(
            f"Retrieved {len(events)} upcoming events for user_id={user_id}, "
            f"tenant_id={tenant_id}, next {hours}h"
        )
        return events
    
    async def get_by_date_range(
        self,
        user_id: int,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Event]:
        """
        Obtiene eventos en un rango de fechas.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            start_date: Fecha inicio (timezone-aware)
            end_date: Fecha fin (timezone-aware)
        
        Returns:
            Lista de eventos en el rango ordenados por fecha
        
        Example:
            from datetime import datetime, timezone
            
            start = datetime(2025, 12, 4, 0, 0, tzinfo=timezone.utc)
            end = datetime(2025, 12, 10, 23, 59, tzinfo=timezone.utc)
            
            events = await event_repo.get_by_date_range(
                user_id=1,
                tenant_id="default",
                start_date=start,
                end_date=end
            )
        """
        logger.debug(
            f"get_by_date_range: user_id={user_id}, tenant_id={tenant_id}, "
            f"start={start_date}, end={end_date}"
        )
        
        stmt = select(Event).where(
            and_(
                Event.user_id == user_id,
                Event.tenant_id == tenant_id,
                Event.start_datetime >= start_date,
                Event.start_datetime <= end_date
            )
        ).order_by(Event.start_datetime.asc())
        
        result = await self.session.execute(stmt)
        events = list(result.scalars().all())
        
        logger.info(
            f"Retrieved {len(events)} events for user_id={user_id}, "
            f"tenant_id={tenant_id}, range={start_date} to {end_date}"
        )
        return events
    
    async def get_today(
        self,
        user_id: int,
        tenant_id: str
    ) -> List[Event]:
        """
        Obtiene eventos de hoy del usuario.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Lista de eventos de hoy ordenados por hora
        
        Example:
            today_events = await event_repo.get_today(1, "default")
        """
        logger.debug(f"get_today: user_id={user_id}, tenant_id={tenant_id}")
        
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        events = await self.get_by_date_range(
            user_id=user_id,
            tenant_id=tenant_id,
            start_date=start_of_day,
            end_date=end_of_day
        )
        
        logger.info(
            f"Retrieved {len(events)} events for today, "
            f"user_id={user_id}, tenant_id={tenant_id}"
        )
        return events
    
    async def mark_completed(
        self,
        event_id: int,
        tenant_id: str
    ) -> Optional[Event]:
        """
        Marca un evento como completado.
        
        Args:
            event_id: ID del evento
            tenant_id: ID del tenant
        
        Returns:
            Evento actualizado o None si no existe
        
        Example:
            completed_event = await event_repo.mark_completed(5, "default")
        """
        logger.debug(f"mark_completed: event_id={event_id}, tenant_id={tenant_id}")
        
        event = await self.update(
            entity_id=event_id,
            tenant_id=tenant_id,
            status="completed"
        )
        
        if event:
            logger.info(f"Event {event_id} marked as completed")
        else:
            logger.warning(f"Event {event_id} not found for tenant {tenant_id}")
        
        return event
    
    async def mark_cancelled(
        self,
        event_id: int,
        tenant_id: str
    ) -> Optional[Event]:
        """
        Marca un evento como cancelado.
        
        Args:
            event_id: ID del evento
            tenant_id: ID del tenant
        
        Returns:
            Evento actualizado o None si no existe
        
        Example:
            cancelled = await event_repo.mark_cancelled(5, "default")
        """
        logger.debug(f"mark_cancelled: event_id={event_id}, tenant_id={tenant_id}")
        
        event = await self.update(
            entity_id=event_id,
            tenant_id=tenant_id,
            status="cancelled"
        )
        
        if event:
            logger.info(f"Event {event_id} marked as cancelled")
        else:
            logger.warning(f"Event {event_id} not found for tenant {tenant_id}")
        
        return event
    
    async def count_by_status(
        self,
        user_id: int,
        tenant_id: str,
        status: str
    ) -> int:
        """
        Cuenta eventos de un usuario por estado.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            status: Estado a contar (pending|completed|cancelled)
        
        Returns:
            Número de eventos con ese estado
        
        Example:
            pending_count = await event_repo.count_by_status(1, "default", "pending")
        """
        logger.debug(
            f"count_by_status: user_id={user_id}, tenant_id={tenant_id}, "
            f"status={status}"
        )
        
        stmt = select(Event).where(
            and_(
                Event.user_id == user_id,
                Event.tenant_id == tenant_id,
                Event.status == status
            )
        )
        result = await self.session.execute(stmt)
        count = len(list(result.scalars().all()))
        
        logger.info(
            f"Count: {count} events with status={status}, "
            f"user_id={user_id}, tenant_id={tenant_id}"
        )
        return count
