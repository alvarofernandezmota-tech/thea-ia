"""
E2E tests for FallbackAgent.

Tests fallback workflows: unknown intents, clarification, suggestions.
"""

import pytest
from src.theaia.agents.fallback_agent.handler import FallbackAgent


class TestFallbackAgentE2E:
    """End-to-End tests for FallbackAgent."""

    @pytest.fixture
    def agent(self, test_user):
        """Create fresh agent for each test."""
        return FallbackAgent(user_id=test_user.id)

    @pytest.fixture
    def context(self, test_user):
        """Create basic context."""
        return {
            "user_id": test_user.id,
            "tenant_id": test_user.tenant_id,
            "session_id": "session_456",
            "state": "initial"
        }

    # ==================== UNKNOWN INTENT TESTS ====================

    def test_unknown_intent_basic(self, agent, context, test_user):
        """Test handling unknown intent."""
        user_input = "hablame de fisica cuantica"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]
        assert isinstance(response, str)

    def test_unknown_intent_with_clarification(self, agent, context, test_user):
        """Test unknown intent with clarification."""
        user_input = "quiero hacer algo pero no sé qué"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "awaiting_clarification", "idle"]

    def test_unclear_input(self, agent, context, test_user):
        """Test handling unclear input."""
        user_input = "esto aquello"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]

    # ==================== SUGGESTION TESTS ====================

    def test_suggest_similar_intent(self, agent, context, test_user):
        """Test suggesting similar intent."""
        user_input = "quiero anotar algo"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]

    def test_suggest_features(self, agent, context, test_user):
        """Test suggesting available features."""
        user_input = "no sé qué hacer"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]

    # ==================== CLARIFICATION TESTS ====================

    def test_clarify_user_intent(self, agent, context, test_user):
        """Test clarifying user intent."""
        user_input = "agenda"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "awaiting_clarification", "idle"]

    def test_partial_match(self, agent, context, test_user):
        """Test partial intent match."""
        user_input = "evento mañana"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]

    def test_typo_handling(self, agent, context, test_user):
        """Test handling typos."""
        user_input = "crer nota"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]

    # ==================== EDGE CASES ====================

    def test_ambiguous_input(self, agent, context, test_user):
        """Test ambiguous input."""
        user_input = "ahora"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]

    def test_request_human_help(self, agent, context, test_user):
        """Test requesting human help."""
        user_input = "necesito hablar con alguien"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]

    def test_report_issue(self, agent, context, test_user):
        """Test reporting issue."""
        user_input = "esto no funciona"
        response, state, updated_context = agent.handle(test_user.id, user_input, context)

        assert response is not None
        assert state in ["completed", "fallback", "idle"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
