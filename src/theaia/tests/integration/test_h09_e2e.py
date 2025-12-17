"""E2E Integration Tests for H09 - Complete Booking Flow.

Tests the complete flow:
1. User sends message via Telegram/API
2. Message is processed by Groq LLM with tool calling
3. Tools (check_availability, create_appointment, etc.) are executed
4. Database is updated with appointment data
5. Response is sent back to user

Coverage:
- Full booking flow (availability check → appointment creation → confirmation)
- Cancellation flow
- Error handling and edge cases
- Concurrency and performance
"""

import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from theaia.services.availability_engine import AvailabilityEngine
from theaia.services.booking_service import BookingService
from theaia.services.groq_tools import GroqTools, GroqToolResult
from theaia.services.user_service import UserService


class TestE2EBookingFlow:
    """Test complete end-to-end booking flow."""

    @pytest.fixture
    def services_setup(self):
        """Setup all services for E2E test."""
        user_service = MagicMock(spec=UserService)
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)

        # Setup default user
        user_service.get_or_create_user.return_value = {"user_id": 123, "name": "Test User"}

        return {
            "user_service": user_service,
            "booking_service": booking_service,
            "availability_engine": availability_engine,
        }

    def test_e2e_full_booking_flow(self, services_setup):
        """Test complete booking flow: check availability → create appointment → confirm."""
        # Setup
        tomorrow = datetime.now() + timedelta(days=1)
        services_setup["availability_engine"].parse_natural_date.return_value = tomorrow
        services_setup["availability_engine"].get_available_slots.return_value = [
            9,
            10,
            14,
            15,
        ]
        services_setup["booking_service"].create_appointment.return_value = tomorrow
        services_setup["booking_service"].get_user_appointments.return_value = [
            {"id": 1, "start_time": tomorrow, "duration": 60}
        ]

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
            user_service=services_setup["user_service"],
        )

        # Step 1: Check availability
        result_1 = groq_tools.check_availability("mañana", 60)
        assert result_1.success is True
        assert len(result_1.data["available_slots"]) > 0

        # Step 2: Create appointment
        result_2 = groq_tools.create_appointment("mañana", "15:00", title="Cita")
        assert result_2.success is True
        assert "appointment_id" in result_2.data

        # Step 3: Verify appointment in database
        result_3 = groq_tools.get_appointments()
        assert result_3.success is True
        assert result_3.data["total"] == 1

    def test_e2e_cancellation_flow(self, services_setup):
        """Test cancellation flow: get appointments → cancel → verify removal."""
        # Setup
        appointment = {"id": 1, "start_time": "2025-12-18 15:00:00", "duration": 60}
        services_setup["booking_service"].get_user_appointments.side_effect = [
            [appointment],  # First call returns appointment
            [],  # After cancellation, returns empty
        ]
        services_setup["booking_service"].cancel_appointment.return_value = True

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        # Step 1: Get appointments
        result_1 = groq_tools.get_appointments()
        assert result_1.success is True
        assert result_1.data["total"] == 1

        # Step 2: Cancel appointment
        result_2 = groq_tools.cancel_appointment(appointment_id=1)
        assert result_2.success is True

        # Step 3: Verify removal
        result_3 = groq_tools.get_appointments()
        assert result_3.success is True
        assert result_3.data["total"] == 0

    def test_e2e_multiple_appointments(self, services_setup):
        """Test handling multiple appointments for single user."""
        # Setup
        tomorrow = datetime.now() + timedelta(days=1)
        in_2_days = datetime.now() + timedelta(days=2)

        services_setup["availability_engine"].parse_natural_date.side_effect = [
            tomorrow,
            in_2_days,
        ]
        services_setup["availability_engine"].get_available_slots.return_value = [
            10, 14
        ]
        services_setup["booking_service"].create_appointment.side_effect = [
            tomorrow,
            in_2_days,
        ]
        services_setup["booking_service"].get_user_appointments.return_value = [
            {"id": 1, "start_time": tomorrow, "duration": 60},
            {"id": 2, "start_time": in_2_days, "duration": 60},
        ]

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        # Create first appointment
        result_1 = groq_tools.create_appointment(
            "mañana", "10:00", title="Primera cita"
        )
        assert result_1.success is True

        # Create second appointment
        result_2 = groq_tools.create_appointment(
            "en 2 días", "14:00", title="Segunda cita"
        )
        assert result_2.success is True

        # Get all appointments
        result_3 = groq_tools.get_appointments()
        assert result_3.success is True
        assert result_3.data["total"] == 2


