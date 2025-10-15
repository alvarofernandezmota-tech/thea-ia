Tests unitarios Thea IA 2.0
Esta carpeta contiene la batería de tests que aseguran la robustez y comportamiento correcto del núcleo conversacional de Thea IA 2.0: router, FSM, máquina de estados y persistencia.

Estructura de archivos
core/
test_router.py

Verifica detección y delegación de intents (agenda, notas, fallback).

Prueba flujos básicos y desambiguación.

test_conversation_manager.py

Testea el ciclo completo de conversación y estado interno FSM.

Incluye cobertura de ambigüedad, delegación, completado y reset.

fsm/
test_state_machine.py

Asegura el correcto ciclo de la máquina de estados: inicialización, desambiguación, delegación, completado.

test_fsm_specials.py

Pruebas específicas de transición por timeout, error y reset de la FSM.

persistence/
test_context_persistence.py

Valida el ciclo de guardado y recuperación de contexto del usuario y estado de la conversación.

Cómo lanzar los tests
Desde la raíz del proyecto, ejecuta:

bash
pytest src/theaia/tests/unit/
Cobertura y finalidad
Todos estos tests confirman:

Integridad y funcionamiento del router y FSM.

Robustez de la máquina de estados conversacional.

Persistencia consistente de contexto y usuario.

Flujos especiales de error, reset y timeout correctamente gestionados.

Es obligatorio tener toda esta batería en verde antes de iniciar el trabajo con agentes (Agenda, Notas, etc.) y evolución funcional.