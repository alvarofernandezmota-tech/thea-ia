"""Tests for Groq Tools Integration.

Comprehensive test suite for GroqToolsIntegration class, validating:
- Tool calling functionality
- Natural language understanding
- Appointment management through tools
- Error handling and edge cases
- Integration with services
"""

import json
from datetime import datetime, timedelta
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from theaia.services.groq_tools import GroqToolsIntegration


# Fixtures
@pytest.fixture
def mock_groq_client():
    """Mock Groq client."""
    return MagicMock()


@pytest.fixture
def mock_user_service():
    """Mock UserService."""
    mock = MagicMock()
    mock.get_user.return_value = {
        "id": 1,
        "telegram_id": 12345,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "timezone": "Europe/Madrid",
    }
    return mock


@pytest.fixture
def mock_booking_service():
    """Mock BookingService."""
    mock = MagicMock()
    mock.check_conflict.return_value = False
    mock.create_appointment.return_value = {
        "id": uuid4(),
        "user_id": 1,
        "title": "Test Appointment",
        "start_time": datetime.now() + timedelta(days=1),
        "end_time": datetime.now() + timedelta(days=1, hours=1),
        "status": "scheduled",
    }
    mock.get_upcoming_appointments.return_value = []
    mock.get_past_appointments.return_value = []
    mock.cancel_appointment.return_value = {"success": True}
    return mock


@pytest.fixture
def mock_availability_engine():
    """Mock AvailabilityEngine."""
    mock = MagicMock()
    
    def parse_date_side_effect(date_str):
        if date_str.lower() == "today":
            return datetime.now()
        elif date_str.lower() == "tomorrow":
            return datetime.now() + timedelta(days=1)
        else:
            return datetime.now() + timedelta(days=7)
    
    def parse_time_side_effect(time_str):
        if "9" in time_str or "09" in time_str:
            return datetime.strptime("09:00", "%H:%M")
        elif "14" in time_str or "2" in time_str:
            return datetime.strptime("14:30", "%H:%M")
        else:
            return datetime.strptime("10:00", "%H:%M")
    
    mock.parse_natural_date.side_effect = parse_date_side_effect
    mock.parse_natural_time.side_effect = parse_time_side_effect
    
    # Mock available slots
    tomorrow = datetime.now() + timedelta(days=1)
    mock.get_available_slots.return_value = [
        {
            "start": tomorrow.replace(hour=9, minute=0),
            "end": tomorrow.replace(hour=10, minute=0),
        },
        {
            "start": tomorrow.replace(hour=14, minute=30),
            "end": tomorrow.replace(hour=15, minute=30),
        },
    ]
    
    return mock


@pytest.fixture
def groq_tools_integration(mock_groq_client, mock_user_service, mock_booking_service, mock_availability_engine):
    """Create GroqToolsIntegration instance."""
    return GroqToolsIntegration(
        groq_client=mock_groq_client,
        user_service=mock_user_service,
        booking_service=mock_booking_service,
        availability_engine=mock_availability_engine,
    )


# Test Classes
class TestGroqToolsIntegrationInit:
    """Test GroqToolsIntegration initialization."""

    def test_initialization(self, groq_tools_integration, mock_groq_client):
        """Test that GroqToolsIntegration initializes correctly."""
        assert groq_tools_integration.groq_client == mock_groq_client
        assert groq_tools_integration.user_service is not None
        assert groq_tools_integration.booking_service is not None
        assert groq_tools_integration.availability_engine is not None

    def test_tools_defined(self, groq_tools_integration):
        """Test that all tools are properly defined."""
        assert len(groq_tools_integration.TOOLS) == 4
        tool_names = [tool["function"]["name"] for tool in groq_tools_integration.TOOLS]
        assert "check_availability" in tool_names
        assert "create_appointment" in tool_names
        assert "get_appointments" in tool_names
        assert "cancel_appointment" in tool_names


