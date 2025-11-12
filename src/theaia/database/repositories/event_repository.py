"""
Event Repository para THEA IA
Gestión de eventos y recordatorios con multi-tenant

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer
"""

from typing import Optional, List
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.event import Event


class EventRepository(BaseRepository[Event]):
    """
    Repository para operaciones CRUD de eventos/recordatorios.
    
    Extiende BaseRepository con métodos específicos para eventos:
    - get_by_user(): Eventos de un usuario
    - get_upcoming(): Próximos eventos
    - get_by_date_range(): Eventos en rango de fechas
    - mark_completed(): Marcar evento como completado
    - get_pending_reminders(): Eventos pendientes de notificar
    
    Example:
        async with get_db() as session:
            event_repo = EventRepository(session)
            upcoming = await event_repo.get_upcoming(user_id=1, tenant_id="default", hours=24)
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa EventRepository.
        
        Args:
            session: AsyncSession de SQLAlchemy
        """
        super().__init__(Event, session)
    
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
            skip: Registros a saltar
            limit: Máximo de registros
        
        Returns:
            Lista de eventos del usuario
        
        Example:
            # Todos los eventos
            events = await event_repo.get_by_user(1, "default")
            
            # Solo pendientes
            pending = await event_repo.get_by_user(1, "default", status="pending")
        """
        stmt = select(Event).where(
            Event.user_id == user_id,
            Event.tenant_id == tenant_id
        )
        
        if status:
            stmt = stmt.where(Event.status == status)
        
        stmt = stmt.order_by(Event.start_datetime.desc()).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
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
            Lista de eventos próximos ordenados por fecha
        
        Example:
            # Próximos eventos en 24h
            upcoming = await event_repo.get_upcoming(1, "default", hours=24)
            
            # Próxima semana
            week = await event_repo.get_upcoming(1, "default", hours=168)
        """
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
        return list(result.scalars().all())
    
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
            Lista de eventos en el rango
        
        Example:
            from datetime import datetime, timezone
            
            start = datetime(2025, 11, 15, 0, 0, tzinfo=timezone.utc)
            end = datetime(2025, 11, 20, 23, 59, tzinfo=timezone.utc)
            
            events = await event_repo.get_by_date_range(
                user_id=1,
                tenant_id="default",
                start_date=start,
                end_date=end
            )
        """
        stmt = select(Event).where(
            and_(
                Event.user_id == user_id,
                Event.tenant_id == tenant_id,
                Event.start_datetime >= start_date,
                Event.start_datetime <= end_date
            )
        ).order_by(Event.start_datetime.asc())
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
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
            Lista de eventos de hoy
        
        Example:
            today_events = await event_repo.get_today(1, "default")
        """
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return await self.get_by_date_range(
            user_id=user_id,
            tenant_id=tenant_id,
            start_date=start_of_day,
            end_date=end_of_day
        )
    
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
            Evento actualizado o None
        
        Example:
            completed_event = await event_repo.mark_completed(5, "default")
        """
        return await self.update(
            entity_id=event_id,
            tenant_id=tenant_id,
            status="completed"
        )
    
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
            Evento actualizado o None
        
        Example:
            cancelled = await event_repo.mark_cancelled(5, "default")
        """
        return await self.update(
            entity_id=event_id,
            tenant_id=tenant_id,
            status="cancelled"
        )
    
    async def get_pending_reminders(
        self,
        tenant_id: str,
        minutes_ahead: int = 30
    ) -> List[Event]:
        """
        Obtiene eventos que necesitan recordatorio próximamente.
        
        Busca eventos:
        - Con status "pending"
        - Que tengan reminder_minutes configurado
        - Cuyo recordatorio debe enviarse en los próximos X minutos
        
        Args:
            tenant_id: ID del tenant
            minutes_ahead: Minutos hacia adelante (default 30)
        
        Returns:
            Lista de eventos que necesitan recordatorio
        
        Example:
            # Recordatorios próximos en 30min
            pending = await event_repo.get_pending_reminders("default", minutes_ahead=30)
            
            for event in pending:
                # Enviar notificación al usuario
                await send_reminder(event.user_id, event.title)
        """
        now = datetime.now(timezone.utc)
        check_until = now + timedelta(minutes=minutes_ahead)
        
        stmt = select(Event).where(
            and_(
                Event.tenant_id == tenant_id,
                Event.status == "pending",
                Event.reminder_minutes.isnot(None),
                Event.start_datetime > now
            )
        )
        
        result = await self.session.execute(stmt)
        all_events = list(result.scalars().all())
        
        # Filtrar eventos cuyo recordatorio debe enviarse ahora
        pending_reminders = []
        for event in all_events:
            reminder_time = event.start_datetime - timedelta(minutes=event.reminder_minutes)
            if now <= reminder_time <= check_until:
                pending_reminders.append(event)
        
        return pending_reminders
    
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
        stmt = select(Event).where(
            and_(
                Event.user_id == user_id,
                Event.tenant_id == tenant_id,
                Event.status == status
            )
        )
        result = await self.session.execute(stmt)
        return len(list(result.scalars().all()))
