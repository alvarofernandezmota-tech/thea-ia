"""
Tests para UserRepository (FASE 8.1).

Cobertura objetivo: 22% → 85%+
Tests: 13 (básicos + avanzados + edge cases)

Autor: Álvaro Fernández Mota
Fecha: 19 Nov 2025
Hito: H02 FASE 8 - Advanced Persistence
"""
import pytest
from sqlalchemy import select
from src.theaia.database.repositories.user_repository import UserRepository
from src.theaia.database.models.user import User


class TestUserRepositoryBasic:
    """Tests básicos CRUD."""

    @pytest.mark.asyncio
    async def test_create_user_basic(self, db_session, test_tenant_id, test_user_data):
        """Crear usuario básico."""
        repo = UserRepository(db_session)
        
        user = await repo.create(**test_user_data)
        
        assert user.id is not None
        assert user.telegram_id == test_user_data["telegram_id"]
        assert user.username == test_user_data["username"]
        assert user.tenant_id == test_tenant_id

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, db_session, test_tenant_id, test_user_data):
        """Obtener usuario por ID."""
        repo = UserRepository(db_session)
        
        # Crear
        created_user = await repo.create(**test_user_data)
        
        # Obtener
        retrieved_user = await repo.get_by_id(created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.telegram_id == test_user_data["telegram_id"]

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, db_session):
        """Obtener usuario inexistente."""
        repo = UserRepository(db_session)
        
        user = await repo.get_by_id(99999)
        
        assert user is None

    @pytest.mark.asyncio
    async def test_update_user(self, db_session, test_tenant_id, test_user_data):
        """Actualizar usuario."""
        repo = UserRepository(db_session)
        
        # Crear
        user = await repo.create(**test_user_data)
        
        # Actualizar (✅ CORREGIDO: añadido test_tenant_id)
        updated_user = await repo.update(
            user.id,
            test_tenant_id,
            first_name="Updated",
            last_name="Name"
        )
        
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"

    @pytest.mark.asyncio
    async def test_delete_user(self, db_session, test_tenant_id, test_user_data):
        """Eliminar usuario."""
        repo = UserRepository(db_session)
        
        # Crear
        user = await repo.create(**test_user_data)
        user_id = user.id
        
        # Eliminar (✅ CORREGIDO: añadido test_tenant_id)
        await repo.delete(user_id, test_tenant_id)
        
        # Verificar eliminación
        deleted_user = await repo.get_by_id(user_id)
        assert deleted_user is None


class TestUserRepositoryTelegram:
    """Tests específicos Telegram."""

    @pytest.mark.asyncio
    async def test_get_by_telegram_id(self, db_session, test_tenant_id, test_user_data):
        """Obtener usuario por Telegram ID."""
        repo = UserRepository(db_session)
        
        # Crear
        created_user = await repo.create(**test_user_data)
        
        # Obtener por Telegram ID
        retrieved_user = await repo.get_by_telegram_id(
            test_user_data["telegram_id"],
            test_tenant_id
        )
        
        assert retrieved_user is not None
        assert retrieved_user.telegram_id == test_user_data["telegram_id"]

    @pytest.mark.asyncio
    async def test_get_or_create_user_new(self, db_session, test_tenant_id, test_user_data):
        """Get or create: usuario nuevo."""
        repo = UserRepository(db_session)
        
        user, created = await repo.get_or_create_telegram_user(
            telegram_id=test_user_data["telegram_id"],
            tenant_id=test_tenant_id,
            defaults={
                "username": test_user_data["username"],
                "first_name": test_user_data["first_name"],
                "last_name": test_user_data["last_name"],
            }
        )
        
        assert user is not None
        assert created is True
        assert user.telegram_id == test_user_data["telegram_id"]

    @pytest.mark.asyncio
    async def test_get_or_create_user_existing(self, db_session, test_tenant_id, test_user_data):
        """Get or create: usuario existente."""
        repo = UserRepository(db_session)
        
        # Crear primero
        original_user = await repo.create(**test_user_data)
        
        # Get or create (debería retornar existente)
        user, created = await repo.get_or_create_telegram_user(
            telegram_id=test_user_data["telegram_id"],
            tenant_id=test_tenant_id,
            defaults={"username": "different"}
        )
        
        assert user.id == original_user.id
        assert created is False


class TestUserRepositoryMultiTenant:
    """Tests multi-tenant isolation."""

    @pytest.mark.asyncio
    async def test_users_isolated_by_tenant(self, db_session, test_user_data):
        """Usuarios aislados por tenant."""
        repo = UserRepository(db_session)
        
        # Usuario tenant 1
        user_data_1 = {**test_user_data, "tenant_id": "tenant_1"}
        user_1 = await repo.create(**user_data_1)
        
        # Usuario tenant 2 (mismo telegram_id)
        user_data_2 = {**test_user_data, "tenant_id": "tenant_2"}
        user_2 = await repo.create(**user_data_2)
        
        # Verificar que son diferentes
        assert user_1.id != user_2.id
        assert user_1.tenant_id == "tenant_1"
        assert user_2.tenant_id == "tenant_2"
        
        # Verificar que no cruzan datos
        retrieved_1 = await repo.get_by_telegram_id(
            test_user_data["telegram_id"],
            "tenant_1"
        )
        assert retrieved_1.id == user_1.id


class TestUserRepositoryPreferences:
    """Tests preferencias de usuario."""

    @pytest.mark.asyncio
    async def test_update_preferences(self, db_session, test_tenant_id, test_user_data):
        """Actualizar preferencias de usuario."""
        repo = UserRepository(db_session)
        
        user = await repo.create(**test_user_data)
        
        prefs = {"language": "en", "notifications": False}
        # ✅ CORREGIDO: añadido test_tenant_id
        updated = await repo.update(user.id, test_tenant_id, preferences=prefs)
        
        assert updated.preferences == prefs

    @pytest.mark.asyncio
    async def test_update_last_activity(self, db_session, test_tenant_id, test_user_data):
        """Actualizar última actividad."""
        repo = UserRepository(db_session)
        
        user = await repo.create(**test_user_data)
        
        # Actualizar última actividad
        updated = await repo.update_last_activity(user.id)
        
        assert updated.last_activity is not None
        assert updated.last_activity > user.created_at


class TestUserRepositoryEdgeCases:
    """Tests casos especiales."""

    @pytest.mark.asyncio
    async def test_create_duplicate_telegram_id_different_tenant(self, db_session, test_user_data):
        """Mismo Telegram ID en tenants diferentes es permitido."""
        repo = UserRepository(db_session)
        
        # Crear en tenant 1
        user_1 = await repo.create(**test_user_data)
        
        # Crear en tenant 2 con mismo telegram_id (debería funcionar)
        user_data_2 = {**test_user_data, "tenant_id": "tenant_2"}
        user_2 = await repo.create(**user_data_2)
        
        assert user_1.id != user_2.id

    @pytest.mark.asyncio
    async def test_get_all_users_by_tenant(self, db_session, test_user_data):
        """Obtener todos los usuarios de un tenant."""
        repo = UserRepository(db_session)
        
        # Crear múltiples usuarios
        for i in range(3):
            data = {
                **test_user_data,
                "telegram_id": 10000 + i,
                "username": f"user_{i}"
            }
            await repo.create(**data)
        
        # Obtener todos (✅ CORREGIDO: añadido tenant_id)
        all_users = await repo.get_all(test_user_data["tenant_id"])
        
        assert len(all_users) >= 3