class TestCheckAvailabilityTool:
    """Test check_availability tool functionality."""

    @pytest.mark.asyncio
    async def test_check_availability_success(self, groq_tools_integration):
        """Test successful availability check."""
        result = await groq_tools_integration._tool_check_availability(
            {"date": "tomorrow", "duration": 60},
            user_id=1,
        )
        
        assert result["status"] == "success"
        assert result["duration_minutes"] == 60
        assert len(result["available_slots"]) > 0
        assert "start_time" in result["available_slots"][0]
        assert "end_time" in result["available_slots"][0]

    @pytest.mark.asyncio
    async def test_check_availability_custom_duration(self, groq_tools_integration):
        """Test availability check with custom duration."""
        result = await groq_tools_integration._tool_check_availability(
            {"date": "today", "duration": 120},
            user_id=1,
        )
        
        assert result["status"] == "success"
        assert result["duration_minutes"] == 120

    @pytest.mark.asyncio
    async def test_check_availability_no_slots(self, groq_tools_integration):
        """Test availability check when no slots available."""
        groq_tools_integration.availability_engine.get_available_slots.return_value = []
        
        result = await groq_tools_integration._tool_check_availability(
            {"date": "tomorrow"},
            user_id=1,
        )
        
        assert result["status"] == "no_slots"

    @pytest.mark.asyncio
    async def test_check_availability_error_handling(self, groq_tools_integration):
        """Test error handling in availability check."""
        groq_tools_integration.availability_engine.parse_natural_date.side_effect = ValueError("Invalid date")
        
        result = await groq_tools_integration._tool_check_availability(
            {"date": "invalid"},
            user_id=1,
        )
        
        assert "error" in result


class TestCreateAppointmentTool:
    """Test create_appointment tool functionality."""

    @pytest.mark.asyncio
    async def test_create_appointment_success(self, groq_tools_integration):
        """Test successful appointment creation."""
        result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "tomorrow",
                "time": "9am",
                "title": "Meeting with client",
                "duration": 60,
            },
            user_id=1,
        )
        
        assert result["status"] == "success"
        assert result["appointment_id"] is not None
        assert "Cita agendada" in result["message"]

    @pytest.mark.asyncio
    async def test_create_appointment_with_description(self, groq_tools_integration):
        """Test appointment creation with description."""
        result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "tomorrow",
                "time": "14:30",
                "title": "Project discussion",
                "duration": 90,
                "description": "Discuss project timeline and requirements",
            },
            user_id=1,
        )
        
        assert result["status"] == "success"
        groq_tools_integration.booking_service.create_appointment.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_appointment_conflict(self, groq_tools_integration):
        """Test appointment creation with time conflict."""
        groq_tools_integration.booking_service.check_conflict.return_value = True
        
        result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "tomorrow",
                "time": "9am",
                "title": "Conflicted meeting",
            },
            user_id=1,
        )
        
        assert result["status"] == "conflict"
        assert "Ya hay una cita" in result["error"]

    @pytest.mark.asyncio
    async def test_create_appointment_missing_required_field(self, groq_tools_integration):
        """Test appointment creation with missing required field."""
        result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "tomorrow",
                # Missing 'time' and 'title'
            },
            user_id=1,
        )
        
        assert "error" in result


class TestGetAppointmentsTool:
    """Test get_appointments tool functionality."""

    @pytest.mark.asyncio
    async def test_get_appointments_upcoming(self, groq_tools_integration):
        """Test retrieving upcoming appointments."""
        mock_appointments = [
            {
                "id": uuid4(),
                "title": "Meeting",
                "start_time": datetime.now() + timedelta(days=1),
                "end_time": datetime.now() + timedelta(days=1, hours=1),
                "status": "scheduled",
            }
        ]
        groq_tools_integration.booking_service.get_upcoming_appointments.return_value = mock_appointments
        
        result = await groq_tools_integration._tool_get_appointments(
            {"filter": "upcoming"},
            user_id=1,
        )
        
        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["filter"] == "upcoming"

    @pytest.mark.asyncio
    async def test_get_appointments_past(self, groq_tools_integration):
        """Test retrieving past appointments."""
        mock_appointments = [
            {
                "id": uuid4(),
                "title": "Past meeting",
                "start_time": datetime.now() - timedelta(days=1),
                "end_time": datetime.now() - timedelta(days=1, hours=-1),
                "status": "completed",
            }
        ]
        groq_tools_integration.booking_service.get_past_appointments.return_value = mock_appointments
        
        result = await groq_tools_integration._tool_get_appointments(
            {"filter": "past"},
            user_id=1,
        )
        
        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["filter"] == "past"

    @pytest.mark.asyncio
    async def test_get_appointments_empty(self, groq_tools_integration):
        """Test retrieving appointments when none exist."""
        groq_tools_integration.booking_service.get_upcoming_appointments.return_value = []
        
        result = await groq_tools_integration._tool_get_appointments(
            {"filter": "upcoming"},
            user_id=1,
        )
        
        assert result["status"] == "empty"
        assert "No hay citas" in result["message"]


