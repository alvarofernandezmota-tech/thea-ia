"""
Tests para Agent Decorators & Registry - H03 Advanced Agent Management
Verifica decorators, registry y dynamic loading.

H03 FASE 1 - BLOQUE 1.3 - TAREA 1.3.3
"""

import pytest
from src.theaia.agents.decorators import (
    agent_handler,
    get_registered_agents,
    get_agent_by_name,
    get_agents_by_intent,
    clear_registry
)
from src.theaia.agents.registry import (
    AgentRegistry,
    get_agent,
    get_all_agents,
    list_intents
)
from src.theaia.agents.base_agent import BaseAgent


class TestAgentDecorator:
    """Tests del decorator @agent_handler."""
    
    def setup_method(self):
        clear_registry()
    
    def test_agent_handler_registration(self):
        @agent_handler(
            name="test_agent",
            intents=["test", "testing"],
            priority=7
        )
        class TestAgent(BaseAgent):
            INTENT = "test"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {"response": "test"}
            @staticmethod
            def get_supported_intents():
                return []

        agents = get_registered_agents()
        assert "test_agent" in agents
        assert agents["test_agent"]["intents"] == ["test", "testing"]
        assert agents["test_agent"]["priority"] == 7
    
    def test_agent_metadata_extraction(self):
        @agent_handler(
            name="meta_agent",
            intents=["meta"],
            priority=5,
            requires_auth=True,
            description="Test metadata agent"
        )
        class MetaAgent(BaseAgent):
            INTENT = "meta"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {}
            @staticmethod
            def get_supported_intents():
                return []

        metadata = get_agent_by_name("meta_agent")
        assert metadata is not None
        assert metadata["name"] == "meta_agent"
        assert metadata["requires_auth"] is True
        assert metadata["description"] == "Test metadata agent"

    def test_get_agents_by_intent(self):
        @agent_handler(name="agent1", intents=["search", "find"], priority=8)
        class Agent1(BaseAgent):
            INTENT = "search"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {}
            @staticmethod
            def get_supported_intents():
                return []

        @agent_handler(name="agent2", intents=["search", "query"], priority=6)
        class Agent2(BaseAgent):
            INTENT = "query"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {}
            @staticmethod
            def get_supported_intents():
                return []

        agents = get_agents_by_intent("search")
        assert len(agents) == 2
        assert any(a["name"] == "agent1" for a in agents)
        assert any(a["name"] == "agent2" for a in agents)


class TestAgentRegistry:
    """Tests del AgentRegistry."""
    
    def setup_method(self):
        clear_registry()
        self.registry = AgentRegistry()
    
    def test_registry_initialization(self):
        assert isinstance(self.registry._agents, dict)
        assert isinstance(self.registry._agent_classes, dict)
        assert self.registry._loaded is False
    
    def test_manual_agent_registration(self):
        class ManualAgent(BaseAgent):
            INTENT = "manual"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {"status": "ok"}
            @staticmethod
            def get_supported_intents():
                return []

        self.registry.register_agent("manual", ManualAgent)
        assert "manual" in self.registry._agent_classes
        assert self.registry._agent_classes["manual"] == ManualAgent

    def test_lazy_agent_instantiation(self):
        class LazyAgent(BaseAgent):
            INTENT = "lazy"
            instantiated = False

            def __init__(self):
                super().__init__()
                LazyAgent.instantiated = True

            async def handle(self, user_input: str, context: dict) -> dict:
                return {}

            @staticmethod
            def get_supported_intents():
                return []

        self.registry.register_agent("lazy", LazyAgent)
        assert LazyAgent.instantiated is False
        agent = self.registry.get_agent("lazy")
        assert LazyAgent.instantiated is True
        assert agent is not None

    def test_get_nonexistent_agent(self):
        agent = self.registry.get_agent("nonexistent")
        assert agent is None
    
    def test_list_intents(self):
        class Agent1(BaseAgent):
            INTENT = "intent1"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {}
            @staticmethod
            def get_supported_intents():
                return []

        class Agent2(BaseAgent):
            INTENT = "intent2"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {}
            @staticmethod
            def get_supported_intents():
                return []

        self.registry.register_agent("intent1", Agent1)
        self.registry.register_agent("intent2", Agent2)
        intents = self.registry.list_intents()
        assert "intent1" in intents
        assert "intent2" in intents

    def test_registry_reload(self):
        class ReloadAgent(BaseAgent):
            INTENT = "reload"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {}
            @staticmethod
            def get_supported_intents():
                return []

        self.registry.register_agent("reload", ReloadAgent)
        self.registry.get_agent("reload")
        assert "reload" in self.registry._agents

        self.registry.reload_agents()
        assert len(self.registry._agents) == 0


class TestGlobalRegistryFunctions:
    """Tests de funciones globales del registry."""
    
    def test_get_agent_global(self):
        class GlobalAgent(BaseAgent):
            INTENT = "global"
            async def handle(self, user_input: str, context: dict) -> dict:
                return {}
            @staticmethod
            def get_supported_intents():
                return []

        from src.theaia.agents.registry import _registry
        _registry.register_agent("global", GlobalAgent)

        agent = get_agent("global")
        assert agent is not None
        assert isinstance(agent, GlobalAgent)

    def test_list_intents_global(self):
        intents = list_intents()
        assert isinstance(intents, list)


# ==================== FIXTURES ====================

@pytest.fixture
def clean_registry():
    clear_registry()
    yield
    clear_registry()

@pytest.fixture
def sample_agent_class():
    class SampleAgent(BaseAgent):
        INTENT = "sample"
        async def handle(self, user_input: str, context: dict) -> dict:
            return {"message": "sample response"}
        @staticmethod
        def get_supported_intents():
            return []
    return SampleAgent
