"""
Tests para EventRepository - H02 PHASE 2
Autor: Álvaro Fernández Mota
Fecha: 19 Nov 2025
Hito: H02 - Advanced Persistence PHASE 2
Coverage target: ≥70%
"""

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.models.event import Event
from src.theaia.database.repositories.event_repository import EventRepository


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_event_data():
    """Datos de ejemplo para crear eventos."""
    now = datetime.now(timezone.utc)
    return {
        "tenant_id": "test_tenant",
        "user_id": 1,
        "title": "Reunión importante",
        "description": "Discutir proyecto Q4",
        "start_datetime": now + timedelta(hours=2),
        "end_datetime": now + timedelta(hours=3),
        "location": "Sala 301",
        "event_type": "work",
        "status": "pending",
        "reminder_minutes": 30
    }


# ============================================================================
# TEST 1-4: CRUD BÁSICO
# ============================================================================

@pytest.mark.asyncio
async def test_create_event_basic(db_session, sample_event_data):
    """Test 1: Crear evento básico"""
    event_repo = EventRepository(db_session)
    
    # Crear instancia del modelo Event
    event = Event(**sample_event_data)
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)
    
    assert event.id is not None
    assert event.title == sample_event_data["title"]
    assert event.user_id == sample_event_data["user_id"]
    assert event.tenant_id == sample_event_data["tenant_id"]
    assert event.status == "pending"
    assert event.created_at is not None
    assert event.updated_at is not None


@pytest.mark.asyncio
async def test_get_event_by_id(db_session, sample_event_data):
    """Test 2: Obtener evento por ID"""
    event_repo = EventRepository(db_session)
    
    # Crear evento
    created_event = Event(**sample_event_data)
    db_session.add(created_event)
    await db_session.commit()
    await db_session.refresh(created_event)
    
    # Obtener por ID
    retrieved_event = await event_repo.get_by_id(
        entity_id=created_event.id,
        tenant_id=sample_event_data["tenant_id"]
    )
    
    assert retrieved_event is not None
    assert retrieved_event.id == created_event.id
    assert retrieved_event.title == created_event.title
    
    # Verificar multi-tenant isolation
    wrong_tenant = await event_repo.get_by_id(
        entity_id=created_event.id,
        tenant_id="wrong_tenant"
    )
    assert wrong_tenant is None


@pytest.mark.asyncio
async def test_update_event(db_session, sample_event_data):
    """Test 3: Actualizar evento"""
    event_repo = EventRepository(db_session)
    
    # Crear evento
    event = Event(**sample_event_data)
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)
    
    # Actualizar
    updated_event = await event_repo.update(
        entity_id=event.id,
        tenant_id=sample_event_data["tenant_id"],
        title="Reunión URGENTE",
        location="Sala 101"
    )
    
    assert updated_event.title == "Reunión URGENTE"
    assert updated_event.location == "Sala 101"
    assert updated_event.description == event.description
    assert updated_event.updated_at >= event.updated_at


@pytest.mark.asyncio
async def test_delete_event(db_session, sample_event_data):
    """Test 4: Eliminar evento"""
    event_repo = EventRepository(db_session)
    
    # Crear evento
    event = Event(**sample_event_data)
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)
    
    # Eliminar
    deleted = await event_repo.delete(
        entity_id=event.id,
        tenant_id=sample_event_data["tenant_id"]
    )
    
    assert deleted is True
    retrieved = await event_repo.get_by_id(event.id, sample_event_data["tenant_id"])
    assert retrieved is None


# ============================================================================
# TEST 5-7: BÚSQUEDAS POR FECHA
# ============================================================================

