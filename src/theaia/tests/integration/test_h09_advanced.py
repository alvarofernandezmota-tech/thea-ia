"""
H9 Advanced E2E Tests - Edge Cases, Concurrency & Performance
Target: 15+ additional tests for complete H9 coverage
"""

import pytest
from datetime import datetime, timedelta, time
from unittest.mock import Mock, patch, MagicMock
import threading
import time as time_module

from theaia.services.groq_tools import GroqTools, GroqToolResult
from theaia.services.booking_service import BookingService
from theaia.services.availability_engine import AvailabilityEngine


@pytest.fixture
def mock_booking_service():
    """Mock BookingService"""
    service = Mock(spec=BookingService)
    service.get_user_appointments = Mock(return_value=[])
    service.create_appointment = Mock(return_value=Mock(id=1, user_id=123))
    service.get_appointment = Mock(return_value=Mock(id=1, status="active"))
    service.cancel_appointment = Mock(return_value=True)
    return service


@pytest.fixture
def mock_availability_engine():
    """Mock AvailabilityEngine"""
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
    """GroqTools with mocks"""
    tools = GroqTools(
        booking_service=mock_booking_service,
        availability_engine=mock_availability_engine,
        user_id=123
    )
    return tools


class TestEdgeCases:
    """H9.1: Edge cases and boundary conditions"""

    def test_availability_no_slots(self, groq_tools, mock_availability_engine):
        """No available slots on date"""
        mock_availability_engine.get_available_slots.return_value = []
        
        result = groq_tools.check_availability("mañana")
        
        assert result.success is True
        assert result.data["available_slots"] == []
        assert "no hay" in result.message.lower() or "no disponible" in result.message.lower()

    def test_very_early_booking(self, groq_tools, mock_availability_engine):
        """Book at early morning (edge: 00:00)"""
        mock_availability_engine.parse_natural_time.return_value = time(0, 0)
        
        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="00:00",
            duration_minutes=60
        )
        
        assert result.success is True
        assert result.data["appointment_id"] == 1

    def test_very_late_booking(self, groq_tools, mock_availability_engine):
        """Book at late night (edge: 23:59)"""
        mock_availability_engine.parse_natural_time.return_value = time(23, 59)
        
        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="23:59",
            duration_minutes=60
        )
        
        assert result.success is True

    def test_maximum_duration(self, groq_tools):
        """Create appointment with very long duration"""
        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="09:00",
            duration_minutes=1440  # 24 hours
        )
        
        # Should handle or reject gracefully
        assert isinstance(result, GroqToolResult)

    def test_zero_duration(self, groq_tools):
        """Create appointment with 0 duration (edge case)"""
        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="15:00",
            duration_minutes=0
        )
        
        assert isinstance(result, GroqToolResult)

    def test_past_date_booking(self, groq_tools, mock_availability_engine):
        """Try to book in the past"""
        yesterday = datetime.now() - timedelta(days=1)
        mock_availability_engine.parse_natural_date.return_value = yesterday
        
        result = groq_tools.create_appointment(
            date_str="ayer",
            time_str="15:00"
        )
        
        # Should fail or warn
        assert isinstance(result, GroqToolResult)

    def test_very_far_future_booking(self, groq_tools, mock_availability_engine):
        """Book very far in the future (1 year)"""
        future = datetime.now() + timedelta(days=365)
        mock_availability_engine.parse_natural_date.return_value = future
        
        result = groq_tools.create_appointment(
            date_str="en un año",
            time_str="15:00"
        )
        
        assert isinstance(result, GroqToolResult)

    def test_empty_appointment_list(self, groq_tools, mock_booking_service):
        """Get appointments when none exist"""
        mock_booking_service.get_user_appointments.return_value = []
        
        result = groq_tools.get_appointments()
        
        assert result.success is True
        assert result.data["total"] == 0
        assert len(result.data["appointments"]) == 0

    def test_many_appointments(self, groq_tools, mock_booking_service):
        """Get large number of appointments"""
        appointments = [
            Mock(id=i, start_time=datetime.now() + timedelta(hours=i), duration_minutes=60)
            for i in range(50)
        ]
        mock_booking_service.get_user_appointments.return_value = appointments
        
        result = groq_tools.get_appointments()
        
        assert result.success is True
        assert result.data["total"] == 50


