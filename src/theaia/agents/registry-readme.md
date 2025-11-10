📋 AgentRegistry — Sistema de Auto-Descubrimiento de Agentes
Archivo: src/theaia/agents/registry.py
Versión: v1.0.0
Status: ✅ Producción

📋 Propósito
AgentRegistry es el sistema de auto-descubrimiento que:

Escanea dinámicamente carpetas de agentes

Carga automáticamente archivos handler.py

Registra agentes en diccionario global

Permite router acceder a agentes por intención

💻 API
python
agent_registry: dict[str, BaseAgent] = {}

def load_agents():
    """Carga todos los agentes auto-descubriendo handler.py en cada carpeta"""
    # Itera carpetas en theaia/agents/
    # Importa handler.py de cada una
    # Si contiene clase que hereda BaseAgent, la registra
🔄 Flujo
text
1. Sistema inicia
2. load_agents() se ejecuta automáticamente
3. Itera carpetas: agenda_agent/, event_agent/, etc.
4. Busca handler.py en cada una
5. Extrae clase Agent y agrega a agent_registry[intent] = instance
6. Router consulta registry para encontrar agente correcto
📊 Estructura Registry
python
agent_registry = {
    "agenda": AgendaAgent(),
    "evento": EventAgent(),
    "nota": NoteAgent(),
    "consulta": QueryAgent(),
    "recordatorio": ReminderAgent(),
    "horario": ScheduleAgent(),
    "fallback": FallbackAgent(),
    "ayuda": HelpAgent()
}
⚙️ Requisitos para Nuevo Agente
Para que un agente se registre automáticamente:

Crear carpeta: src/theaia/agents/mi_agent/

Crear handler.py con clase que herede BaseAgent

Clase debe tener atributo/propiedad INTENT

Reiniciar sistema (load_agents() se ejecuta al import)

AgentRegistry v1.0 — Auto-Discovery System