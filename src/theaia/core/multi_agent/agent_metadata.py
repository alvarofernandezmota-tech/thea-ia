"""
Agent Metadata - H07.1
Metadata structure for agent registration and discovery
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Set, Optional, Any
import uuid


class AgentStatus(Enum):
    """Agent health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"


class AgentCapability(Enum):
    """Agent capabilities for discovery"""
    CALENDAR_MANAGEMENT = "calendar_management"
    EVENT_CREATION = "event_creation"
    EVENT_QUERY = "event_query"
    NOTE_MANAGEMENT = "note_management"
    REMINDER_MANAGEMENT = "reminder_management"
    NATURAL_LANGUAGE_PROCESSING = "nlp"
    CONTEXT_MANAGEMENT = "context_management"
    USER_MANAGEMENT = "user_management"
    FALLBACK = "fallback"
    HELP = "help"


@dataclass
class PerformanceMetrics:
    """Performance metrics for an agent"""
    average_response_time: float = 0.0  # seconds
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    last_request_time: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests
    
    @property
    def error_rate(self) -> float:
        """Calculate error rate"""
        return 1.0 - self.success_rate


@dataclass
class AgentMetadata:
    """
    Complete metadata for an agent in the registry
    """
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: str = ""  # e.g., "AgendaAgent", "NoteAgent"
    version: str = "1.0.0"
    capabilities: Set[AgentCapability] = field(default_factory=set)
    status: AgentStatus = AgentStatus.HEALTHY
    
    # Load and capacity
    current_load: int = 0  # Number of active requests
    max_capacity: int = 100  # Maximum concurrent requests
    
    # Performance
    metrics: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    
    # Registration info
    registered_at: datetime = field(default_factory=datetime.now)
    last_heartbeat: datetime = field(default_factory=datetime.now)
    
    # Additional metadata
    tags: Dict[str, str] = field(default_factory=dict)
    priority: int = 0  # Higher priority agents preferred
    
    # Health check configuration
    health_check_interval: int = 30  # seconds
    health_check_timeout: int = 5  # seconds
    
    def __post_init__(self):
        """Validate metadata after initialization"""
        if not self.agent_type:
            raise ValueError("agent_type is required")
        if self.max_capacity <= 0:
            raise ValueError("max_capacity must be positive")
        if self.current_load < 0:
            raise ValueError("current_load cannot be negative")
    
    @property
    def load_percentage(self) -> float:
        """Calculate current load as percentage"""
        if self.max_capacity == 0:
            return 100.0
        return (self.current_load / self.max_capacity) * 100
    
    @property
    def available_capacity(self) -> int:
        """Get available capacity"""
        return max(0, self.max_capacity - self.current_load)
    
    @property
    def is_available(self) -> bool:
        """Check if agent is available to handle requests"""
        return (
            self.status == AgentStatus.HEALTHY and
            self.current_load < self.max_capacity
        )
    
    @property
    def is_overloaded(self) -> bool:
        """Check if agent is overloaded"""
        return self.current_load >= self.max_capacity
    
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has specific capability"""
        return capability in self.capabilities
    
    def add_capability(self, capability: AgentCapability):
        """Add capability to agent"""
        self.capabilities.add(capability)
    
    def remove_capability(self, capability: AgentCapability):
        """Remove capability from agent"""
        self.capabilities.discard(capability)
    
    def update_heartbeat(self):
        """Update last heartbeat timestamp"""
        self.last_heartbeat = datetime.now()
    
    def increment_load(self):
        """Increment current load"""
        self.current_load = min(self.current_load + 1, self.max_capacity)
    
    def decrement_load(self):
        """Decrement current load"""
        self.current_load = max(0, self.current_load - 1)
    
    def update_metrics(
        self,
        response_time: float,
        success: bool
    ):
        """Update performance metrics"""
        self.metrics.total_requests += 1
        if success:
            self.metrics.successful_requests += 1
        else:
            self.metrics.failed_requests += 1
        
        # Update average response time (moving average)
        n = self.metrics.total_requests
        current_avg = self.metrics.average_response_time
        self.metrics.average_response_time = (
            (current_avg * (n - 1) + response_time) / n
        )
        
        self.metrics.last_request_time = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "version": self.version,
            "capabilities": [c.value for c in self.capabilities],
            "status": self.status.value,
            "current_load": self.current_load,
            "max_capacity": self.max_capacity,
            "load_percentage": self.load_percentage,
            "available_capacity": self.available_capacity,
            "is_available": self.is_available,
            "metrics": {
                "average_response_time": self.metrics.average_response_time,
                "total_requests": self.metrics.total_requests,
                "success_rate": self.metrics.success_rate,
                "error_rate": self.metrics.error_rate,
            },
            "registered_at": self.registered_at.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "tags": self.tags,
            "priority": self.priority,
        }
