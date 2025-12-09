"""
Event Aggregation System
Aggregates and processes events from multiple sources with filtering and pattern matching.

Author: Álvaro Fernández Mota
Date: 09 December 2025
Version: 1.0.0
"""

from typing import Optional, List, Dict, Any, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
from collections import deque

logger = logging.getLogger(__name__)


class EventPriority(Enum):
    """Event priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Event:
    """
    Represents a single event in the system.
    
    Attributes:
        event_type: Type/category of event
        data: Event payload data
        timestamp: When event occurred
        priority: Event priority level
        source: Where event originated from
        metadata: Additional event metadata
        event_id: Unique event identifier
    
    Example:
        >>> event = Event(
        ...     event_type="user_login",
        ...     data={"user_id": 123},
        ...     priority=EventPriority.NORMAL
        ... )
    """
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    source: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_id: Optional[str] = None
    
    def __post_init__(self):
        """Generate event ID if not provided"""
        if not self.event_id:
            self.event_id = f"{self.event_type}_{self.timestamp.timestamp()}"
    
    def matches_filter(
        self,
        event_types: Optional[List[str]] = None,
        priority_min: Optional[EventPriority] = None,
        priority_max: Optional[EventPriority] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        source: Optional[str] = None
    ) -> bool:
        """
        Check if event matches given filters.
        
        Args:
            event_types: List of event types to match
            priority_min: Minimum priority level
            priority_max: Maximum priority level
            start_time: Minimum timestamp
            end_time: Maximum timestamp
            source: Event source to match
            
        Returns:
            True if event matches all filters
        """
        # Check event type
        if event_types and self.event_type not in event_types:
            return False
        
        # Check priority range
        if priority_min and self.priority.value < priority_min.value:
            return False
        if priority_max and self.priority.value > priority_max.value:
            return False
        
        # Check time range
        if start_time and self.timestamp < start_time:
            return False
        if end_time and self.timestamp > end_time:
            return False
        
        # Check source
        if source and self.source != source:
            return False
        
        return True


@dataclass
class EventPattern:
    """
    Defines a pattern of events to match.
    
    Attributes:
        event_sequence: Ordered list of event types to match
        within_seconds: Time window for pattern match
        action: Callback when pattern matches
        min_occurrences: Minimum times pattern must occur
        metadata: Additional pattern metadata
    """
    event_sequence: List[str]
    within_seconds: float
    action: Callable[[List[Event]], Awaitable[None]]
    min_occurrences: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


class EventAggregator:
    """
    Aggregates and processes events from multiple sources.
    
    Features:
        - Event collection from multiple sources
        - Filtering by type, priority, time, source
        - Pattern matching across event sequences
        - Batch and real-time processing
        - Event history management
    
    Example:
        >>> aggregator = EventAggregator("user_activity")
        >>> aggregator.add_event("login", {"user_id": 123})
        >>> events = aggregator.get_events(event_type="login")
    """
    
    def __init__(
        self,
        name: str,
        max_events: int = 10000,
        auto_cleanup: bool = True,
        cleanup_after_seconds: float = 3600
    ):
        """
        Initialize event aggregator.
        
        Args:
            name: Aggregator name
            max_events: Maximum events to store
            auto_cleanup: Whether to auto-cleanup old events
            cleanup_after_seconds: Age threshold for cleanup
        """
        self.name = name
        self.max_events = max_events
        self.auto_cleanup = auto_cleanup
        self.cleanup_after_seconds = cleanup_after_seconds
        
        self.events: deque = deque(maxlen=max_events)
        self.patterns: List[EventPattern] = []
        self.event_counts: Dict[str, int] = {}
        
        logger.info(f"EventAggregator '{name}' initialized (max_events={max_events})")
    
    def add_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        priority: EventPriority = EventPriority.NORMAL,
        source: Optional[str] = None,
        **metadata
    ) -> Event:
        """
        Add a new event to the aggregator.
        
        Args:
            event_type: Type of event
            data: Event data payload
            priority: Event priority level
            source: Event source identifier
            **metadata: Additional metadata
            
        Returns:
            Created Event object
        """
        event = Event(
            event_type=event_type,
            data=data,
            priority=priority,
            source=source,
            metadata=metadata
        )
        
        self.events.append(event)
        
        # Update event counts
        self.event_counts[event_type] = self.event_counts.get(event_type, 0) + 1
        
        # Auto-cleanup if enabled
        if self.auto_cleanup:
            self._cleanup_old_events()
        
        logger.debug(f"Event '{event_type}' added (id={event.event_id})")
        
        return event
    
    def get_events(
        self,
        event_type: Optional[str] = None,
        priority_min: Optional[EventPriority] = None,
        priority_max: Optional[EventPriority] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Event]:
        """
        Get events matching filters.
        
        Args:
            event_type: Filter by event type
            priority_min: Minimum priority
            priority_max: Maximum priority
            start_time: Minimum timestamp
            end_time: Maximum timestamp
            source: Filter by source
            limit: Maximum events to return
            
        Returns:
            List of matching events
        """
        event_types = [event_type] if event_type else None
        
        matching_events = [
            event for event in self.events
            if event.matches_filter(
                event_types=event_types,
                priority_min=priority_min,
                priority_max=priority_max,
                start_time=start_time,
                end_time=end_time,
                source=source
            )
        ]
        
        if limit:
            matching_events = matching_events[:limit]
        
        return matching_events
    
    def filter_events(
        self,
        event_types: Optional[List[str]] = None,
        priority_min: Optional[EventPriority] = None,
        priority_max: Optional[EventPriority] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        source: Optional[str] = None
    ) -> List[Event]:
        """
        Filter events by multiple criteria.
        
        Args:
            event_types: List of event types to include
            priority_min: Minimum priority
            priority_max: Maximum priority
            start_time: Minimum timestamp
            end_time: Maximum timestamp
            source: Filter by source
            
        Returns:
            List of matching events
        """
        return [
            event for event in self.events
            if event.matches_filter(
                event_types=event_types,
                priority_min=priority_min,
                priority_max=priority_max,
                start_time=start_time,
                end_time=end_time,
                source=source
            )
        ]
    
    def register_pattern(
        self,
        event_sequence: List[str],
        within_seconds: float,
        action: Callable[[List[Event]], Awaitable[None]],
        min_occurrences: int = 1,
        **metadata
    ) -> EventPattern:
        """
        Register a pattern to watch for in event stream.
        
        Args:
            event_sequence: Ordered list of event types
            within_seconds: Time window for pattern
            action: Callback when pattern matches
            min_occurrences: Minimum pattern occurrences
            **metadata: Additional pattern metadata
            
        Returns:
            Created EventPattern object
        """
        pattern = EventPattern(
            event_sequence=event_sequence,
            within_seconds=within_seconds,
            action=action,
            min_occurrences=min_occurrences,
            metadata=metadata
        )
        
        self.patterns.append(pattern)
        logger.info(f"Pattern registered: {event_sequence} within {within_seconds}s")
        
        return pattern
    
    async def check_patterns(self) -> List[List[Event]]:
        """
        Check for pattern matches in recent events.
        
        Returns:
            List of matched event sequences
        """
        matches = []
        
        for pattern in self.patterns:
            pattern_matches = self._find_pattern_matches(pattern)
            
            # Execute action for each match
            for match in pattern_matches:
                try:
                    await pattern.action(match)
                    matches.append(match)
                except Exception as e:
                    logger.error(f"Pattern action failed: {e}")
        
        return matches
    
    def _find_pattern_matches(self, pattern: EventPattern) -> List[List[Event]]:
        """
        Find all occurrences of pattern in events.
        
        Args:
            pattern: Pattern to search for
            
        Returns:
            List of matched event sequences
        """
        matches = []
        events_list = list(self.events)
        
        # Search for pattern starting at each event
        for i in range(len(events_list)):
            match = self._check_pattern_at_index(pattern, events_list, i)
            if match:
                matches.append(match)
        
        return matches
    
    def _check_pattern_at_index(
        self,
        pattern: EventPattern,
        events: List[Event],
        start_index: int
    ) -> Optional[List[Event]]:
        """
        Check if pattern matches starting at given index.
        
        Args:
            pattern: Pattern to match
            events: List of events
            start_index: Starting index
            
        Returns:
            Matched events if pattern found, None otherwise
        """
        if start_index >= len(events):
            return None
        
        start_event = events[start_index]
        matched_events = []
        pattern_index = 0
        
        # Check if first event matches pattern start
        if start_event.event_type != pattern.event_sequence[0]:
            return None
        
        matched_events.append(start_event)
        pattern_index = 1
        
        # Look for remaining pattern events within time window
        time_window = timedelta(seconds=pattern.within_seconds)
        
        for i in range(start_index + 1, len(events)):
            event = events[i]
            
            # Check if still within time window
            if event.timestamp - start_event.timestamp > time_window:
                break
            
            # Check if matches next pattern element
            if pattern_index < len(pattern.event_sequence):
                if event.event_type == pattern.event_sequence[pattern_index]:
                    matched_events.append(event)
                    pattern_index += 1
                    
                    # Pattern complete
                    if pattern_index == len(pattern.event_sequence):
                        return matched_events
        
        return None
    
    def get_event_counts(self, event_types: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Get counts of events by type.
        
        Args:
            event_types: Specific types to count (None for all)
            
        Returns:
            Dictionary of event type -> count
        """
        if event_types:
            return {
                event_type: self.event_counts.get(event_type, 0)
                for event_type in event_types
            }
        return self.event_counts.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of aggregated events.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.events:
            return {
                "name": self.name,
                "total_events": 0,
                "event_types": 0,
                "patterns": len(self.patterns),
                "oldest_event": None,
                "newest_event": None
            }
        
        return {
            "name": self.name,
            "total_events": len(self.events),
            "event_types": len(self.event_counts),
            "patterns": len(self.patterns),
            "oldest_event": self.events[0].timestamp.isoformat(),
            "newest_event": self.events[-1].timestamp.isoformat(),
            "event_counts": self.event_counts.copy()
        }
    
    def clear_events(self, event_type: Optional[str] = None) -> int:
        """
        Clear events from aggregator.
        
        Args:
            event_type: Specific type to clear (None for all)
            
        Returns:
            Number of events cleared
        """
        if event_type:
            # Clear specific event type
            original_count = len(self.events)
            self.events = deque(
                (e for e in self.events if e.event_type != event_type),
                maxlen=self.max_events
            )
            cleared = original_count - len(self.events)
            
            # Update counts
            if event_type in self.event_counts:
                del self.event_counts[event_type]
            
            logger.info(f"Cleared {cleared} events of type '{event_type}'")
            return cleared
        else:
            # Clear all events
            count = len(self.events)
            self.events.clear()
            self.event_counts.clear()
            logger.info(f"Cleared all {count} events")
            return count
    
    def _cleanup_old_events(self) -> int:
        """
        Remove events older than cleanup threshold.
        
        Returns:
            Number of events removed
        """
        if not self.auto_cleanup:
            return 0
        
        cutoff_time = datetime.now() - timedelta(seconds=self.cleanup_after_seconds)
        original_count = len(self.events)
        
        # Remove old events
        self.events = deque(
            (e for e in self.events if e.timestamp > cutoff_time),
            maxlen=self.max_events
        )
        
        removed = original_count - len(self.events)
        
        if removed > 0:
            logger.debug(f"Cleaned up {removed} old events")
        
        return removed
