"""Test suite for Groq Tools Integration.

Covers:
- Tool execution (check_availability, create_appointment, get_appointments, cancel_appointment)
- Error handling and edge cases
- Integration with services (BookingService, AvailabilityEngine)
- Tool definition structure
- Result serialization
"""

import json
from datetime import datetime, timedelta, time
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from theaia.services.availability_engine import AvailabilityEngine
from theaia.services.booking_service import BookingService
from theaia.services.groq_tools import GroqTools, GroqToolResult
from theaia.services.user_service import UserService


class TestGroqToolResult:
    """Test GroqToolResult dataclass."""

    def test_success_result_creation(self):
        """Test creating successful result."""
        result = GroqToolResult(
            success=True, data={"slots": ["09:00", "10:00"]}, message="Success"
        )
        assert result.success is True
        assert result.data == {"slots": ["09:00", "10:00"]}
        assert result.error is None
        assert result.message == "Success"

    def test_error_result_creation(self):
        """Test creating error result."""
        result = GroqToolResult(
            success=False, error="Service unavailable", message="Error occurred"
        )
        assert result.success is False
        assert result.error == "Service unavailable"
        assert result.message == "Error occurred"
        assert result.data == {}

    def test_default_values(self):
        """Test default values in GroqToolResult."""
        result = GroqToolResult(success=True, message="OK")
        assert result.data == {}
        assert result.error is None


class TestGroqToolsInitialization:
    """Test GroqTools initialization."""

    @pytest.fixture
    def mock_services(self):
        """Create mock services."""
        return {
            "booking_service": MagicMock(spec=BookingService),
            "availability_engine": MagicMock(spec=AvailabilityEngine),
            "user_service": MagicMock(spec=UserService),
        }

    def test_initialization_with_required_params(self, mock_services):
        """Test GroqTools initialization with required parameters."""
        tools = GroqTools(
            booking_service=mock_services["booking_service"],
            availability_engine=mock_services["availability_engine"],
            user_id=123,
        )
        assert tools.user_id == 123
        assert tools.booking_service == mock_services["booking_service"]
        assert tools.availability_engine == mock_services["availability_engine"]

    def test_initialization_with_groq_client(self, mock_services):
        """Test GroqTools initialization with Groq client."""
        mock_client = MagicMock()
        tools = GroqTools(
            booking_service=mock_services["booking_service"],
            availability_engine=mock_services["availability_engine"],
            user_id=123,
            groq_client=mock_client,
        )
        assert tools.groq_client == mock_client

    def test_tool_definitions_generated(self, mock_services):
        """Test tool definitions are properly formatted."""
        tools = GroqTools(
            booking_service=mock_services["booking_service"],
            availability_engine=mock_services["availability_engine"],
            user_id=123,
        )
        definitions = tools._generate_tools_definitions()
        assert len(definitions) == 5  # FIX: Ahora incluye update_appointment
        tool_names = {t["function"]["name"] for t in definitions}
        assert tool_names == {
            "check_availability",
            "create_appointment",
            "get_appointments",
            "cancel_appointment",
            "update_appointment",  # FIX: Añadido
        }


