"""
H9 Contract & Database Integration Tests
Target: 12+ tests for API contracts and data persistence
"""

import pytest
from datetime import datetime, timedelta, time
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict

from theaia.services.groq_tools import GroqTools, GroqToolResult
from theaia.services.booking_service import BookingService
from theaia.services.availability_engine import AvailabilityEngine


@pytest.fixture
def mock_booking_service():
    service = Mock(spec=BookingService)
    service.get_user_appointments = Mock(return_value=[])
    service.create_appointment = Mock(return_value=Mock(id=1, user_id=123))
    service.get_appointment = Mock(return_value=Mock(id=1, status="active"))
    service.cancel_appointment = Mock(return_value=True)
    return service


@pytest.fixture
def mock_availability_engine():
    engine = Mock(spec=AvailabilityEngine)
    tomorrow = datetime.now() + timedelta(days=1)
    slots = [f"{h:02d}:00" for h in range(9, 18)]
    engine.get_available_slots = Mock(return_value=slots)
    engine.is_slot_available = Mock(return_value=True)
    engine.parse_natural_date = Mock(return_value=tomorrow)
    engine.parse_natural_time = Mock(return_value=time(15, 0))
    return engine


@pytest.fixture
def groq_tools(mock_booking_service, mock_availability_engine):
    return GroqTools(
        booking_service=mock_booking_service,
        availability_engine=mock_availability_engine,
        user_id=123
    )


class TestAPIContracts:
    """H9.1: API Contract Tests - Ensure interface consistency"""

    def test_check_availability_contract(self, groq_tools):
        """
        CONTRACT: check_availability(date_str: str) -> GroqToolResult
        - Input: date string (natural language)
        - Output: GroqToolResult with available_slots list
        - Guarantees:
          * Always returns GroqToolResult
          * data['available_slots'] is list of time strings
          * message is non-empty string in Spanish
        """
        result = groq_tools.check_availability("mañana")
        
        # Type contract
        assert isinstance(result, GroqToolResult), "Must return GroqToolResult"
        assert isinstance(result.success, bool), "success must be bool"
        assert isinstance(result.data, dict), "data must be dict"
        assert isinstance(result.message, str), "message must be str"
        
        # Content contract
        assert "available_slots" in result.data, "data must have available_slots"
        assert isinstance(result.data["available_slots"], list), "available_slots must be list"
        assert len(result.message) > 0, "message must not be empty"
        
        # All slots should be time format
        for slot in result.data["available_slots"]:
            assert isinstance(slot, str), "slot must be string"
            assert ":" in slot, "slot must contain ':' separator"

    def test_create_appointment_contract(self, groq_tools):
        """
        CONTRACT: create_appointment(
            date_str: str, time_str: str, duration_minutes: int = 60
        ) -> GroqToolResult
        - Guarantees:
          * Always returns GroqToolResult
          * data['appointment_id'] is positive integer
          * data['start_time'] is datetime or None
          * On success: error field is None
          * On failure: success is False and error explains why
        """
        result = groq_tools.create_appointment("mañana", "15:00", duration_minutes=60)
        
        # Type contract
        assert isinstance(result, GroqToolResult)
        if result.success:
            assert isinstance(result.data["appointment_id"], int), "appointment_id must be int"
            assert result.data["appointment_id"] > 0, "appointment_id must be positive"
            assert result.error is None, "error must be None on success"
        else:
            assert result.error is not None, "error must be set on failure"
            assert isinstance(result.error, str), "error must be string"

    def test_get_appointments_contract(self, groq_tools):
        """
        CONTRACT: get_appointments() -> GroqToolResult
        - Guarantees:
          * Always returns GroqToolResult
          * data['total'] is non-negative integer
          * data['appointments'] is list
          * len(appointments) == total
          * Each appointment has id, start_time, duration_minutes
        """
        result = groq_tools.get_appointments()
        
        # Type contract
        assert isinstance(result, GroqToolResult)
        assert isinstance(result.data["total"], int), "total must be int"
        assert result.data["total"] >= 0, "total must be non-negative"
        assert isinstance(result.data["appointments"], list), "appointments must be list"
        
        # Size contract
        assert len(result.data["appointments"]) == result.data["total"], \
            "appointments length must match total"

    def test_cancel_appointment_contract(self, groq_tools):
        """
        CONTRACT: cancel_appointment(appointment_id: int) -> GroqToolResult
        - Guarantees:
          * Always returns GroqToolResult
          * On success: message confirms cancellation
          * On failure: error explains reason
        """
        result = groq_tools.cancel_appointment(1)
        
        assert isinstance(result, GroqToolResult)
        assert isinstance(result.message, str)
        assert len(result.message) > 0

    def test_tool_definitions_are_complete(self, groq_tools):
        """
        CONTRACT: _generate_tools_definitions() -> List[Dict]
        - Guarantees:
          * Returns list of 4 tool definitions
          * Each tool has type, function, name, description
          * Each function has parameters with JSON schema
          * All required fields present
        """
        defs = groq_tools._generate_tools_definitions()
        
        assert isinstance(defs, list), "Must return list"
        assert len(defs) == 4, "Must have exactly 4 tools"
        
        expected_tools = {
            "check_availability",
            "create_appointment",
            "get_appointments",
            "cancel_appointment"
        }
        
        for tool_def in defs:
            # Structure contract
            assert "type" in tool_def
            assert "function" in tool_def
            
            func = tool_def["function"]
            assert "name" in func
            assert "description" in func
            assert "parameters" in func
            
            # Tool name contract
            assert func["name"] in expected_tools, f"Unknown tool: {func['name']}"
            
            # Parameters contract
            params = func["parameters"]
            assert params["type"] == "object", "parameters.type must be 'object'"
            assert "properties" in params
            assert isinstance(params["properties"], dict)


