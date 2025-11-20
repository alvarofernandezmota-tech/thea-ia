"""
Tests para ConversationRepository - H02 PHASE 2
Autor: Álvaro Fernández Mota
Fecha: 19 Nov 2025
Hito: H02 - Advanced Persistence PHASE 2
Coverage target: ≥70%
"""

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.models.conversation import Conversation
from src.theaia.database.repositories.conversation_repository import ConversationRepository


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_conversation_data():
    """Datos de ejemplo para crear conversaciones."""
    now = datetime.now(timezone.utc)
    return {
        "tenant_id": "test_tenant",
        "user_id": 1,
        "session_id": "telegram_123456",
        "current_state": "idle",
        "is_active": True,
        "started_at": now,
        "last_activity": now,
        "context_data": {}
    }


# ============================================================================
# TEST 1-4: CRUD BÁSICO
# ============================================================================

@pytest.mark.asyncio
async def test_create_conversation(db_session, sample_conversation_data):
    """Test 1: Crear conversación básica"""
    conv_repo = ConversationRepository(db_session)
    
    now = datetime.now(timezone.utc)
    conv = Conversation(**{
        **sample_conversation_data,
        "started_at": now,
        "last_activity": now
    })
    db_session.add(conv)
    await db_session.commit()
    await db_session.refresh(conv)
    
    assert conv.id is not None
    assert conv.session_id == "telegram_123456"
    assert conv.current_state == "idle"
    assert conv.is_active is True
    assert conv.started_at is not None
    assert conv.last_activity is not None


@pytest.mark.asyncio
async def test_get_by_session_id(db_session, sample_conversation_data):
    """Test 2: Obtener conversación por session_id"""
    conv_repo = ConversationRepository(db_session)
    
    # Crear conversación
    now = datetime.now(timezone.utc)
    conv = Conversation(**{
        **sample_conversation_data,
        "started_at": now,
        "last_activity": now
    })
    db_session.add(conv)
    await db_session.commit()
    await db_session.refresh(conv)
    
    # Obtener por session_id
    retrieved = await conv_repo.get_by_session_id(
        session_id="telegram_123456",
        tenant_id=sample_conversation_data["tenant_id"]
    )
    
    assert retrieved is not None
    assert retrieved.id == conv.id
    assert retrieved.session_id == "telegram_123456"
    
    # Verificar multi-tenant isolation
    wrong_tenant = await conv_repo.get_by_session_id(
        session_id="telegram_123456",
        tenant_id="wrong_tenant"
    )
    assert wrong_tenant is None


@pytest.mark.asyncio
async def test_update_conversation(db_session, sample_conversation_data):
    """Test 3: Actualizar conversación"""
    conv_repo = ConversationRepository(db_session)
    
    # Crear conversación
    now = datetime.now(timezone.utc)
    conv = Conversation(**{
        **sample_conversation_data,
        "started_at": now,
        "last_activity": now
    })
    db_session.add(conv)
    await db_session.commit()
    await db_session.refresh(conv)
    
    # Actualizar
    updated_conv = await conv_repo.update(
        entity_id=conv.id,
        tenant_id=sample_conversation_data["tenant_id"],
        current_state="processing"
    )
    
    assert updated_conv.current_state == "processing"
    assert updated_conv.session_id == conv.session_id


@pytest.mark.asyncio
async def test_delete_conversation(db_session, sample_conversation_data):
    """Test 4: Eliminar conversación"""
    conv_repo = ConversationRepository(db_session)
    
    # Crear conversación
    now = datetime.now(timezone.utc)
    conv = Conversation(**{
        **sample_conversation_data,
        "started_at": now,
        "last_activity": now
    })
    db_session.add(conv)
    await db_session.commit()
    await db_session.refresh(conv)
    
    # Eliminar
    deleted = await conv_repo.delete(
        entity_id=conv.id,
        tenant_id=sample_conversation_data["tenant_id"]
    )
    
    assert deleted is True
    retrieved = await conv_repo.get_by_id(conv.id, sample_conversation_data["tenant_id"])
    assert retrieved is None


# ============================================================================
# TEST 5-7: GET_OR_CREATE Y ESTADOS
# ============================================================================

