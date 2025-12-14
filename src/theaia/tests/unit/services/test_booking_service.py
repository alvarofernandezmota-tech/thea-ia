"""Unit tests for BookingService.

Tests cover appointment creation, cancellation, conflict detection, and statistics.
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.theaia.services.booking_service import BookingService
from src.theaia.services.user_service import UserService
from src.theaia.database.models import Appointment


@pytest.fixture
def user_service():
    """Create a UserService instance."""
    return UserService()


@pytest.fixture
def booking_service():
    """Create a BookingService instance."""
    return BookingService()


@pytest.fixture
def sample_user(user_service):
    """Create a sample user for testing."""
    return user_service.create_user(
        telegram_id="123456789",
        username="test_user",
        first_name="Test",
        timezone="America/New_York",
        tenant_id="test-tenant-001",  # ✅ ADDED
    )


@pytest.fixture
def sample_appointment_data():
    """Return sample appointment data."""
    start_time = datetime.utcnow() + timedelta(days=1, hours=10)
    end_time = start_time + timedelta(hours=1)
    
    return {
        "title": "Doctor's Appointment",
        "description": "General checkup",
        "start_time": start_time,
        "end_time": end_time,
    }


class TestBookingServiceCreate:
    """Tests for appointment creation."""

    def test_create_appointment_success(self, booking_service, sample_user, sample_appointment_data):
        """Test successful appointment creation."""
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        assert appointment is not None
        assert appointment.user_id == sample_user.telegram_id
        assert appointment.title == sample_appointment_data["title"]
        assert appointment.status == "scheduled"
        assert appointment.created_at is not None

    def test_create_appointment_minimal_data(self, booking_service, sample_user):
        """Test appointment creation with minimal data."""
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            title="Quick Meeting",
            start_time=start_time,
            end_time=end_time,
        )
        
        assert appointment is not None
        assert appointment.title == "Quick Meeting"
        assert appointment.description is None or appointment.description == ""

    def test_create_appointment_with_conflict(self, booking_service, sample_user, sample_appointment_data):
        """Test that creating conflicting appointment fails."""
        # Create first appointment
        booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        # Try to create overlapping appointment
        conflicting_data = {
            "title": "Conflicting Event",
            "start_time": sample_appointment_data["start_time"] + timedelta(minutes=30),
            "end_time": sample_appointment_data["end_time"] + timedelta(minutes=30),
        }
        
        with pytest.raises(ValueError, match="conflict"):
            booking_service.create_appointment(
                user_id=sample_user.telegram_id,
                **conflicting_data,
            )

    def test_create_appointment_invalid_time_range(self, booking_service, sample_user):
        """Test that invalid time range raises error."""
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time - timedelta(hours=1)  # End before start
        
        with pytest.raises(ValueError, match="end_time.*start_time"):
            booking_service.create_appointment(
                user_id=sample_user.telegram_id,
                title="Invalid Event",
                start_time=start_time,
                end_time=end_time,
            )

    def test_create_appointment_in_past(self, booking_service, sample_user):
        """Test that creating appointments in the past fails."""
        start_time = datetime.utcnow() - timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        with pytest.raises(ValueError, match="past"):
            booking_service.create_appointment(
                user_id=sample_user.telegram_id,
                title="Past Event",
                start_time=start_time,
                end_time=end_time,
            )

    def test_create_appointment_nonexistent_user(self, booking_service):
        """Test creating appointment for non-existent user."""
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        with pytest.raises(ValueError, match="user.*not found"):
            booking_service.create_appointment(
                user_id="nonexistent",
                title="Test",
                start_time=start_time,
                end_time=end_time,
            )


class TestBookingServiceRetrieve:
    """Tests for appointment retrieval."""

    def test_get_upcoming_appointments(self, booking_service, sample_user, sample_appointment_data):
        """Test retrieving upcoming appointments."""
        # Create appointments
        booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        upcoming = booking_service.get_upcoming_appointments(sample_user.telegram_id)
        
        assert len(upcoming) >= 1
        assert all(app.status == "scheduled" for app in upcoming)
        assert all(app.start_time > datetime.utcnow() for app in upcoming)

    def test_get_past_appointments(self, booking_service, sample_user):
        """Test retrieving past appointments."""
        # Create past appointment (manually)
        start_time = datetime.utcnow() - timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        appointment = booking_service._create_appointment_raw(
            user_id=sample_user.telegram_id,
            title="Past Meeting",
            start_time=start_time,
            end_time=end_time,
            status="completed",
        )
        
        past = booking_service.get_past_appointments(sample_user.telegram_id)
        
        assert len(past) >= 1
        assert any(app.id == appointment.id for app in past)

    def test_get_appointments_by_date_range(self, booking_service, sample_user):
        """Test retrieving appointments in a date range."""
        start_date = datetime.utcnow().date()
        end_date = start_date + timedelta(days=7)
        
        # Create appointments within range
        for i in range(3):
            start_time = datetime.utcnow() + timedelta(days=i+1, hours=10)
            end_time = start_time + timedelta(hours=1)
            
            booking_service.create_appointment(
                user_id=sample_user.telegram_id,
                title=f"Appointment {i+1}",
                start_time=start_time,
                end_time=end_time,
            )
        
        # Create appointment outside range
        outside_time = datetime.utcnow() + timedelta(days=10)
        outside_end = outside_time + timedelta(hours=1)
        booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            title="Outside Range",
            start_time=outside_time,
            end_time=outside_end,
        )
        
        appointments = booking_service.get_appointments_by_date_range(
            user_id=sample_user.telegram_id,
            start_date=start_date,
            end_date=end_date,
        )
        
        assert len(appointments) == 3
        assert all(
            start_date <= app.start_time.date() <= end_date 
            for app in appointments
        )

    def test_get_appointment_by_id(self, booking_service, sample_user, sample_appointment_data):
        """Test retrieving specific appointment."""
        created = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        retrieved = booking_service.get_appointment(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_appointment_not_found(self, booking_service):
        """Test retrieving non-existent appointment."""
        appointment = booking_service.get_appointment("nonexistent")
        assert appointment is None


class TestBookingServiceCancel:
    """Tests for appointment cancellation."""

    def test_cancel_appointment_success(self, booking_service, sample_user, sample_appointment_data):
        """Test successful appointment cancellation."""
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        result = booking_service.cancel_appointment(
            appointment_id=appointment.id,
            reason="User cancelled",
        )
        
        assert result is True
        
        updated = booking_service.get_appointment(appointment.id)
        assert updated.status == "cancelled"
        assert updated.cancellation_reason == "User cancelled"

    def test_cancel_appointment_not_found(self, booking_service):
        """Test cancelling non-existent appointment."""
        with pytest.raises(ValueError, match="not found"):
            booking_service.cancel_appointment(
                appointment_id="nonexistent",
                reason="Test",
            )

    def test_cancel_already_cancelled(self, booking_service, sample_user, sample_appointment_data):
        """Test cancelling already cancelled appointment."""
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        booking_service.cancel_appointment(appointment.id, "First cancel")
        
        with pytest.raises(ValueError, match="already"):
            booking_service.cancel_appointment(appointment.id, "Second cancel")

    def test_cancel_completed_appointment(self, booking_service, sample_user):
        """Test cancelling completed appointment."""
        start_time = datetime.utcnow() - timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        appointment = booking_service._create_appointment_raw(
            user_id=sample_user.telegram_id,
            title="Completed Event",
            start_time=start_time,
            end_time=end_time,
            status="completed",
        )
        
        with pytest.raises(ValueError, match="completed"):
            booking_service.cancel_appointment(appointment.id, "Cancel")


class TestBookingServiceConflict:
    """Tests for conflict detection."""

    def test_check_conflict_exact_overlap(self, booking_service, sample_user, sample_appointment_data):
        """Test detecting exact time overlap."""
        booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        has_conflict = booking_service.check_conflict(
            user_id=sample_user.telegram_id,
            start_time=sample_appointment_data["start_time"],
            end_time=sample_appointment_data["end_time"],
        )
        
        assert has_conflict is True

    def test_check_conflict_partial_overlap(self, booking_service, sample_user, sample_appointment_data):
        """Test detecting partial overlap."""
        booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        # Starts before, ends during
        has_conflict = booking_service.check_conflict(
            user_id=sample_user.telegram_id,
            start_time=sample_appointment_data["start_time"] - timedelta(minutes=30),
            end_time=sample_appointment_data["start_time"] + timedelta(minutes=30),
        )
        
        assert has_conflict is True

    def test_check_conflict_no_overlap(self, booking_service, sample_user, sample_appointment_data):
        """Test no conflict when times don't overlap."""
        booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        # Completely after existing appointment
        has_conflict = booking_service.check_conflict(
            user_id=sample_user.telegram_id,
            start_time=sample_appointment_data["end_time"] + timedelta(hours=1),
            end_time=sample_appointment_data["end_time"] + timedelta(hours=2),
        )
        
        assert has_conflict is False

    def test_check_conflict_touching_times(self, booking_service, sample_user, sample_appointment_data):
        """Test no conflict when times touch but don't overlap."""
        booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        # Starts exactly when existing ends
        has_conflict = booking_service.check_conflict(
            user_id=sample_user.telegram_id,
            start_time=sample_appointment_data["end_time"],
            end_time=sample_appointment_data["end_time"] + timedelta(hours=1),
        )
        
        assert has_conflict is False

    def test_check_conflict_empty_schedule(self, booking_service, sample_user):
        """Test no conflict on empty schedule."""
        has_conflict = booking_service.check_conflict(
            user_id=sample_user.telegram_id,
            start_time=datetime.utcnow() + timedelta(days=1),
            end_time=datetime.utcnow() + timedelta(days=1, hours=1),
        )
        
        assert has_conflict is False