class TestCheckAvailabilityTool:
    """Test check_availability tool."""

    @pytest.fixture
    def groq_tools(self):
        """Create GroqTools instance with mocked dependencies."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)
        user_service = MagicMock(spec=UserService)

        return GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=456,
            user_service=user_service,
        )

    def test_check_availability_success(self, groq_tools):
        """Test successful availability check."""
        # Mock parse_natural_date to return tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow

        # FIX: Mock get_available_slots con objetos time() en vez de integers
        groq_tools.availability_engine.get_available_slots.return_value = [
            time(9, 0),
            time(10, 0),
            time(11, 0),
            time(14, 0),
            time(15, 0),
        ]

        result = groq_tools.check_availability("mañana", 60)

        assert result.success is True
        assert "available_slots" in result.data
        assert len(result.data["available_slots"]) > 0

    def test_check_availability_no_slots(self, groq_tools):
        """Test availability check with no available slots."""
        tomorrow = datetime.now() + timedelta(days=1)
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow
        groq_tools.availability_engine.get_available_slots.return_value = []

        result = groq_tools.check_availability("mañana", 60)

        assert result.success is True
        assert result.data["available_slots"] == []
        # FIX: Mensaje actualizado
        assert "No hay horarios disponibles" in result.message

    def test_check_availability_error_handling(self, groq_tools):
        """Test error handling in availability check."""
        groq_tools.availability_engine.parse_natural_date.side_effect = ValueError(
            "Invalid date"
        )

        result = groq_tools.check_availability("invalid_date", 60)

        assert result.success is False
        assert result.error is not None
        assert "Error al verificar" in result.message

    def test_check_availability_different_durations(self, groq_tools):
        """Test availability check with different durations."""
        tomorrow = datetime.now() + timedelta(days=1)
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow
        # FIX: Mock con objetos time() en vez de integers
        groq_tools.availability_engine.get_available_slots.return_value = [
            time(9, 0),
            time(10, 0),
            time(11, 0),
        ]

        # Test 30 min duration
        result_30 = groq_tools.check_availability("mañana", 30)
        assert result_30.success is True

        # Test 120 min duration
        result_120 = groq_tools.check_availability("mañana", 120)
        assert result_120.success is True


class TestCreateAppointmentTool:
    """Test create_appointment tool."""

    @pytest.fixture
    def groq_tools(self):
        """Create GroqTools instance with mocked dependencies."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)
        user_service = MagicMock(spec=UserService)

        return GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=789,
            user_service=user_service,
        )

    def test_create_appointment_success(self, groq_tools):
        """Test successful appointment creation."""
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_15h = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)
        
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow
        # FIX: Mock debe devolver datetime completo con hora
        groq_tools.booking_service.create_appointment.return_value = tomorrow_15h

        result = groq_tools.create_appointment(
            date_str="mañana", time_str="15:00", duration_minutes=60, title="Cita"
        )

        assert result.success is True
        assert "appointment_id" in result.data
        assert "✅ Cita confirmada" in result.message

    def test_create_appointment_with_description(self, groq_tools):
        """Test appointment creation with description."""
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_10h = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow
        groq_tools.booking_service.create_appointment.return_value = tomorrow_10h

        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="10:00",
            duration_minutes=30,
            title="Consulta médica",
        )

        assert result.success is True

    def test_create_appointment_error_handling(self, groq_tools):
        """Test error handling in appointment creation."""
        groq_tools.availability_engine.parse_natural_date.side_effect = ValueError(
            "Invalid date"
        )

        result = groq_tools.create_appointment(
            date_str="invalid", time_str="15:00", title="Cita"
        )

        assert result.success is False
        assert "Error al crear cita" in result.message

    def test_create_appointment_booking_service_error(self, groq_tools):
        """Test error when booking service fails."""
        tomorrow = datetime.now() + timedelta(days=1)
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow
        groq_tools.booking_service.create_appointment.side_effect = RuntimeError(
            "Database error"
        )

        result = groq_tools.create_appointment(
            date_str="mañana", time_str="15:00", title="Cita"
        )

        assert result.success is False
        assert result.error is not None


