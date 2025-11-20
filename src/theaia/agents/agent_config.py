"""
Agent Configuration System for THEA-IA.

Modern configuration management for agents including
intent mapping, priority, metadata, and dynamic features.

Version: v0.16.0 (H03)
Author: Álvaro Fernández Mota
Date: 20 Nov 2025
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class AgentPriority(Enum):
    """Agent execution priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class AgentConfig:
    """
    Configuration for an agent.
    
    Attributes:
        name: Agent identifier (e.g., "agenda", "note")
        display_name: Human-readable name
        description: Agent purpose description
        intents: List of intents this agent handles
        priority: Execution priority
        enabled: Whether agent is active
        requires_database: Database access requirement
        max_context_length: Maximum conversation turns to keep
        timeout_seconds: Operation timeout
        metadata: Additional configuration data
    """
    name: str
    display_name: str
    description: str
    intents: List[str]
    priority: AgentPriority = AgentPriority.MEDIUM
    enabled: bool = True
    requires_database: bool = True
    max_context_length: int = 10
    timeout_seconds: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.name:
            raise ValueError("Agent name cannot be empty")
        if not self.intents:
            raise ValueError(f"Agent {self.name} must handle at least one intent")
        if not self.display_name:
            self.display_name = self.name.title()
    
    def handles_intent(self, intent: str) -> bool:
        """Check if agent handles given intent."""
        return intent.lower() in [i.lower() for i in self.intents]
    
    def add_intent(self, intent: str) -> None:
        """Add new intent to agent."""
        if not self.handles_intent(intent):
            self.intents.append(intent)
    
    def remove_intent(self, intent: str) -> None:
        """Remove intent from agent."""
        self.intents = [i for i in self.intents if i.lower() != intent.lower()]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'intents': self.intents,
            'priority': self.priority.name,
            'enabled': self.enabled,
            'requires_database': self.requires_database,
            'max_context_length': self.max_context_length,
            'timeout_seconds': self.timeout_seconds,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentConfig":
        """Create config from dictionary."""
        priority_str = data.get('priority', 'MEDIUM')
        priority = AgentPriority[priority_str] if priority_str in AgentPriority.__members__ else AgentPriority.MEDIUM
        
        return cls(
            name=data['name'],
            display_name=data.get('display_name', data['name'].title()),
            description=data.get('description', ''),
            intents=data.get('intents', []),
            priority=priority,
            enabled=data.get('enabled', True),
            requires_database=data.get('requires_database', True),
            max_context_length=data.get('max_context_length', 10),
            timeout_seconds=data.get('timeout_seconds', 30),
            metadata=data.get('metadata', {})
        )


# ==================== PREDEFINED CONFIGURATIONS ====================

AGENDA_CONFIG = AgentConfig(
    name="agenda",
    display_name="Agenda Agent",
    description="Manages calendar events and appointments",
    intents=["create_event", "list_events", "edit_event", "delete_event", "evento", "cita"],
    priority=AgentPriority.HIGH,
    requires_database=True,
    max_context_length=15,
    timeout_seconds=45,
    metadata={
        "supports_recurring": True,
        "timezone_aware": True,
        "conflict_detection": True
    }
)

NOTE_CONFIG = AgentConfig(
    name="note",
    display_name="Note Agent",
    description="Creates and manages notes with tags and search",
    intents=["create_note", "list_notes", "search_notes", "edit_note", "delete_note", "nota", "apuntar"],
    priority=AgentPriority.MEDIUM,
    requires_database=True,
    max_context_length=10,
    timeout_seconds=30,
    metadata={
        "supports_tags": True,
        "full_text_search": True,
        "supports_categories": True
    }
)

REMINDER_CONFIG = AgentConfig(
    name="reminder",
    display_name="Reminder Agent",
    description="Manages reminders and alerts",
    intents=["create_reminder", "list_reminders", "edit_reminder", "delete_reminder", "recordatorio", "recordar"],
    priority=AgentPriority.HIGH,
    requires_database=True,
    max_context_length=10,
    timeout_seconds=30,
    metadata={
        "supports_recurring": True,
        "location_based": True,
        "priority_levels": True
    }
)

