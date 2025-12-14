"""Unit tests for AvailabilityEngine.

Tests cover slot generation, natural language parsing, and flexible 24/7 scheduling.
"""

import pytest
from datetime import datetime, timedelta, time, date
from dateutil.parser import parse as parse_date

from src.theaia.services.availability_engine import AvailabilityEngine
from src.theaia.services.booking_service import BookingService


@pytest.fixture
def availability_engine():
    """Create an AvailabilityEngine instance."""
    return AvailabilityEngine()


@pytest.fixture
def booking_service():
    """Create a BookingService instance."""
    return BookingService()


@pytest.fixture
def sample_user():
    """Create a sample user dict."""
    return {
        'id': 1,
        'telegram_id': 123456789,
        'username': 'test_user',
        'timezone': 'America/New_York',
        'tenant_id': 'test-tenant-001'
    }


class TestAvailabilityEngineSlotGeneration:
    """Tests for available slot generation."""

    def test_get_available_slots_24_7(self, availability_engine, booking_service, sample_user):
        """Test that slots are available 24/7 (no restrictions)."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=60,  # 1 hour slots
        )
        
        # Should have 24 one-hour slots
        assert len(slots) == 24
        
        # Verify slots cover entire day
        assert slots[0].time() == time(0, 0)  # 00:00
        assert slots[-1].time() == time(23, 0)  # 23:00

    def test_get_available_slots_with_existing_appointment(self, availability_engine, booking_service, sample_user):
        """Test that occupied slots are excluded."""
        target_date = datetime.utcnow() + timedelta(days=1)
        target_datetime = target_date.replace(hour=14, minute=0, second=0, microsecond=0)
        
        # Create appointment at 14:00-15:00
        booking_service.create_appointment(
            user_id=sample_user['telegram_id'],
            title="Busy Slot",
            start_time=target_datetime,
            duration_minutes=60,
        )
        
        slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=60,
        )
        
        # Should have 23 slots (24 - 1 occupied)
        assert len(slots) == 23
        
        # Verify 14:00 is not in slots
        slot_times = [s.time() for s in slots]
        assert time(14, 0) not in slot_times

    def test_get_available_slots_with_conflicts(self, availability_engine, booking_service, sample_user):
        """Test handling multiple overlapping slots."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        # Create 3 appointments
        for i in range(3):
            start = target_date.replace(hour=10 + i*2, minute=0, second=0, microsecond=0)
            booking_service.create_appointment(
                user_id=sample_user['telegram_id'],
                title=f"Appointment {i+1}",
                start_time=start,
                duration_minutes=60,
            )
        
        slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=60,
        )
        
        # Should have 21 slots (24 - 3 occupied)
        assert len(slots) == 21

    def test_get_available_slots_custom_duration(self, availability_engine, booking_service, sample_user):
        """Test slot generation with custom duration."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        # 30-minute slots
        slots_30 = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=30,
        )
        
        # Should have 48 slots (24 hours * 60 / 30)
        assert len(slots_30) == 48
        
        # 2-hour slots
        slots_120 = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=120,
        )
        
        # Should have 12 slots (24 hours * 60 / 120)
        assert len(slots_120) == 12

    def test_get_available_slots_saturday(self, availability_engine, sample_user):
        """Test that Saturday has available slots (no weekday restriction)."""
        # Get next Saturday
        today = datetime.utcnow().date()
        days_until_saturday = (5 - today.weekday()) % 7  # 5 = Saturday
        if days_until_saturday == 0:
            days_until_saturday = 7
        saturday = datetime.combine(today + timedelta(days=days_until_saturday), time(0, 0))
        
        slots = availability_engine.get_available_slots(
            date=saturday,
            duration_minutes=60,
        )
        
        # Should have 24 slots even on Saturday
        assert len(slots) == 24

    def test_get_available_slots_sunday(self, availability_engine, sample_user):
        """Test that Sunday has available slots (no weekend restriction)."""
        # Get next Sunday
        today = datetime.utcnow().date()
        days_until_sunday = (6 - today.weekday()) % 7  # 6 = Sunday
        if days_until_sunday == 0:
            days_until_sunday = 7
        sunday = datetime.combine(today + timedelta(days=days_until_sunday), time(0, 0))
        
        slots = availability_engine.get_available_slots(
            date=sunday,
            duration_minutes=60,
        )
        
        # Should have 24 slots even on Sunday
        assert len(slots) == 24

    def test_get_available_slots_early_morning(self, availability_engine, sample_user):
        """Test that early morning slots (3-4am) are available."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=60,
        )
        
        # Find 3am slot
        early_morning_slot = None
        for slot in slots:
            if slot.time() == time(3, 0):
                early_morning_slot = slot
                break
        
        assert early_morning_slot is not None


