"""
E2E tests for QueryAgent.

Tests query workflows: search events, notes, reminders, statistics.
"""

import pytest
from src.theaia.agents.query_agent.handler import QueryAgent


class TestQueryAgentE2E:
    """End-to-End tests for QueryAgent."""

    @pytest.fixture
    def agent(self, test_user):
        """Create fresh agent for each test."""
        return QueryAgent(user_id=test_user.id)

    @pytest.fixture
    def context(self, test_user):
        """Create basic context."""
        return {
            "user_id": test_user.id,
            "tenant_id": test_user.tenant_id,
            "session_id": "session_456",
            "state": "initial"
        }

    # ==================== QUERY EVENTS TESTS ====================

    def test_query_events_today(self, agent, context, test_user):
        """Test querying events for today."""
        user_input = "¿cuántos eventos tengo hoy?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]
        assert isinstance(response, str)

    def test_query_events_tomorrow(self, agent, context, test_user):
        """Test querying events for tomorrow."""
        user_input = "¿qué tengo mañana?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_events_by_name(self, agent, context, test_user):
        """Test querying event by name."""
        user_input = "¿cuándo es la reunión?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_upcoming_events(self, agent, context, test_user):
        """Test querying upcoming events."""
        user_input = "¿qué viene próximamente?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_events_week(self, agent, context, test_user):
        """Test querying events for this week."""
        user_input = "eventos de esta semana"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]
    
    # ==================== QUERY NOTES TESTS ====================

    def test_query_notes_recent(self, agent, context, test_user):
        """Test querying recent notes."""
        user_input = "¿qué notas tengo recientes?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_notes_search(self, agent, context, test_user):
        """Test searching notes."""
        user_input = "buscar notas sobre Python"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_notes_count(self, agent, context, test_user):
        """Test counting notes."""
        user_input = "¿cuántas notas tengo?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    # ==================== QUERY REMINDERS TESTS ====================

    def test_query_reminders_pending(self, agent, context, test_user):
        """Test querying pending reminders."""
        user_input = "¿qué recordatorios tengo pendientes?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_reminders_today(self, agent, context, test_user):
        """Test querying reminders for today."""
        user_input = "recordatorios de hoy"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]
    
    def test_query_reminders_overdue(self, agent, context, test_user):
        """Test querying overdue reminders."""
        user_input = "¿qué recordatorios vencieron?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    # ==================== STATISTICS TESTS ====================

    def test_query_summary_today(self, agent, context, test_user):
        """Test querying today's summary."""
        user_input = "resumen de hoy"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_statistics_month(self, agent, context, test_user):
        """Test querying monthly statistics."""
        user_input = "¿cuántos eventos tengo este mes?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_all_pending(self, agent, context, test_user):
        """Test querying all pending items."""
        user_input = "¿qué pendiente tengo?"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]

    def test_query_empty_results(self, agent, context, test_user):
        """Test query with no results."""
        user_input = "eventos del año 2099"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "answered", "idle", "awaiting_query"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
