📅 Schedule Agent — Gestor de Agenda Semanal
Versión: v1.0.0
Última actualización: 2025-11-10 17:55 CET (S39)
Status: ✅ Producción

📋 Propósito
El Schedule Agent gestiona horarios, agendas semanales y planificación. Captura día/período, tipo de acción (consulta/agregar/eliminar) y registra cambios en agenda.

Responsabilidades:

✅ Consultar horario usuario

✅ Agregar/modificar actividades

✅ Eliminar eventos agenda

✅ Gestionar conversaciones multi-turno

✅ Mantener estado FSM

🏗️ Arquitectura
text
schedule_agent/
├── handler.py (ScheduleAgent)
├── schedule_conversation_manager.py
├── model/schedule_fsm.py (FSM 3 estados)
├── tests/
└── README.md
Intenciones: horario, agenda semanal, planning, schedule

🔄 Flujo
text
Usuario: "Muestra mi agenda de mañana"
↓
THEA: "¿Para qué día o periodo quieres ver tu horario?"
[awaiting_day]
↓
Usuario: "Para mañana"
↓
THEA: "¿Quieres consultar, añadir o eliminar algo?"
[awaiting_action]
↓
Usuario: "Consultar"
↓
THEA: "Acción 'consultar' registrada para mañana."
[completed]
💻 Componentes
ScheduleAgent (handler.py)

Hereda BaseAgent

4 intenciones soportadas

Delegación a conversation manager

ScheduleConversationManager

Orquesta FSM simple (3 estados)

Captura día + acción

ScheduleFSM

Estado: awaiting_day

Estado: awaiting_action

Estado: completed

🧪 Testing
Coverage: 85%+

Flujos:

✅ Consulta horario

✅ Agregar evento

✅ Eliminar evento

✅ Contexto persistente

📌 Meta
Campo	Valor
Versión	v1.0.0
Estados FSM	3
Intenciones	4
Test Coverage	85%
Status	✅ Production
Schedule Agent v1.0 — Gestor de Agenda Conversacional