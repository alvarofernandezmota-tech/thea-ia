import pytest
from src.theaia.agents.schedule_agent.handler import ScheduleAgent


@pytest.fixture
def agent():
    """Create test agent."""
    user_id = 123  # Integer user_id
    return ScheduleAgent(user_id)


def test_schedule_agent_initialization(agent):
    """Test agent initializes correctly."""
    assert agent is not None
    assert agent.user_id == 123
    assert agent.conversation_manager is not None


def test_get_supported_intents(agent):
    """Test agent returns supported intents."""
    intents = agent.get_supported_intents()
    assert isinstance(intents, list)
    assert len(intents) > 0
    assert "horario" in intents
    assert "agenda" in intents
    assert "optimizar" in intents


@pytest.mark.asyncio
async def test_handle_message_optimize(agent):
    """Test handling optimize intent."""
    context = {"user_id": 123, "session_id": "test_session"}
    
    response, state, updated_context = await agent.handle_message(
        123, "optimiza mi agenda de hoy", context
    )
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_handle_message_free_time(agent):
    """Test handling free time intent."""
    context = {"user_id": 123, "session_id": "test_session"}
    
    response, state, updated_context = await agent.handle_message(
        123, "¿cuándo tengo tiempo libre?", context
    )
    
    assert response is not None
    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_handle_message_prioritize(agent):
    """Test handling prioritize intent."""
    context = {"user_id": 123, "session_id": "test_session"}
    
    response, state, updated_context = await agent.handle_message(
        123, "priorizar mis tareas", context
    )
    
    assert response is not None
    assert isinstance(response, str)
    assert "prioriza" in response.lower() or "tarea" in response.lower()


@pytest.mark.asyncio
async def test_handle_message_unknown_intent(agent):
    """Test handling unknown intent returns help."""
    context = {"user_id": 123, "session_id": "test_session"}
    
    response, state, updated_context = await agent.handle_message(
        123, "algo random sin intención", context
    )
    
    assert response is not None
    assert isinstance(response, str)
    # Should return help message
    assert "agenda" in response.lower() or "ayuda" in response.lower()