class TestBookingServiceStatistics:
    """Tests for appointment statistics."""

    def test_get_appointment_stats(self, booking_service, sample_user):
        """Test retrieving appointment statistics."""
        # Create several appointments
        for i in range(3):
            start_time = datetime.utcnow() + timedelta(days=i+1)
            end_time = start_time + timedelta(hours=1)
            booking_service.create_appointment(
                user_id=sample_user.telegram_id,
                title=f"Appointment {i+1}",
                start_time=start_time,
                end_time=end_time,
            )
        
        stats = booking_service.get_appointment_stats(sample_user.telegram_id)
        
        assert stats is not None
        assert stats["total_appointments"] == 3
        assert stats["scheduled"] == 3
        assert stats["cancelled"] == 0
        assert stats["completed"] == 0

    def test_get_stats_empty(self, booking_service, sample_user):
        """Test stats for user with no appointments."""
        stats = booking_service.get_appointment_stats(sample_user.telegram_id)
        
        assert stats["total_appointments"] == 0
        assert stats["scheduled"] == 0

    def test_get_stats_after_cancellation(self, booking_service, sample_user, sample_appointment_data):
        """Test stats reflect cancellations."""
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        booking_service.cancel_appointment(appointment.id, "Test")
        
        stats = booking_service.get_appointment_stats(sample_user.telegram_id)
        
        assert stats["total_appointments"] == 1
        assert stats["scheduled"] == 0
        assert stats["cancelled"] == 1