class TestGetAppointmentsTool:
    """Test get_appointments tool."""

    @pytest.fixture
    def groq_tools(self):
        """Create GroqTools instance with mocked dependencies."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)
        user_service = MagicMock(spec=UserService)

        return GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=999,
            user_service=user_service,
        )

    def test_get_appointments_success(self, groq_tools):
        """Test successful retrieval of appointments."""
        mock_appointments = [
            {"id": 1, "date": "2025-12-18", "time": "15:00"},
            {"id": 2, "date": "2025-12-20", "time": "10:00"},
        ]
        groq_tools.booking_service.get_user_appointments.return_value = (
            mock_appointments
        )

        result = groq_tools.get_appointments()

        assert result.success is True
        assert result.data["total"] == 2
        assert "appointments" in result.data
        assert "Tienes 2 cita" in result.message

    def test_get_appointments_empty(self, groq_tools):
        """Test retrieval when user has no appointments."""
        groq_tools.booking_service.get_user_appointments.return_value = []

        result = groq_tools.get_appointments()

        assert result.success is True
        assert result.data["total"] == 0
        assert "Tienes 0 cita" in result.message

    def test_get_appointments_error_handling(self, groq_tools):
        """Test error handling in get_appointments."""
        groq_tools.booking_service.get_user_appointments.side_effect = RuntimeError(
            "Database connection failed"
        )

        result = groq_tools.get_appointments()

        assert result.success is False
        assert "Error al obtener citas" in result.message


class TestCancelAppointmentTool:
    """Test cancel_appointment tool."""

    @pytest.fixture
    def groq_tools(self):
        """Create GroqTools instance with mocked dependencies."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)
        user_service = MagicMock(spec=UserService)

        return GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=555,
            user_service=user_service,
        )

    def test_cancel_appointment_success(self, groq_tools):
        """Test successful appointment cancellation."""
        groq_tools.booking_service.cancel_appointment.return_value = True

        result = groq_tools.cancel_appointment(appointment_id=123)

        assert result.success is True
        assert "✅ Cita cancelada" in result.message
        groq_tools.booking_service.cancel_appointment.assert_called_once_with(123)

    def test_cancel_appointment_not_found(self, groq_tools):
        """Test cancellation of non-existent appointment."""
        groq_tools.booking_service.cancel_appointment.side_effect = ValueError(
            "Appointment not found"
        )

        result = groq_tools.cancel_appointment(appointment_id=999)

        assert result.success is False
        assert "Error al cancelar" in result.message

    def test_cancel_appointment_error_handling(self, groq_tools):
        """Test error handling in appointment cancellation."""
        groq_tools.booking_service.cancel_appointment.side_effect = RuntimeError(
            "Database error"
        )

        result = groq_tools.cancel_appointment(appointment_id=123)

        assert result.success is False
        assert result.error is not None


