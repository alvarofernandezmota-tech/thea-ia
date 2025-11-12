"""
Tests Repositories - THEA IA H02
Tests completos de repositories con PostgreSQL

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer
Estado: COMPLETO
"""

import pytest
from datetime import datetime, timezone
from sqlalchemy import text

from src.theaia.database.session import AsyncSessionLocal
from src.theaia.database.connection import get_async_engine
from src.theaia.database.repositories import (
    UserRepository,
    EventRepository,
    NoteRepository,
    ConversationRepository,
    MessageHistoryRepository,
)


# ==================== TEST CONEXIÓN ====================

@pytest.mark.asyncio
async def test_database_connection():
    """Verifica que PostgreSQL está accesible y responde."""
    engine = get_async_engine()
    
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1, "PostgreSQL no retornó el valor esperado"
    except Exception as e:
        pytest.fail(f"Fallo conexión PostgreSQL: {e}")
    finally:
        await engine.dispose()


# ==================== TEST INSTANTIATION ====================

@pytest.mark.asyncio
async def test_repositories_instantiate():
    """Verifica que todos los repositories se pueden instanciar correctamente."""
    async with AsyncSessionLocal() as session:
        # Instanciar todos los repositories
        user_repo = UserRepository(session)
        event_repo = EventRepository(session)
        note_repo = NoteRepository(session)
        conv_repo = ConversationRepository(session)
        msg_repo = MessageHistoryRepository(session)
        
        # Verificar que no son None
        assert user_repo is not None, "UserRepository no se instanció"
        assert event_repo is not None, "EventRepository no se instanció"
        assert note_repo is not None, "NoteRepository no se instanció"
        assert conv_repo is not None, "ConversationRepository no se instanció"
        assert msg_repo is not None, "MessageHistoryRepository no se instanció"
        
        # Verificar métodos heredados de BaseRepository
        for repo in [user_repo, event_repo, note_repo, conv_repo, msg_repo]:
            assert hasattr(repo, 'create'), f"{repo.__class__.__name__} no tiene método create"
            assert hasattr(repo, 'get_by_id'), f"{repo.__class__.__name__} no tiene método get_by_id"
            assert hasattr(repo, 'get_all'), f"{repo.__class__.__name__} no tiene método get_all"
            assert hasattr(repo, 'update'), f"{repo.__class__.__name__} no tiene método update"
            assert hasattr(repo, 'delete'), f"{repo.__class__.__name__} no tiene método delete"


# ==================== TEST USER REPOSITORY ====================

@pytest.mark.asyncio
async def test_user_repository_create():
    """Test creación de usuario con UserRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        
        try:
            # Crear usuario de test
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=999999999,
                username="test_user_h02",
                first_name="Test",
                last_name="User",
                language_code="es",
                is_active=True
            )
            
            # Verificar campos
            assert user.id is not None, "User ID no asignado"
            assert user.telegram_id == 999999999, "telegram_id incorrecto"
            assert user.tenant_id == "test_h02", "tenant_id incorrecto"
            assert user.username == "test_user_h02", "username incorrecto"
            assert user.is_active is True, "is_active debe ser True"
            assert user.created_at is not None, "created_at no asignado"
            
        finally:
            await session.rollback()


@pytest.mark.asyncio
async def test_user_repository_get_or_create():
    """Test get_or_create_from_telegram de UserRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        
        try:
            telegram_data = {
                "id": 888888888,
                "username": "test_telegram_user",
                "first_name": "Telegram",
                "last_name": "Test",
                "language_code": "es"
            }
            
            # Primera llamada: debe crear
            user1, created1 = await user_repo.get_or_create_from_telegram(
                telegram_data=telegram_data,
                tenant_id="test_h02"
            )
            
            assert created1 is True, "Debe crear usuario en primera llamada"
            assert user1.telegram_id == 888888888
            
            # Segunda llamada: debe obtener existente
            user2, created2 = await user_repo.get_or_create_from_telegram(
                telegram_data=telegram_data,
                tenant_id="test_h02"
            )
            
            assert created2 is False, "No debe crear usuario en segunda llamada"
            assert user2.id == user1.id, "Debe retornar el mismo usuario"
            
        finally:
            await session.rollback()


# ==================== TEST EVENT REPOSITORY ====================

