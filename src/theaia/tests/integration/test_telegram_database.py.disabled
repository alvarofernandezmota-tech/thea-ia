import pytest
from src.theaia.database.session import SessionLocal
from src.theaia.database.models.user import User
from src.theaia.database.models.message_history import MessageHistory
from src.theaia.database.repositories.user_repository import UserRepository
from src.theaia.database.repositories.message_history_repository import MessageHistoryRepository
from datetime import datetime, timezone


class TestTelegramDatabaseIntegration:
    """Test Telegram adapter database integration with PostgreSQL."""
    
    def test_user_repository_create(self):
        """Test user creation and retrieval from PostgreSQL."""
        session = SessionLocal()
        
        try:
            repo = UserRepository(session)
            
            # Datos de usuario de prueba
            user_data = {
                "telegram_id": 987654321,
                "username": "test_telegram_user",
                "first_name": "Test",
                "last_name": "User",
                "is_bot": False,
                "language_code": "es"
            }
            
            # Crear usuario
            user = User(
                telegram_id=user_data["telegram_id"],
                username=user_data["username"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                is_bot=user_data["is_bot"],
                language_code=user_data["language_code"],
                tenant_id="test_tenant",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # Verificaciones
            assert user.id is not None
            assert user.telegram_id == 987654321
            assert user.username == "test_telegram_user"
            assert user.first_name == "Test"
            assert user.tenant_id == "test_tenant"
            
            # Verificar que se puede recuperar
            retrieved_user = session.query(User).filter_by(
                telegram_id=987654321,
                tenant_id="test_tenant"
            ).first()
            
            assert retrieved_user is not None
            assert retrieved_user.id == user.id
            
            # Cleanup
            session.delete(user)
            session.commit()
            
            print("✅ UserRepository CREATE test PASSED")
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def test_message_repository_create(self):
        """Test message creation and storage in PostgreSQL."""
        session = SessionLocal()
        
        try:
            # Primero crear un usuario para asociar mensajes
            user = User(
                telegram_id=111222333,
                username="test_msg_user",
                first_name="Msg",
                last_name="Test",
                is_bot=False,
                language_code="es",
                tenant_id="test_tenant",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # Crear mensaje
            message = MessageHistory(
                user_id=user.id,
                tenant_id="test_tenant",
                message_type="user_input",
                content="Test message for database",
                sender="user",
                conversation_id=f"conv_{user.id}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            session.add(message)
            session.commit()
            session.refresh(message)
            
            # Verificaciones
            assert message.id is not None
            assert message.user_id == user.id
            assert message.content == "Test message for database"
            assert message.message_type == "user_input"
            assert message.sender == "user"
            assert message.tenant_id == "test_tenant"
            
            # Verificar que se puede recuperar
            retrieved_msg = session.query(MessageHistory).filter_by(
                user_id=user.id,
                tenant_id="test_tenant"
            ).first()
            
            assert retrieved_msg is not None
            assert retrieved_msg.id == message.id
            assert retrieved_msg.content == "Test message for database"
            
            # Cleanup
            session.delete(message)
            session.delete(user)
            session.commit()
            
            print("✅ MessageHistoryRepository CREATE test PASSED")
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def test_user_telegram_attributes(self):
        """Test user Telegram-specific attributes."""
        session = SessionLocal()
        
        try:
            user = User(
                telegram_id=555666777,
                username="telegram_bot_test",
                first_name="Bot",
                last_name="Test",
                is_bot=True,
                language_code="en",
                tenant_id="test_tenant",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # Verificaciones de atributos Telegram
            assert user.is_bot is True
            assert user.language_code == "en"
            assert user.telegram_id == 555666777
            assert user.username == "telegram_bot_test"
            
            # Cleanup
            session.delete(user)
            session.commit()
            
            print("✅ User Telegram attributes test PASSED")
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def test_database_connection(self):
        """Test basic database connectivity."""
        session = SessionLocal()
        
        try:
            # Verificar que la conexión funciona
            assert session is not None
            
            # Intentar una query simple
            result = session.query(User).limit(1).all()
            assert isinstance(result, list)
            
            print("✅ Database connection test PASSED")
            
        except Exception as e:
            raise e
        finally:
            session.close()
