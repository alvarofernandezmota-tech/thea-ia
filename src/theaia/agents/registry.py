# src/theaia/agents/registry.py

import pkgutil
import importlib
from theaia.agents.base_agent import BaseAgent

agent_registry: dict[str, BaseAgent] = {}

def load_agents():
    """
    Escanea src/theaia/agents/*/handler.py para registrar agentes.
    Cada handler.py debe exponer una clase que herede de BaseAgent
    y defina la constante INTENT.
    """
    package = importlib.import_module("theaia.agents")
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        try:
            module = importlib.import_module(f"theaia.agents.{name}.handler")
        except ModuleNotFoundError:
            continue
        for attr in dir(module):
            cls = getattr(module, attr)
            if (
                isinstance(cls, type)
                and issubclass(cls, BaseAgent)
                and cls is not BaseAgent
            ):
                agent_registry[cls.INTENT] = cls()

# Cargar agentes al importar el módulo
load_agents()
