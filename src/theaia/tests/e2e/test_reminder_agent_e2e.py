"""
E2E tests for ReminderAgent.

Tests reminder workflows: create, list, edit, complete, delete.
"""

import pytest
from src.theaia.agents.reminder_agent.handler import ReminderAgent


class TestReminderAgentE2E:
    """End-to-End tests for ReminderAgent."""
    
    @pytest.fixture
    def agent(self, test_user):
        """Create fresh agent for each test."""
        return ReminderAgent(user_id=test_user.id)
    
    @pytest.fixture
    def context(self, test_user):
        """Create basic context."""
        return {
            "user_id": test_user.id,
            "tenant_id": test_user.tenant_id,
            "session_id": "session_789",
            "state": "initial"
        }
    
    # ==================== CREATE REMINDER TESTS ====================
    
    @pytest.mark.asyncio
    async def test_create_reminder_basic(self, agent, context, test_user):
        """Test creating a basic reminder."""
        user_input = "crear recordatorio"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert state in ["in_progress", "completed"]
    
    @pytest.mark.asyncio
    async def test_create_reminder_with_datetime(self, agent, context, test_user):
        """Test creating reminder with datetime."""
        user_input = "recordarme mañana a las 10am"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert state in ["in_progress", "completed"]
    
    @pytest.mark.asyncio
    async def test_create_reminder_multi_step(self, agent, context, test_user):
        """Test multi-step reminder creation."""
        # Step 1: Iniciar
        response1, state1, context1 = await agent.handle(
            test_user.id, "crear recordatorio", context
        )
        assert "título" in response1.lower() or "recordatorio" in response1.lower()
        
        # Step 2: Dar título
        response2, state2, context2 = await agent.handle(
            test_user.id, "Llamar al dentista", context1
        )
        assert "cuándo" in response2.lower() or "fecha" in response2.lower()
        
        # Step 3: Dar fecha
        response3, state3, context3 = await agent.handle(
            test_user.id, "mañana 10am", context2
        )
        assert state3 in ["in_progress", "completed"]
    
    # ==================== LIST REMINDER TESTS ====================
    
    @pytest.mark.asyncio
    async def test_list_reminders(self, agent, context, test_user):
        """Test listing reminders."""
        user_input = "listar recordatorios"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert state in ["completed", "in_progress"]
    
    @pytest.mark.asyncio
    async def test_list_reminders_pending(self, agent, context, test_user):
        """Test listing pending reminders."""
        user_input = "mis recordatorios pendientes"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
    
    # ==================== COMPLETE REMINDER TESTS ====================
    
    @pytest.mark.asyncio
    async def test_complete_reminder(self, agent, context, test_user):
        """Test completing a reminder."""
        user_input = "completar recordatorio"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert state in ["completed", "in_progress"]
    
    # ==================== DELETE REMINDER TESTS ====================
    
    @pytest.mark.asyncio
    async def test_delete_reminder(self, agent, context, test_user):
        """Test deleting a reminder."""
        user_input = "eliminar recordatorio"
        response, state, updated_context = await agent.handle(
            test_user.id, user_input, context
        )
        
        assert response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