@pytest.mark.asyncio
async def test_get_upcoming_events(db_session, sample_event_data):
    """Test 5: Obtener eventos próximos (24h)"""
    event_repo = EventRepository(db_session)
    now = datetime.now(timezone.utc)
    
    # Evento en 1 hora
    event1 = Event(**{**sample_event_data, "title": "Evento 1h", 
                      "start_datetime": now + timedelta(hours=1)})
    db_session.add(event1)
    
    # Evento en 12 horas
    event2 = Event(**{**sample_event_data, "title": "Evento 12h",
                      "start_datetime": now + timedelta(hours=12)})
    db_session.add(event2)
    
    # Evento en 48 horas (NO debería aparecer)
    event3 = Event(**{**sample_event_data, "title": "Evento 48h",
                      "start_datetime": now + timedelta(hours=48)})
    db_session.add(event3)
    
    # Evento cancelado (NO debería aparecer)
    event4 = Event(**{**sample_event_data, "title": "Evento cancelado",
                      "start_datetime": now + timedelta(hours=2), "status": "cancelled"})
    db_session.add(event4)
    
    await db_session.commit()
    
    # Buscar upcoming
    upcoming = await event_repo.get_upcoming(
        user_id=sample_event_data["user_id"],
        tenant_id=sample_event_data["tenant_id"],
        hours=24
    )
    
    assert len(upcoming) == 2
    assert upcoming[0].title == "Evento 1h"
    assert upcoming[1].title == "Evento 12h"


@pytest.mark.asyncio
async def test_get_by_date_range(db_session, sample_event_data):
    """Test 6: Obtener eventos en rango de fechas"""
    event_repo = EventRepository(db_session)
    now = datetime.now(timezone.utc)
    start_range = now + timedelta(days=1)
    end_range = now + timedelta(days=3)
    
    # Evento antes del rango
    event1 = Event(**{**sample_event_data, "title": "Antes",
                      "start_datetime": now})
    db_session.add(event1)
    
    # Eventos dentro del rango
    event2 = Event(**{**sample_event_data, "title": "Dentro 1",
                      "start_datetime": now + timedelta(days=1, hours=6)})
    db_session.add(event2)
    
    event3 = Event(**{**sample_event_data, "title": "Dentro 2",
                      "start_datetime": now + timedelta(days=2)})
    db_session.add(event3)
    
    # Evento después del rango
    event4 = Event(**{**sample_event_data, "title": "Después",
                      "start_datetime": now + timedelta(days=5)})
    db_session.add(event4)
    
    await db_session.commit()
    
    # Buscar en rango
    events_in_range = await event_repo.get_by_date_range(
        user_id=sample_event_data["user_id"],
        tenant_id=sample_event_data["tenant_id"],
        start_date=start_range,
        end_date=end_range
    )
    
    assert len(events_in_range) == 2
    assert all(e.title.startswith("Dentro") for e in events_in_range)


@pytest.mark.asyncio
async def test_get_today_events(db_session, sample_event_data):
    """Test 7: Obtener eventos de hoy"""
    event_repo = EventRepository(db_session)
    now = datetime.now(timezone.utc)
    
    # Evento hoy
    today_event = Event(**{**sample_event_data, "title": "Hoy",
                           "start_datetime": now.replace(hour=14, minute=0)})
    db_session.add(today_event)
    
    # Evento ayer
    yesterday_event = Event(**{**sample_event_data, "title": "Ayer",
                               "start_datetime": now - timedelta(days=1)})
    db_session.add(yesterday_event)
    
    # Evento mañana
    tomorrow_event = Event(**{**sample_event_data, "title": "Mañana",
                              "start_datetime": now + timedelta(days=1)})
    db_session.add(tomorrow_event)
    
    await db_session.commit()
    
    # Buscar eventos de hoy
    today_events = await event_repo.get_today(
        user_id=sample_event_data["user_id"],
        tenant_id=sample_event_data["tenant_id"]
    )
    
    assert len(today_events) == 1
    assert today_events[0].title == "Hoy"


# ============================================================================
# TEST 8-9: ESTADO MANAGEMENT
# ============================================================================

@pytest.mark.asyncio
async def test_mark_completed(db_session, sample_event_data):
    """Test 8: Marcar evento como completado"""
    event_repo = EventRepository(db_session)
    
    # Crear evento
    event = Event(**sample_event_data)
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)
    
    assert event.status == "pending"
    
    # Marcar como completado
    completed_event = await event_repo.mark_completed(
        event_id=event.id,
        tenant_id=sample_event_data["tenant_id"]
    )
    
    assert completed_event is not None
    assert completed_event.status == "completed"
    assert completed_event.updated_at >= event.updated_at


