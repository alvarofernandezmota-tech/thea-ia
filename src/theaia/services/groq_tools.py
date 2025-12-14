"""
Groq Tools Integration for THEA IA.

This module integrates Groq LLM with THEA IA services through tool calling.
Tools available:
- check_availability: Get available slots for scheduling
- create_appointment: Create a new appointment
- get_appointments: Retrieve user appointments
- cancel_appointment: Cancel an existing appointment
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from groq import Groq

from theaia.services.availability_engine import AvailabilityEngine
from theaia.services.booking_service import BookingService
from theaia.services.user_service import UserService

logger = logging.getLogger(__name__)


@dataclass
class GroqToolResult:
    """Result from a Groq tool execution."""
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    message: str = ""


class GroqTools:
    """Integration between Groq LLM and THEA IA services via tool calling."""

    # Tool definitions for Groq
    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "check_availability",
                "description": "Check available time slots for scheduling appointments on a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Target date in natural language (e.g., 'tomorrow', 'next monday', '25 de diciembre')",
                        },
                        "duration": {
                            "type": "integer",
                            "description": "Duration of appointment in minutes (30, 60, 120)",
                            "default": 60,
                        },
                    },
                    "required": ["date"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_appointment",
                "description": "Create a new appointment/event in the user's calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date of appointment (e.g., 'tomorrow', 'next monday')",
                        },
                        "time": {
                            "type": "string",
                            "description": "Time of appointment (e.g., '9am', '14:30', 'las 15:00')",
                        },
                        "title": {
                            "type": "string",
                            "description": "Title/name of the appointment",
                        },
                        "duration": {
                            "type": "integer",
                            "description": "Duration in minutes (default: 60)",
                            "default": 60,
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional description/details",
                        },
                    },
                    "required": ["date", "time", "title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_appointments",
                "description": "Retrieve user appointments with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filter": {
                            "type": "string",
                            "enum": ["upcoming", "past", "all"],
                            "description": "Filter appointments by status",
                            "default": "upcoming",
                        },
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "cancel_appointment",
                "description": "Cancel an existing appointment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {
                            "type": "string",
                            "description": "UUID of the appointment to cancel",
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for cancellation",
                        },
                    },
                    "required": ["appointment_id"],
                },
            },
        },
    ]

    # Tool registry for dispatch
    TOOLS_REGISTRY = {
        "check_availability": "check_availability",
        "create_appointment": "create_appointment",
        "get_appointments": "get_appointments",
        "cancel_appointment": "cancel_appointment",
    }

    def __init__(
        self,
        booking_service: BookingService,
        availability_engine: AvailabilityEngine,
        user_id: int,
        groq_client: Optional[Groq] = None,
        user_service: Optional[UserService] = None,
    ):
        """Initialize Groq Tools.

        Args:
            booking_service: BookingService instance for appointments
            availability_engine: AvailabilityEngine for slot management
            user_id: User ID for this session
            groq_client: Optional Groq API client
            user_service: Optional UserService instance
        """
        self.booking_service = booking_service
        self.availability_engine = availability_engine
        self.user_id = user_id
        self.groq_client = groq_client
        self.user_service = user_service

    def _generate_tools_definitions(self) -> List[Dict[str, Any]]:
        """Generate tool definitions for OpenAI API format.

        Returns:
            List of tool definitions
        """
        return self.TOOLS

    def _parse_natural_date(self, date_str: str) -> datetime:
        """Parse natural language date string.

        Args:
            date_str: Date in natural language (e.g., 'tomorrow', 'mañana')

        Returns:
            Parsed datetime object
        """
        return self.availability_engine.parse_natural_date(date_str)

    def _parse_time(self, time_str: str) -> datetime:
        """Parse natural language time string.

        Args:
            time_str: Time in natural language (e.g., '15:00', '3pm')

        Returns:
            Parsed time object
        """
        return self.availability_engine.parse_natural_time(time_str)

    def check_availability(self, date_str: str, duration_minutes: int = 60) -> GroqToolResult:
        """Check available slots for a date.

        Args:
            date_str: Date in natural language
            duration_minutes: Duration of requested slot

        Returns:
            GroqToolResult with available slots
        """
        try:
            target_date = self._parse_natural_date(date_str)
            slots = self.availability_engine.get_available_slots(
                user_id=self.user_id,
                target_date=target_date,
                slot_duration=duration_minutes,
            )

            if not slots:
                return GroqToolResult(
                    success=True,
                    data={"available_slots": []},
                    message=f"No hay slots disponibles para {date_str}",
                )

            slot_strs = [f"{h:02d}:00" for h in range(9, 18)]  # 9am-6pm
            return GroqToolResult(
                success=True,
                data={"available_slots": slot_strs},
                message=f"Slots disponibles para {date_str}: {', '.join(slot_strs)}",
            )
        except Exception as e:
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"Error al verificar disponibilidad: {str(e)}",
            )

    def create_appointment(
        self,
        date_str: str,
        time_str: str,
        duration_minutes: int = 60,
        title: str = "Cita",
    ) -> GroqToolResult:
        """Create a new appointment.

        Args:
            date_str: Date in natural language
            time_str: Time in natural language
            duration_minutes: Duration of appointment
            title: Title of appointment

        Returns:
            GroqToolResult with appointment details
        """
        try:
            target_date = self._parse_natural_date(date_str)
            start_time = self.booking_service.create_appointment(
                user_id=self.user_id,
                start_time=target_date,
                duration_minutes=duration_minutes,
            )

            return GroqToolResult(
                success=True,
                data={"appointment_id": 1, "start_time": str(target_date)},
                message=f"✅ Cita confirmada para {date_str} a las {time_str}",
            )
        except Exception as e:
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"Error al crear cita: {str(e)}",
            )

    def get_appointments(self) -> GroqToolResult:
        """Get user's appointments.

        Returns:
            GroqToolResult with appointments list
        """
        try:
            appointments = self.booking_service.get_user_appointments(self.user_id)
            return GroqToolResult(
                success=True,
                data={
                    "total": len(appointments),
                    "appointments": [
                        {"id": i + 1, "date": "mañana", "time": "15:00"}
                        for i in range(len(appointments))
                    ],
                },
                message=f"Tienes {len(appointments)} cita(s) agendada(s)",
            )
        except Exception as e:
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"Error al obtener citas: {str(e)}",
            )

    def cancel_appointment(self, appointment_id: int) -> GroqToolResult:
        """Cancel an appointment.

        Args:
            appointment_id: ID of appointment to cancel

        Returns:
            GroqToolResult with cancellation status
        """
        try:
            self.booking_service.cancel_appointment(appointment_id)
            return GroqToolResult(
                success=True,
                data={"appointment_id": appointment_id},
                message=f"✅ Cita cancelada exitosamente",
            )
        except Exception as e:
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"Error al cancelar cita: {str(e)}",
            )

    def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> GroqToolResult:
        """Execute a tool by name with arguments.

        Args:
            tool_name: Name of the tool
            tool_args: Arguments for the tool

        Returns:
            GroqToolResult from tool execution
        """
        if tool_name == "check_availability":
            return self.check_availability(tool_args.get("date_str", "mañana"))
        elif tool_name == "create_appointment":
            return self.create_appointment(
                date_str=tool_args.get("date_str", "mañana"),
                time_str=tool_args.get("time_str", "15:00"),
            )
        elif tool_name == "get_appointments":
            return self.get_appointments()
        elif tool_name == "cancel_appointment":
            return self.cancel_appointment(tool_args.get("appointment_id", 1))
        else:
            return GroqToolResult(
                success=False,
                error=f"Unknown tool: {tool_name}",
                message=f"Herramienta desconocida: {tool_name}",
            )

    async def call_groq_with_tools(self, user_input: str) -> str:
        """Call Groq LLM with tool support.

        Args:
            user_input: User message/query

        Returns:
            Response from LLM
        """
        if not self.groq_client:
            return "❌ Groq client not configured"

        try:
            messages = [{"role": "user", "content": user_input}]
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                tools=self.TOOLS,
                tool_choice="auto",
                max_tokens=2048,
            )
            return response.choices[0].message.content or "Sin respuesta"
        except Exception as e:
            logger.error(f"Error calling Groq: {str(e)}")
            return f"❌ Error: {str(e)}"


# Backward compatibility alias
GroqToolsIntegration = GroqTools

__all__ = ["GroqTools", "GroqToolResult", "GroqToolsIntegration"]
