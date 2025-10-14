# src/theaia/tests/core/test_bot_factory.py

from src.theaia.core.bot_factory import BotFactory

class DummyAgent:
    def __init__(self, nombre):
        self.nombre = nombre

def test_register_and_create_agent():
    factory = BotFactory()
    factory.register_agent("dummy", DummyAgent)
    bot = factory.create_agent("dummy", "Thea")
    assert isinstance(bot, DummyAgent)
    assert bot.nombre == "Thea"
    assert "dummy" in factory.list_agents()

def test_unregistered_agent_returns_none():
    factory = BotFactory()
    bot = factory.create_agent("nope", "Test")
    assert bot is None
