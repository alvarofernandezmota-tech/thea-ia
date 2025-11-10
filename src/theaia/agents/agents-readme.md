📖 Agents Module — Documentación General
Módulo: src/theaia/agents/
Versión: v1.0.0 | Status: ✅ Producción

📋 Descripción General
El módulo agents orquesta todos los agentes conversacionales de THEA IA. Proporciona:

BaseAgent: Clase abstracta base

Registry System: Auto-descubrimiento de agentes

8 Agentes Implementados: agenda, event, note, query, reminder, schedule, fallback, help

🏗️ Estructura
text
src/theaia/agents/
├── base_agent.py           # Clase abstracta
├── registry.py             # Auto-discovery
├── __init__.py             # Exports
├── agenda_agent/           # 8 agentes
├── event_agent/
├── note_agent/
├── query_agent/
├── reminder_agent/
├── schedule_agent/
├── fallback_agent/
└── help_agent/
🎯 Agentes Disponibles
Agente	Intenciones	Estados	Documentación
agenda_agent	cita, reunión	6	[252-254]
event_agent	evento, fiesta	7	[255-257]
note_agent	nota, apunte	5	[258-260]
query_agent	consulta, pregunta	5	[261-263]
reminder_agent	recordatorio	6	[264-266], [275-277]
schedule_agent	horario, agenda	3	[267-269], [278-280]
fallback_agent	no_match	2	[287-289]
help_agent	ayuda, help	5	[290-297]
🔄 Flujo Principal
text
1. Router recibe intención del usuario
2. Consulta agent_registry.get(intent)
3. Ejecuta agent.handle(user_id, message, context)
4. Devuelve respuesta estructurada
📚 Archivos de Raíz
** base_agent-README.md** — Clase abstracta

** registry-README.md** — Sistema auto-discovery

** agents_init-README.md** — Package init

✅ Características
✅ 8 agentes completamente funcionales

✅ FSM multi-turno en cada agente

✅ Auto-discovery de agentes

✅ Contrato estandarizado (BaseAgent)

✅ 85%+ test coverage

✅ 30+ MDs documentación

Agents Module v1.0 — Sistema Conversacional Escalable