@pytest.mark.asyncio
async def test_get_or_create_new(db_session, sample_conversation_data):
    """Test 5: get_or_create - crear nueva conversación"""
    conv_repo = ConversationRepository(db_session)
    
    conv, created = await conv_repo.get_or_create(
        user_id=sample_conversation_data["user_id"],
        tenant_id=sample_conversation_data["tenant_id"],
        session_id="new_session_789",
        initial_state="idle"
    )
    
    assert created is True
    assert conv.session_id == "new_session_789"
    assert conv.current_state == "idle"
    assert conv.is_active is True


@pytest.mark.asyncio
async def test_get_or_create_existing(db_session, sample_conversation_data):
    """Test 6: get_or_create - obtener existente"""
    conv_repo = ConversationRepository(db_session)
    
    # Crear conversación inicial
    conv1, created1 = await conv_repo.get_or_create(
        user_id=sample_conversation_data["user_id"],
        tenant_id=sample_conversation_data["tenant_id"],
        session_id="existing_session",
        initial_state="idle"
    )
    
    assert created1 is True
    
    # Obtener la misma conversación
    conv2, created2 = await conv_repo.get_or_create(
        user_id=sample_conversation_data["user_id"],
        tenant_id=sample_conversation_data["tenant_id"],
        session_id="existing_session",
        initial_state="idle"
    )
    
    assert created2 is False
    assert conv2.id == conv1.id


@pytest.mark.asyncio
async def test_update_state(db_session, sample_conversation_data):
    """Test 7: Actualizar estado FSM"""
    conv_repo = ConversationRepository(db_session)
    
    # Crear conversación
    now = datetime.now(timezone.utc)
    conv = Conversation(**{
        **sample_conversation_data,
        "started_at": now,
        "last_activity": now
    })
    db_session.add(conv)
    await db_session.commit()
    await db_session.refresh(conv)
    
    # Actualizar estado
    updated = await conv_repo.update_state(
        conversation_id=conv.id,
        tenant_id=sample_conversation_data["tenant_id"],
        new_state="awaiting_confirmation",
        context={"action": "create_event", "title": "Reunión"}
    )
    
    assert updated.current_state == "awaiting_confirmation"
    assert updated.context_data["action"] == "create_event"
    assert updated.context_data["title"] == "Reunión"


# ============================================================================
# TEST 8-10: GESTIÓN DE ACTIVIDAD
# ============================================================================

@pytest.mark.asyncio
async def test_get_active(db_session, sample_conversation_data):
    """Test 8: Obtener conversaciones activas"""
    conv_repo = ConversationRepository(db_session)
    
    now = datetime.now(timezone.utc)
    
    # Crear 3 activas
    for i in range(3):
        conv = Conversation(**{
            **sample_conversation_data,
            "session_id": f"active_{i}",
            "is_active": True,
            "started_at": now,
            "last_activity": now
        })
        db_session.add(conv)
    
    # Crear 2 inactivas
    for i in range(2):
        conv = Conversation(**{
            **sample_conversation_data,
            "session_id": f"inactive_{i}",
            "is_active": False,
            "started_at": now,
            "last_activity": now
        })
        db_session.add(conv)
    
    await db_session.commit()
    
    # Obtener solo activas
    active = await conv_repo.get_active(
        user_id=sample_conversation_data["user_id"],
        tenant_id=sample_conversation_data["tenant_id"]
    )
    
    assert len(active) == 3
    for conv in active:
        assert conv.is_active is True


@pytest.mark.asyncio
async def test_close_conversation(db_session, sample_conversation_data):
    """Test 9: Cerrar conversación"""
    conv_repo = ConversationRepository(db_session)
    
    # Crear conversación activa
    now = datetime.now(timezone.utc)
    conv = Conversation(**{
        **sample_conversation_data,
        "started_at": now,
        "last_activity": now
    })
    db_session.add(conv)
    await db_session.commit()
    await db_session.refresh(conv)
    
    assert conv.is_active is True
    
    # Cerrar
    closed = await conv_repo.close_conversation(
        conversation_id=conv.id,
        tenant_id=sample_conversation_data["tenant_id"],
        final_state="closed"
    )
    
    assert closed.is_active is False
    assert closed.current_state == "closed"


