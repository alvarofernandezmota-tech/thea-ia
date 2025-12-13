"""Groq Tools Integration for THEA IA.

This module integrates Groq LLM with THEA IA services through tool calling.
Tools available:
- check_availability: Get available slots for scheduling
- create_appointment: Create a new appointment
- get_appointments: Retrieve user appointments
- cancel_appointment: Cancel an existing appointment
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from groq import Groq

from theaia.services.availability_engine import AvailabilityEngine
from theaia.services.booking_service import BookingService
from theaia.services.user_service import UserService

logger = logging.getLogger(__name__)


class GroqToolsIntegration:
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

    def __init__(
        self,
        groq_client: Groq,
        user_service: UserService,
        booking_service: BookingService,
        availability_engine: AvailabilityEngine,
    ):
        """Initialize Groq Tools Integration.

        Args:
            groq_client: Groq API client
            user_service: UserService instance for user operations
            booking_service: BookingService instance for appointments
            availability_engine: AvailabilityEngine for slot management
        """
        self.groq_client = groq_client
        self.user_service = user_service
        self.booking_service = booking_service
        self.availability_engine = availability_engine

    async def call_groq_with_tools(
        self, user_input: str, user_id: int
    ) -> str:
        """Call Groq LLM with tool support and execute requested tools.

        Args:
            user_input: User message/query
            user_id: User ID from Telegram

        Returns:
            Final response from LLM after tool execution
        """
        try:
            # Get user for context
            user = self.user_service.get_user(user_id)
            if not user:
                return "❌ Usuario no encontrado. Por favor, usa /start primero."

            # System prompt with user context
            system_prompt = f"""
Eres THEA IA, un asistente inteligente para agendamiento de citas.
Detalles del usuario:
- Nombre: {user.get('first_name', '')} {user.get('last_name', '')}
- Zona horaria: {user.get('timezone', 'UTC')}
- ID: {user_id}

Tu rol:
1. Entender las necesidades del usuario sobre citas/calendario
2. Usar las herramientas disponibles para ayudar (check availability, crear citas, etc.)
3. Ser conversacional y amable
4. Si el usuario quiere ver disponibilidad, usa check_availability
5. Si quiere agendar, usa create_appointment
6. Si quiere ver sus citas, usa get_appointments
7. Si quiere cancelar, usa cancel_appointment

