"""
Tests para MessageHistoryRepository - H02 PHASE 2
Autor: Álvaro Fernández Mota
Fecha: 19 Nov 2025
Hito: H02 - Advanced Persistence PHASE 2 + Context Window Management
Coverage target: ≥70%
"""

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.theaia.database.models.message_history import MessageHistory
from src.theaia.database.models.conversation import Conversation
from src.theaia.database.repositories.message_history_repository import MessageHistoryRepository


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_conversation(db_session):
    """Conversación de ejemplo para mensajes."""
    async def _create():
        now = datetime.now(timezone.utc)
        conv = Conversation(
            tenant_id="test_tenant",
            user_id=1,
            session_id=f"test_session_{uuid.uuid4()}",
            current_state="idle",
            is_active=True,
            started_at=now,
            last_activity=now,
            context_data={}
        )
        db_session.add(conv)
        await db_session.commit()
        await db_session.refresh(conv)
        return conv
    return _create


@pytest.fixture
def sample_message_data():
    """Datos de ejemplo para crear mensajes."""
    return {
        "tenant_id": "test_tenant",
        "message_id": f"msg_{uuid.uuid4()}",
        "user_message": "Quiero crear un evento",
        "bot_response": "¿Qué título tiene el evento?",
        "intent_detected": "create_event",
        "entities_extracted": {"datetime": "2025-11-20T15:00:00Z"},
        "confidence_score": 0.95,
        "processing_time_ms": 120
    }


# ============================================================================
# TEST 1-4: CRUD BÁSICO
# ============================================================================

@pytest.mark.asyncio
async def test_add_message(db_session, sample_conversation, sample_message_data):
    """Test 1: Crear mensaje básico"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    msg = await msg_repo.add_message(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"],
        message_id=sample_message_data["message_id"],
        user_message=sample_message_data["user_message"],
        bot_response=sample_message_data["bot_response"],
        intent_detected=sample_message_data["intent_detected"],
        entities_extracted=sample_message_data["entities_extracted"],
        confidence_score=sample_message_data["confidence_score"],
        processing_time_ms=sample_message_data["processing_time_ms"]
    )
    
    assert msg.id is not None
    assert msg.message_id == sample_message_data["message_id"]
    assert msg.user_message == "Quiero crear un evento"
    assert msg.intent_detected == "create_event"
    assert msg.confidence_score == 0.95


@pytest.mark.asyncio
async def test_get_message_by_id(db_session, sample_conversation, sample_message_data):
    """Test 2: Obtener mensaje por ID"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    created_msg = await msg_repo.add_message(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"],
        message_id=sample_message_data["message_id"],
        user_message=sample_message_data["user_message"]
    )
    
    retrieved = await msg_repo.get_by_id(
        entity_id=created_msg.id,
        tenant_id=sample_message_data["tenant_id"]
    )
    
    assert retrieved is not None
    assert retrieved.id == created_msg.id


@pytest.mark.asyncio
async def test_update_message(db_session, sample_conversation, sample_message_data):
    """Test 3: Actualizar mensaje"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    msg = await msg_repo.add_message(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"],
        message_id=sample_message_data["message_id"],
        user_message=sample_message_data["user_message"]
    )
    
    updated = await msg_repo.update(
        entity_id=msg.id,
        tenant_id=sample_message_data["tenant_id"],
        bot_response="Evento creado correctamente"
    )
    
    assert updated.bot_response == "Evento creado correctamente"


@pytest.mark.asyncio
async def test_delete_message(db_session, sample_conversation, sample_message_data):
    """Test 4: Eliminar mensaje"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    msg = await msg_repo.add_message(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"],
        message_id=sample_message_data["message_id"],
        user_message=sample_message_data["user_message"]
    )
    
    deleted = await msg_repo.delete(
        entity_id=msg.id,
        tenant_id=sample_message_data["tenant_id"]
    )
    
    assert deleted is True


# ============================================================================
# TEST 5-7: CONTEXT WINDOW (FASE 7.3)
# ============================================================================

@pytest.mark.asyncio
async def test_add_message_with_prune(db_session, sample_conversation, sample_message_data):
    """Test 5: Auto-pruning de mensajes antiguos"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    # Crear 52 mensajes (supera MAX_CONTEXT_MESSAGES=50)
    for i in range(52):
        await msg_repo.add_message_with_prune(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"msg_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje {i}"
        )
    
    # Verificar que solo quedan 50
    all_messages = await msg_repo.get_conversation_history(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"],
        limit=100
    )
    
    assert len(all_messages) == 50


@pytest.mark.asyncio
async def test_get_context_window(db_session, sample_conversation, sample_message_data):
    """Test 6: Obtener ventana de contexto"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    # Crear 10 mensajes
    for i in range(10):
        await msg_repo.add_message(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"msg_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje {i}",
            bot_response=f"Respuesta {i}"
        )
    
    # Obtener ventana de 5 mensajes
    window = await msg_repo.get_context_window(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"],
        limit=5
    )
    
    assert len(window) == 5