class TestBookingServiceStatusTransitions:
    """Tests for appointment status transitions."""

    def test_status_transition_scheduled_to_completed(self, booking_service, sample_user, sample_appointment_data):
        """Test transitioning from scheduled to completed."""
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        booking_service.mark_completed(appointment.id)
        
        updated = booking_service.get_appointment(appointment.id)
        assert updated.status == "completed"

    def test_status_transition_scheduled_to_cancelled(self, booking_service, sample_user, sample_appointment_data):
        """Test transitioning from scheduled to cancelled."""
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            **sample_appointment_data,
        )
        
        booking_service.cancel_appointment(appointment.id, "User request")
        
        updated = booking_service.get_appointment(appointment.id)
        assert updated.status == "cancelled"


class TestBookingServiceEdgeCases:
    """Tests for edge cases."""

    def test_appointment_exactly_24_hours(self, booking_service, sample_user):
        """Test creating appointment that lasts exactly 24 hours."""
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time + timedelta(days=1)
        
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            title="24-hour Event",
            start_time=start_time,
            end_time=end_time,
        )
        
        assert appointment is not None
        assert (appointment.end_time - appointment.start_time).days == 1

    def test_appointment_with_very_long_title(self, booking_service, sample_user):
        """Test appointment with very long title."""
        long_title = "A" * 500  # Very long title
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        appointment = booking_service.create_appointment(
            user_id=sample_user.telegram_id,
            title=long_title,
            start_time=start_time,
            end_time=end_time,
        )
        
        assert appointment is not None
        assert len(appointment.title) == 500

    def test_multiple_users_no_conflict(self, booking_service, user_service, sample_appointment_data):
        """Test that different users' appointments don't conflict."""
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
        
        # Both create at same time - should not conflict
        booking_service.create_appointment(
            user_id=user1.telegram_id,
            **sample_appointment_data,
        )
        
        appointment2 = booking_service.create_appointment(
            user_id=user2.telegram_id,
            **sample_appointment_data,
        )
        
        assert appointment2 is not None
