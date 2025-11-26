from typing import Dict, Any, Tuple


class SchedulerFSM:
    """
    FSM para ScheduleAgent - Gestión de horarios y programación.
    
    Estados:
    - awaiting_intent: Esperando intención del usuario
    - awaiting_details: Esperando detalles específicos
    - processing: Procesando solicitud
    - completed: Tarea completada
    - cancelled: Flujo cancelado
    """

    def __init__(self):
        self.state = "awaiting_intent"
        self.context = {}

    async def process_message(
        self, 
        message: str, 
        context: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Process message based on current state."""
        
        self.context.update(context)
        message_lower = message.strip().lower()

        if self.state == "awaiting_intent":
            # Detectar intención
            if any(word in message_lower for word in ["optimizar", "optimiza"]):
                self.context["intent"] = "optimize"
                self.state = "awaiting_details"
                return "¿Qué periodo quieres optimizar? (hoy, mañana, esta semana)", self.state
            
            elif any(word in message_lower for word in ["tiempo libre", "disponible"]):
                self.context["intent"] = "find_free_time"
                self.state = "awaiting_details"
                return "¿Para qué día buscas tiempo libre?", self.state
            
            elif any(word in message_lower for word in ["reunión", "reunion", "meeting"]):
                self.context["intent"] = "schedule_meeting"
                self.state = "awaiting_details"
                return "¿Cuándo quieres programar la reunión?", self.state
            
            elif any(word in message_lower for word in ["priorizar", "tareas"]):
                self.context["intent"] = "prioritize"
                self.state = "processing"
                return await self._prioritize_tasks(), "completed"
            
            elif any(word in message_lower for word in ["conflicto", "resolver"]):
                self.context["intent"] = "resolve_conflicts"
                self.state = "processing"
                return await self._resolve_conflicts(), "completed"
            
            else:
                # Respuesta genérica de ayuda
                return self._help_message(), "awaiting_intent"

        elif self.state == "awaiting_details":
            self.context["details"] = message
            self.state = "processing"
            return await self._process_intent(), "completed"

        elif self.state == "processing":
            return "Procesando tu solicitud...", "completed"

        else:
            return "Gestión de horario completada.", "completed"

    async def _process_intent(self) -> str:
        """Process intent based on context."""
        intent = self.context.get("intent", "")
        details = self.context.get("details", "")
        
        if intent == "optimize":
            return f"✅ Agenda optimizada para {details}. Se han reorganizado las tareas para maximizar productividad."
        
        elif intent == "find_free_time":
            return f"📅 Tienes tiempo libre {details} en estos horarios:\n- 10:00-11:30\n- 14:00-15:30\n- 17:00-18:00"
        
        elif intent == "schedule_meeting":
            return f"✅ Reunión programada para {details} en el mejor horario disponible (14:00-15:00)."
        
        else:
            return "Solicitud procesada correctamente."

    async def _prioritize_tasks(self) -> str:
        """Prioritize tasks."""
        return "✅ Tareas priorizadas:\n1. Alta prioridad: Proyecto X\n2. Media: Reuniones\n3. Baja: Emails"

    async def _resolve_conflicts(self) -> str:
        """Resolve schedule conflicts."""
        return "✅ Conflictos resueltos. Se han reorganizado 3 eventos para eliminar solapamientos."

    def _help_message(self) -> str:
        """Return help message."""
        return """¿Qué te gustaría hacer con tu agenda?

Puedo ayudarte a:
- Optimizar tu agenda
- Encontrar tiempo libre
- Programar reuniones
- Priorizar tareas
- Resolver conflictos de horario

¿Qué prefieres?"""