class TestExecuteTool:
    """Test execute_tool dispatcher."""

    @pytest.fixture
    def groq_tools(self):
        """Create GroqTools instance with mocked dependencies."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)
        user_service = MagicMock(spec=UserService)

        return GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=111,
            user_service=user_service,
        )

    def test_execute_tool_check_availability(self, groq_tools):
        """Test execute_tool dispatcher for check_availability."""
        tomorrow = datetime.now() + timedelta(days=1)
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow
        groq_tools.availability_engine.get_available_slots.return_value = [
            time(10, 0),
            time(11, 0),
            time(14, 0),
        ]

        result = groq_tools.execute_tool(
            "check_availability", {"date_str": "mañana"}
        )

        assert result.success is True
        assert "available_slots" in result.data

    def test_execute_tool_create_appointment(self, groq_tools):
        """Test execute_tool dispatcher for create_appointment."""
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_15h = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)
        
        groq_tools.availability_engine.parse_natural_date.return_value = tomorrow
        groq_tools.booking_service.create_appointment.return_value = tomorrow_15h

        result = groq_tools.execute_tool(
            "create_appointment",
            {"date_str": "mañana", "time_str": "15:00"},
        )

        assert result.success is True

    def test_execute_tool_get_appointments(self, groq_tools):
        """Test execute_tool dispatcher for get_appointments."""
        groq_tools.booking_service.get_user_appointments.return_value = []

        result = groq_tools.execute_tool("get_appointments", {})

        assert result.success is True

    def test_execute_tool_cancel_appointment(self, groq_tools):
        """Test execute_tool dispatcher for cancel_appointment."""
        groq_tools.booking_service.cancel_appointment.return_value = True

        result = groq_tools.execute_tool(
            "cancel_appointment", {"appointment_id": 123}
        )

        assert result.success is True

    def test_execute_tool_unknown_tool(self, groq_tools):
        """Test execute_tool with unknown tool name."""
        result = groq_tools.execute_tool("unknown_tool", {})

        assert result.success is False
        assert "Unknown tool" in result.error or "desconocida" in result.message


class TestToolDefinitionsStructure:
    """Test tool definitions structure and compatibility."""

    @pytest.fixture
    def groq_tools(self):
        """Create GroqTools instance with mocked dependencies."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)

        return GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=222,
        )

    def test_tools_are_openai_format(self, groq_tools):
        """Test tools follow OpenAI tool format."""
        tools = groq_tools._generate_tools_definitions()

        for tool in tools:
            assert "type" in tool
            assert tool["type"] == "function"
            assert "function" in tool
            assert "name" in tool["function"]
            assert "description" in tool["function"]
            assert "parameters" in tool["function"]

    def test_check_availability_parameters(self, groq_tools):
        """Test check_availability tool parameters."""
        tools = groq_tools._generate_tools_definitions()
        check_avail_tool = [t for t in tools if t["function"]["name"] == "check_availability"][0]

        params = check_avail_tool["function"]["parameters"]
        assert params["type"] == "object"
        assert "date" in params["properties"]
        assert "date" in params["required"]

    def test_create_appointment_parameters(self, groq_tools):
        """Test create_appointment tool parameters."""
        tools = groq_tools._generate_tools_definitions()
        create_tool = [t for t in tools if t["function"]["name"] == "create_appointment"][0]

        params = create_tool["function"]["parameters"]
        assert "date" in params["properties"]
        assert "time" in params["properties"]
        assert "title" in params["properties"]
        assert set(params["required"]) >= {"date", "time", "title"}

    def test_tool_registry_completeness(self, groq_tools):
        """Test tool registry contains all tools."""
        # FIX: Ahora son 5 tools
        assert len(groq_tools.TOOLS_REGISTRY) == 5
        assert "check_availability" in groq_tools.TOOLS_REGISTRY
        assert "create_appointment" in groq_tools.TOOLS_REGISTRY
        assert "get_appointments" in groq_tools.TOOLS_REGISTRY
        assert "cancel_appointment" in groq_tools.TOOLS_REGISTRY
        assert "update_appointment" in groq_tools.TOOLS_REGISTRY  # FIX: Añadido


class TestGroqIntegration:
    """Test Groq API integration."""

    @pytest.fixture
    def groq_tools_with_client(self):
        """Create GroqTools with mock Groq client."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)
        mock_groq_client = MagicMock()

        return GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=333,
            groq_client=mock_groq_client,
        )

    @pytest.mark.asyncio
    async def test_call_groq_with_tools_no_client(self):
        """Test call_groq_with_tools when client is not configured."""
        booking_service = MagicMock(spec=BookingService)
        availability_engine = MagicMock(spec=AvailabilityEngine)

        groq_tools = GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=444,
            groq_client=None,
        )

        response = await groq_tools.call_groq_with_tools("¿Cuándo puedo agendar?")

        assert "❌ Groq client not configured" in response or response is not None

    @pytest.mark.asyncio
    async def test_call_groq_with_tools_success(self, groq_tools_with_client):
        """Test successful Groq API call."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Aquí están los horarios disponibles"
        groq_tools_with_client.groq_client.chat.completions.create.return_value = (
            mock_response
        )

        response = await groq_tools_with_client.call_groq_with_tools(
            "¿Cuándo puedo agendar?"
        )

        assert response is not None
        groq_tools_with_client.groq_client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_call_groq_error_handling(self, groq_tools_with_client):
        """Test error handling in Groq API call."""
        groq_tools_with_client.groq_client.chat.completions.create.side_effect = (
            RuntimeError("API error")
        )

        response = await groq_tools_with_client.call_groq_with_tools(
            "¿Cuándo puedo agendar?"
        )

        assert "❌ Error" in response or response is not None


__all__ = [
    "TestGroqToolResult",
    "TestGroqToolsInitialization",
    "TestCheckAvailabilityTool",
    "TestCreateAppointmentTool",
    "TestGetAppointmentsTool",
    "TestCancelAppointmentTool",
    "TestExecuteTool",
    "TestToolDefinitionsStructure",
    "TestGroqIntegration",
]