class TestAvailabilityEngineNaturalLanguageParsing:
    """Tests for natural language date/time parsing."""

    def test_parse_natural_date_today(self, availability_engine):
        """Test parsing 'today'."""
        parsed = availability_engine.parse_natural_date("hoy")
        expected = datetime.utcnow().date()
        
        assert parsed == expected

    def test_parse_natural_date_tomorrow(self, availability_engine):
        """Test parsing 'tomorrow'."""
        parsed = availability_engine.parse_natural_date("mañana")
        expected = (datetime.utcnow() + timedelta(days=1)).date()
        
        assert parsed == expected

    def test_parse_natural_date_monday(self, availability_engine):
        """Test parsing specific day of week."""
        parsed = availability_engine.parse_natural_date("lunes")
        
        # Should be a future Monday
        assert parsed.weekday() == 0  # Monday
        assert parsed >= datetime.utcnow().date()

    def test_parse_natural_date_saturday(self, availability_engine):
        """Test parsing Saturday (ensures no weekday restriction)."""
        parsed = availability_engine.parse_natural_date("sábado")
        
        assert parsed.weekday() == 5  # Saturday
        assert parsed >= datetime.utcnow().date()

    def test_parse_natural_time_morning(self, availability_engine):
        """Test parsing morning times."""
        parsed = availability_engine.parse_natural_time("9")
        assert parsed.hour == 13  # Spanish: 9 = 1 PM by default

    def test_parse_natural_time_afternoon(self, availability_engine):
        """Test parsing afternoon times."""
        parsed = availability_engine.parse_natural_time("3")
        assert parsed.hour == 15  # 3 PM

    def test_parse_natural_time_evening(self, availability_engine):
        """Test parsing evening times."""
        parsed = availability_engine.parse_natural_time("8")
        assert parsed.hour == 20  # 8 PM

    def test_parse_natural_time_early_morning(self, availability_engine):
        """Test parsing early morning (ensures 24/7 flexibility)."""
        parsed = availability_engine.parse_natural_time("3 de la mañana")
        assert parsed.hour == 3

    def test_parse_natural_time_specific_minutes(self, availability_engine):
        """Test parsing time with specific minutes."""
        parsed = availability_engine.parse_natural_time("10:45")
        assert parsed.hour == 10
        assert parsed.minute == 45


class TestAvailabilityEngineNextSlot:
    """Tests for finding next available slot."""

    def test_get_next_available_slot(self, availability_engine, sample_user):
        """Test getting the very next available slot."""
        next_slot = availability_engine.get_next_available_slot(
            duration_minutes=60,
        )
        
        assert next_slot is not None
        assert next_slot > datetime.utcnow()

    def test_get_next_available_slot_with_appointments(self, availability_engine, booking_service, sample_user):
        """Test next available considering existing appointments."""
        # Create appointment at tomorrow 10:00-11:00
        tomorrow = datetime.utcnow() + timedelta(days=1)
        slot_start = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        
        booking_service.create_appointment(
            user_id=sample_user['telegram_id'],
            title="First Appointment",
            start_time=slot_start,
            duration_minutes=60,
        )
        
        next_slot = availability_engine.get_next_available_slot(
            duration_minutes=60,
        )
        
        # Should not be 10:00-11:00
        assert next_slot is not None
        assert not (next_slot.hour == 10 and next_slot.date() == tomorrow.date())