@pytest.mark.asyncio
async def test_mark_cancelled(db_session, sample_event_data):
    """Test 9: Marcar evento como cancelado"""
    event_repo = EventRepository(db_session)
    
    # Crear evento
    event = Event(**sample_event_data)
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)
    
    # Marcar como cancelado
    cancelled_event = await event_repo.mark_cancelled(
        event_id=event.id,
        tenant_id=sample_event_data["tenant_id"]
    )
    
    assert cancelled_event is not None
    assert cancelled_event.status == "cancelled"


# ============================================================================
# TEST 10-12: BÚSQUEDAS AVANZADAS
# ============================================================================

@pytest.mark.asyncio
async def test_get_pending_reminders(db_session, sample_event_data):
    """Test 10: Obtener eventos que necesitan recordatorio"""
    event_repo = EventRepository(db_session)
    now = datetime.now(timezone.utc)
    
    # Evento con recordatorio pronto
    event1 = Event(**{
        **sample_event_data,
        "title": "Con recordatorio pronto",
        "start_datetime": now + timedelta(minutes=35),
        "reminder_minutes": 30
    })
    db_session.add(event1)
    
    # Evento con recordatorio lejano
    event2 = Event(**{
        **sample_event_data,
        "title": "Recordatorio lejano",
        "start_datetime": now + timedelta(hours=2),
        "reminder_minutes": 30
    })
    db_session.add(event2)
    
    # Evento sin recordatorio
    # ✅ CRÍTICO: NO incluir reminder_minutes para que quede None
    event3_data = {
        **sample_event_data,
        "title": "Sin recordatorio",
        "start_datetime": now + timedelta(hours=1)
    }
    # Remover reminder_minutes del dict
    event3_data.pop("reminder_minutes", None)
    event3 = Event(**event3_data)
    db_session.add(event3)
    
    await db_session.commit()
    
    # Buscar recordatorios pendientes
    pending_reminders = await event_repo.get_pending_reminders(
        tenant_id=sample_event_data["tenant_id"],
        minutes_ahead=30
    )
    
    assert len(pending_reminders) == 1
    assert pending_reminders[0].title == "Con recordatorio pronto"
    assert pending_reminders[0].reminder_minutes == 30


@pytest.mark.asyncio
async def test_count_by_status(db_session, sample_event_data):
    """Test 11: Contar eventos por estado"""
    event_repo = EventRepository(db_session)
    
    # Crear 3 eventos pending
    for i in range(3):
        event = Event(**{
            **sample_event_data,
            "title": f"Pending {i}",
            "status": "pending"
        })
        db_session.add(event)
    
    # Crear 2 eventos completed
    for i in range(2):
        event = Event(**{
            **sample_event_data,
            "title": f"Completed {i}",
            "status": "completed"
        })
        db_session.add(event)
    
    # Crear 1 evento cancelled
    event = Event(**{
        **sample_event_data,
        "title": "Cancelled",
        "status": "cancelled"
    })
    db_session.add(event)
    
    await db_session.commit()
    
    # Contar por estado
    pending_count = await event_repo.count_by_status(
        user_id=sample_event_data["user_id"],
        tenant_id=sample_event_data["tenant_id"],
        status="pending"
    )
    completed_count = await event_repo.count_by_status(
        user_id=sample_event_data["user_id"],
        tenant_id=sample_event_data["tenant_id"],
        status="completed"
    )
    cancelled_count = await event_repo.count_by_status(
        user_id=sample_event_data["user_id"],
        tenant_id=sample_event_data["tenant_id"],
        status="cancelled"
    )
    
    assert pending_count == 3
    assert completed_count == 2
    assert cancelled_count == 1


