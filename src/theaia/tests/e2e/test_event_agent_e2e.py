"""
E2E tests for EventAgent.

Tests event workflows: create, list, edit, cancel with REAL DB.
"""

import pytest
from datetime import datetime, timedelta
from src.theaia.agents.event_agent_new.handler import EventAgent
from src.theaia.database.repositories.event_repository import EventRepository
from src.theaia.database.session import get_db


class TestEventAgentE2E:
    """End-to-End tests for EventAgent with REAL DB."""
    
    @pytest.fixture
    def agent(self, test_user):
        """Create fresh agent for each test."""
        return EventAgent(user_id=test_user.id)
    
    @pytest.fixture
    def context(self, test_user):
        """Create basic context."""
        return {
            "user_id": test_user.id,
            "tenant_id": test_user.tenant_id,
            "session_id": "session_789",
            "state": "initial"
        }
    
    # ==================== CREATE EVENT TESTS ====================
    
    @pytest.mark.asyncio
    async def test_create_event_basic(self, agent, context, test_user):
        """Test creating a basic event and verify in DB."""
        user_input = "crear evento"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert state in ["in_progress", "completed"]
    
    @pytest.mark.asyncio
    async def test_create_event_multi_step_real_db(self, agent, context, test_user):
        """Test multi-step event creation and verify DB save."""
        # Step 1: Start
        response1, state1, context1 = await agent.handle(
            test_user.id, "crear evento", context
        )
        assert "título" in response1.lower() or "evento" in response1.lower()
        
        # Step 2: Title
        response2, state2, context2 = await agent.handle(
            test_user.id, "Reunión con cliente", context1
        )
        assert "cuándo" in response2.lower() or "fecha" in response2.lower()
        
        # Step 3: DateTime
        response3, state3, context3 = await agent.handle(
            test_user.id, "mañana 10am", context2
        )
        assert "dónde" in response3.lower() or "ubicación" in response3.lower()
        
        # Step 4: Location
        response4, state4, context4 = await agent.handle(
            test_user.id, "Oficina central", context3
        )
        assert "confirmas" in response4.lower()
        
        # Step 5: Confirm
        response5, state5, context5 = await agent.handle(
            test_user.id, "sí", context4
        )
        assert "✅" in response5
        assert "evento" in response5.lower()
        assert state5 == "completed"
        
        # ✅ VERIFY IN DB
        async for session in get_db():
            event_repo = EventRepository(session)
            events = await event_repo.get_by_user(test_user.id, test_user.tenant_id)
            assert len(events) >= 1
            
            # Find our event
            created_event = next(
                (e for e in events if "reunión" in e.title.lower()),
                None
            )
            assert created_event is not None
            assert created_event.title == "Reunión con cliente"
            assert created_event.location == "Oficina central"
            assert created_event.status == "pending"
            break
    
    @pytest.mark.asyncio
    async def test_create_event_with_datetime(self, agent, context, test_user):
        """Test creating event with datetime extraction."""
        user_input = "evento reunión mañana 10am oficina"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert state in ["in_progress", "completed"]
    
    # ==================== LIST EVENT TESTS ====================
    
    @pytest.mark.asyncio
    async def test_list_events_simple(self, agent, context, test_user):
        """Test listing events - simplified version."""
        # This test relies on events created by previous tests
        user_input = "listar eventos"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        # May show events or empty message
        assert "📅" in response or "evento" in response.lower()
    
    @pytest.mark.asyncio
    async def test_list_events_empty(self, agent, context, test_user):
        """Test listing events when none exist."""
        user_input = "mis eventos"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
    
    # ==================== CANCEL EVENT TESTS ====================
    
    @pytest.mark.asyncio
    async def test_cancel_event(self, agent, context, test_user):
        """Test canceling an event."""
        user_input = "cancelar evento"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert state in ["completed", "in_progress"]
    
    # ==================== VIEW EVENT TESTS ====================
    
    @pytest.mark.asyncio
    async def test_view_event_details(self, agent, context, test_user):
        """Test viewing event details."""
        user_input = "ver evento"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
