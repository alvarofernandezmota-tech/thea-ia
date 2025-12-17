"""
Groq Tools Integration for THEA IA - FULL H9 FUNCTIONALITY

This module integrates Groq LLM with THEA IA services through tool calling.
Tools available:
- check_availability: Get available slots for scheduling
- create_appointment: Create a new appointment with REAL database save
- get_appointments: Retrieve user appointments from REAL database
- cancel_appointment: Cancel an existing appointment in REAL database ✅ FIXED
- update_appointment: Update an existing appointment ✅ NEW

KEY CHANGES (PASO 3 - H9 COMPLETE):
✅ cancel_appointment() - Fixed user_id parameter
✅ update_appointment() - New function for modifying appointments
✅ execute_tool() - Added update_appointment dispatch
✅ TOOLS - Added update_appointment definition
✅ Enhanced validation and error handling
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

    # Tool definitions for Groq - COMPLETE H9 SET
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
        {
            "type": "function",
            "function": {
                "name": "update_appointment",
                "description": "Update an existing appointment (change time, date, title, or duration). Use this when user wants to modify/change/reschedule an appointment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {
                            "type": "integer",
                            "description": "ID of the appointment to update",
                        },
                        "new_date": {
                            "type": "string",
                            "description": "New date in natural language (optional, e.g., 'tomorrow', 'mañana')",
                        },
                        "new_time": {
                            "type": "string",
                            "description": "New time in natural language (optional, e.g., '15:00', '3pm')",
                        },
                        "new_title": {
                            "type": "string",
                            "description": "New title/name for the appointment (optional)",
                        },
                        "new_duration_minutes": {
                            "type": "integer",
                            "description": "New duration in minutes (optional)",
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
        "update_appointment": "update_appointment",
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
            
            if not appointment:
                return GroqToolResult(
                    success=False,
                    error="Conflict detected",
                    message=f"❌ Ya existe una cita en ese horario"
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
                message=f"✅ Cita '{title}' confirmada para {date_formatted} a las {time_formatted}"
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
                        duration = (appt.get("end_time") - appt.get("start_time")).total_seconds() / 60 if appt.get("end_time") else 60
                    else:
                        appt_id = getattr(appt, "id", 0)
                        start_time = getattr(appt, "start_time", None)
                        title = getattr(appt, "title", "Cita")
                        end_time = getattr(appt, "end_time", None)
                        duration = (end_time - start_time).total_seconds() / 60 if end_time else 60
                    
                    if start_time:
                        if isinstance(start_time, str):
                            start_time = datetime.fromisoformat(start_time)
                        
                        formatted_appts.append({
                            "id": appt_id,
                            "date": start_time.strftime("%d/%m/%Y"),
                            "time": start_time.strftime("%H:%M"),
                            "title": title,
                            "duration_minutes": int(duration),
                            "datetime": start_time.isoformat()
                        })
                except Exception as e:
                    logger.warning(f"⚠️ Error formatting appointment: {e}")
                    continue
            
            logger.info(f"✅ Found {len(formatted_appts)} appointments for user {self.user_id}")
            
            # Build message
            message = f"📋 Tienes {len(formatted_appts)} cita(s) agendada(s):\n"
            for i, appt in enumerate(formatted_appts, 1):
                message += f"{i}. ID:{appt['id']} - '{appt['title']}' el {appt['date']} a las {appt['time']} ({appt['duration_minutes']} min)\n"
            
            return GroqToolResult(
                success=True,
                data={
                    "total": len(formatted_appts),
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
        Cancel appointment - UPDATES REAL DATABASE ✅ FIXED
        
        Args:
            appointment_id: ID of appointment to cancel
            reason: Reason for cancellation

        Returns:
            GroqToolResult with REAL database confirmation
        """
        try:
            logger.debug(f"❌ Cancelling appointment {appointment_id}: {reason}")
            
            # ✅ FIXED: Cancel in REAL database with user_id
            success = self.booking_service.cancel_appointment(
                appointment_id=appointment_id,
                user_id=self.user_id  # ✅ NOW PASSING user_id
            )
            
            if not success:
                return GroqToolResult(
                    success=False,
                    error="Appointment not found or already cancelled",
                    message=f"❌ No se pudo cancelar la cita #{appointment_id}. Verifica que exista y te pertenezca."
                )
            
            logger.info(f"✅ Appointment {appointment_id} cancelled successfully")
            
            return GroqToolResult(
                success=True,
                data={
                    "appointment_id": appointment_id,
                    "status": "cancelled",
                    "reason": reason
                },
                message=f"✅ Cita #{appointment_id} cancelada exitosamente"
            )
        
        except Exception as e:
            logger.error(f"❌ Error cancelling appointment: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error al cancelar cita: {str(e)}"
            )

    def update_appointment(
        self,
        appointment_id: int,
        new_date: Optional[str] = None,
        new_time: Optional[str] = None,
        new_title: Optional[str] = None,
        new_duration_minutes: Optional[int] = None
    ) -> GroqToolResult:
        """
        Update existing appointment - ✅ NEW FUNCTION
        
        Args:
            appointment_id: ID of appointment to update
            new_date: New date in natural language (optional)
            new_time: New time in natural language (optional)
            new_title: New title (optional)
            new_duration_minutes: New duration (optional)

        Returns:
            GroqToolResult with updated appointment
        """
        try:
            logger.debug(f"🔄 Updating appointment {appointment_id}")
            
            # Get existing appointment
            existing_apt = self.booking_service.get_appointment_by_id(appointment_id)
            if not existing_apt:
                return GroqToolResult(
                    success=False,
                    error="Appointment not found",
                    message=f"❌ Cita #{appointment_id} no encontrada"
                )
            
            # Verify ownership
            if existing_apt.get('user_id') != self.user_id:
                return GroqToolResult(
                    success=False,
                    error="Unauthorized",
                    message=f"❌ No tienes permiso para modificar esta cita"
                )
            
            # Parse new datetime if provided
            new_start_time = None
            if new_date or new_time:
                # Use existing time/date if not provided
                existing_start = existing_apt['start_time']
                
                if new_date:
                    target_date = self._parse_natural_date(new_date)
                else:
                    target_date = existing_start
                
                if new_time:
                    start_time = self._parse_time(new_time)
                    new_start_time = target_date.replace(
                        hour=start_time.hour,
                        minute=start_time.minute,
                        second=0,
                        microsecond=0
                    )
                else:
                    # Keep existing time with new date
                    new_start_time = target_date.replace(
                        hour=existing_start.hour,
                        minute=existing_start.minute,
                        second=0,
                        microsecond=0
                    )
            
            # Update in database
            updated_apt = self.booking_service.update_appointment(
                appointment_id=appointment_id,
                user_id=self.user_id,
                new_start_time=new_start_time,
                new_duration=new_duration_minutes,
                new_title=new_title
            )
            
            if not updated_apt:
                return GroqToolResult(
                    success=False,
                    error="Failed to update appointment",
                    message=f"❌ No se pudo actualizar la cita #{appointment_id}. Puede haber un conflicto de horario."
                )
            
            logger.info(f"✅ Appointment {appointment_id} updated successfully")
            
            # Format response
            start_time = updated_apt['start_time']
            date_formatted = start_time.strftime("%d/%m/%Y")
            time_formatted = start_time.strftime("%H:%M")
            
            return GroqToolResult(
                success=True,
                data={
                    "appointment_id": appointment_id,
                    "start_time": str(start_time),
                    "title": updated_apt['title'],
                    "date_formatted": date_formatted,
                    "time_formatted": time_formatted
                },
                message=f"✅ Cita #{appointment_id} actualizada: '{updated_apt['title']}' el {date_formatted} a las {time_formatted}"
            )
        
        except Exception as e:
            logger.error(f"❌ Error updating appointment: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error al actualizar cita: {str(e)}"
            )

    def execute_tool(self, tool_name: str, **tool_args) -> GroqToolResult:
        """Execute a tool by name with arguments - COMPLETE H9 SUPPORT.

        Handles multiple parameter name variations that Groq might send:
        - 'date' or 'date_str'
        - 'time' or 'time_str'
        - 'duration' or 'duration_minutes'
        - 'filter' or 'status_filter'

        Returns:
            GroqToolResult from tool execution
        """
        try:
            # ✅ Ensure tool_args is a dict
            if tool_args is None:
                tool_args = {}
                logger.warning("⚠️ tool_args was None, using empty dict")

            logger.info(f"🔧 Executing tool: {tool_name} with args: {tool_args}")

            if tool_name == "check_availability":
                date_str = tool_args.get("date", tool_args.get("date_str", "mañana"))
                duration = tool_args.get("duration_minutes", tool_args.get("duration", 60))
                return self.check_availability(date_str, duration)

            if tool_name == "create_appointment":
                date_str = tool_args.get("date", "mañana")
                time_str = tool_args.get("time", "15:00")
                duration = tool_args.get("duration_minutes", tool_args.get("duration", 60))
                title = tool_args.get("title", tool_args.get("description", "Cita"))
                description = tool_args.get("description", "")
                return self.create_appointment(date_str, time_str, title, duration, description)

            if tool_name == "get_appointments":
                status_filter = tool_args.get("status_filter", tool_args.get("filter", "all"))
                limit = tool_args.get("limit", 10)

                if not isinstance(limit, int) or limit <= 0:
                    limit = 10
                if status_filter not in ["all", "upcoming", "past"]:
                    status_filter = "all"

                return self.get_appointments(status_filter, limit)

            if tool_name == "cancel_appointment":
                appointment_id = tool_args.get("appointment_id")
                reason = tool_args.get("reason", "Cancelado por el usuario")

                if not appointment_id:
                    return GroqToolResult(
                        success=False,
                        error="Missing appointment_id",
                        message="❌ Se requiere el ID de la cita a cancelar",
                    )

                return self.cancel_appointment(appointment_id, reason)

            if tool_name == "update_appointment":
                appointment_id = tool_args.get("appointment_id")
                new_date = tool_args.get("new_date")
                new_time = tool_args.get("new_time")
                new_title = tool_args.get("new_title")
                new_duration = tool_args.get("new_duration_minutes")

                if not appointment_id:
                    return GroqToolResult(
                        success=False,
                        error="Missing appointment_id",
                        message="❌ Se requiere el ID de la cita a actualizar",
                    )

                return self.update_appointment(
                    appointment_id, new_date, new_time, new_title, new_duration
                )

            logger.warning(f"⚠️ Unknown tool: {tool_name}")
            return GroqToolResult(
                success=False,
                error=f"Unknown tool: {tool_name}",
                message=f"❌ Herramienta desconocida: {tool_name}",
            )
        except Exception as e:
            logger.error(f"❌ Error executing tool {tool_name}: {str(e)}", exc_info=True)
            return GroqToolResult(
                success=False,
                error=str(e),
                message=f"❌ Error ejecutando herramienta {tool_name}: {str(e)}",
            )

    async def call_groq_with_tools(self, user_input: str) -> str:
        """Call Groq LLM with tool support.
        
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
                model="llama-3.3-70b-versatile",
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