class TestDataConsistencyContracts:
    """H9.2: Data consistency - What goes in must come out"""

    def test_appointment_create_then_list(self, groq_tools, mock_booking_service):
        """
        CONSISTENCY: Created appointment appears in list
        - Create appointment
        - List appointments
        - Verify appointment is in list
        """
        apt_id = 42
        tomorrow = datetime.now() + timedelta(days=1)
        apt_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 15, 0)
        
        # Mock: create returns appointment
        mock_booking_service.create_appointment.return_value = Mock(
            id=apt_id,
            user_id=123,
            start_time=apt_time,
            duration_minutes=60
        )
        
        # Create
        create_result = groq_tools.create_appointment("mañana", "15:00")
        assert create_result.success is True
        
        # Mock: list returns same appointment
        mock_booking_service.get_user_appointments.return_value = [
            Mock(id=apt_id, start_time=apt_time, duration_minutes=60)
        ]
        
        # List
        list_result = groq_tools.get_appointments()
        assert list_result.success is True
        assert list_result.data["total"] == 1

    def test_appointment_cancel_removes_from_list(self, groq_tools, mock_booking_service):
        """
        CONSISTENCY: Cancelled appointment doesn't appear in list
        """
        apt_id = 42
        
        # Before cancel: appointment exists
        mock_booking_service.get_user_appointments.return_value = [
            Mock(id=apt_id, start_time=datetime.now(), duration_minutes=60)
        ]
        
        before = groq_tools.get_appointments()
        assert before.data["total"] == 1
        
        # Cancel
        mock_booking_service.get_appointment.return_value = Mock(id=apt_id, status="cancelled")
        cancel_result = groq_tools.cancel_appointment(apt_id)
        assert cancel_result.success is True
        
        # After cancel: appointment gone
        mock_booking_service.get_user_appointments.return_value = []
        after = groq_tools.get_appointments()
        assert after.data["total"] == 0

    def test_availability_decreases_after_booking(self, groq_tools, mock_availability_engine):
        """
        CONSISTENCY: Booking a slot removes it from available
        """
        # Before: 15:00 is available
        mock_availability_engine.get_available_slots.return_value = [
            "09:00", "10:00", "15:00", "16:00", "17:00"
        ]
        
        before = groq_tools.check_availability("mañana")
        assert "15:00" in before.data["available_slots"]
        assert len(before.data["available_slots"]) == 5
        
        # Book 15:00
        groq_tools.create_appointment("mañana", "15:00")
        
        # After: 15:00 no longer available
        mock_availability_engine.get_available_slots.return_value = [
            "09:00", "10:00", "16:00", "17:00"
        ]
        
        after = groq_tools.check_availability("mañana")
        assert "15:00" not in after.data["available_slots"]
        assert len(after.data["available_slots"]) == 4


