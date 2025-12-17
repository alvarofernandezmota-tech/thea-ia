"""
Groq Tools Integration for THEA IA - PASO 2 ACTUALIZADO

This module integrates Groq LLM with THEA IA services through tool calling.
Tools available:
- check_availability: Get available slots for scheduling
- create_appointment: Create a new appointment with REAL database save
- get_appointments: Retrieve user appointments from REAL database
- cancel_appointment: Cancel an existing appointment in REAL database

KEY CHANGES (PASO 2):
✅ execute_tool() - Fixed parameter mapping
✅ check_availability() - Returns REAL slots from AvailabilityEngine
✅ create_appointment() - Saves to REAL database
✅ get_appointments() - Returns REAL data from database
✅ cancel_appointment() - Updates REAL database
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

    # Tool definitions for Groq - FIXED with correct parameter names
    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "check_availability",
                "description": "Check available time slots for scheduling appointments on a specific date. Returns real available slots from the calendar engine.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Target date in natural language (e.g., 'tomorrow', 'next monday', 'mañana', '25 de diciembre')",
                        },
                        "duration_minutes": {
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
                "description": "Create a new appointment/event and SAVE it to the real database. Returns confirmation with appointment ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date of appointment in natural language (e.g., 'tomorrow', 'next monday', 'mañana')",
                        },
                        "time": {
                            "type": "string",
                            "description": "Time of appointment in natural language (e.g., '9am', '14:30', '3pm', 'las 15:00')",
                        },
                        "title": {
                            "type": "string",
                            "description": "Title/name/description of the appointment",
                        },
                        "duration_minutes": {
                            "type": "integer",
                            "description": "Duration in minutes (default: 60)",
                            "default": 60,
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional additional details/description",
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
                "description": "Retrieve user's appointments from the real database with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status_filter": {
                            "type": "string",
                            "enum": ["upcoming", "past", "all"],
                            "description": "Filter appointments by status (default: all)",
                            "default": "all",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of appointments to return",
                            "default": 10,
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
                "description": "Cancel an existing appointment and update the real database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {
                            "type": "integer",
                            "description": "ID of the appointment to cancel",
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for cancellation (optional)",
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
            time_str: Time in natural language (e.g., '15:00', '3pm', 'las 3 de la tarde')

        Returns:
            Parsed time object
        """
        return self.availability_engine.parse_natural_time(time_str)

    def check_availability(
        self,
        date_str: str,
        duration_minutes: int = 60
    ) -> GroqToolResult:
        """
        Check available slots - RETURNS REAL DATA FROM AVAILABILITY ENGINE
        
        Args:
            date_str: Date in natural language
            duration_minutes: Duration of requested slot

        Returns:
            GroqToolResult with REAL available slots
        """
        try:
            logger.debug(f"🔍 Checking availability for {date_str} ({duration_minutes} min)")
            
            # Parse natural date
            target_date = self._parse_natural_date(date_str)
            logger.debug(f"📅 Parsed date: {target_date}")
            
            # Get REAL slots from AvailabilityEngine
            slots = self.availability_engine.get_available_slots(date=target_date, duration_minutes=duration_minutes)
            
            if not slots:
                logger.info(f"⚠️ No slots available for {date_str}")
                return GroqToolResult(
                    success=True,
                    data={"available_slots": [], "date": date_str},
                    message=f"⚠️ No hay horarios disponibles para {date_str}"
                )
            
            # Format slots as strings (HH:MM)
            slot_strs = [f"{slot.hour:02d}:{slot.minute:02d}" for slot in slots]
            logger.info(f"✅ Found {len(slot_strs)} slots for {date_str}: {slot_strs[:5]}")
            
            return GroqToolResult(
                success=True,
                data={
                    "available_slots": slot_strs,
                    "date": date_str,
                    "count": len(slot_strs)
                },
                message=f"✅ Horarios disponibles para {date_str}:\n{', '.join(slot_strs[:5])}" + 
                        (f"\n... y {len(slot_strs) - 5} más" if len(slot_strs) > 5 else "")
            )
        
        except Exception as e:
            logger.error(f"❌ Error checking availability: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error al verificar disponibilidad: {str(e)}"
            )

    def create_appointment(
        self,
        date_str: str,
        time_str: str,
        title: str = "Cita",
        duration_minutes: int = 60,
        description: str = ""
    ) -> GroqToolResult:
        """
        Create appointment - SAVES TO REAL DATABASE
        
        Args:
            date_str: Date in natural language
            time_str: Time in natural language
            title: Appointment title/description
            duration_minutes: Duration of appointment
            description: Additional description

        Returns:
            GroqToolResult with REAL database confirmation
        """
        try:
            logger.debug(f"📅 Creating appointment: {date_str} at {time_str}")
            
            # Parse natural date and time
            target_date = self._parse_natural_date(date_str)
            start_time = self._parse_time(time_str)
            
            # Combine date + time
            appointment_datetime = target_date.replace(
                hour=start_time.hour,
                minute=start_time.minute,
                second=0,
                microsecond=0
            )
            
            logger.debug(f"⏰ Combined datetime: {appointment_datetime}")
            
            # Create appointment in REAL database
            appointment = self.booking_service.create_appointment(
                user_id=self.user_id,
                start_time=appointment_datetime,
                duration_minutes=duration_minutes,
                title=title,
                description=description or "Cita agendada por THEA IA"
            )
            
            logger.info(f"✅ Appointment created: {appointment}")
            
            # Format response with REAL data
            date_formatted = target_date.strftime("%d/%m/%Y")
            time_formatted = f"{start_time.hour:02d}:{start_time.minute:02d}"
            
            return GroqToolResult(
                success=True,
                data={
                    "appointment_id": appointment.get("id", 1) if isinstance(appointment, dict) else 1,
                    "start_time": str(appointment_datetime),
                    "title": title,
                    "date_formatted": date_formatted,
                    "time_formatted": time_formatted
                },
                message=f"✅ Cita confirmada para {date_formatted} a las {time_formatted}"
            )
        
        except Exception as e:
            logger.error(f"❌ Error creating appointment: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error al crear cita: {str(e)}"
            )

    def get_appointments(
        self,
        status_filter: str = "all",
        limit: int = 10
    ) -> GroqToolResult:
        """
        Get appointments - RETURNS REAL DATA FROM DATABASE
        
        Args:
            status_filter: Filter type (all, upcoming, past)
            limit: Maximum appointments to return

        Returns:
            GroqToolResult with REAL appointments from database
        """
        try:
            logger.debug(f"📋 Getting appointments (filter={status_filter}, limit={limit})")
            
            # Get REAL appointments from database
            appointments = self.booking_service.get_user_appointments(self.user_id)
            
            if not appointments:
                logger.info(f"📋 No appointments found for user {self.user_id}")
                return GroqToolResult(
                    success=True,
                    data={"total": 0, "appointments": []},
                    message="📋 No tienes citas agendadas"
                )
            
            # Format appointments for response
            formatted_appts = []
            for appt in appointments[:limit]:
                try:
                    # Handle both dict and object formats
                    if isinstance(appt, dict):
                        appt_id = appt.get("id", 0)
                        start_time = appt.get("start_time")
                        title = appt.get("title", "Cita")
                    else:
                        appt_id = getattr(appt, "id", 0)
                        start_time = getattr(appt, "start_time", None)
                        title = getattr(appt, "title", "Cita")
                    
                    if start_time:
                        if isinstance(start_time, str):
                            start_time = datetime.fromisoformat(start_time)
                        
                        formatted_appts.append({
                            "id": appt_id,
                            "date": start_time.strftime("%d/%m/%Y"),
                            "time": start_time.strftime("%H:%M"),
                            "title": title,
                            "datetime": start_time.isoformat()
                        })
                except Exception as e:
                    logger.warning(f"⚠️ Error formatting appointment: {e}")
                    continue
            
            logger.info(f"✅ Found {len(formatted_appts)} appointments for user {self.user_id}")
            
            # Build message
            message = f"📋 Tienes {len(appointments)} cita(s) agendada(s):\n"
            for i, appt in enumerate(formatted_appts, 1):
                message += f"{i}. {appt['date']} a las {appt['time']}\n"
            
            return GroqToolResult(
                success=True,
                data={
                    "total": len(appointments),
                    "appointments": formatted_appts,
                    "user_id": self.user_id
                },
                message=message.strip()
            )
        
        except Exception as e:
            logger.error(f"❌ Error getting appointments: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error al obtener citas: {str(e)}"
            )

    def cancel_appointment(
        self,
        appointment_id: int,
        reason: str = "Cancelado por el usuario"
    ) -> GroqToolResult:
        """
        Cancel appointment - UPDATES REAL DATABASE
        
        Args:
            appointment_id: ID of appointment to cancel
            reason: Reason for cancellation

        Returns:
            GroqToolResult with REAL database confirmation
        """
        try:
            logger.debug(f"❌ Cancelling appointment {appointment_id}: {reason}")
            
            # Cancel in REAL database
            appointment = self.booking_service.cancel_appointment(appointment_id)
            
            logger.info(f"✅ Appointment {appointment_id} cancelled successfully")
            
            return GroqToolResult(
                success=True,
                data={
                    "appointment_id": appointment_id,
                    "status": "cancelled"
                },
                message=f"✅ Cita cancelada exitosamente"
            )
        
        except Exception as e:
            logger.error(f"❌ Error cancelling appointment: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error al cancelar cita: {str(e)}"
            )

    def execute_tool(self, tool_name: str, **tool_args) -> GroqToolResult:
        """
        Execute a tool by name with arguments - FIXED PARAMETER MAPPING
        
        Handles multiple parameter name variations that Groq might send:
        - 'date' or 'date_str'
        - 'time' or 'time_str'
        - 'duration' or 'duration_minutes'
        - 'filter' or 'status_filter'

        Args:
            tool_name: Name of the tool to execute
            **tool_args: Arguments for the tool (flexible parameter names)

        Returns:
            GroqToolResult from tool execution
        """
        try:
            logger.info(f"🔧 Executing tool: {tool_name} with args: {tool_args}")
            
            if tool_name == "check_availability":
                # Support both 'date' and 'date_str' parameter names
                date_str = tool_args.get("date", tool_args.get("date_str", "mañana"))
                duration = tool_args.get("duration_minutes", tool_args.get("duration", 60))
                return self.check_availability(date_str, duration)
            
            elif tool_name == "create_appointment":
                # Support flexible parameter names
                date_str = tool_args.get("date", "mañana")
                time_str = tool_args.get("time", "15:00")
                duration = tool_args.get("duration_minutes", tool_args.get("duration", 60))
                title = tool_args.get("title", tool_args.get("description", "Cita"))
                description = tool_args.get("description", "")
                return self.create_appointment(date_str, time_str, title, duration, description)
            
            elif tool_name == "get_appointments":
                # Support flexible parameter names
                status_filter = tool_args.get("status_filter", tool_args.get("filter", "all"))
                limit = tool_args.get("limit", 10)
                return self.get_appointments(status_filter, limit)
            
            elif tool_name == "cancel_appointment":
                # Support flexible parameter names
                appointment_id = tool_args.get("appointment_id")
                reason = tool_args.get("reason", "Cancelado por el usuario")
                
                if not appointment_id:
                    return GroqToolResult(
                        success=False,
                        error="Missing appointment_id",
                        message="❌ Se requiere el ID de la cita a cancelar"
                    )
                
                return self.cancel_appointment(appointment_id, reason)
            
            else:
                logger.warning(f"⚠️ Unknown tool: {tool_name}")
                return GroqToolResult(
                    success=False,
                    error=f"Unknown tool: {tool_name}",
                    message=f"❌ Herramienta desconocida: {tool_name}"
                )
        
        except Exception as e:
            logger.error(f"❌ Error executing tool {tool_name}: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error ejecutando herramienta {tool_name}: {str(e)}"
            )

    async def call_groq_with_tools(self, user_input: str) -> str:
        """
        Call Groq LLM with tool support.
        
        NOTE: This is kept for backward compatibility.
        BookingAgent + LLMClient.call_with_tools() is preferred.

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
            logger.error(f"❌ Error calling Groq: {str(e)}", exc_info=True)
            return f"❌ Error: {str(e)}"


# Backward compatibility alias
GroqToolsIntegration = GroqTools

__all__ = ["GroqTools", "GroqToolResult", "GroqToolsIntegration"]