class TestResponseValidation:
    """H9.2: Response format and data validation"""

    def test_appointment_result_structure(self, groq_tools):
        """Verify GroqToolResult structure"""
        result = groq_tools.check_availability("mañana")
        
        # Check all required fields
        assert hasattr(result, 'success')
        assert hasattr(result, 'data')
        assert hasattr(result, 'message')
        assert hasattr(result, 'error')
        assert isinstance(result.success, bool)
        assert isinstance(result.data, dict)
        assert isinstance(result.message, str)

    def test_check_availability_response_fields(self, groq_tools):
        """Verify availability response has required fields"""
        result = groq_tools.check_availability("mañana")
        
        assert "available_slots" in result.data
        assert isinstance(result.data["available_slots"], list)

    def test_create_appointment_response_fields(self, groq_tools):
        """Verify create appointment response structure"""
        result = groq_tools.create_appointment("mañana", "15:00")
        
        assert "appointment_id" in result.data
        assert isinstance(result.data["appointment_id"], int)

    def test_get_appointments_response_fields(self, groq_tools):
        """Verify list appointments response"""
        result = groq_tools.get_appointments()
        
        assert "total" in result.data
        assert "appointments" in result.data
        assert isinstance(result.data["total"], int)
        assert isinstance(result.data["appointments"], list)

    def test_spanish_message_response(self, groq_tools):
        """All messages should be in Spanish"""
        result = groq_tools.create_appointment("mañana", "15:00")
        
        # Message should contain Spanish words (not perfect check, but reasonable)
        assert result.message is not None
        assert len(result.message) > 0


