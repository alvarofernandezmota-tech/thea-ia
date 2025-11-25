🔍 Query Agent — Gestor de Consultas e Información
Versión: v1.0.0 | Status: ✅ Producción | Intenciones: 5

📋 Propósito
Query Agent procesa consultas, búsquedas y preguntas del usuario. Captura información, procesa con LLM/búsqueda, proporciona respuesta y permite seguimiento.

🏗️ Arquitectura
text
query_agent/
├── handler.py (QueryAgent)
├── query_conversation_manager.py
├── model/query_fsm.py (FSM 5 estados)
├── tests/
└── README.md
Intenciones soportadas:

consulta, buscar, pregunta, información, query

🔄 Flujo
text
Usuario: "¿Cuál es el precio del Bitcoin?"
↓
THEA: "¿Qué consulta quieres realizar?"
[awaiting_query]
↓
Usuario: "Quiero saber el precio del Bitcoin"
↓
THEA: "He procesado tu consulta. Aquí está la información..."
[answered]
↓
Usuario: "¿Necesitas más detalles?"
↓
Usuario: "Sí, ¿qué pasó en 2021?" (follow-up)
[processing → answered]
💻 QueryFSM (5 Estados)
Estado	Propósito	Transición
awaiting_query	Capturar pregunta	→ processing
processing	Procesar consulta	→ answered
answered	Responder usuario	→ follow_up / completed
follow_up	Permitir nuevas preguntas	→ processing / completed
error	Manejo errores	(terminal)
Método core: _process_query(query) → simula búsqueda/LLM

🧪 Testing
Coverage: 85%+

test_handle_basic_query()

test_follow_up_questions()

test_query_completion()

Query Agent v1.0 — Consultas conversacionales multi-turno