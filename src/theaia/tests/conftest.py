# src/theaia/tests/conftest.py
import pytest

class DummyAgent:
    """
    Un agente simulado que responde con un texto fijo.
    """
    def __init__(self, response_text):
        self.response_text = response_text

    def handle(self, user_id, message, context):
        return {"status": "ok", "message": self.response_text, "context": context}

    def can_handle(self, intent: str) -> bool:
        """
        Simula la capacidad de manejar cualquier intención para los tests.
        """
        return True

@pytest.fixture
def dummy_agent_factory():
    """
    Una factory fixture que permite crear instancias de DummyAgent.
    """
    return DummyAgent

def replace_agent(router, agent_class, dummy_instance):
    """
    Reemplaza un agente en el router por una instancia simulada.
    """
    router.agents = [dummy_instance if isinstance(agent, agent_class) else agent for agent in router.agents]

@pytest.fixture
def agent_replacer():
    """
    Una fixture que proporciona la función de reemplazo de agentes.
    """
    return replace_agent
