📦 Agents Package — Raíz del Módulo Agentes
Archivo: src/theaia/agents/__init__.py
Versión: v1.0.0

📋 Propósito
Archivo de inicialización que expone la API pública del módulo agents:

Importa BaseAgent (clase base)

Importa agent_registry (registro global)

Carga dinámicamente todos los agentes

💻 Exporta
python
from theaia.agents.base_agent import BaseAgent
from theaia.agents.registry import agent_registry, load_agents

__all__ = ["BaseAgent", "agent_registry", "load_agents"]
🔧 Uso
python
from theaia.agents import BaseAgent, agent_registry, load_agents

# Acceder agente por intención
agenda = agent_registry.get("agenda")

# Crear nuevo agente
class MiAgent(BaseAgent):
    def get_supported_intents(self):
        return ["mi_intención"]
Agents Init v1.0