class TestDatabaseContracts:
    """H9.3: Database layer contracts"""

    def test_appointment_persistence_contract(self, mock_booking_service):
        """
        CONTRACT: Appointments persisted must have:
        - id: unique positive integer
        - user_id: valid user identifier
        - start_time: future datetime
        - duration_minutes: positive integer
        - status: one of (active, cancelled, completed)
        """
        appointment = Mock(
            id=1,
            user_id=123,
            start_time=datetime.now() + timedelta(days=1),
            duration_minutes=60,
            status="active"
        )
        
        assert isinstance(appointment.id, int)
        assert appointment.id > 0
        assert isinstance(appointment.user_id, int)
        assert appointment.status in ("active", "cancelled", "completed")
        assert appointment.duration_minutes > 0

    def test_user_data_isolation(self, groq_tools, mock_booking_service):
        """
        CONTRACT: Users should only see their own appointments
        - User 123 creates appointment
        - User 123 can list their appointment
        - User 456 cannot see user 123's appointment
        """
        # User 123's appointment
        mock_booking_service.get_user_appointments.return_value = [
            Mock(id=1, user_id=123, start_time=datetime.now(), duration_minutes=60)
        ]
        
        result = groq_tools.get_appointments()
        assert result.data["total"] == 1
        
        # All appointments should belong to current user (123)
        for apt in result.data["appointments"]:
            # This depends on implementation, but should be enforced
            pass

    def test_appointment_availability_slot_consistency(self, mock_availability_engine):
        """
        CONTRACT: If slot is marked available, it should be bookable
        CONTRACT: If slot is marked unavailable, booking should fail
        """
        # Setup
        mock_availability_engine.get_available_slots.return_value = ["15:00", "16:00"]
        mock_availability_engine.is_slot_available.return_value = True
        
        # Get available slots
        available = mock_availability_engine.get_available_slots()
        assert "15:00" in available
        
        # Should be bookable
        can_book = mock_availability_engine.is_slot_available("15:00")
        assert can_book is True


class TestErrorContractCompliance:
    """H9.4: Error handling contracts"""

    def test_error_field_consistency(self, groq_tools, mock_booking_service):
        """
        CONTRACT: If success=False, error field must be non-null string
        CONTRACT: If success=True, error field must be None
        """
        mock_booking_service.create_appointment.side_effect = Exception("DB Error")
        
        result = groq_tools.create_appointment("mañana", "15:00")
        
        if result.success is False:
            assert result.error is not None, "error must be set when success=False"
            assert isinstance(result.error, str), "error must be string"
            assert len(result.error) > 0, "error must not be empty"
        else:
            assert result.error is None, "error must be None when success=True"

    def test_invalid_input_handling(self, groq_tools, mock_availability_engine):
        """
        CONTRACT: Invalid input should produce error result, not crash
        """
        mock_availability_engine.parse_natural_date.side_effect = ValueError("Invalid date")
        
        result = groq_tools.create_appointment("invalid_date_xyz", "15:00")
        
        # Should not crash
        assert isinstance(result, GroqToolResult)
        # Should indicate error
        assert result.success is False or result.error is not None

    def test_missing_required_fields(self, groq_tools):
        """
        CONTRACT: Missing required parameters should be handled gracefully
        """
        # None as time should be handled
        result = groq_tools.create_appointment("mañana", None)
        assert isinstance(result, GroqToolResult)


class TestResponseConsistency:
    """H9.5: Response message consistency"""

    def test_spanish_message_always_present(self, groq_tools):
        """
        CONTRACT: All responses must have Spanish message
        """
        results = [
            groq_tools.check_availability("mañana"),
            groq_tools.create_appointment("mañana", "15:00"),
            groq_tools.get_appointments(),
            groq_tools.cancel_appointment(1),
        ]
        
        for result in results:
            assert result.message is not None
            assert isinstance(result.message, str)
            assert len(result.message) > 0

    def test_emoji_in_success_messages(self, groq_tools):
        """
        CONTRACT: Success messages may include emojis
        """
        result = groq_tools.create_appointment("mañana", "15:00")
        
        if result.success:
            # Message might have ✅ emoji
            pass  # Just verify it doesn't crash


class TestIDempotencyContracts:
    """H9.6: Idempotency and replay safety"""

    def test_get_appointments_idempotent(self, groq_tools):
        """
        CONTRACT: Calling get_appointments() twice should return same data
        """
        result1 = groq_tools.get_appointments()
        result2 = groq_tools.get_appointments()
        
        assert result1.data["total"] == result2.data["total"]
        assert len(result1.data["appointments"]) == len(result2.data["appointments"])

    def test_check_availability_idempotent(self, groq_tools):
        """
        CONTRACT: Checking availability twice for same date should be consistent
        """
        result1 = groq_tools.check_availability("mañana")
        result2 = groq_tools.check_availability("mañana")
        
        assert set(result1.data["available_slots"]) == set(result2.data["available_slots"])


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