@pytest.mark.asyncio
async def test_get_by_user_with_filter(db_session, sample_event_data):
    """Test 12: Obtener eventos de usuario con filtro"""
    event_repo = EventRepository(db_session)
    
    # Usuario 1 - pending
    for i in range(5):
        event = Event(**{
            **sample_event_data,
            "user_id": 1,
            "title": f"User1 Pending {i}",
            "status": "pending"
        })
        db_session.add(event)
    
    # Usuario 1 - completed
    for i in range(3):
        event = Event(**{
            **sample_event_data,
            "user_id": 1,
            "title": f"User1 Completed {i}",
            "status": "completed"
        })
        db_session.add(event)
    
    # Usuario 2
    event = Event(**{
        **sample_event_data,
        "user_id": 2,
        "title": "User2 Event",
        "status": "pending"
    })
    db_session.add(event)
    
    await db_session.commit()
    
    # Tests
    all_user1 = await event_repo.get_by_user(1, sample_event_data["tenant_id"])
    assert len(all_user1) == 8
    
    pending_user1 = await event_repo.get_by_user(
        1, sample_event_data["tenant_id"], status="pending")
    assert len(pending_user1) == 5
    
    completed_user1 = await event_repo.get_by_user(
        1, sample_event_data["tenant_id"], status="completed")
    assert len(completed_user1) == 3
    
    # Paginación
    page1 = await event_repo.get_by_user(1, sample_event_data["tenant_id"], skip=0, limit=3)
    assert len(page1) == 3
    
    page2 = await event_repo.get_by_user(1, sample_event_data["tenant_id"], skip=3, limit=3)
    assert len(page2) == 3


# ============================================================================
# TEST 13: MULTI-TENANT ISOLATION
# ============================================================================

@pytest.mark.asyncio
async def test_multi_tenant_isolation_comprehensive(db_session, sample_event_data):
    """Test 13: Aislamiento multi-tenant comprehensivo"""
    event_repo = EventRepository(db_session)
    tenant_a_data = {**sample_event_data, "tenant_id": "tenant_a"}
    tenant_b_data = {**sample_event_data, "tenant_id": "tenant_b"}
    
    # Crear eventos tenant A
    event_a1 = Event(**{**tenant_a_data, "title": "Event A1"})
    event_a2 = Event(**{**tenant_a_data, "title": "Event A2"})
    event_a3 = Event(**{**tenant_a_data, "title": "Event A3"})
    db_session.add(event_a1)
    db_session.add(event_a2)
    db_session.add(event_a3)
    
    # Crear eventos tenant B
    event_b1 = Event(**{**tenant_b_data, "title": "Event B1"})
    event_b2 = Event(**{**tenant_b_data, "title": "Event B2"})
    db_session.add(event_b1)
    db_session.add(event_b2)
    
    await db_session.commit()
    await db_session.refresh(event_a1)
    await db_session.refresh(event_b1)
    
    # Tests de aislamiento
    retrieved_a = await event_repo.get_by_id(event_a1.id, "tenant_a")
    assert retrieved_a is not None
    
    retrieved_wrong = await event_repo.get_by_id(event_a1.id, "tenant_b")
    assert retrieved_wrong is None
    
    events_tenant_a = await event_repo.get_by_user(1, "tenant_a")
    events_tenant_b = await event_repo.get_by_user(1, "tenant_b")
    
    assert len(events_tenant_a) == 3
    assert len(events_tenant_b) == 2
    
    count_a = await event_repo.count_by_status(1, "tenant_a", "pending")
    count_b = await event_repo.count_by_status(1, "tenant_b", "pending")
    
    assert count_a == 3
    assert count_b == 2
    
    updated = await event_repo.update(event_a1.id, "tenant_a", title="Updated A1")
    assert updated is not None
    
    not_updated = await event_repo.update(event_a1.id, "tenant_b", title="Hacked")
    assert not_updated is None
    
    deleted_wrong = await event_repo.delete(event_b1.id, "tenant_a")
    assert deleted_wrong is False
    
    deleted_correct = await event_repo.delete(event_b1.id, "tenant_b")
    assert deleted_correct is True
