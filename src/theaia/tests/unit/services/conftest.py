"""Shared pytest fixtures for service unit tests."""

import pytest
import pytest_asyncio
from src.theaia.services.user_service import UserService
from src.theaia.services.booking_service import BookingService
from src.theaia.services.availability_engine import AvailabilityEngine
from src.theaia.database.session import SessionLocal


@pytest_asyncio.fixture
async def user_service():
    """Create a UserService instance."""
    return UserService()


@pytest_asyncio.fixture
async def booking_service():
    """Create a BookingService instance."""
    return BookingService()


@pytest.fixture
def availability_engine():
    """Create an AvailabilityEngine instance."""
    return AvailabilityEngine()


@pytest_asyncio.fixture
async def sample_user(user_service):
    """Create a sample user with required tenant_id."""
    return await user_service.create_user(
        telegram_id=123456789,
        username="test_user",
        timezone="America/New_York",
        tenant_id="test-tenant-001",  # ✅ TENANT_ID PROVIDED
    )


@pytest_asyncio.fixture
async def db_session():
    """Provide a database session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
