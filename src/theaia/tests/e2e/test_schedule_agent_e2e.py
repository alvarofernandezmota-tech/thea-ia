"""
E2E tests for ScheduleAgent.

Tests scheduling workflows: optimize, plan, reschedule.
"""

import pytest
from src.theaia.agents.schedule_agent.handler import ScheduleAgent


class TestScheduleAgentE2E:
    """End-to-End tests for ScheduleAgent."""
    
    @pytest.fixture
    def agent(self, test_user):
        """Create fresh agent for each test."""
        return ScheduleAgent(user_id=test_user.id)
    
    @pytest.fixture
    def context(self, test_user):
        """Create basic context."""
        return {
            "user_id": test_user.id,
            "tenant_id": test_user.tenant_id,
            "session_id": "session_schedule_456",
            "state": "initial"
        }
    
    # ==================== SCHEDULE OPTIMIZATION TESTS ====================
    
    @pytest.mark.asyncio
    async def test_optimize_schedule(self, agent, context, test_user):
        """Test optimizing daily schedule."""
        user_input = "optimiza mi agenda de hoy"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_find_free_time(self, agent, context, test_user):
        """Test finding free time slots."""
        user_input = "¿cuándo tengo tiempo libre mañana?"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_schedule_meeting_time(self, agent, context, test_user):
        """Test scheduling meeting at best time."""
        user_input = "programa la reunión en el mejor momento"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_prioritize_tasks(self, agent, context, test_user):
        """Test prioritizing tasks for week."""
        user_input = "ordena mis tareas por prioridad esta semana"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_balance_workload(self, agent, context, test_user):
        """Test balancing workload."""
        user_input = "distribuye mi trabajo equitativamente"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    # ==================== RESCHEDULE TESTS ====================
    
    @pytest.mark.asyncio
    async def test_reschedule_all_conflicts(self, agent, context, test_user):
        """Test rescheduling conflicting events."""
        user_input = "resuelve los conflictos de mi agenda"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_compress_schedule(self, agent, context, test_user):
        """Test compressing schedule to free time."""
        user_input = "comprime mi agenda para liberar tiempo"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_spread_tasks(self, agent, context, test_user):
        """Test spreading tasks across week."""
        user_input = "distribuye mis tareas a lo largo de la semana"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    # ==================== PLANNING TESTS ====================
    
    @pytest.mark.asyncio
    async def test_plan_project(self, agent, context, test_user):
        """Test planning project timeline."""
        user_input = "planifica el proyecto en mi agenda"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_estimate_duration(self, agent, context, test_user):
        """Test estimating task duration."""
        user_input = "¿cuánto tiempo necesito para esta tarea?"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_create_timeline(self, agent, context, test_user):
        """Test creating project timeline."""
        user_input = "crea una línea de tiempo para el mes"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    # ==================== CAPACITY TESTS ====================
    
    @pytest.mark.asyncio
    async def test_check_availability(self, agent, context, test_user):
        """Test checking availability."""
        user_input = "¿estoy disponible el 25 a las 14:00?"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_capacity_analysis(self, agent, context, test_user):
        """Test analyzing schedule capacity."""
        user_input = "analiza mi capacidad de trabajo"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_suggest_breaks(self, agent, context, test_user):
        """Test suggesting break times."""
        user_input = "sugiere descansos en mi agenda"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_workload_balance_check(self, agent, context, test_user):
        """Test checking workload balance."""
        user_input = "¿está equilibrada mi carga de trabajo?"
        response, state, updated_context = await agent.handle_message(
            test_user.id, user_input, context
        )
        
        assert response is not None
        assert isinstance(response, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
