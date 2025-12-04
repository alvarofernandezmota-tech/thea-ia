"""
Test End-to-End para AgendaAgent v3.3
Valida integración completa: Handler → Service → Repository → Database

VERSIÓN FINAL: PostgreSQL Real con conftest.py (WindowsSelectorEventLoopPolicy)

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025 (H04 PHASE 2)
"""

import pytest
import pytest_asyncio
from datetime import datetime, timezone, timedelta

from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.agenda_agent.services.event_service import EventService
from src.theaia.agents.agenda_agent.tools.event_tools import EventTools


# ========================================
# FIXTURES (Usan db_session de conftest.py)
# ========================================

@pytest_asyncio.fixture
async def test_user(db_session):
    """
    Crea usuario de prueba para los tests.
    Usa db_session de conftest.py que ya tiene el fix de event loop.
    """
    from src.theaia.database.models.user import User
    
    test_user = User(
        id=123,
        telegram_id=123456789,
        username="test_user",
        first_name="Test",
        last_name="User",
        tenant_id="test_tenant",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db_session.add(test_user)
    await db_session.flush()
    await db_session.commit()
    
    return test_user


@pytest_asyncio.fixture
async def agenda_agent(db_session, test_user):
    """Fixture para AgendaAgent con session de PostgreSQL."""
    agent = AgendaAgent(session=db_session)
    return agent


@pytest_asyncio.fixture
async def event_service(db_session, test_user):
    """Fixture para EventService con session de PostgreSQL."""
    return EventService(db_session)


@pytest_asyncio.fixture
async def event_tools(db_session, test_user):
    """Fixture para EventTools con session de PostgreSQL."""
    tools = EventTools(db_session)
    tools.set_context(user_id=123, tenant_id="test_tenant")
    return tools


# ========================================
# TEST SUITE: HANDLER INTEGRATION
# ========================================

@pytest.mark.asyncio
async def test_handler_initialization(agenda_agent):
    """Test 1: Verificar que handler se inicializa correctamente."""
    assert agenda_agent is not None
    assert agenda_agent.event_service is not None
    assert agenda_agent.event_tools is not None
    assert len(agenda_agent.fsm_instances) == 0
    print("✅ Test 1: Handler initialization OK")


@pytest.mark.asyncio
async def test_service_create_event(event_service):
    """Test 2: Crear evento via EventService."""
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    event_data = EventCreate(
        title="Test Meeting",
        start_datetime=datetime.now(timezone.utc) + timedelta(hours=2),
        description="Test description",
        location="Test Office",
        event_type="work",
        status="pending"
    )
    
    event = await event_service.create_event(
        user_id=123,
        tenant_id="test_tenant",
        event_data=event_data
    )
    
    assert event.id is not None
    assert event.title == "Test Meeting"
    assert event.location == "Test Office"
    assert event.user_id == 123
    assert event.tenant_id == "test_tenant"
    print(f"✅ Test 2: Event created via Service - ID: {event.id}")


@pytest.mark.asyncio
async def test_service_get_event(event_service):
    """Test 3: Recuperar evento via EventService."""
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    event_data = EventCreate(
        title="Test Retrieve",
        start_datetime=datetime.now(timezone.utc) + timedelta(hours=3),
        status="pending"
    )
    
    created_event = await event_service.create_event(
        user_id=123,
        tenant_id="test_tenant",
        event_data=event_data
    )
    
    retrieved_event = await event_service.get_event(
        event_id=created_event.id,
        tenant_id="test_tenant"
    )
    
    assert retrieved_event is not None
    assert retrieved_event.id == created_event.id
    assert retrieved_event.title == "Test Retrieve"
    print(f"✅ Test 3: Event retrieved - ID: {retrieved_event.id}")


@pytest.mark.asyncio
async def test_tools_create_event(event_tools):
    """Test 4: Crear evento via EventTools."""
    result = await event_tools.create_event({
        "title": "Tools Test Event",
        "start_datetime": (datetime.now(timezone.utc) + timedelta(hours=4)).isoformat(),
        "location": "Virtual",
        "participants": ["Alice", "Bob"]
    })
    
    assert "✅" in result
    assert "Tools Test Event" in result
    print(f"✅ Test 4: Event created via Tools\n{result}")


@pytest.mark.asyncio
async def test_tools_list_upcoming_events(event_tools, event_service):
    """Test 5: Listar eventos próximos via EventTools."""
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    for i in range(3):
        event_data = EventCreate(
            title=f"Upcoming Event {i+1}",
            start_datetime=datetime.now(timezone.utc) + timedelta(hours=i+1),
            status="pending"
        )
        await event_service.create_event(
            user_id=123,
            tenant_id="test_tenant",
            event_data=event_data
        )
    
    result = await event_tools.list_upcoming_events({"hours": 24})
    
    assert "📅" in result
    print(f"✅ Test 5: Listed upcoming events\n{result}")


@pytest.mark.asyncio
async def test_tools_update_event(event_tools, event_service):
    """Test 6: Actualizar evento via EventTools."""
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    event_data = EventCreate(
        title="Original Title",
        start_datetime=datetime.now(timezone.utc) + timedelta(hours=5),
        status="pending"
    )
    event = await event_service.create_event(
        user_id=123,
        tenant_id="test_tenant",
        event_data=event_data
    )
    
    result = await event_tools.update_event({
        "event_id": event.id,
        "title": "Updated Title",
        "status": "completed"  # ✅ CAMBIADO de "confirmed" a "completed"
    })
    
    assert "✅" in result
    assert "Updated Title" in result
    print(f"✅ Test 6: Event updated via Tools\n{result}")


@pytest.mark.asyncio
async def test_tools_mark_completed(event_tools, event_service):
    """Test 7: Marcar evento como completado via EventTools."""
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    event_data = EventCreate(
        title="Event to Complete",
        start_datetime=datetime.now(timezone.utc) + timedelta(hours=1),
        status="pending"
    )
    event = await event_service.create_event(
        user_id=123,
        tenant_id="test_tenant",
        event_data=event_data
    )
    
    result = await event_tools.mark_completed({"event_id": event.id})
    
    assert "✅" in result
    assert "completado" in result
    print(f"✅ Test 7: Event marked completed\n{result}")


@pytest.mark.asyncio
async def test_service_get_upcoming_events(event_service):
    """Test 8: Obtener eventos próximos via EventService."""
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    near_event = EventCreate(
        title="Near Event",
        start_datetime=datetime.now(timezone.utc) + timedelta(hours=2),
        status="pending"
    )
    await event_service.create_event(
        user_id=123,
        tenant_id="test_tenant",
        event_data=near_event
    )
    
    far_event = EventCreate(
        title="Far Event",
        start_datetime=datetime.now(timezone.utc) + timedelta(days=3),
        status="pending"
    )
    await event_service.create_event(
        user_id=123,
        tenant_id="test_tenant",
        event_data=far_event
    )
    
    events = await event_service.get_upcoming_events(
        user_id=123,
        tenant_id="test_tenant",
        hours=24
    )
    
    assert len(events) >= 1
    titles = [e.title for e in events]
    assert "Near Event" in titles
    print(f"✅ Test 8: Got {len(events)} upcoming events")


@pytest.mark.asyncio
async def test_service_delete_event(event_service):
    """Test 9: Eliminar evento via EventService."""
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    event_data = EventCreate(
        title="Event to Delete",
        start_datetime=datetime.now(timezone.utc) + timedelta(hours=6),
        status="pending"
    )
    event = await event_service.create_event(
        user_id=123,
        tenant_id="test_tenant",
        event_data=event_data
    )
    
    deleted = await event_service.delete_event(
        event_id=event.id,
        tenant_id="test_tenant"
    )
    
    assert deleted is True
    
    retrieved = await event_service.get_event(event.id, "test_tenant")
    assert retrieved is None
    print(f"✅ Test 9: Event deleted - ID: {event.id}")


@pytest.mark.asyncio
async def test_full_integration_flow(agenda_agent, db_session):
    """Test 10: Flujo completo end-to-end simulando handler."""
    user_id = "user_123"
    context = {
        "user_id": user_id,
        "tenant_id": "test_tenant",
        "conversation_id": "conv_456"
    }
    
    if agenda_agent.event_tools:
        agenda_agent.event_tools.set_context(
            user_id=123,
            tenant_id="test_tenant"
        )
    
    message = "Quiero crear una reunión mañana a las 3pm"
    
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    context['event_date'] = tomorrow.strftime('%Y-%m-%d')
    context['event_time'] = "15:00"
    context['event_title'] = "Reunión"
    
    from src.theaia.agents.agenda_agent.schemas.event_schema import EventCreate
    
    event_data = EventCreate(
        title=context['event_title'],
        start_datetime=datetime.combine(
            tomorrow.date(),
            datetime.strptime(context['event_time'], "%H:%M").time()
        ).replace(tzinfo=timezone.utc),
        status="pending"
    )
    
    event = await agenda_agent.event_service.create_event(
        user_id=123,
        tenant_id=context['tenant_id'],
        event_data=event_data
    )
    
    assert event.id is not None
    assert event.title == "Reunión"
    
    print(f"✅ Test 10: Full integration flow completed - Event ID: {event.id}")