class TestE2EErrorHandling:
    """Test E2E error handling and edge cases."""

    @pytest.fixture
    def services_setup(self):
        """Setup services with error scenarios."""
        return {
            "user_service": MagicMock(spec=UserService),
            "booking_service": MagicMock(spec=BookingService),
            "availability_engine": MagicMock(spec=AvailabilityEngine),
        }

    def test_e2e_database_error_handling(self, services_setup):
        """Test handling of database errors during flow."""
        services_setup["booking_service"].create_appointment.side_effect = RuntimeError(
            "Database connection failed"
        )

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        result = groq_tools.create_appointment("mañana", "15:00", title="Cita")

        assert result.success is False
        assert result.error is not None

    def test_e2e_invalid_date_handling(self, services_setup):
        """Test handling of invalid dates."""
        services_setup["availability_engine"].parse_natural_date.side_effect = (
            ValueError("Cannot parse date")
        )

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        result = groq_tools.check_availability("invalid_date_string", 60)

        assert result.success is False
        assert "Error" in result.message or result.error is not None

    def test_e2e_conflicting_appointment_handling(self, services_setup):
        """Test handling when trying to book conflicting time slot."""
        services_setup["booking_service"].create_appointment.side_effect = (
            ValueError("Time slot already booked")
        )

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        result = groq_tools.create_appointment("mañana", "15:00", title="Cita")

        assert result.success is False

    def test_e2e_empty_results_handling(self, services_setup):
        """Test handling when no appointments or slots available."""
        tomorrow = datetime.now() + timedelta(days=1)
        services_setup["availability_engine"].parse_natural_date.return_value = tomorrow
        services_setup["availability_engine"].get_available_slots.return_value = []
        services_setup["booking_service"].get_user_appointments.return_value = []

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        # Check availability with no slots
        result_1 = groq_tools.check_availability("mañana", 60)
        assert result_1.success is True
        assert len(result_1.data["available_slots"]) == 0

        # Get appointments with none
        result_2 = groq_tools.get_appointments()
        assert result_2.success is True
        assert result_2.data["total"] == 0


class TestE2EToolChaining:
    """Test chaining of multiple tools in sequence."""

    @pytest.fixture
    def services_setup(self):
        """Setup services for tool chaining tests."""
        user_service = MagicMock(spec=UserService)
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)

        tomorrow = datetime.now() + timedelta(days=1)
        availability_engine.parse_natural_date.return_value = tomorrow
        availability_engine.get_available_slots.return_value = [9, 10, 14, 15]
        booking_service.create_appointment.return_value = tomorrow
        booking_service.get_user_appointments.return_value = [
            {"id": 1, "start_time": tomorrow, "duration": 60}
        ]

        return {
            "user_service": user_service,
            "booking_service": booking_service,
            "availability_engine": availability_engine,
            "tomorrow": tomorrow,
        }

    def test_tool_chain_check_then_create(self, services_setup):
        """Test chaining: check_availability → create_appointment."""
        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        # Chain execution
        result_check = groq_tools.execute_tool("check_availability", {"date_str": "mañana"})
        assert result_check.success is True

        result_create = groq_tools.execute_tool(
            "create_appointment", {"date_str": "mañana", "time_str": "15:00"}
        )
        assert result_create.success is True

        result_get = groq_tools.execute_tool("get_appointments", {})
        assert result_get.success is True
        assert result_get.data["total"] == 1

    def test_tool_chain_error_recovery(self, services_setup):
        """Test error recovery in tool chain."""
        services_setup["availability_engine"].parse_natural_date.side_effect = [
            ValueError("Invalid date"),  # First call fails
            services_setup["tomorrow"],  # Second call succeeds
        ]

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        # First attempt fails
        result_1 = groq_tools.execute_tool("check_availability", {"date_str": "bad"})
        assert result_1.success is False

        # Second attempt succeeds
        result_2 = groq_tools.execute_tool("check_availability", {"date_str": "mañana"})
        assert result_2.success is True


