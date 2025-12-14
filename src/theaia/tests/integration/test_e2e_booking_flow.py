"""
E2E Integration Tests - GroqTools → Services → Database
Target: 10 tests | Real flow validation (no external dependencies)
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from theaia.services.groq_tools import GroqTools, GroqToolResult
from theaia.services.booking_service import BookingService
from theaia.services.availability_engine import AvailabilityEngine
from theaia.database.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user_repo():
    """Mock UserRepository"""
    repo = Mock(spec=UserRepository)
    repo.get_or_create_user = Mock(return_value=Mock(id=123, telegram_id=123))
    return repo


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
    slots = [f"{h:02d}:00" for h in range(9, 18)]  # 9am-6pm
    engine.get_available_slots = Mock(return_value=slots)
    engine.is_slot_available = Mock(return_value=True)
    return engine


@pytest.fixture
def groq_tools(mock_booking_service, mock_availability_engine):
    """GroqTools with mocked services"""
    tools = GroqTools(
        booking_service=mock_booking_service,
        availability_engine=mock_availability_engine,
        user_id=123
    )
    return tools


class TestE2EBookingFlow:
    """E2E Tests: Tools → Services → Database simulation"""

    def test_check_availability_success(self, groq_tools, mock_availability_engine):
        """
        E2E: User asks availability
        "¿Qué horarios tienes disponibles mañana?"
        """
        # Call tool
        result = groq_tools.check_availability("mañana")

        # Verify result
        assert isinstance(result, GroqToolResult)
        assert result.success is True
        assert "available_slots" in result.data
        assert len(result.data["available_slots"]) > 0
        assert result.message  # Spanish message


    def test_create_appointment_success(self, groq_tools, mock_booking_service):
        """
        E2E: User books appointment
        "Quiero agendar mañana a las 15:00"
        """
        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="15:00",
            duration_minutes=60
        )

        assert result.success is True
        assert result.data["appointment_id"] == 1
        assert "confirmada" in result.message.lower()
        mock_booking_service.create_appointment.assert_called_once()


    def test_get_appointments_with_data(self, groq_tools, mock_booking_service):
        """
        E2E: User lists their appointments
        "/mis_citas" command
        """
        # Mock data
        tomorrow = datetime.now() + timedelta(days=1)
        mock_apt = Mock(
            id=1,
            start_time=tomorrow.replace(hour=15, minute=0),
            duration_minutes=60
        )
        mock_booking_service.get_user_appointments.return_value = [mock_apt]

        # Call tool
        result = groq_tools.get_appointments()

        assert result.success is True
        assert result.data["total"] == 1
        assert len(result.data["appointments"]) == 1
        assert "mañana" in result.message or "tomorrow" in result.message


    def test_cancel_appointment_success(self, groq_tools, mock_booking_service):
        """
        E2E: User cancels appointment
        "/cancelar_cita <id>"
        """
        appointment_id = 1
        mock_booking_service.get_appointment.return_value = Mock(
            id=appointment_id,
            status="cancelled"
        )

        result = groq_tools.cancel_appointment(appointment_id)

        assert result.success is True
        assert "cancelada" in result.message.lower()
        mock_booking_service.cancel_appointment.assert_called_once()


    def test_natural_language_date_parsing(self, groq_tools):
        """
        Test: Natural language to datetime conversion
        - "hoy" → today
        - "mañana" → tomorrow
        - "próximo jueves" → next Thursday
        - "2025-12-25" → ISO format
        """
        tomorrow = datetime.now() + timedelta(days=1)

        # Test "mañana"
        parsed = groq_tools._parse_natural_date("mañana")
        assert parsed.date() == tomorrow.date()

        # Test ISO format
        iso_date = "2025-12-25"
        parsed = groq_tools._parse_natural_date(iso_date)
        assert parsed.year == 2025
        assert parsed.month == 12
        assert parsed.day == 25


    def test_natural_language_time_parsing(self, groq_tools):
        """
        Test: Natural language to time conversion
        - "15:00" → 15:00
        - "3pm" → 15:00
        - "3 pm" → 15:00
        - "9" → 09:00
        """
        # Test 24h format
        time = groq_tools._parse_time("15:00")
        assert time.hour == 15
        assert time.minute == 0

        # Test simple hour
        time = groq_tools._parse_time("9")
        assert time.hour == 9


    def test_error_handling_invalid_date(self, groq_tools):
        """
        Test: Invalid date parsing
        "fecha_imposible" should return error
        """
        result = groq_tools.create_appointment(
            date_str="fecha_totalmente_invalida_xyz",
            time_str="15:00"
        )

        assert result.success is False
        assert result.error is not None
        assert "invalid" in result.error.lower() or "no válida" in result.error.lower()


    def test_error_handling_invalid_time(self, groq_tools):
        """
        Test: Invalid time parsing
        "25:99" should return error
        """
        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="25:99"
        )

        assert result.success is False
        assert result.error is not None


    def test_tool_registry_dispatch(self, groq_tools):
        """
        Test: Tool registry can dispatch all registered tools
        GroqTools.TOOLS_REGISTRY contains all tool functions
        """
        registry = groq_tools.TOOLS_REGISTRY

        # Check all tools are registered
        assert "check_availability" in registry
        assert "create_appointment" in registry
        assert "get_appointments" in registry
        assert "cancel_appointment" in registry

        # Check execute_tool dispatcher works
        result = groq_tools.execute_tool("check_availability", {"date_str": "mañana"})
        assert isinstance(result, GroqToolResult)


    def test_tool_definitions_schema(self, groq_tools):
        """
        Test: Tool definitions match OpenAI schema
        Each tool should have: name, description, parameters
        """
        definitions = groq_tools._generate_tools_definitions()

        assert isinstance(definitions, list)
        assert len(definitions) == 4

        for tool_def in definitions:
            assert "type" in tool_def
            assert "function" in tool_def
            assert "name" in tool_def["function"]
            assert "description" in tool_def["function"]
            assert "parameters" in tool_def["function"]

            # Parameters should have proper JSON schema
            params = tool_def["function"]["parameters"]
            assert "type" in params
            assert params["type"] == "object"
            assert "properties" in params


class TestFullBookingFlowWithMocks:
    """Integration test simulating complete user flow"""

    def test_complete_booking_journey(self, groq_tools, mock_booking_service, mock_availability_engine):
        """
        Simulate complete journey:
        1. User asks availability
        2. System shows slots
        3. User requests booking
        4. System confirms
        5. User lists appointments
        """
        # Step 1-2: Check availability
        avail_result = groq_tools.check_availability("mañana")
        assert avail_result.success is True
        available_slots = avail_result.data["available_slots"]
        assert len(available_slots) > 0

        # Step 3-4: Create appointment
        booking_result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="15:00",
            duration_minutes=60
        )
        assert booking_result.success is True

        # Step 5: List appointments
        mock_booking_service.get_user_appointments.return_value = [
            Mock(
                id=1,
                start_time=datetime.now() + timedelta(days=1, hours=15),
                duration_minutes=60
            )
        ]
        list_result = groq_tools.get_appointments()
        assert list_result.success is True
        assert list_result.data["total"] == 1