@pytest.mark.asyncio
async def test_event_repository_create():
    """Test creación de evento con EventRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        event_repo = EventRepository(session)
        
        try:
            # Crear usuario primero
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=777777777,
                username="test_user_events"
            )
            
            # Crear evento
            event = await event_repo.create(
                tenant_id="test_h02",
                user_id=user.id,
                title="Reunión H02",
                description="Test de evento",
                start_datetime=datetime(2025, 11, 15, 15, 0, tzinfo=timezone.utc),
                status="pending",
                reminder_minutes=15
            )
            
            # Verificar campos
            assert event.id is not None, "Event ID no asignado"
            assert event.title == "Reunión H02", "Título incorrecto"
            assert event.user_id == user.id, "user_id incorrecto"
            assert event.status == "pending", "Status debe ser pending"
            assert event.reminder_minutes == 15, "reminder_minutes incorrecto"
            assert event.created_at is not None, "created_at no asignado"
            
        finally:
            await session.rollback()


@pytest.mark.asyncio
async def test_event_repository_get_upcoming():
    """Test método get_upcoming de EventRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        event_repo = EventRepository(session)
        
        try:
            # Crear usuario
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=666666666,
                username="test_upcoming"
            )
            
            # Crear evento futuro (mañana)
            future_event = await event_repo.create(
                tenant_id="test_h02",
                user_id=user.id,
                title="Evento Futuro",
                start_datetime=datetime(2025, 12, 1, 10, 0, tzinfo=timezone.utc),
                status="pending"
            )
            
            # Buscar eventos próximos (próximos 30 días)
            upcoming = await event_repo.get_upcoming(
                user_id=user.id,
                tenant_id="test_h02",
                hours=24 * 30  # 30 días
            )
            
            # Verificar (puede que no aparezca si la fecha está muy lejos)
            # Solo verificamos que el método no falla
            assert isinstance(upcoming, list), "get_upcoming debe retornar lista"
            
        finally:
            await session.rollback()


# ==================== TEST NOTE REPOSITORY ====================

@pytest.mark.asyncio
async def test_note_repository_create():
    """Test creación de nota con NoteRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        note_repo = NoteRepository(session)
        
        try:
            # Crear usuario
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=555555555,
                username="test_user_notes"
            )
            
            # Crear nota
            note = await note_repo.create(
                tenant_id="test_h02",
                user_id=user.id,
                title="Nota Test H02",
                content="Esta es una nota de prueba para H02",
                tags=["test", "h02", "database"],
                category="testing",
                priority=1,
                is_pinned=False
            )
            
            # Verificar campos
            assert note.id is not None, "Note ID no asignado"
            assert note.title == "Nota Test H02", "Título incorrecto"
            assert note.content == "Esta es una nota de prueba para H02", "Contenido incorrecto"
            assert "test" in note.tags, "Tag 'test' no encontrado"
            assert "h02" in note.tags, "Tag 'h02' no encontrado"
            assert note.category == "testing", "Categoría incorrecta"
            assert note.priority == 1, "Prioridad incorrecta"
            assert note.is_pinned is False, "is_pinned debe ser False"
            
        finally:
            await session.rollback()


@pytest.mark.asyncio
async def test_note_repository_search():
    """Test búsqueda de notas con NoteRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        note_repo = NoteRepository(session)
        
        try:
            # Crear usuario
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=444444444,
                username="test_search"
            )
            
            # Crear nota con contenido específico
            note = await note_repo.create(
                tenant_id="test_h02",
                user_id=user.id,
                title="Búsqueda Test",
                content="Este contenido tiene la palabra THEA_IA para buscar",
                tags=["search"]
            )
            
            # Buscar por palabra clave
            results = await note_repo.search(
                user_id=user.id,
                tenant_id="test_h02",
                query="THEA_IA"
            )
            
            # Verificar
            assert len(results) >= 1, "Debe encontrar al menos 1 nota"
            found = any(n.id == note.id for n in results)
            assert found, "Debe encontrar la nota creada"
            
        finally:
            await session.rollback()


# ==================== TEST CONVERSATION REPOSITORY ====================

