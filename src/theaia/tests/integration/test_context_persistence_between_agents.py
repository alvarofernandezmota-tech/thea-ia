"""
Test: Context Persistence Between Agents - REFACTORIZADO H02 FINAL
PostgreSQL + THEA-IA Ecosystem - 100% Funcional
Responsable: Álvaro Fernández Mota
Fecha: 15 Nov 2025
"""
import pytest
from src.theaia.database.session import AsyncSessionLocal
from src.theaia.database.repositories.user_repository import UserRepository
from src.theaia.database.repositories.conversation_repository import ConversationRepository


@pytest.mark.asyncio
async def test_context_persistence_across_agents():
    """
    Verifica persistencia de contexto PostgreSQL entre diferentes estados FSM.
    
    Flujo:
    1. Crear usuario
    2. Crear conversación con estado "agenda_collecting"
    3. Actualizar contexto
    4. Crear conversación con estado "note_creating"
    5. Verificar persistencia de contexto original
    """
    
    async with AsyncSessionLocal() as session:
        # Repositorios
        user_repo = UserRepository(session)
        conv_repo = ConversationRepository(session)
        
        # PASO 1: Crear usuario
        telegram_data = {
            "id": 999888777,
            "username": "test_persist",
            "first_name": "Test",
            "last_name": "Persist"
        }
        
        user, user_created = await user_repo.get_or_create_from_telegram(
            telegram_data=telegram_data,
            tenant_id="test_tenant_persist"
        )
        
        assert user is not None
        assert user.telegram_id == 999888777
        
        # PASO 2: Crear conversación estado "agenda_collecting"
        conv_agenda, agenda_created = await conv_repo.get_or_create(
            user_id=user.id,
            tenant_id="test_tenant_persist",
            session_id=f"session_agenda_{user.telegram_id}",
            initial_state="agenda_collecting"
        )
        
        assert conv_agenda is not None
        assert conv_agenda.current_state == "agenda_collecting"
        assert conv_agenda.user_id == user.id
        
        # PASO 3: Actualizar contexto con datos de agenda
        conv_agenda.context_data = {
            "agent_intent": "agenda",
            "step": "date_input",
            "data": {"meeting": "team sync", "date": "2025-11-20"}
        }
        await session.commit()
        
        # PASO 4: Crear nueva conversación para "note"
        conv_note, note_created = await conv_repo.get_or_create(
            user_id=user.id,
            tenant_id="test_tenant_persist",
            session_id=f"session_note_{user.telegram_id}",
            initial_state="note_creating"
        )
        
        assert conv_note is not None
        assert conv_note.current_state == "note_creating"
        assert conv_note.user_id == user.id
        assert conv_note.id != conv_agenda.id  # Diferentes conversaciones
        
        # PASO 5: Verificar que conversación agenda persiste
        await session.refresh(conv_agenda)
        
        assert conv_agenda.current_state == "agenda_collecting"
        assert conv_agenda.context_data["agent_intent"] == "agenda"
        assert conv_agenda.context_data["step"] == "date_input"
        assert conv_agenda.context_data["data"]["meeting"] == "team sync"
        
        # PASO 6: Verificar ambas conversaciones por session_id
        conv_agenda_check = await conv_repo.get_by_session_id(
            session_id=f"session_agenda_{user.telegram_id}",
            tenant_id="test_tenant_persist"
        )
        
        conv_note_check = await conv_repo.get_by_session_id(
            session_id=f"session_note_{user.telegram_id}",
            tenant_id="test_tenant_persist"
        )
        
        assert conv_agenda_check is not None
        assert conv_note_check is not None
        assert conv_agenda_check.id == conv_agenda.id
        assert conv_note_check.id == conv_note.id
        
        # Cleanup - Argumentos posicionales
        await conv_repo.delete(conv_agenda.id, "test_tenant_persist")
        await conv_repo.delete(conv_note.id, "test_tenant_persist")
        await session.commit()
        
        print("\n✅ Context Persistence Test PASSED")
        print(f"   User ID: {user.id}")
        print(f"   Telegram ID: {user.telegram_id}")
        print(f"   User created: {user_created}")
        print(f"   Agenda created: {agenda_created}")
        print(f"   Agenda state: {conv_agenda.current_state}")
        print(f"   Agenda context: {conv_agenda.context_data}")
        print(f"   Note created: {note_created}")
        print(f"   Note state: {conv_note.current_state}")
        print(f"   Both conversations verified via session_id ✅")
