FSM Module Documentation - Thea IA 2.0
📚 Componentes del FSM
Este módulo implementa la Máquina de Estados Finita (FSM) para la orquestación de flujos conversacionales en Thea IA 2.0 y la gestión de la desambiguación de intenciones.

Archivos Principales:
conversation_manager.py

Ubicación: src/theaia/core/fsm/conversation_manager.py

Descripción: Clase ConversationManager, corazón del FSM global. Maneja estados, desambiguación de intents y delegación a agentes específicos.

state_machine.py

Ubicación: src/theaia/core/fsm/state_machine.py

Descripción: Define BaseStateMachine (clase abstracta) y ConversationStateMachine con estados y transiciones iniciales.

global_states.py

Ubicación: src/theaia/core/fsm/states/global_states.py

Descripción: Contiene la enumeración GlobalState, validación de transiciones y descripciones de cada estado global.

transitions.py

Ubicación: src/theaia/core/fsm/transitions.py

Descripción: Configuración centralizada de reglas de transiciones, condiciones y callbacks.

disambiguation_state.py

Ubicación: src/theaia/core/fsm/states/disambiguation_state.py

Descripción: Módulo para manejar tipos de desambiguación, generar preguntas y procesar elecciones del usuario.

agent_states.py

Ubicación: src/theaia/core/fsm/states/agent_states.py

Descripción: Mapeo de intents a AgentType, estados iniciales y capacidades de cada agente.

🚀 Ejemplo de Uso
python
from src.theaia.core.fsm.conversation_manager import ConversationManager
from src.theaia.core.fsm.states.global_states import GlobalState

# Crear manager para un usuario
cm = ConversationManager(user_id="user123")

# Detectar intents candidatos (externo)
intents = ['notas', 'agenda']

# Procesar input ambiguo
response, state, context = cm.process_input("Recordar reunión y tomar nota", intents)
print(response)  # "¿Quieres guardar esto como nota o como cita?"

# Usuario elige opción
response, state, context = cm.process_input("cita", [])
print(response)  # "Procesando tu solicitud como agenda..."
print(state)     # "agent_delegated"

# Delegar al agente y completar conversión
response, state, context = cm.process_input("Detalles de la cita", [])
print(response)  # "Tarea completada. ¿En qué más puedo ayudarte?"
📝 Versión
FSM Module v2.1.0

Fecha de Actualización: 2025-10-15 19:30 CEST

🔧 Configuración
Dependencia principal: transitions

Variables de entorno opcionales:

FSM_TIMEOUT_MINUTES

FSM_MAX_DISAMBIGUATION_RETRIES

🧪 Testing
Tests unitarios:

bash
pytest src/theaia/tests/unit/fsm/ -v
Tests E2E para flujo de desambiguación:

bash
pytest src/theaia/tests/e2e/test_fsm_disambiguation.py -v
Fin de documentación del FSM
Módulo FSM Thea IA 2.0

FSM - Máquina de estados conversacional
Este módulo gestiona el ciclo, la lógica y las transiciones de estado para el sistema de conversación en Thea IA 2.0.

Arquitectura
BaseStateMachine: Clase abstracta con lógica de configuración base (estados, transiciones universales, manejo de contexto).

ConversationStateMachine: Implementa estados concretos de la conversación, transiciones de ciclo conversacional (ambigüedad, delegación, completado, error, timeout).

Estados principales:
initial: Estado por defecto al inicio.

awaiting_disambiguation: Esperando resolución de intents.

agent_delegated: Intención delegada al agente correspondiente.

completed: Conversación finalizada.

error_state: Error o excepción.

session_timeout: Conversación expirada o fuera de tiempo.

Triggers/transiciones:
request_disambiguation

delegate_to_agent

resolve_disambiguation

complete_conversation

timeout_session

reset / error (universales)

Helpers para testing
Métodos auxiliares (_test_handle_ambiguity, _test_resolve_disambiguation, etc.) en la clase ConversationStateMachine para facilitar pruebas unitarias y simulación de flujos.

Ejemplo de uso
python
fsm = ConversationStateMachine(user_id="12345")
fsm._test_handle_ambiguity(["agenda", "notas"])
fsm._test_resolve_disambiguation("agenda")
fsm._test_complete_task()
print(fsm.state)  # 'completed'
Cobertura de tests
Los tests unitarios comprueban:

Transiciones correctas entre estados (tests en /tests/unit/fsm/)

Gestión de errores, timeout y reset

Cohesión y persistencia del contexto de usuario

Extensibilidad
Puedes añadir nuevos estados, triggers o agentes creando nuevas subclases sobre BaseStateMachine y adaptando las transiciones en setup_transitions().

El robusto diseño FSM es fundamental para la fiabilidad y escalabilidad de Thea IA 2.0 antes de evolucionar a agentes complejos.

