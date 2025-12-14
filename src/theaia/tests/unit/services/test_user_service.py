"""Unit tests for UserService.

Tests cover all CRUD operations, timezone management, and user tracking.
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.theaia.services.user_service import UserService
from src.theaia.database.models import User


@pytest.fixture
def user_service():
    """Create a UserService instance for testing."""
    return UserService()


@pytest.fixture
def sample_telegram_id():
    """Return a sample Telegram ID."""
    return "123456789"


@pytest.fixture
def sample_user_data():
    """Return sample user data."""
    return {
        "telegram_id": "123456789",
        "username": "test_user",
        "first_name": "Test",
        "last_name": "User",
        "timezone": "America/New_York",
        "tenant_id": "test-tenant-001",  # ✅ ADDED
    }


class TestUserServiceCreate:
    """Tests for user creation."""

    def test_create_user_success(self, user_service, sample_user_data):
        """Test successful user creation."""
        user = user_service.create_user(
            telegram_id=sample_user_data["telegram_id"],
            username=sample_user_data["username"],
            first_name=sample_user_data["first_name"],
            last_name=sample_user_data["last_name"],
            timezone=sample_user_data["timezone"],
            tenant_id=sample_user_data["tenant_id"],  # ✅ ADDED
        )
        
        assert user is not None
        assert user.telegram_id == sample_user_data["telegram_id"]
        assert user.username == sample_user_data["username"]
        assert user.first_name == sample_user_data["first_name"]
        assert user.timezone == sample_user_data["timezone"]
        assert user.tenant_id == sample_user_data["tenant_id"]  # ✅ ADDED
        assert user.created_at is not None

    def test_create_user_with_minimal_data(self, user_service):
        """Test user creation with minimal required data."""
        user = user_service.create_user(
            telegram_id="987654321",
            username="minimal_user",
            tenant_id="test-tenant-001",  # ✅ ADDED
        )
        
        assert user is not None
        assert user.telegram_id == "987654321"
        assert user.username == "minimal_user"
        assert user.tenant_id == "test-tenant-001"  # ✅ ADDED
        assert user.timezone is None or user.timezone == "UTC"

    def test_create_user_duplicate_telegram_id(self, user_service, sample_user_data):
        """Test that creating duplicate telegram IDs raises error."""
        # Create first user
        user_service.create_user(**sample_user_data)
        
        # Try to create duplicate
        with pytest.raises(ValueError, match="already exists"):
            user_service.create_user(**sample_user_data)

    def test_create_user_sets_last_interaction(self, user_service):
        """Test that last_interaction is set on creation."""
        before_creation = datetime.utcnow()
        user = user_service.create_user(
            telegram_id="111111111",
            username="test_interaction",
            tenant_id="test-tenant-001",  # ✅ ADDED
        )
        after_creation = datetime.utcnow()
        
        assert user.last_interaction is not None
        assert before_creation <= user.last_interaction <= after_creation


class TestUserServiceRead:
    """Tests for user retrieval."""

    def test_get_user_existing(self, user_service, sample_user_data):
        """Test retrieving an existing user."""
        created_user = user_service.create_user(**sample_user_data)
        retrieved_user = user_service.get_user(created_user.telegram_id)
        
        assert retrieved_user is not None
        assert retrieved_user.telegram_id == created_user.telegram_id
        assert retrieved_user.username == created_user.username

    def test_get_user_not_found(self, user_service):
        """Test retrieving a non-existent user."""
        user = user_service.get_user("nonexistent")
        assert user is None

    def test_get_user_by_username(self, user_service, sample_user_data):
        """Test retrieving user by username."""
        created_user = user_service.create_user(**sample_user_data)
        retrieved_user = user_service.get_user_by_username(created_user.username)
        
        assert retrieved_user is not None
        assert retrieved_user.username == created_user.username

    def test_get_user_by_username_not_found(self, user_service):
        """Test retrieving non-existent user by username."""
        user = user_service.get_user_by_username("nonexistent_user")
        assert user is None


class TestUserServiceUpdate:
    """Tests for user updates."""

    def test_update_user_timezone(self, user_service, sample_user_data):
        """Test updating user timezone."""
        user = user_service.create_user(**sample_user_data)
        new_timezone = "Europe/Madrid"
        
        updated_user = user_service.update_user(
            telegram_id=user.telegram_id,
            timezone=new_timezone,
        )
        
        assert updated_user.timezone == new_timezone

    def test_update_user_username(self, user_service, sample_user_data):
        """Test updating user username."""
        user = user_service.create_user(**sample_user_data)
        new_username = "updated_username"
        
        updated_user = user_service.update_user(
            telegram_id=user.telegram_id,
            username=new_username,
        )
        
        assert updated_user.username == new_username

    def test_update_user_multiple_fields(self, user_service, sample_user_data):
        """Test updating multiple fields."""
        user = user_service.create_user(**sample_user_data)
        
        updated_user = user_service.update_user(
            telegram_id=user.telegram_id,
            first_name="Updated",
            last_name="Name",
            timezone="Asia/Tokyo",
        )
        
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.timezone == "Asia/Tokyo"

    def test_update_user_not_found(self, user_service):
        """Test updating non-existent user."""
        with pytest.raises(ValueError, match="not found"):
            user_service.update_user(
                telegram_id="nonexistent",
                username="new_name",
            )

    def test_update_user_updates_modified_timestamp(self, user_service, sample_user_data):
        """Test that update changes modified_at timestamp."""
        user = user_service.create_user(**sample_user_data)
        original_modified = user.modified_at
        
        import time
        time.sleep(0.1)  # Ensure time difference
        
        updated_user = user_service.update_user(
            telegram_id=user.telegram_id,
            username="new_username",
        )
        
        assert updated_user.modified_at > original_modified


class TestUserServiceDelete:
    """Tests for user deletion."""

    def test_delete_user_success(self, user_service, sample_user_data):
        """Test successful user deletion."""
        user = user_service.create_user(**sample_user_data)
        telegram_id = user.telegram_id
        
        result = user_service.delete_user(telegram_id)
        assert result is True
        
        # Verify user is deleted
        deleted_user = user_service.get_user(telegram_id)
        assert deleted_user is None

    def test_delete_user_not_found(self, user_service):
        """Test deleting non-existent user."""
        with pytest.raises(ValueError, match="not found"):
            user_service.delete_user("nonexistent")

    def test_delete_user_idempotent_false(self, user_service, sample_user_data):
        """Test that double delete raises error."""
        user = user_service.create_user(**sample_user_data)
        user_service.delete_user(user.telegram_id)
        
        with pytest.raises(ValueError):
            user_service.delete_user(user.telegram_id)


class TestUserServiceInteractionTracking:
    """Tests for user interaction tracking."""

    def test_update_last_interaction(self, user_service, sample_user_data):
        """Test updating last interaction timestamp."""
        user = user_service.create_user(**sample_user_data)
        original_time = user.last_interaction
        
        import time
        time.sleep(0.1)
        
        user_service.update_last_interaction(user.telegram_id)
        updated_user = user_service.get_user(user.telegram_id)
        
        assert updated_user.last_interaction > original_time

    def test_update_last_interaction_not_found(self, user_service):
        """Test updating interaction for non-existent user."""
        with pytest.raises(ValueError, match="not found"):
            user_service.update_last_interaction("nonexistent")

    def test_get_inactive_users(self, user_service):
        """Test retrieving inactive users."""
        # Create multiple users
        user1 = user_service.create_user(
            telegram_id="111",
            username="user1",
            tenant_id="test-tenant-001",  # ✅ ADDED
        )
        user2 = user_service.create_user(
            telegram_id="222",
            username="user2",
            tenant_id="test-tenant-001",  # ✅ ADDED
        )
        
        # Mark user1 as inactive (older than 30 days)
        inactive_threshold = datetime.utcnow() - timedelta(days=31)
        user_service._db_session.query(User).filter(
            User.telegram_id == user1.telegram_id
        ).update({"last_interaction": inactive_threshold})
        
        # Get inactive users
        inactive = user_service.get_inactive_users(days=30)
        
        assert len(inactive) >= 1
        assert any(u.telegram_id == user1.telegram_id for u in inactive)


class TestUserServicePreferences:
    """Tests for user preferences."""

    def test_get_user_preferences(self, user_service, sample_user_data):
        """Test retrieving user preferences."""
        user = user_service.create_user(**sample_user_data)
        prefs = user_service.get_user_preferences(user.telegram_id)
        
        assert prefs is not None
        assert "timezone" in prefs
        assert prefs["timezone"] == sample_user_data["timezone"]

    def test_update_user_preferences(self, user_service, sample_user_data):
        """Test updating user preferences."""
        user = user_service.create_user(**sample_user_data)
        
        new_prefs = {
            "timezone": "Europe/London",
            "language": "es",
            "notifications_enabled": False,
        }
        
        user_service.update_user_preferences(
            telegram_id=user.telegram_id,
            preferences=new_prefs,
        )
        
        prefs = user_service.get_user_preferences(user.telegram_id)
        assert prefs["timezone"] == "Europe/London"
        assert prefs["language"] == "es"
        assert prefs["notifications_enabled"] is False


class TestUserServiceEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_create_user_empty_username(self, user_service):
        """Test creating user with empty username."""
        with pytest.raises(ValueError):
            user_service.create_user(
                telegram_id="123",
                username="",
                tenant_id="test-tenant-001",  # ✅ ADDED
            )

    def test_create_user_empty_telegram_id(self, user_service):
        """Test creating user with empty telegram ID."""
        with pytest.raises(ValueError):
            user_service.create_user(
                telegram_id="",
                username="test",
                tenant_id="test-tenant-001",  # ✅ ADDED
            )

    def test_create_user_invalid_timezone(self, user_service):
        """Test creating user with invalid timezone."""
        with pytest.raises(ValueError, match="timezone"):
            user_service.create_user(
                telegram_id="123",
                username="test",
                timezone="Invalid/Timezone",
                tenant_id="test-tenant-001",  # ✅ ADDED
            )

    def test_user_data_integrity(self, user_service, sample_user_data):
        """Test that user data is not modified unexpectedly."""
        user = user_service.create_user(**sample_user_data)
        
        # Retrieve and verify data integrity
        retrieved = user_service.get_user(user.telegram_id)
        
        assert retrieved.telegram_id == user.telegram_id
        assert retrieved.username == user.username
        assert retrieved.first_name == user.first_name
        assert retrieved.last_name == user.last_name
        assert retrieved.timezone == user.timezone

    def test_concurrent_user_creation(self, user_service):
        """Test concurrent user creation doesn't cause issues."""
        import concurrent.futures
        
        def create_user(user_id):
            return user_service.create_user(
                telegram_id=str(user_id),
                username=f"user_{user_id}",
                tenant_id="test-tenant-001",  # ✅ ADDED
            )
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(create_user, range(1000, 1010)))
        
        assert len(results) == 10
        assert all(r is not None for r in results)
