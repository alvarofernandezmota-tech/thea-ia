import pytest
from src.theaia.agents.schedule_agent.model.scheduler_fsm import SchedulerFSM


@pytest.fixture
def fsm():
    """Create test FSM."""
    return SchedulerFSM()


@pytest.mark.asyncio
async def test_fsm_initialization(fsm):
    """Test FSM initializes correctly."""
    assert fsm is not None
    assert fsm.state == "awaiting_intent"
    assert isinstance(fsm.context, dict)


@pytest.mark.asyncio
async def test_fsm_optimize_intent(fsm):
    """Test FSM handles optimize intent."""
    context = {}
    
    response, state = await fsm.process_message("optimiza mi agenda", context)
    
    assert state == "awaiting_details"
    assert "periodo" in response.lower() or "optimizar" in response.lower()


@pytest.mark.asyncio
async def test_fsm_free_time_intent(fsm):
    """Test FSM handles free time intent."""
    context = {}
    
    response, state = await fsm.process_message("tiempo libre mañana", context)
    
    assert state == "awaiting_details"
    assert "día" in response.lower() or "libre" in response.lower()


@pytest.mark.asyncio
async def test_fsm_prioritize_intent(fsm):
    """Test FSM handles prioritize intent."""
    context = {}
    
    response, state = await fsm.process_message("priorizar tareas", context)
    
    assert state == "completed"
    assert "prioriza" in response.lower() or "tarea" in response.lower()


@pytest.mark.asyncio
async def test_fsm_full_flow(fsm):
    """Test complete FSM flow."""
    context = {}
    
    # Step 1: State optimize intent
    response, state = await fsm.process_message("optimizar agenda", context)
    assert state == "awaiting_details"
    
    # Update context with new state
    context["fsm_state"] = state
    fsm.state = state
    
    # Step 2: Provide details
    response, state = await fsm.process_message("hoy", context)
    assert state == "completed"
    assert "optimizada" in response.lower() or "reorganizado" in response.lower()


@pytest.mark.asyncio
async def test_fsm_unknown_intent(fsm):
    """Test FSM handles unknown intent with help."""
    context = {}
    
    response, state = await fsm.process_message("comando desconocido", context)
    
    assert state == "awaiting_intent"
    assert "agenda" in response.lower() or "ayuda" in response.lower()
