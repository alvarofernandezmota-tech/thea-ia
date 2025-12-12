"""
Unit tests for OrchestratorAdapter
Tests intent-to-task conversion, callbacks, and lifecycle management.

Author: Álvaro Fernández Mota
Date: 12 December 2025
Version: 1.0.0
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from theaia.core.multi_agent.orchestrator_adapter import (
    OrchestratorAdapter,
    TaskRequest,
    TaskResponse,
)
from theaia.core.multi_agent.task_delegator import (
    TaskDelegator,
    Task,
    TaskPriority,
    TaskStatus,
)
from theaia.core.multi_agent.agent_registry import AgentRegistry
from theaia.core.multi_agent.agent_metadata import (
    AgentMetadata,
    AgentStatus,
    AgentCapability,
)
from theaia.core.multi_agent.discovery_service import DiscoveryService
from theaia.core.multi_agent.message.broker import MessageBroker


@pytest.fixture
def agent_registry():
    """Create agent registry with test agents"""
    registry = AgentRegistry()
    registry.clear()
    
    agent1 = AgentMetadata(
        agent_id="calendar_agent",
        agent_type="worker",
        capabilities={
            AgentCapability.CALENDAR_MANAGEMENT,
            AgentCapability.EVENT_CREATION
        },
        max_capacity=10,
        status=AgentStatus.HEALTHY,
    )
    
    agent2 = AgentMetadata(
        agent_id="note_agent",
        agent_type="worker",
        capabilities={AgentCapability.NOTE_MANAGEMENT},
        max_capacity=10,
        status=AgentStatus.HEALTHY,
    )
    
    registry.register(agent1)
    registry.register(agent2)
    
    yield registry
    
    registry.clear()


@pytest.fixture
def discovery_service(agent_registry):
    """Create discovery service"""
    return DiscoveryService(agent_registry)


@pytest.fixture
def message_broker():
    """Create message broker"""
    return MessageBroker()


@pytest.fixture
def task_delegator(agent_registry, discovery_service, message_broker):
    """Create task delegator"""
    return TaskDelegator(agent_registry, discovery_service, message_broker)


@pytest.fixture
def adapter(task_delegator):
    """Create orchestrator adapter"""
    return OrchestratorAdapter(task_delegator)


# ============================================================================
# INTENT TO CAPABILITY MAPPING TESTS
# ============================================================================

def test_default_intent_mappings(adapter):
    """Test default intent to capability mappings exist"""
    assert "create_event" in adapter._intent_to_capability
    assert "create_note" in adapter._intent_to_capability
    assert "create_reminder" in adapter._intent_to_capability
    assert "web_search" in adapter._intent_to_capability
    
    assert adapter._intent_to_capability["create_event"] == AgentCapability.EVENT_CREATION
    assert adapter._intent_to_capability["create_note"] == AgentCapability.NOTE_MANAGEMENT


def test_register_custom_intent_capability(adapter):
    """Test registering custom intent mapping"""
    adapter.register_intent_capability("custom_intent", AgentCapability.NATURAL_LANGUAGE_PROCESSING)
    
    assert "custom_intent" in adapter._intent_to_capability
    assert adapter._intent_to_capability["custom_intent"] == AgentCapability.NATURAL_LANGUAGE_PROCESSING


# ============================================================================
# TASK CREATION FROM INTENT TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_create_task_from_known_intent(adapter):
    """Test creating task from known intent"""
    task_request = TaskRequest(
        intent="create_event",
        message="Crear reunión mañana a las 10",
        user_id="user123",
        conversation_id="conv456",
        context={"timezone": "Europe/Madrid"},
        priority=TaskPriority.HIGH,
    )
    
    task = await adapter.create_task_from_intent(task_request)
    
    assert task.task_type == AgentCapability.EVENT_CREATION.value
    assert task.priority == TaskPriority.HIGH
    assert task.payload["message"] == "Crear reunión mañana a las 10"
    assert task.payload["user_id"] == "user123"
    assert task.payload["conversation_id"] == "conv456"
    assert task.payload["intent"] == "create_event"
    assert task.payload["context"]["timezone"] == "Europe/Madrid"


@pytest.mark.asyncio
async def test_create_task_from_unknown_intent(adapter):
    """Test creating task from unknown intent uses GENERAL_ASSISTANCE"""
    task_request = TaskRequest(
        intent="unknown_intent",
        message="Do something",
        user_id="user123",
        conversation_id="conv456",
        context={},
    )
    
    task = await adapter.create_task_from_intent(task_request)
    
    assert task.task_type == AgentCapability.FALLBACK.value
    assert task.payload["intent"] == "unknown_intent"


@pytest.mark.asyncio
async def test_create_task_with_metadata(adapter):
    """Test creating task with metadata"""
    metadata = {"source": "telegram", "chat_id": "123"}
    
    task_request = TaskRequest(
        intent="create_note",
        message="Save this note",
        user_id="user123",
        conversation_id="conv456",
        context={},
        metadata=metadata,
    )
    
    task = await adapter.create_task_from_intent(task_request)
    
    assert task.metadata == metadata


# ============================================================================
# TASK DELEGATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_delegate_task_async_success(adapter):
    """Test successful async task delegation"""
    task_request = TaskRequest(
        intent="create_event",
        message="Create event",
        user_id="user123",
        conversation_id="conv456",
        context={},
    )
    
    response = await adapter.delegate_task_async(task_request)
    
    assert response.status == TaskStatus.ASSIGNED
    assert response.task_id in adapter.task_delegator.tasks
    assert "agente" in response.message.lower()


@pytest.mark.asyncio
async def test_delegate_task_async_no_agent(adapter):
    """Test delegation when no agent available"""
    task_request = TaskRequest(
        intent="unknown_capability",
        message="Do something impossible",
        user_id="user123",
        conversation_id="conv456",
        context={},
    )
    
    # Custom mapping to non-existent capability
    adapter.register_intent_capability("unknown_capability", AgentCapability.NATURAL_LANGUAGE_PROCESSING)
    
    # Remove all agents
    adapter.task_delegator.agent_registry.clear()
    
    response = await adapter.delegate_task_async(task_request)
    
    assert response.status == TaskStatus.FAILED
    assert "no se pudo asignar" in response.message.lower()
    assert response.error == "No available agents"


@pytest.mark.asyncio
async def test_delegate_task_with_progress_callback(adapter):
    """Test delegation with progress callback"""
    callback_data = []
    
    def progress_callback(task_id, progress, message):
        callback_data.append((task_id, progress, message))
    
    task_request = TaskRequest(
        intent="create_event",
        message="Create event",
        user_id="user123",
        conversation_id="conv456",
        context={},
    )
    
    response = await adapter.delegate_task_async(
        task_request,
        progress_callback=progress_callback
    )
    
    assert response.status == TaskStatus.ASSIGNED
    
    # Simulate progress update
    task = adapter.task_delegator.get_task(response.task_id)
    await adapter.task_delegator.update_task_progress(
        response.task_id,
        50,
        "Half done",
        task.assigned_agent_id
    )
    
    assert len(callback_data) == 1
    assert callback_data[0][0] == response.task_id
    assert callback_data[0][1] == 50


# ============================================================================
# TASK STATUS AND RESPONSE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_get_task_response_completed(adapter):
    """Test getting response from completed task"""
    task_request = TaskRequest(
        intent="create_event",
        message="Create event",
        user_id="user123",
        conversation_id="conv456",
        context={},
    )
    
    response = await adapter.delegate_task_async(task_request)
    task_id = response.task_id
    
    # Complete task
    task = adapter.task_delegator.get_task(task_id)
    task.max_retries = 0  # Prevent retries for this test
    task.max_retries = 0  # Prevent retries for this test
    task.max_retries = 0  # Prevent retries for this test
    task.max_retries = 0  # Prevent retries for this test
    task.max_retries = 0  # Prevent retries for this test
    task.max_retries = 0  # Prevent retries for this test
    await adapter.task_delegator.complete_task(
        task_id,
        {"event_id": "evt123"},
        task.assigned_agent_id
    )
    
    task_response = await adapter.get_task_response(task_id)
    
    assert task_response.status == TaskStatus.COMPLETED
    assert task_response.result == {"event_id": "evt123"}
    assert "completada" in task_response.message.lower()


@pytest.mark.asyncio
async def test_get_task_response_failed(adapter):
    """Test getting response from failed task"""
    task_request = TaskRequest(
        intent="create_event",
        message="Create event",
        user_id="user123",
        conversation_id="conv456",
        context={},
    )
    
    response = await adapter.delegate_task_async(task_request)
    task_id = response.task_id
    
    # Fail task
    task = adapter.task_delegator.get_task(task_id)
    task.max_retries = 0  # Prevent retries for this test