@pytest.mark.asyncio
async def test_get_recent(db_session, sample_conversation, sample_message_data):
    """Test 7: Obtener mensajes recientes"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    # Crear 15 mensajes
    for i in range(15):
        await msg_repo.add_message(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"msg_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje {i}"
        )
    
    # Obtener últimos 10
    recent = await msg_repo.get_recent(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"],
        limit=10
    )
    
    assert len(recent) == 10


# ============================================================================
# TEST 8-10: BÚSQUEDAS Y ANÁLISIS ML
# ============================================================================

@pytest.mark.asyncio
async def test_get_conversation_history(db_session, sample_conversation, sample_message_data):
    """Test 8: Obtener historial completo"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    # Crear 20 mensajes
    for i in range(20):
        await msg_repo.add_message(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"msg_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje {i}"
        )
    
    history = await msg_repo.get_conversation_history(
        conversation_id=conv.id,
        tenant_id=sample_message_data["tenant_id"]
    )
    
    assert len(history) == 20


@pytest.mark.asyncio
async def test_get_by_intent(db_session, sample_conversation, sample_message_data):
    """Test 9: Filtrar por intent"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    intents = ["create_event", "create_note", "create_event", "query", "create_event"]
    
    for i, intent in enumerate(intents):
        await msg_repo.add_message(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"msg_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje {i}",
            intent_detected=intent,
            confidence_score=0.8 + (i * 0.02)
        )
    
    events = await msg_repo.get_by_intent(
        tenant_id=sample_message_data["tenant_id"],
        intent="create_event"
    )
    
    assert len(events) == 3


@pytest.mark.asyncio
async def test_get_statistics(db_session, sample_conversation, sample_message_data):
    """Test 10: Estadísticas ML"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    test_data = [
        ("create_event", 0.95, 100),
        ("create_event", 0.90, 150),
        ("create_note", 0.85, 120),
        ("query", 0.75, 200),
        ("create_event", 0.92, 110)
    ]
    
    for i, (intent, conf, time_ms) in enumerate(test_data):
        await msg_repo.add_message(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"msg_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje {i}",
            intent_detected=intent,
            confidence_score=conf,
            processing_time_ms=time_ms
        )
    
    stats = await msg_repo.get_statistics(
        tenant_id=sample_message_data["tenant_id"]
    )
    
    assert stats["total_messages"] == 5
    assert stats["intent_distribution"]["create_event"] == 3


# ============================================================================
# TEST 11-13: RENDIMIENTO Y LIMPIEZA
# ============================================================================

@pytest.mark.asyncio
async def test_analyze_performance(db_session, sample_conversation, sample_message_data):
    """Test 11: Análisis de rendimiento"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    test_cases = [
        (0.95, 100),
        (0.90, 550),
        (0.45, 150),
        (None, 100),
        (0.85, 600),
        (0.40, 120),
    ]
    
    for i, (conf, time_ms) in enumerate(test_cases):
        await msg_repo.add_message(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"msg_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje {i}",
            intent_detected="create_event" if conf else None,
            confidence_score=conf,
            processing_time_ms=time_ms
        )
    
    perf = await msg_repo.analyze_performance(
        tenant_id=sample_message_data["tenant_id"],
        hours=24
    )
    
    assert perf["slow_queries"] == 2
    assert perf["low_confidence"] == 2
    assert perf["failed_detections"] == 1


@pytest.mark.asyncio
async def test_delete_old_messages(db_session, sample_conversation, sample_message_data):
    """Test 12: Eliminar mensajes antiguos"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    now = datetime.now(timezone.utc)
    
    # Mensajes antiguos
    for i in range(5):
        msg = MessageHistory(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            user_id=1,
            message_id=f"old_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje antiguo {i}"
        )
        db_session.add(msg)
        await db_session.flush()
        msg.created_at = now - timedelta(days=100)
    
    # Mensajes recientes
    for i in range(3):
        await msg_repo.add_message(
            conversation_id=conv.id,
            tenant_id=sample_message_data["tenant_id"],
            message_id=f"recent_{i}_{uuid.uuid4()}",
            user_message=f"Mensaje reciente {i}"
        )
    
    await db_session.commit()
    
    deleted = await msg_repo.delete_old_messages(
        tenant_id=sample_message_data["tenant_id"],
        days=90
    )
    
    assert deleted == 5


@pytest.mark.asyncio
async def test_multi_tenant_isolation(db_session, sample_conversation, sample_message_data):
    """Test 13: Aislamiento multi-tenant"""
    conv = await sample_conversation()
    msg_repo = MessageHistoryRepository(db_session)
    
    await msg_repo.add_message(
        conversation_id=conv.id,
        tenant_id="tenant_1",
        message_id="msg_tenant1",
        user_message="Mensaje tenant 1"
    )
    
    await msg_repo.add_message(
        conversation_id=conv.id,
        tenant_id="tenant_2",
        message_id="msg_tenant2",
        user_message="Mensaje tenant 2"
    )
    
    tenant1_msgs = await msg_repo.get_conversation_history(
        conversation_id=conv.id,
        tenant_id="tenant_1"
    )
    
    tenant2_msgs = await msg_repo.get_conversation_history(
        conversation_id=conv.id,
        tenant_id="tenant_2"
    )
    
    assert len(tenant1_msgs) == 1
    assert len(tenant2_msgs) == 1