Siempre responde en el idioma del usuario (preferiblemente español).
Sé conciso pero informativo.
            """

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ]

            # Initial call to Groq with tools
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                tools=self.TOOLS,
                tool_choice="auto",
                max_tokens=2048,
            )

            # Process response and handle tool calls
            assistant_message = response.choices[0].message
            messages.append({"role": "assistant", "content": assistant_message})

            # Handle tool calls if any
            if assistant_message.tool_calls:
                tool_results = []

                for tool_call in assistant_message.tool_calls:
                    logger.info(
                        f"Tool call: {tool_call.function.name} with args: {tool_call.function.arguments}"
                    )

                    # Parse tool arguments
                    try:
                        tool_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        tool_args = tool_call.function.arguments

                    # Execute tool
                    tool_result = await self._execute_tool(
                        tool_call.function.name, tool_args, user_id
                    )
                    tool_results.append(
                        {
                            "type": "tool",
                            "name": tool_call.function.name,
                            "content": json.dumps(tool_result)
                            if isinstance(tool_result, (dict, list))
                            else str(tool_result),
                        }
                    )

                # Add tool results to messages
                messages.append({"role": "user", "content": tool_results})

                # Get final response from LLM
                final_response = self.groq_client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=messages,
                    max_tokens=2048,
                )

                return final_response.choices[0].message.content
            else:
                # No tool calls, return direct response
                return assistant_message.content

        except Exception as e:
            logger.error(f"Error in Groq tools integration: {str(e)}", exc_info=True)
            return f"❌ Error procesando tu solicitud: {str(e)}"

    async def _execute_tool(
        self, tool_name: str, tool_args: Dict[str, Any], user_id: int
    ) -> Any:
        """Execute a tool and return result.

        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments for the tool
            user_id: User ID from Telegram

        Returns:
            Result from tool execution
        """
        try:
            if tool_name == "check_availability":
                return await self._tool_check_availability(tool_args, user_id)
            elif tool_name == "create_appointment":
                return await self._tool_create_appointment(tool_args, user_id)
            elif tool_name == "get_appointments":
                return await self._tool_get_appointments(tool_args, user_id)
            elif tool_name == "cancel_appointment":
                return await self._tool_cancel_appointment(tool_args, user_id)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {"error": str(e)}

    async def _tool_check_availability(
        self, args: Dict[str, Any], user_id: int
    ) -> Dict[str, Any]:
        """Check available slots for scheduling.

        Args:
            args: Tool arguments with 'date' and optional 'duration'
            user_id: User ID

        Returns:
            Dictionary with available slots
        """
        try:
            date_str = args.get("date", "today")
            duration = args.get("duration", 60)

            # Parse natural language date
            target_date = self.availability_engine.parse_natural_date(date_str)

            # Get available slots
            slots = self.availability_engine.get_available_slots(
                user_id=user_id, target_date=target_date, slot_duration=duration
            )

            if not slots:
                return {
                    "status": "no_slots",
                    "message": f"No hay slots disponibles para {date_str}",
                }

            return {
                "status": "success",
                "date": date_str,
                "duration_minutes": duration,
                "available_slots": [
                    {
                        "start_time": slot["start"],
                        "end_time": slot["end"],
                        "formatted": f"{slot['start'].strftime('%H:%M')} - {slot['end'].strftime('%H:%M')}",
                    }
                    for slot in slots[:5]  # Return top 5 slots
                ],
            }
        except Exception as e:
            return {"error": str(e)}

    async def _tool_create_appointment(
        self, args: Dict[str, Any], user_id: int
    ) -> Dict[str, Any]:
        """Create a new appointment.

        Args:
            args: Tool arguments with 'date', 'time', 'title', optional 'duration', 'description'
            user_id: User ID

        Returns:
            Dictionary with creation result
        """
        try:
            date_str = args.get("date", "today")
            time_str = args.get("time")
            title = args.get("title")
            duration = args.get("duration", 60)
            description = args.get("description", "")

            if not time_str or not title:
                return {"error": "Falta 'time' o 'title' en los argumentos"}

            # Parse date and time
            target_date = self.availability_engine.parse_natural_date(date_str)
            target_time = self.availability_engine.parse_natural_time(time_str)

            # Combine date and time
            start_datetime = datetime.combine(
                target_date.date(), target_time.time()
            )
            end_datetime = start_datetime + (
                datetime.timedelta(minutes=duration)
                - datetime.timedelta(hours=start_datetime.hour, minutes=start_datetime.minute)
            )
            end_datetime = start_datetime + datetime.timedelta(minutes=duration)

            # Check for conflicts
            if self.booking_service.check_conflict(user_id, start_datetime, end_datetime):
                return {
                    "error": "Ya hay una cita en ese horario",
                    "status": "conflict",
                }

            # Create appointment
            appointment = self.booking_service.create_appointment(
                user_id=user_id,
                title=title,
                start_time=start_datetime,
                end_time=end_datetime,
                description=description,
            )

            return {
                "status": "success",
                "appointment_id": str(appointment["id"]),
                "message": f"✅ Cita agendada: {title} el {start_datetime.strftime('%d de %B a las %H:%M')}",
                "details": appointment,
            }
        except Exception as e:
            return {"error": str(e)}

    async def _tool_get_appointments(
        self, args: Dict[str, Any], user_id: int
    ) -> Dict[str, Any]:
        """Retrieve user appointments.

        Args:
            args: Tool arguments with optional 'filter' (upcoming/past/all)
            user_id: User ID

        Returns:
            Dictionary with appointments list
        """
        try:
            filter_type = args.get("filter", "upcoming")

            if filter_type == "upcoming":
                appointments = self.booking_service.get_upcoming_appointments(user_id)
                label = "Próximas"
            elif filter_type == "past":
                appointments = self.booking_service.get_past_appointments(user_id)
                label = "Pasadas"
            else:
                # Get all
                upcoming = self.booking_service.get_upcoming_appointments(user_id)
                past = self.booking_service.get_past_appointments(user_id)
                appointments = upcoming + past
                label = "Todas"

            if not appointments:
                return {
                    "status": "empty",
                    "message": f"No hay citas {label.lower()}",
                }

            return {
                "status": "success",
                "count": len(appointments),
                "filter": filter_type,
                "appointments": [
                    {
                        "id": str(apt["id"]),
                        "title": apt["title"],
                        "start_time": apt["start_time"].isoformat()
                        if isinstance(apt["start_time"], datetime)
                        else apt["start_time"],
                        "end_time": apt["end_time"].isoformat()
                        if isinstance(apt["end_time"], datetime)
                        else apt["end_time"],
                        "status": apt.get("status", "scheduled"),
                    }
                    for apt in appointments[:10]  # Limit to 10
                ],
            }
        except Exception as e:
            return {"error": str(e)}

    async def _tool_cancel_appointment(
        self, args: Dict[str, Any], user_id: int
    ) -> Dict[str, Any]:
        """Cancel an appointment.

        Args:
            args: Tool arguments with 'appointment_id' and optional 'reason'
            user_id: User ID

        Returns:
            Dictionary with cancellation result
        """
        try:
            appointment_id = args.get("appointment_id")
            reason = args.get("reason", "User requested cancellation")

            if not appointment_id:
                return {"error": "Falta 'appointment_id'"}

            # Convert to UUID if string
            if isinstance(appointment_id, str):
                appointment_id = UUID(appointment_id)

            # Cancel appointment
            result = self.booking_service.cancel_appointment(
                appointment_id=appointment_id, reason=reason
            )

            if result["success"]:
                return {
                    "status": "success",
                    "message": f"✅ Cita cancelada exitosamente",
                    "details": result,
                }
            else:
                return {
                    "status": "error",
                    "message": result.get("message", "Error al cancelar la cita"),
                }
        except Exception as e:
            return {"error": str(e)}
