FSM — Máquina de Estados Conversacional THEA IA
Versión: v2.1.0
Última actualización: 2025-11-03
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Ubicación: src/theaia/core/fsm/

Índice
Objetivo del módulo

Componentes y estructura

Arquitectura y flujo de estados

Ejemplo de uso

Estados, triggers y agentes

Variables y configuración

Testing y cobertura

Buenas prácticas y troubleshooting

Checklist de auditoría FSM

Referencias cruzadas y responsables

1. Objetivo del módulo
La FSM de THEA IA orquesta el flujo completo de cada conversación inteligente, desambigua intents, delega tareas a agentes y gestiona robustamente errores, timeout y recuperación. Es base para auditar y evolucionar todo el ecosistema multiagente.

2. Componentes y estructura
Archivo	Descripción
conversation_manager.py	Clase ConversationManager, core FSM global y centralizador
state_machine.py	Base de estados y transiciones principales
global_states.py	Enumera GlobalState y validaciones de transición
disambiguation_state.py	Lógica para resolver intents ambiguos e interacción guiada
agent_states.py	Mapeo entre intents, agents, entry states
transitions.py	Definición de trigger, reglas y callbacks de logging/auditoría
3. Arquitectura y flujo de estados
text
graph TD
    A[IDLE]
    B[WAITING_USER]
    C[PROCESSING]
    D[AGENT_DISPATCH]
    E[CONFIRMATION]
    F[FALLBACK]
    G[ERROR]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> A
Modularidad total, extensible con nuevos agentes o adaptadores.

Logs y auditoría activos para cada cambio de estado y trigger.

4. Ejemplo de uso
python
from src.theaia.core.fsm.conversation_manager import ConversationManager
cm = ConversationManager(user_id="user123")
response, state, context = cm.process_input("Recordar reunión y tomar nota", ['notas', 'agenda'])
print(response)  # "¿Quieres guardar esto como nota o como cita?"
response, state, context = cm.process_input("cita", [])
response, state, context = cm.process_input("Detalles de la cita", [])
5. Estados, triggers y agentes
Estado	Trigger/Transición	Responsable	Descripción
initial	-	FSM	Inicio del flujo conversacional
awaiting_disambiguation	request_disambiguation	FSM/Usuario	Resolución de intents/usos
agent_delegated	delegate_to_agent	Agent Manager	Tarea transferida a agente
completed	complete_conversation	FSM/Agente	Conversa finalizada
error_state	error/reset	FSM/Logger	Manejo excepción/recuperación
session_timeout	timeout_session/reset	FSM/ContextMgr	Expiración del contexto
6. Variables y configuración
Dependencia principal: transitions (pip)

Variables en .env:

FSM_TIMEOUT_MINUTES

FSM_MAX_DISAMBIGUATION_RETRIES

7. Testing y cobertura
Tests unitarios:
pytest src/theaia/tests/unit/fsm/ -v

Tests E2E de desambiguación:
pytest src/theaia/tests/e2e/test_fsm_disambiguation.py -v

Cobertura >90%, incluye casos de error, timeout y reset.

8. Buenas prácticas y troubleshooting
Todas las transiciones están documentadas y testeadas unitariamente.

Logs de auditoría para todo cambio crítico de estado.

Troubleshooting y FAQs en el README local.

Uso de context snapshot en debug/desarrollo.

Mantenimiento regular de la tabla de estados y triggers.

9. Checklist de auditoría FSM
 Todos los triggers y estados tienen docstring y test asociado.

 Logs y auditoría activa en producción/desarrollo.

 Fallback perfectamente robusto en casos nulos o de error.

 Timeout y reintentos están correctamente parametrizados.

 Manual y flowchart de estados reflejado en el README.

 Config YAML/Python sincronizado con la implementación.

10. Referencias cruzadas y responsables
📄 [docs/agents.md]: Orquestación y lógica de agentes.

📄 [docs/audit_checklist.md]: Puntos a auditar en FSM.

📄 [docs/onboarding.md]: Guía para extender o customizar la FSM.

📄 [src/theaia/core/fsm/README.md]: Documentación local de implementación.

Responsable del módulo FSM: Álvaro Fernández Mota (CEO THEA IA) y equipo-core.