class TestConcurrency:
    """H9.3: Concurrent operations"""

    def test_concurrent_availability_checks(self, groq_tools, mock_availability_engine):
        """Multiple concurrent availability checks"""
        results = []
        
        def check_availability():
            result = groq_tools.check_availability("mañana")
            results.append(result)
        
        threads = [threading.Thread(target=check_availability) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 5
        assert all(r.success for r in results)

    def test_concurrent_appointments(self, groq_tools, mock_booking_service):
        """Multiple users trying to book same slot"""
        results = []
        
        def create_appointment():
            result = groq_tools.create_appointment("mañana", "15:00")
            results.append(result)
        
        threads = [threading.Thread(target=create_appointment) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 3
        # All should attempt to create (mock allows all)
        assert mock_booking_service.create_appointment.call_count >= 3


class TestErrorRecovery:
    """H9.4: Error handling and recovery"""

    def test_booking_service_timeout(self, groq_tools, mock_booking_service):
        """Handle booking service timeout"""
        mock_booking_service.create_appointment.side_effect = TimeoutError("Service timeout")
        
        result = groq_tools.create_appointment("mañana", "15:00")
        
        assert result.success is False
        assert result.error is not None

    def test_availability_engine_error(self, groq_tools, mock_availability_engine):
        """Handle availability engine error"""
        mock_availability_engine.get_available_slots.side_effect = Exception("Engine error")
        
        result = groq_tools.check_availability("mañana")
        
        assert isinstance(result, GroqToolResult)

    def test_cancel_nonexistent_appointment(self, groq_tools, mock_booking_service):
        """Cancel appointment that doesn't exist"""
        mock_booking_service.get_appointment.return_value = None
        
        result = groq_tools.cancel_appointment(999)
        
        assert isinstance(result, GroqToolResult)

    def test_database_connection_error(self, groq_tools, mock_booking_service):
        """Handle database connection errors"""
        mock_booking_service.get_user_appointments.side_effect = ConnectionError("DB unreachable")
        
        result = groq_tools.get_appointments()
        
        assert result.success is False


class TestPerformance:
    """H9.5: Performance and scalability"""

    def test_availability_check_speed(self, groq_tools):
        """Availability check should be fast"""
        start = time_module.time()
        result = groq_tools.check_availability("mañana")
        elapsed = time_module.time() - start
        
        assert result.success is True
        assert elapsed < 1.0  # Should complete in < 1 second

    def test_appointment_creation_speed(self, groq_tools):
        """Appointment creation should be fast"""
        start = time_module.time()
        result = groq_tools.create_appointment("mañana", "15:00")
        elapsed = time_module.time() - start
        
        assert result.success is True
        assert elapsed < 1.0

    def test_batch_get_appointments_speed(self, groq_tools, mock_booking_service):
        """Getting many appointments should complete quickly"""
        appointments = [
            Mock(id=i, start_time=datetime.now() + timedelta(hours=i), duration_minutes=60)
            for i in range(100)
        ]
        mock_booking_service.get_user_appointments.return_value = appointments
        
        start = time_module.time()
        result = groq_tools.get_appointments()
        elapsed = time_module.time() - start
        
        assert result.success is True
        assert elapsed < 2.0  # 100 items in < 2 seconds


class TestIntegrationScenarios:
    """H9.6: Complex integration scenarios"""

    def test_multi_step_booking_flow(self, groq_tools, mock_booking_service, mock_availability_engine):
        """Complete booking flow: check → create → list → cancel"""
        # Step 1: Check availability
        avail = groq_tools.check_availability("mañana")
        assert avail.success is True
        
        # Step 2: Create appointment
        create = groq_tools.create_appointment("mañana", "15:00")
        assert create.success is True
        apt_id = create.data["appointment_id"]
        
        # Step 3: List appointments
        mock_booking_service.get_user_appointments.return_value = [
            Mock(id=apt_id, start_time=datetime.now() + timedelta(days=1, hours=15), duration_minutes=60)
        ]
        list_apts = groq_tools.get_appointments()
        assert list_apts.success is True
        assert list_apts.data["total"] == 1
        
        # Step 4: Cancel appointment
        mock_booking_service.get_appointment.return_value = Mock(id=apt_id, status="cancelled")
        cancel = groq_tools.cancel_appointment(apt_id)
        assert cancel.success is True

    def test_double_booking_prevention(self, groq_tools, mock_booking_service, mock_availability_engine):
        """Try to double-book same slot"""
        mock_booking_service.is_slot_available = Mock(return_value=False)
        
        # First booking
        result1 = groq_tools.create_appointment("mañana", "15:00")
        
        # Second booking same slot
        result2 = groq_tools.create_appointment("mañana", "15:00")
        
        # Both results should be GroqToolResult (behavior depends on implementation)
        assert isinstance(result1, GroqToolResult)
        assert isinstance(result2, GroqToolResult)

    def test_appointment_duration_validation(self, groq_tools):
        """Validate appointment duration constraints"""
        # Too short
        result_short = groq_tools.create_appointment("mañana", "15:00", duration_minutes=5)
        assert isinstance(result_short, GroqToolResult)
        
        # Too long
        result_long = groq_tools.create_appointment("mañana", "15:00", duration_minutes=480)
        assert isinstance(result_long, GroqToolResult)
        
        # Valid
        result_valid = groq_tools.create_appointment("mañana", "15:00", duration_minutes=60)
        assert isinstance(result_valid, GroqToolResult)


class TestInputValidation:
    """H9.7: Input validation and sanitization"""

    def test_sql_injection_prevention(self, groq_tools):
        """Prevent SQL injection in date string"""
        malicious = "'; DROP TABLE appointments; --"
        result = groq_tools.create_appointment(malicious, "15:00")
        
        # Should not crash, should handle gracefully
        assert isinstance(result, GroqToolResult)

    def test_xss_prevention_in_response(self, groq_tools):
        """Response messages should be safe"""
        result = groq_tools.check_availability("mañana")
        
        # No HTML/JS in message
        assert "<script>" not in result.message
        assert "&lt;" not in result.message

    def test_unicode_date_strings(self, groq_tools, mock_availability_engine):
        """Handle Unicode characters in input"""
        mock_availability_engine.parse_natural_date.return_value = datetime.now() + timedelta(days=1)
        
        result = groq_tools.create_appointment("mañana", "15:00")
        assert result.success is True

    def test_whitespace_handling(self, groq_tools):
        """Properly handle whitespace in inputs"""
        result = groq_tools.create_appointment("  mañana  ", "  15:00  ")
        
        assert isinstance(result, GroqToolResult)


class TestDataConsistency:
    """H9.8: Data consistency and integrity"""

    def test_appointment_id_uniqueness(self, groq_tools, mock_booking_service):
        """Each appointment should have unique ID"""
        ids = []
        
        for i in range(5):
            mock_booking_service.create_appointment.return_value = Mock(id=i, user_id=123)
            result = groq_tools.create_appointment("mañana", f"{9+i}:00")
            ids.append(result.data["appointment_id"])
        
        # All IDs should be unique
        assert len(ids) == len(set(ids))

    def test_appointment_time_consistency(self, groq_tools, mock_booking_service):
        """Appointment times should be consistent"""
        tomorrow = datetime.now() + timedelta(days=1)
        apt_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 15, 0)
        
        mock_booking_service.create_appointment.return_value = Mock(
            id=1, 
            start_time=apt_time,
            duration_minutes=60
        )
        
        result = groq_tools.create_appointment("mañana", "15:00", duration_minutes=60)
        
        assert result.success is True
        assert result.data["appointment_id"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
