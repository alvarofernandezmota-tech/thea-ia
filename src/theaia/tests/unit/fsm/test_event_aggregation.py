"""
Tests for Event Aggregation System
Tests event collection, filtering, and pattern matching.

Author: Álvaro Fernández Mota
Date: 09 December 2025
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from src.theaia.core.fsm.event_aggregation import (
    EventAggregator,
    Event,
    EventPattern,
    EventPriority
)


class TestEvent:
    """Test Event class"""
    
    def test_create_simple_event(self):
        """Test creating a simple event"""
        event = Event(
            event_type="test_event",
            data={"key": "value"}
        )
        
        assert event.event_type == "test_event"
        assert event.data == {"key": "value"}
        assert event.priority == EventPriority.NORMAL
        assert event.event_id is not None
    
    def test_create_event_with_priority(self):
        """Test event with custom priority"""
        event = Event(
            event_type="critical_event",
            data={},
            priority=EventPriority.CRITICAL
        )
        
        assert event.priority == EventPriority.CRITICAL
    
    def test_create_event_with_source(self):
        """Test event with source"""
        event = Event(
            event_type="user_action",
            data={},
            source="web_app"
        )
        
        assert event.source == "web_app"
    
    def test_event_id_auto_generated(self):
        """Test event ID is auto-generated"""
        event = Event(event_type="test", data={})
        
        assert event.event_id is not None
        assert "test" in event.event_id
    
    def test_matches_filter_event_type(self):
        """Test filtering by event type"""
        event = Event(event_type="login", data={})
        
        assert event.matches_filter(event_types=["login", "logout"])
        assert not event.matches_filter(event_types=["signup"])
    
    def test_matches_filter_priority(self):
        """Test filtering by priority"""
        event = Event(
            event_type="test",
            data={},
            priority=EventPriority.HIGH
        )
        
        assert event.matches_filter(priority_min=EventPriority.NORMAL)
        assert event.matches_filter(priority_max=EventPriority.CRITICAL)
        assert not event.matches_filter(priority_min=EventPriority.CRITICAL)
    
    def test_matches_filter_time_range(self):
        """Test filtering by time range"""
        event = Event(event_type="test", data={})
        
        now = datetime.now()
        past = now - timedelta(hours=1)
        future = now + timedelta(hours=1)
        
        assert event.matches_filter(start_time=past, end_time=future)
        assert not event.matches_filter(start_time=future)
        assert not event.matches_filter(end_time=past)
    
    def test_matches_filter_source(self):
        """Test filtering by source"""
        event = Event(event_type="test", data={}, source="api")
        
        assert event.matches_filter(source="api")
        assert not event.matches_filter(source="web")


class TestEventAggregator:
    """Test EventAggregator class"""
    
    def test_create_aggregator(self):
        """Test creating aggregator"""
        aggregator = EventAggregator("test_agg")
        
        assert aggregator.name == "test_agg"
        assert len(aggregator.events) == 0
        assert aggregator.max_events == 10000
    
    def test_create_aggregator_custom_max(self):
        """Test aggregator with custom max events"""
        aggregator = EventAggregator("test", max_events=100)
        
        assert aggregator.max_events == 100
    
    def test_add_single_event(self):
        """Test adding a single event"""
        aggregator = EventAggregator("test")
        
        event = aggregator.add_event("login", {"user_id": 123})
        
        assert len(aggregator.events) == 1
        assert event.event_type == "login"
        assert event.data["user_id"] == 123
    
    def test_add_multiple_events(self):
        """Test adding multiple events"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("event1", {})
        aggregator.add_event("event2", {})
        aggregator.add_event("event3", {})
        
        assert len(aggregator.events) == 3
    
    def test_add_event_with_priority(self):
        """Test adding event with priority"""
        aggregator = EventAggregator("test")
        
        event = aggregator.add_event(
            "error",
            {"message": "critical error"},
            priority=EventPriority.CRITICAL
        )
        
        assert event.priority == EventPriority.CRITICAL
    
    def test_add_event_with_source(self):
        """Test adding event with source"""
        aggregator = EventAggregator("test")
        
        event = aggregator.add_event(
            "api_call",
            {},
            source="backend_api"
        )
        
        assert event.source == "backend_api"
    
    def test_get_events_all(self):
        """Test getting all events"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("event1", {})
        aggregator.add_event("event2", {})
        
        events = aggregator.get_events()
        
        assert len(events) == 2
    
    def test_get_events_by_type(self):
        """Test filtering events by type"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("login", {})
        aggregator.add_event("logout", {})
        aggregator.add_event("login", {})
        
        login_events = aggregator.get_events(event_type="login")
        
        assert len(login_events) == 2
        assert all(e.event_type == "login" for e in login_events)
    
    def test_get_events_by_priority(self):
        """Test filtering events by priority"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("e1", {}, priority=EventPriority.LOW)
        aggregator.add_event("e2", {}, priority=EventPriority.HIGH)
        aggregator.add_event("e3", {}, priority=EventPriority.CRITICAL)
        
        high_priority = aggregator.get_events(priority_min=EventPriority.HIGH)
        
        assert len(high_priority) == 2
    
    def test_get_events_with_limit(self):
        """Test limiting number of returned events"""
        aggregator = EventAggregator("test")
        
        for i in range(10):
            aggregator.add_event("test", {"index": i})
        
        events = aggregator.get_events(limit=5)
        
        assert len(events) == 5
    
    def test_filter_events_multiple_types(self):
        """Test filtering by multiple event types"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("login", {})
        aggregator.add_event("logout", {})
        aggregator.add_event("signup", {})
        aggregator.add_event("login", {})
        
        events = aggregator.filter_events(event_types=["login", "logout"])
        
        assert len(events) == 3
    
    def test_filter_events_by_source(self):
        """Test filtering by source"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("action", {}, source="web")
        aggregator.add_event("action", {}, source="mobile")
        aggregator.add_event("action", {}, source="web")
        
        web_events = aggregator.filter_events(source="web")
        
        assert len(web_events) == 2
    
    def test_filter_events_time_range(self):
        """Test filtering by time range"""
        aggregator = EventAggregator("test")
        
        # Add events
        aggregator.add_event("old", {})
        asyncio.run(asyncio.sleep(0.01))
        aggregator.add_event("recent", {})
        
        # Filter recent events
        cutoff = datetime.now() - timedelta(seconds=0.005)
        recent_events = aggregator.filter_events(start_time=cutoff)
        
        assert len(recent_events) >= 1
    
    def test_register_pattern(self):
        """Test registering event pattern"""
        aggregator = EventAggregator("test")
        
        async def action(events):
            pass
        
        pattern = aggregator.register_pattern(
            event_sequence=["login", "page_view", "logout"],
            within_seconds=60,
            action=action
        )
        
        assert len(aggregator.patterns) == 1
        assert pattern.event_sequence == ["login", "page_view", "logout"]
    
    @pytest.mark.asyncio
    async def test_pattern_matching_simple(self):
        """Test simple pattern matching"""
        aggregator = EventAggregator("test")
        matches_found = []
        
        async def action(events):
            matches_found.append(events)
        
        aggregator.register_pattern(
            event_sequence=["step1", "step2"],
            within_seconds=1.0,
            action=action
        )
        
        # Add matching events
        aggregator.add_event("step1", {})
        aggregator.add_event("step2", {})
        
        await aggregator.check_patterns()
        
        assert len(matches_found) == 1
        assert len(matches_found[0]) == 2
    
    @pytest.mark.asyncio
    async def test_pattern_matching_complex(self):
        """Test complex pattern with multiple events"""
        aggregator = EventAggregator("test")
        matches_found = []
        
        async def action(events):
            matches_found.append(events)
        
        aggregator.register_pattern(
            event_sequence=["login", "view", "click", "logout"],
            within_seconds=5.0,
            action=action
        )
        
        # Add matching sequence
        aggregator.add_event("login", {})
        aggregator.add_event("view", {})
        aggregator.add_event("click", {})
        aggregator.add_event("logout", {})
        
        await aggregator.check_patterns()
        
        assert len(matches_found) == 1
        assert len(matches_found[0]) == 4
    
    @pytest.mark.asyncio
    async def test_pattern_no_match_wrong_order(self):
        """Test pattern doesn't match wrong order"""
        aggregator = EventAggregator("test")
        matches_found = []
        
        async def action(events):
            matches_found.append(events)
        
        aggregator.register_pattern(
            event_sequence=["step1", "step2"],
            within_seconds=1.0,
            action=action
        )
        
        # Add in wrong order
        aggregator.add_event("step2", {})
        aggregator.add_event("step1", {})
        
        await aggregator.check_patterns()
        
        assert len(matches_found) == 0
    
    @pytest.mark.asyncio
    async def test_pattern_no_match_outside_window(self):
        """Test pattern doesn't match outside time window"""
        aggregator = EventAggregator("test", auto_cleanup=False)
        matches_found = []
        
        async def action(events):
            matches_found.append(events)
        
        aggregator.register_pattern(
            event_sequence=["step1", "step2"],
            within_seconds=0.001,  # Very short window
            action=action
        )
        
        # Add with delay
        aggregator.add_event("step1", {})
        await asyncio.sleep(0.01)
        aggregator.add_event("step2", {})
        
        await aggregator.check_patterns()
        
        assert len(matches_found) == 0
    
    def test_get_event_counts_all(self):
        """Test getting counts of all event types"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("login", {})
        aggregator.add_event("login", {})
        aggregator.add_event("logout", {})
        
        counts = aggregator.get_event_counts()
        
        assert counts["login"] == 2
        assert counts["logout"] == 1
    
    def test_get_event_counts_specific(self):
        """Test getting counts of specific types"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("login", {})
        aggregator.add_event("logout", {})
        aggregator.add_event("signup", {})
        
        counts = aggregator.get_event_counts(event_types=["login", "logout"])
        
        assert "login" in counts
        assert "logout" in counts
        assert "signup" not in counts
    
    def test_get_summary_empty(self):
        """Test summary with no events"""
        aggregator = EventAggregator("test")
        
        summary = aggregator.get_summary()
        
        assert summary["name"] == "test"
        assert summary["total_events"] == 0
        assert summary["oldest_event"] is None
    
    def test_get_summary_with_events(self):
        """Test summary with events"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("event1", {})
        aggregator.add_event("event2", {})
        
        summary = aggregator.get_summary()
        
        assert summary["total_events"] == 2
        assert summary["event_types"] == 2
        assert summary["oldest_event"] is not None
        assert summary["newest_event"] is not None
    
    def test_clear_all_events(self):
        """Test clearing all events"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("e1", {})
        aggregator.add_event("e2", {})
        
        cleared = aggregator.clear_events()
        
        assert cleared == 2
        assert len(aggregator.events) == 0
    
    def test_clear_specific_event_type(self):
        """Test clearing specific event type"""
        aggregator = EventAggregator("test")
        
        aggregator.add_event("login", {})
        aggregator.add_event("logout", {})
        aggregator.add_event("login", {})
        
        cleared = aggregator.clear_events(event_type="login")
        
        assert cleared == 2
        assert len(aggregator.events) == 1
        assert aggregator.events[0].event_type == "logout"
    
    def test_max_events_limit(self):
        """Test max events limit is enforced"""
        aggregator = EventAggregator("test", max_events=5)
        
        # Add more than max
        for i in range(10):
            aggregator.add_event("test", {"index": i})
        
        assert len(aggregator.events) == 5
        # Should keep most recent
        assert aggregator.events[-1].data["index"] == 9
    
    def test_auto_cleanup_disabled(self):
        """Test auto cleanup can be disabled"""
        aggregator = EventAggregator(
            "test",
            auto_cleanup=False,
            cleanup_after_seconds=0.001
        )
        
        aggregator.add_event("old", {})
        
        # Should not cleanup
        assert len(aggregator.events) == 1
    
    @pytest.mark.asyncio
    async def test_multiple_patterns(self):
        """Test multiple patterns can coexist"""
        aggregator = EventAggregator("test")
        matches1 = []
        matches2 = []
        
        async def action1(events):
            matches1.append(events)
        
        async def action2(events):
            matches2.append(events)
        
        aggregator.register_pattern(
            event_sequence=["a", "b"],
            within_seconds=1.0,
            action=action1
        )
        
        aggregator.register_pattern(
            event_sequence=["a", "b", "c"],
            within_seconds=1.0,
            action=action2
        )
        
        # Add events
        aggregator.add_event("a", {})
        aggregator.add_event("b", {})
        aggregator.add_event("c", {})
        
        await aggregator.check_patterns()
        
        assert len(matches1) >= 1
        assert len(matches2) >= 1
    
    def test_event_metadata(self):
        """Test events can have metadata"""
        aggregator = EventAggregator("test")
        
        event = aggregator.add_event(
            "custom",
            {},
            custom_field="value",
            another_field=123
        )
        
        assert event.metadata["custom_field"] == "value"
        assert event.metadata["another_field"] == 123