class TestCancelAppointmentTool:
    """Test cancel_appointment tool functionality."""

    @pytest.mark.asyncio
    async def test_cancel_appointment_success(self, groq_tools_integration):
        """Test successful appointment cancellation."""
        appointment_id = str(uuid4())
        
        result = await groq_tools_integration._tool_cancel_appointment(
            {
                "appointment_id": appointment_id,
                "reason": "User requested",
            },
            user_id=1,
        )
        
        assert result["status"] == "success"
        assert "Cita cancelada" in result["message"]

    @pytest.mark.asyncio
    async def test_cancel_appointment_missing_id(self, groq_tools_integration):
        """Test cancellation without appointment ID."""
        result = await groq_tools_integration._tool_cancel_appointment(
            {"reason": "User requested"},
            user_id=1,
        )
        
        assert "error" in result
        assert "appointment_id" in result["error"]

    @pytest.mark.asyncio
    async def test_cancel_appointment_not_found(self, groq_tools_integration):
        """Test cancellation of non-existent appointment."""
        groq_tools_integration.booking_service.cancel_appointment.return_value = {
            "success": False,
            "message": "Appointment not found",
        }
        
        result = await groq_tools_integration._tool_cancel_appointment(
            {"appointment_id": str(uuid4())},
            user_id=1,
        )
        
        assert result["status"] == "error"


class TestGroqToolCalling:
    """Test Groq LLM tool calling integration."""

    @pytest.mark.asyncio
    async def test_call_groq_with_no_tools(self, groq_tools_integration, mock_groq_client):
        """Test calling Groq without tool invocation."""
        # Mock response without tool calls
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_message.tool_calls = None
        mock_message.content = "Hola, ¿cómo puedo ayudarte?"
        mock_response.choices = [MagicMock(message=mock_message)]
        mock_groq_client.chat.completions.create.return_value = mock_response
        
        result = await groq_tools_integration.call_groq_with_tools(
            user_input="Hola",
            user_id=1,
        )
        
        assert "Hola" in result or "ayudarte" in result
        assert mock_groq_client.chat.completions.create.call_count == 1

    @pytest.mark.asyncio
    async def test_call_groq_with_tool_execution(self, groq_tools_integration, mock_groq_client):
        """Test calling Groq with tool execution."""
        # Mock tool call response
        tool_call = MagicMock()
        tool_call.function.name = "check_availability"
        tool_call.function.arguments = json.dumps({"date": "tomorrow"})
        
        mock_message_with_tools = MagicMock()
        mock_message_with_tools.tool_calls = [tool_call]
        mock_message_with_tools.content = ""
        
        mock_final_message = MagicMock()
        mock_final_message.content = "Aquí están los horarios disponibles..."
        
        # First call returns tool request, second returns final response
        responses = [
            MagicMock(choices=[MagicMock(message=mock_message_with_tools)]),
            MagicMock(choices=[MagicMock(message=mock_final_message)]),
        ]
        mock_groq_client.chat.completions.create.side_effect = responses
        
        result = await groq_tools_integration.call_groq_with_tools(
            user_input="Muéstrame disponibilidad para mañana",
            user_id=1,
        )
        
        assert result is not None
        assert mock_groq_client.chat.completions.create.call_count == 2

    @pytest.mark.asyncio
    async def test_call_groq_user_not_found(self, groq_tools_integration, mock_user_service):
        """Test calling Groq when user doesn't exist."""
        mock_user_service.get_user.return_value = None
        
        result = await groq_tools_integration.call_groq_with_tools(
            user_input="Hola",
            user_id=999,
        )
        
        assert "Usuario no encontrado" in result