QUERY_CONFIG = AgentConfig(
    name="query",
    display_name="Query Agent",
    description="Answers questions about user data",
    intents=["query", "search", "ask", "consulta", "pregunta", "buscar"],
    priority=AgentPriority.MEDIUM,
    requires_database=True,
    max_context_length=5,
    timeout_seconds=20,
    metadata={
        "supports_analytics": True,
        "natural_language": True
    }
)

HELP_CONFIG = AgentConfig(
    name="help",
    display_name="Help Agent",
    description="Provides help and guidance",
    intents=["help", "ayuda", "tutorial", "guide"],
    priority=AgentPriority.LOW,
    requires_database=False,
    max_context_length=3,
    timeout_seconds=15,
    metadata={
        "interactive_tutorial": True,
        "command_list": True
    }
)

FALLBACK_CONFIG = AgentConfig(
    name="fallback",
    display_name="Fallback Agent",
    description="Handles unknown intents gracefully",
    intents=["fallback", "unknown", "desconocido"],
    priority=AgentPriority.CRITICAL,
    requires_database=False,
    max_context_length=3,
    timeout_seconds=10,
    metadata={
        "always_available": True,
        "suggests_alternatives": True
    }
)

SCHEDULE_CONFIG = AgentConfig(
    name="schedule",
    display_name="Schedule Agent",
    description="Manages schedules and planning",
    intents=["schedule", "plan", "planificar", "horario"],
    priority=AgentPriority.MEDIUM,
    requires_database=True,
    max_context_length=10,
    timeout_seconds=30,
    metadata={
        "weekly_planning": True,
        "optimization": True,
        "conflict_resolution": True
    }
)


# ==================== AGENT CONFIGS REGISTRY ====================

DEFAULT_AGENT_CONFIGS: Dict[str, AgentConfig] = {
    "agenda": AGENDA_CONFIG,
    "note": NOTE_CONFIG,
    "reminder": REMINDER_CONFIG,
    "query": QUERY_CONFIG,
    "help": HELP_CONFIG,
    "fallback": FALLBACK_CONFIG,
    "schedule": SCHEDULE_CONFIG
}


# ==================== UTILITY FUNCTIONS ====================

def get_agent_config(agent_name: str) -> Optional[AgentConfig]:
    """
    Get agent configuration by name.
    
    Args:
        agent_name: Agent identifier (case-insensitive)
        
    Returns:
        AgentConfig if found, None otherwise
    """
    return DEFAULT_AGENT_CONFIGS.get(agent_name.lower())


def get_config_for_intent(intent: str) -> Optional[AgentConfig]:
    """
    Get agent config that handles given intent.
    
    Args:
        intent: Intent string to match (case-insensitive)
        
    Returns:
        AgentConfig if found, None otherwise (prioritized by priority level)
    """
    matching_configs = []
    
    for config in DEFAULT_AGENT_CONFIGS.values():
        if config.enabled and config.handles_intent(intent):
            matching_configs.append(config)
    
    if not matching_configs:
        return None
    
    # Return highest priority config
    return max(matching_configs, key=lambda c: c.priority.value)


def list_all_intents() -> List[str]:
    """Get sorted list of all supported intents."""
    intents = []
    for config in DEFAULT_AGENT_CONFIGS.values():
        if config.enabled:
            intents.extend(config.intents)
    return sorted(set(intents))


def list_enabled_agents() -> List[str]:
    """Get list of enabled agent names."""
    return [name for name, config in DEFAULT_AGENT_CONFIGS.items() if config.enabled]


def get_agents_by_priority(priority: AgentPriority) -> List[AgentConfig]:
    """Get all agents with specific priority level."""
    return [
        config for config in DEFAULT_AGENT_CONFIGS.values()
        if config.enabled and config.priority == priority
    ]
