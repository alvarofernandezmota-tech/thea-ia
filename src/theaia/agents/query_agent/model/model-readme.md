🤖 Query FSM — 5 Estados
text
awaiting_query → processing → answered → follow_up/completed
Estados:

awaiting_query — Capturar consulta

processing — Procesar con LLM/búsqueda

answered — Respuesta lista

follow_up — Permitir preguntas adicionales

error — Error

Método: _process_query() simula búsqueda

Tests: 8+ cases ✅