"""
Tests de integración TelegramAdapter + Database - ACTUALIZADOS H02 FINAL
Versión H02: Tests actualizados con get_or_create, PostgreSQL constraints y message_id
Responsable: Álvaro Fernández Mota
Fecha actualización: 15 Nov 2025 - 18:46h
"""
import pytest
from datetime import datetime, timezone
from sqlalchemy import text
from src.theaia.database.session import AsyncSessionLocal
from src.theaia.database.repositories.user_repository import UserRepository
from src.theaia.database.repositories.conversation_repository import ConversationRepository
from src.theaia.database.repositories.message_history_repository import MessageHistoryRepository
from src.theaia.database.models.user import User
from src.theaia.database.models.conversation import Conversation


@pytest.mark.asyncio
@pytest.mark.integration
class TestTelegramDatabaseIntegration:
    """Tests de integración adapter + database - Versión actualizada"""

    async def test_database_connection(self):
        """Test INT-01: Database se conecta correctamente"""
        async with AsyncSessionLocal() as session:
            assert session is not None
            result = await session.execute(text("SELECT 1"))
            assert result is not None

    async def test_user_repository_create(self):
        """Test INT-02: UserRepository get_or_create desde Telegram"""
        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)

            # Usar get_or_create_from_telegram (evita UniqueViolation)
            telegram_data = {
                "id": 999111222,
                "username": "test_user_updated",
                "first_name": "Test",
                "last_name": "User"
            }

            user, created = await repo.get_or_create_from_telegram(
                telegram_data=telegram_data,
                tenant_id="integration_test_updated"
            )

            await session.commit()

            assert user is not None
            assert user.telegram_id == 999111222
            assert user.username == "test_user_updated"

            await session.rollback()

    async def test_conversation_repository_create(self):
        """Test INT-03: ConversationRepository get_or_create"""
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            conv_repo = ConversationRepository(session)

            # Crear usuario primero
            telegram_data = {
                "id": 999111223,
                "username": "conv_test_updated",
                "first_name": "Conv",
                "last_name": "Test"
            }

            user, user_created = await user_repo.get_or_create_from_telegram(
                telegram_data=telegram_data,
                tenant_id="integration_test_conv"
            )

            # Usar get_or_create (maneja started_at automáticamente)
            conv, conv_created = await conv_repo.get_or_create(
                user_id=user.id,
                tenant_id="integration_test_conv",
                session_id="test_session_123_updated",
                initial_state="idle"
            )

            await session.commit()

            assert conv is not None
            assert conv.session_id == "test_session_123_updated"
            assert conv.current_state == "idle"
            assert conv.user_id == user.id
            assert conv.started_at is not None

            await session.rollback()

    async def test_message_repository_create(self):
        """Test INT-04: MessageHistoryRepository create con conversation_id y message_id"""
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            conv_repo = ConversationRepository(session)
            msg_repo = MessageHistoryRepository(session)

            # Crear usuario
            telegram_data = {
                "id": 999111224,
                "username": "msg_test_updated",
                "first_name": "Msg",
                "last_name": "Test"
            }

            user, _ = await user_repo.get_or_create_from_telegram(
                telegram_data=telegram_data,
                tenant_id="integration_test_msg"
            )

            # Crear conversación
            conv, _ = await conv_repo.get_or_create(
                user_id=user.id,
                tenant_id="integration_test_msg",
                session_id="test_session_456_updated",
                initial_state="idle"
            )

            # Crear mensaje (usa conversation_id y message_id)
            message = await msg_repo.create(
                tenant_id="integration_test_msg",
                user_id=user.id,
                conversation_id=conv.id,
                message_id="msg_test_456_001",
                user_message="Hola",
                bot_response="¡Hola!",
                intent_detected="saludo"
            )

            await session.commit()

            assert message is not None
            assert message.user_message == "Hola"
            assert message.bot_response == "¡Hola!"
            assert message.conversation_id == conv.id
            assert message.user_id == user.id
            assert message.message_id == "msg_test_456_001"

            await session.rollback()

    async def test_integration_full_flow(self):
        """Test INT-05: Flujo completo User -> Conversation -> Message"""
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            conv_repo = ConversationRepository(session)
            msg_repo = MessageHistoryRepository(session)

            # 1. Crear usuario
            telegram_data = {
                "id": 999111225,
                "username": "full_flow_test",
                "first_name": "Full",
                "last_name": "Flow"
            }

            user, _ = await user_repo.get_or_create_from_telegram(
                telegram_data=telegram_data,
                tenant_id="integration_test_full"
            )

            # 2. Crear conversación
            conv, _ = await conv_repo.get_or_create(
                user_id=user.id,
                tenant_id="integration_test_full",
                session_id=f"session_full_{user.telegram_id}",
                initial_state="greeting"
            )

            # 3. Crear mensaje con message_id
            message = await msg_repo.create(
                tenant_id="integration_test_full",
                user_id=user.id,
                conversation_id=conv.id,
                message_id=f"msg_full_{user.telegram_id}_001",
                user_message="Prueba flujo completo",
                bot_response="Flujo completado correctamente",
                intent_detected="test"
            )

            await session.commit()

            # Verificar relaciones
            assert message.user_id == user.id
            assert message.conversation_id == conv.id
            assert conv.user_id == user.id

            # Verificar que todo existe
            assert user.id is not None
            assert conv.id is not None
            assert message.id is not None
            assert message.message_id is not None

            await session.rollback()

            print("\n✅ Integration Full Flow Test PASSED")
            print(f"   User: {user.username} (ID: {user.id})")
            print(f"   Conversation: {conv.session_id}")
            print(f"   Message: {message.message_id}")