class TestGroqToolsErrorHandling:
    """Test error handling in Groq Tools Integration."""

    @pytest.mark.asyncio
    async def test_tool_execution_error(self, groq_tools_integration):
        """Test handling of tool execution errors."""
        groq_tools_integration.availability_engine.parse_natural_date.side_effect = Exception("Parse error")
        
        result = await groq_tools_integration._tool_check_availability(
            {"date": "invalid_date"},
            user_id=1,
        )
        
        assert "error" in result

    @pytest.mark.asyncio
    async def test_invalid_tool_name(self, groq_tools_integration):
        """Test handling of invalid tool names."""
        result = await groq_tools_integration._execute_tool(
            tool_name="invalid_tool",
            tool_args={},
            user_id=1,
        )
        
        assert "error" in result
        assert "Unknown tool" in result["error"]

    @pytest.mark.asyncio
    async def test_groq_api_error(self, groq_tools_integration, mock_groq_client):
        """Test handling of Groq API errors."""
        mock_groq_client.chat.completions.create.side_effect = Exception("API Error")
        
        result = await groq_tools_integration.call_groq_with_tools(
            user_input="Hola",
            user_id=1,
        )
        
        assert "Error procesando" in result


class TestGroqToolsSpanishSupport:
    """Test Spanish language support in tools."""

    @pytest.mark.asyncio
    async def test_spanish_date_parsing(self, groq_tools_integration):
        """Test Spanish date parsing."""
        result = await groq_tools_integration._tool_check_availability(
            {"date": "mañana", "duration": 60},
            user_id=1,
        )
        
        # Should handle Spanish dates
        assert result is not None

    @pytest.mark.asyncio
    async def test_spanish_time_parsing(self, groq_tools_integration):
        """Test Spanish time parsing."""
        result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "mañana",
                "time": "las 14:30",
                "title": "Reunión importante",
            },
            user_id=1,
        )
        
        assert result is not None


class TestGroqToolsEdgeCases:
    """Test edge cases in Groq Tools Integration."""

    @pytest.mark.asyncio
    async def test_very_long_appointment_title(self, groq_tools_integration):
        """Test appointment creation with very long title."""
        long_title = "A" * 500
        
        result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "tomorrow",
                "time": "9am",
                "title": long_title,
            },
            user_id=1,
        )
        
        assert result is not None

    @pytest.mark.asyncio
    async def test_multiple_tool_calls_sequence(self, groq_tools_integration):
        """Test sequence of multiple tool calls."""
        # Check availability
        avail_result = await groq_tools_integration._tool_check_availability(
            {"date": "tomorrow"},
            user_id=1,
        )
        assert avail_result["status"] == "success"
        
        # Create appointment
        create_result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "tomorrow",
                "time": "9am",
                "title": "Follow-up",
            },
            user_id=1,
        )
        assert create_result["status"] == "success"
        
        # Get appointments
        get_result = await groq_tools_integration._tool_get_appointments(
            {"filter": "upcoming"},
            user_id=1,
        )
        assert get_result is not None

    @pytest.mark.asyncio
    async def test_appointment_at_midnight(self, groq_tools_integration):
        """Test appointment at midnight edge case."""
        groq_tools_integration.availability_engine.parse_natural_time.return_value = datetime.strptime("00:00", "%H:%M")
        
        result = await groq_tools_integration._tool_create_appointment(
            {
                "date": "tomorrow",
                "time": "00:00",
                "title": "Midnight meeting",
                "duration": 60,
            },
            user_id=1,
        )
        
        # Should support midnight appointments (24/7 philosophy)
        assert result is not None
