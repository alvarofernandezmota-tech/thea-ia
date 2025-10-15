# src/theaia/core/fsm/states/agent_states.py

from typing import Dict, List, Any, Optional
from enum import Enum

class AgentType(Enum):
    """Tipos de agentes disponibles en Thea IA 2.0"""
    
    NOTE_AGENT = "NoteAgent"
    AGENDA_AGENT = "AgendaAgent"
    REMINDER_AGENT = "ReminderAgent"
    EVENT_AGENT = "EventAgent"
    HELP_AGENT = "HelpAgent"
    QUERY_AGENT = "QueryAgent"
    SCHEDULER_AGENT = "SchedulerAgent"
    FALLBACK_AGENT = "FallbackAgent"

class AgentStateMapping:
    """Mapeo de intents a agentes y sus estados iniciales"""
    
    INTENT_TO_AGENT = {
        # Notas y documentación
        "notas": AgentType.NOTE_AGENT,
        "note": AgentType.NOTE_AGENT,
        "apunte": AgentType.NOTE_AGENT,
        "documentar": AgentType.NOTE_AGENT,
        
        # Agenda y citas
        "agenda": AgentType.AGENDA_AGENT,
        "cita": AgentType.AGENDA_AGENT,
        "agendar": AgentType.AGENDA_AGENT,
        "reunion": AgentType.AGENDA_AGENT,
        "meeting": AgentType.AGENDA_AGENT,
        
        # Recordatorios y alertas
        "recordatorio": AgentType.REMINDER_AGENT,
        "recordar": AgentType.REMINDER_AGENT,
        "avisar": AgentType.REMINDER_AGENT,
        "alerta": AgentType.REMINDER_AGENT,
        
        # Eventos
        "event": AgentType.EVENT_AGENT,
        "evento": AgentType.EVENT_AGENT,
        
        # Ayuda
        "help": AgentType.HELP_AGENT,
        "ayuda": AgentType.HELP_AGENT,
        
        # Consultas
        "query": AgentType.QUERY_AGENT,
        "consulta": AgentType.QUERY_AGENT,
        "pregunta": AgentType.QUERY_AGENT,
        
        # Programación
        "scheduler": AgentType.SCHEDULER_AGENT,
        "programar": AgentType.SCHEDULER_AGENT,
        "schedule": AgentType.SCHEDULER_AGENT,
        
        # Fallback
        "fallback": AgentType.FALLBACK_AGENT,
        "unknown": AgentType.FALLBACK_AGENT
    }
    
    AGENT_INITIAL_STATES = {
        AgentType.NOTE_AGENT: "awaiting_note_text",
        AgentType.AGENDA_AGENT: "awaiting_date_time", 
        AgentType.REMINDER_AGENT: "awaiting_reminder_details",
        AgentType.EVENT_AGENT: "awaiting_event_details",
        AgentType.HELP_AGENT: "showing_help",
        AgentType.QUERY_AGENT: "processing_query",
        AgentType.SCHEDULER_AGENT: "awaiting_schedule_details",
        AgentType.FALLBACK_AGENT: "processing_fallback"
    }
    
    AGENT_CLASS_NAMES = {
        AgentType.NOTE_AGENT: "NoteAgent",
        AgentType.AGENDA_AGENT: "AgendaAgent",
        AgentType.REMINDER_AGENT: "ReminderAgent", 
        AgentType.EVENT_AGENT: "EventAgent",
        AgentType.HELP_AGENT: "HelpAgent",
        AgentType.QUERY_AGENT: "QueryAgent",
        AgentType.SCHEDULER_AGENT: "SchedulerAgent",
        AgentType.FALLBACK_AGENT: "FallbackAgent"
    }
    
    @classmethod
    def get_agent_for_intent(cls, intent: str) -> AgentType:
        """Obtiene el agente apropiado para un intent"""
        return cls.INTENT_TO_AGENT.get(intent.lower(), AgentType.FALLBACK_AGENT)
    
    @classmethod
    def get_initial_state(cls, agent_type: AgentType) -> str:
        """Obtiene el estado inicial de un agente"""
        return cls.AGENT_INITIAL_STATES.get(agent_type, "initial")
    
    @classmethod
    def get_class_name(cls, agent_type: AgentType) -> str:
        """Obtiene el nombre de clase de un agente"""
        return cls.AGENT_CLASS_NAMES.get(agent_type, "FallbackAgent")

class AgentCapabilities:
    """Define las capacidades de cada agente"""
    
    CAPABILITIES = {
        AgentType.NOTE_AGENT: {
            "actions": ["create_note", "edit_note", "delete_note", "list_notes"],
            "inputs": ["text", "title", "tags"],
            "outputs": ["confirmation", "note_content", "note_list"],
            "features": ["text_storage", "search", "categorization"]
        },
        
        AgentType.AGENDA_AGENT: {
            "actions": ["create_appointment", "edit_appointment", "delete_appointment", "list_appointments"],
            "inputs": ["date", "time", "description", "participants", "location"],
            "outputs": ["confirmation", "appointment_details", "calendar_view"],
            "features": ["calendar_integration", "reminders", "participant_management"]
        },
        
        AgentType.REMINDER_AGENT: {
            "actions": ["create_reminder", "edit_reminder", "delete_reminder", "list_reminders"],
            "inputs": ["datetime", "message", "frequency", "priority"],
            "outputs": ["confirmation", "reminder_details", "notification"],
            "features": ["time_based_alerts", "recurring_reminders", "priority_levels"]
        },
        
        AgentType.EVENT_AGENT: {
            "actions": ["create_event", "edit_event", "delete_event", "list_events"],
            "inputs": ["title", "date", "time", "location", "description"],
            "outputs": ["confirmation", "event_details", "event_list"],
            "features": ["event_management", "location_handling", "duration_tracking"]
        },
        
        AgentType.HELP_AGENT: {
            "actions": ["show_help", "explain_feature", "guide_user"],
            "inputs": ["topic", "context"],
            "outputs": ["help_text", "instructions", "examples"],
            "features": ["contextual_help", "feature_explanation", "usage_guidance"]
        },
        
        AgentType.QUERY_AGENT: {
            "actions": ["process_question", "search_information", "provide_answer"],
            "inputs": ["question", "context", "filters"],
            "outputs": ["answer", "search_results", "clarification"],
            "features": ["information_retrieval", "context_understanding", "answer_formatting"]
        },
        
        AgentType.SCHEDULER_AGENT: {
            "actions": ["schedule_task", "reschedule", "find_availability"],
            "inputs": ["task", "constraints", "preferences", "duration"],
            "outputs": ["schedule", "availability", "conflicts"],
            "features": ["automatic_scheduling", "conflict_detection", "preference_matching"]
        },
        
        AgentType.FALLBACK_AGENT: {
            "actions": ["handle_unknown", "suggest_alternatives", "escalate"],
            "inputs": ["any_input"],
            "outputs": ["fallback_response", "suggestions", "escalation"],
            "features": ["error_handling", "suggestion_generation", "graceful_degradation"]
        }
    }
    
    @classmethod
    def get_capabilities(cls, agent_type: AgentType) -> Dict[str, List[str]]:
        """Obtiene las capacidades de un agente"""
        return cls.CAPABILITIES.get(agent_type, {})
    
    @classmethod
    def can_handle_action(cls, agent_type: AgentType, action: str) -> bool:
        """Verifica si un agente puede manejar una acción"""
        capabilities = cls.get_capabilities(agent_type)
        return action in capabilities.get("actions", [])

# Exportaciones
__all__ = [
    'AgentType',
    'AgentStateMapping',
    'AgentCapabilities'
]