@pytest.mark.asyncio
async def test_update_activity(db_session, sample_conversation_data):
    """Test 10: Actualizar actividad"""
    conv_repo = ConversationRepository(db_session)
    
    # Crear conversación
    now = datetime.now(timezone.utc)
    conv = Conversation(**{
        **sample_conversation_data,
        "started_at": now,
        "last_activity": now
    })
    db_session.add(conv)
    await db_session.commit()
    await db_session.refresh(conv)
    
    original_activity = conv.last_activity
    
    # Esperar un momento
    import asyncio
    await asyncio.sleep(0.1)
    
    # Actualizar actividad
    updated = await conv_repo.update_activity(
        conversation_id=conv.id,
        tenant_id=sample_conversation_data["tenant_id"],
        message_id="msg_123"
    )
    
    assert updated.last_activity > original_activity
    assert updated.last_message_id == "msg_123"


# ============================================================================
# TEST 11-13: BÚSQUEDAS Y ESTADÍSTICAS
# ============================================================================

@pytest.mark.asyncio
async def test_get_by_state(db_session, sample_conversation_data):
    """Test 11: Obtener conversaciones por estado"""
    conv_repo = ConversationRepository(db_session)
    
    now = datetime.now(timezone.utc)
    
    # Crear conversaciones con diferentes estados
    states = ["idle", "processing", "processing", "awaiting_confirmation"]
    
    for i, state in enumerate(states):
        conv = Conversation(**{
            **sample_conversation_data,
            "session_id": f"session_{i}",
            "current_state": state,
            "started_at": now,
            "last_activity": now
        })
        db_session.add(conv)
    
    await db_session.commit()
    
    # Buscar por estado "processing"
    processing = await conv_repo.get_by_state(
        tenant_id=sample_conversation_data["tenant_id"],
        state="processing"
    )
    
    assert len(processing) == 2
    for conv in processing:
        assert conv.current_state == "processing"


@pytest.mark.asyncio
async def test_get_inactive_since(db_session, sample_conversation_data):
    """Test 12: Obtener conversaciones inactivas"""
    conv_repo = ConversationRepository(db_session)
    
    now = datetime.now(timezone.utc)
    
    # Crear conversación antigua
    old_time = now - timedelta(minutes=60)
    old_conv = Conversation(**{
        **sample_conversation_data,
        "started_at": old_time,
        "last_activity": old_time
    })
    db_session.add(old_conv)
    await db_session.flush()
    
    # Crear conversación reciente
    recent_conv = Conversation(**{
        **sample_conversation_data,
        "session_id": "recent_session",
        "started_at": now,
        "last_activity": now
    })
    db_session.add(recent_conv)
    
    await db_session.commit()
    
    # Buscar inactivas (30+ minutos)
    inactive = await conv_repo.get_inactive_since(
        tenant_id=sample_conversation_data["tenant_id"],
        minutes=30
    )
    
    assert len(inactive) == 1
    assert inactive[0].id == old_conv.id


@pytest.mark.asyncio
async def test_count_by_state(db_session, sample_conversation_data):
    """Test 13: Contar conversaciones por estado"""
    conv_repo = ConversationRepository(db_session)
    
    now = datetime.now(timezone.utc)
    
    # Crear conversaciones con diferentes estados
    states = {
        "idle": 3,
        "processing": 2,
        "awaiting_confirmation": 1
    }
    
    session_counter = 0
    for state, count in states.items():
        for _ in range(count):
            conv = Conversation(**{
                **sample_conversation_data,
                "session_id": f"session_{session_counter}",
                "current_state": state,
                "started_at": now,
                "last_activity": now
            })
            db_session.add(conv)
            session_counter += 1
    
    await db_session.commit()
    
    # Contar por estado
    counts = await conv_repo.count_by_state(
        tenant_id=sample_conversation_data["tenant_id"]
    )
    
    assert counts["idle"] == 3
    assert counts["processing"] == 2
    assert counts["awaiting_confirmation"] == 1
