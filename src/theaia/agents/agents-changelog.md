📝 Agents Module CHANGELOG — Release Notes
Módulo: src/theaia/agents/

v1.0.0 — 2025-11-10 (S39-AUDIT)
✨ NUEVO
BaseAgent: Clase abstracta base con interfaz estándar

get_supported_intents() - Lista de intenciones

can_handle(intent) - Verificación de capacidad

handle(user_id, message, context) - Procesamiento

Registry System: Auto-discovery dinámico

load_agents() - Escanea handler.py automáticamente

agent_registry - Diccionario global de agentes

8 Agentes Conversacionales:

agenda_agent (6 estados)

event_agent (7 estados)

note_agent (5 estados)

query_agent (5 estados)

reminder_agent (6 estados)

schedule_agent (3 estados)

fallback_agent (2 estados)

help_agent (5 estados)

Documentación Completa:

3 MDs raíz (base_agent, registry, init)

24 MDs agentes (3 c/u)

3 MDs generales (README, ROADMAP, CHANGELOG)

Total: 30+ documentos

📊 Estadísticas
Agentes: 8

Estados FSM: 32 totales

Intenciones: 25+

Test Coverage: 85%+

Líneas código: 2000+

Líneas documentación: 5000+

🔗 Referencias
base_agent-README.md

registry-README.md

agents_init-README.md

[287-289] fallback_agent (3 MDs)

[290-297] help_agent (3 MDs)

AGENTS-README.md

AGENTS-ROADMAP.md

v0.9.0 — 2025-10-28 (Pre-release)
Primeros 6 agentes (agenda, event, note, query, reminder, schedule)

Estructura base

Agents Changelog v1.0