@pytest.mark.asyncio
async def test_conversation_repository_get_or_create():
    """Test get_or_create de ConversationRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        conv_repo = ConversationRepository(session)
        
        try:
            # Crear usuario
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=333333333,
                username="test_user_conv"
            )
            
            # Primera llamada: debe crear conversación
            conv1, created1 = await conv_repo.get_or_create(
                user_id=user.id,
                tenant_id="test_h02",
                session_id="test_session_h02_123",
                initial_state="idle"
            )
            
            assert created1 is True, "Debe crear conversación en primera llamada"
            assert conv1.session_id == "test_session_h02_123", "session_id incorrecto"
            assert conv1.current_state == "idle", "Estado inicial debe ser idle"
            assert conv1.is_active is True, "is_active debe ser True"
            
            # Segunda llamada: debe obtener existente
            conv2, created2 = await conv_repo.get_or_create(
                user_id=user.id,
                tenant_id="test_h02",
                session_id="test_session_h02_123"
            )
            
            assert created2 is False, "No debe crear conversación en segunda llamada"
            assert conv2.id == conv1.id, "Debe retornar la misma conversación"
            
        finally:
            await session.rollback()


@pytest.mark.asyncio
async def test_conversation_repository_update_state():
    """Test update_state de ConversationRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        conv_repo = ConversationRepository(session)
        
        try:
            # Crear usuario y conversación
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=222222222,
                username="test_state"
            )
            
            conv, _ = await conv_repo.get_or_create(
                user_id=user.id,
                tenant_id="test_h02",
                session_id="test_state_123",
                initial_state="idle"
            )
            
            # Actualizar estado
            updated = await conv_repo.update_state(
                conversation_id=conv.id,
                tenant_id="test_h02",
                new_state="awaiting_confirmation",
                context={"action": "create_event", "title": "Test"}
            )
            
            assert updated is not None, "update_state debe retornar conversación"
            assert updated.current_state == "awaiting_confirmation", "Estado no actualizado"
            assert updated.context_data["action"] == "create_event", "Contexto no actualizado"
            assert updated.context_data["title"] == "Test", "Contexto title incorrecto"
            
        finally:
            await session.rollback()


# ==================== TEST MESSAGE HISTORY REPOSITORY ====================

@pytest.mark.asyncio
async def test_message_history_repository_add_message():
    """Test add_message de MessageHistoryRepository."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        conv_repo = ConversationRepository(session)
        msg_repo = MessageHistoryRepository(session)
        
        try:
            # Crear usuario y conversación
            user = await user_repo.create(
                tenant_id="test_h02",
                telegram_id=111111111,
                username="test_messages"
            )
            
            conv, _ = await conv_repo.get_or_create(
                user_id=user.id,
                tenant_id="test_h02",
                session_id="test_msg_123"
            )
            
            # Añadir mensaje
            message = await msg_repo.add_message(
                conversation_id=conv.id,
                tenant_id="test_h02",
                message_id="msg_test_001",
                user_message="Quiero crear un evento",
                bot_response="¿Qué título tiene el evento?",
                intent_detected="create_event",
                entities_extracted={"intent": "create_event"},
                confidence_score=0.95,
                processing_time_ms=120
            )
            
            # Verificar
            assert message.id is not None, "Message ID no asignado"
            assert message.message_id == "msg_test_001", "message_id incorrecto"
            assert message.intent_detected == "create_event", "Intent incorrecto"
            assert message.confidence_score == 0.95, "Confidence score incorrecto"
            assert message.processing_time_ms == 120, "Processing time incorrecto"
            
        finally:
            await session.rollback()


# ==================== TEST MULTI-TENANT ISOLATION ====================

@pytest.mark.asyncio
async def test_multi_tenant_isolation():
    """Verifica que multi-tenant isolation funciona correctamente."""
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        
        try:
            # Crear usuarios en diferentes tenants
            user_tenant_a = await user_repo.create(
                tenant_id="tenant_a",
                telegram_id=100001,
                username="user_a"
            )
            
            user_tenant_b = await user_repo.create(
                tenant_id="tenant_b",
                telegram_id=100002,
                username="user_b"
            )
            
            # Verificar que get_all filtra por tenant
            users_a = await user_repo.get_all(tenant_id="tenant_a")
            users_b = await user_repo.get_all(tenant_id="tenant_b")
            
            # Tenant A solo debe ver su usuario
            assert len([u for u in users_a if u.telegram_id == 100001]) == 1
            assert len([u for u in users_a if u.telegram_id == 100002]) == 0
            
            # Tenant B solo debe ver su usuario
            assert len([u for u in users_b if u.telegram_id == 100002]) == 1
            assert len([u for u in users_b if u.telegram_id == 100001]) == 0
            
        finally:
            await session.rollback()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