class TestAvailabilityEngineWeeklyView:
    """Tests for weekly availability."""

    def test_get_available_slots_for_week(self, availability_engine, sample_user):
        """Test retrieving available slots for entire week."""
        start_date = datetime.utcnow() + timedelta(days=1)
        
        weekly_slots = availability_engine.get_available_slots_for_week(
            start_date=start_date,
            duration_minutes=120,  # 2-hour slots
        )
        
        # Should have 7 days * 12 slots per day = 84 slots
        total_slots = sum(len(slots) for slots in weekly_slots.values())
        assert total_slots == 7 * 12

    def test_week_includes_weekend(self, availability_engine, sample_user):
        """Test that weekly view includes weekend slots."""
        # Start from a Monday
        monday = datetime.utcnow().date()
        # Adjust to next Monday if needed
        days_until_monday = (7 - monday.weekday()) % 7
        if days_until_monday == 0 and monday <= datetime.utcnow().date():
            days_until_monday = 7
        start_date = datetime.combine(monday + timedelta(days=days_until_monday), time(0, 0))
        
        weekly_slots = availability_engine.get_available_slots_for_week(
            start_date=start_date,
            duration_minutes=60,
        )
        
        # Extract unique dates
        dates = set()
        for date_key, slots in weekly_slots.items():
            dates.update(slot.date() for slot in slots)
        
        # Should include Saturday (weekday 5) and Sunday (weekday 6)
        weekday_numbers = [d.weekday() for d in dates]
        assert 5 in weekday_numbers  # Saturday
        assert 6 in weekday_numbers  # Sunday


class TestAvailabilityEngineFlexibility:
    """Tests for 24/7 flexible scheduling philosophy."""

    def test_flexible_calendar_no_business_hours(self, availability_engine, sample_user):
        """Verify no business hour restrictions exist."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        # Should be able to schedule at 2am
        slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=60,
        )
        
        # Verify 2am slot exists
        early_slot = None
        for slot in slots:
            if slot.time() == time(2, 0):
                early_slot = slot
                break
        
        assert early_slot is not None

    def test_flexible_calendar_midnight_slot(self, availability_engine, sample_user):
        """Test midnight availability."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=60,
        )
        
        # Should include midnight (00:00)
        has_midnight = any(s.time() == time(0, 0) for s in slots)
        assert has_midnight

    def test_user_decides_everything(self, availability_engine, booking_service, sample_user):
        """Test that user has complete control over scheduling."""
        # Try to schedule at unusual time
        target_date = datetime.utcnow() + timedelta(days=1)
        unusual_time = target_date.replace(hour=3, minute=45, second=0, microsecond=0)  # 3:45 AM
        
        # Should succeed (no restrictions)
        appointment = booking_service.create_appointment(
            user_id=sample_user['telegram_id'],
            title="Late Night Session",
            start_time=unusual_time,
            duration_minutes=60,
        )
        
        assert appointment is not None
        assert appointment['start_time'].time() == time(3, 45)


class TestAvailabilityEngineEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_slot_duration_edge_values(self, availability_engine, sample_user):
        """Test with extreme slot durations."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        # Very short slots (15 minutes)
        short_slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=15,
        )
        assert len(short_slots) == 96  # 24 * 60 / 15
        
        # Full day slot
        full_day = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=1440,  # 24 hours
        )
        assert len(full_day) == 1

    def test_consecutive_slot_continuity(self, availability_engine, sample_user):
        """Test that slots are continuous and adjacent."""
        target_date = datetime.utcnow() + timedelta(days=1)
        
        slots = availability_engine.get_available_slots(
            date=target_date,
            duration_minutes=60,
        )
        
        # Verify slots are in order
        for i in range(len(slots) - 1):
            assert slots[i] < slots[i+1]