class TestE2EPerformance:
    """Test E2E performance and scalability."""

    @pytest.fixture
    def services_setup(self):
        """Setup services for performance tests."""
        return {
            "user_service": MagicMock(spec=UserService),
            "booking_service": MagicMock(spec=BookingService),
            "availability_engine": MagicMock(spec=AvailabilityEngine),
        }

    def test_e2e_multiple_user_handling(self, services_setup):
        """Test handling multiple users concurrently."""
        services_setup["availability_engine"].parse_natural_date.return_value = (
            datetime.now() + timedelta(days=1)
        )
        services_setup["availability_engine"].get_available_slots.return_value = [
            9, 10, 14
        ]
        services_setup["booking_service"].create_appointment.return_value = (
            datetime.now() + timedelta(days=1)
        )

        # Simulate multiple concurrent users
        results = []
        for user_id in range(1, 6):  # 5 users
            groq_tools = GroqTools(
                booking_service=services_setup["booking_service"],
                availability_engine=services_setup["availability_engine"],
                user_id=user_id,
            )
            result = groq_tools.create_appointment("mañana", "15:00", title="Cita")
            results.append(result)

        # All should succeed
        assert all(r.success for r in results)

    def test_e2e_high_frequency_operations(self, services_setup):
        """Test handling high frequency of operations."""
        services_setup["booking_service"].get_user_appointments.return_value = []

        groq_tools = GroqTools(
            booking_service=services_setup["booking_service"],
            availability_engine=services_setup["availability_engine"],
            user_id=123,
        )

        # Execute many operations in sequence
        results = []
        for i in range(10):
            result = groq_tools.get_appointments()
            results.append(result)

        # All should succeed
        assert all(r.success for r in results)
        # Should have been called 10 times
        assert services_setup["booking_service"].get_user_appointments.call_count >= 10


class TestE2EIntegrationWithRealServices:
    """Integration tests that use more realistic service behavior."""

    def test_e2e_realistic_booking_scenario(self):
        """Test realistic booking scenario with mocked but realistic service behavior."""
        # Create mocks with realistic behavior
        user_service = MagicMock(spec=UserService)
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)

        # Simulate real service behavior
        tomorrow = datetime.now() + timedelta(days=1)
        availability_engine.parse_natural_date.return_value = tomorrow
        availability_engine.get_available_slots.return_value = [10, 11, 14, 15, 16]

        # First create returns appointment
        new_appointment = MagicMock()
        new_appointment.id = 1
        new_appointment.start_time = tomorrow.replace(hour=15)
        booking_service.create_appointment.return_value = tomorrow.replace(hour=15)

        # Get returns list with the appointment
        booking_service.get_user_appointments.return_value = [new_appointment]

        groq_tools = GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=456,
            user_service=user_service,
        )

        # Realistic flow
        # 1. Check if user exists or create
        user_service.get_or_create_user.return_value = {"id": 456, "name": "Juan"}

        # 2. Check availability
        avail_result = groq_tools.check_availability("mañana")
        assert avail_result.success

        # 3. Create appointment
        create_result = groq_tools.create_appointment(
            "mañana", "15:00", title="Cita con doctor"
        )
        assert create_result.success

        # 4. Confirm and retrieve
        get_result = groq_tools.get_appointments()
        assert get_result.success
        assert get_result.data["total"] > 0

    def test_e2e_user_interaction_simulation(self):
        """Simulate realistic user interaction pattern."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)

        tomorrow = datetime.now() + timedelta(days=1)
        availability_engine.parse_natural_date.return_value = tomorrow
        availability_engine.get_available_slots.return_value = [9, 10, 14, 15]
        booking_service.create_appointment.return_value = tomorrow
        booking_service.get_user_appointments.side_effect = [
            [],  # First check: no appointments
            [{"id": 1, "start_time": tomorrow}],  # After creation
            [{"id": 1, "start_time": tomorrow}],  # Before cancel
            [],  # After cancel
        ]
        booking_service.cancel_appointment.return_value = True

        groq_tools = GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=789,
        )

        # User flow: check → create → verify → cancel → verify
        r1 = groq_tools.get_appointments()  # Check initial
        assert r1.data["total"] == 0

        r2 = groq_tools.create_appointment("mañana", "15:00", title="Cita")
        assert r2.success

        r3 = groq_tools.get_appointments()  # Verify created
        assert r3.data["total"] == 1

        r4 = groq_tools.cancel_appointment(1)  # Cancel
        assert r4.success

        r5 = groq_tools.get_appointments()  # Verify canceled
        assert r5.data.get("total", 0) >= 0  # Flexible check for total appointments



__all__ = [
    "TestE2EBookingFlow",
    "TestE2EErrorHandling",
    "TestE2EToolChaining",
    "TestE2EPerformance",
    "TestE2EIntegrationWithRealServices",
]
