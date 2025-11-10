Thea IA 2.0 - Núcleo Conversacional
Este módulo contiene la arquitectura central del sistema conversacional de Thea IA 2.0. Gestiona la lógica base, el enrutamiento de intents y la integración nativa con FSM y agentes.

Arquitectura principal
CoreRouter
Es el punto de entrada de cada request.

Detecta intents, maneja desambiguación, delega flujo a ConversationManager y agentes.

Compatible y flexible para ampliación de agentes futuros.

ConversationManager
Orquesta la gestión de contexto, ciclo de usuario y transición FSM.

Interactúa con la máquina de estados, maneja el ciclo conversacional de cada usuario.

Encapsula lógica de persistencia y recuperación de contexto.

Integración con FSM
Enlazado directo con ConversationStateMachine: cada flujo de usuario es un ciclo FSM.

Soporta triggers: desambiguación, delegación, completado, error, timeout, reset.

100% testable y escalable.

Persistencia de contexto
Guarda y recupera estado/conversación de cada usuario vía context_repository.

Permite retomar sesiones, aprendizaje continuo y robustez ante fallos.

Extensibilidad y agentes
El Core está listo para nuevos agentes (ej: Agenda, Notas, etc) vía subclases y ampliaciones en la detección de intents y lógica FSM.

Cada agente define su propio Ciclo FSM, transiciones y lógica de negocio.

Tests y robustez
Los tests incluidos (ver /tests/unit/) cubren:

CoreRouter: intención, desambiguación, fallback, delegación, ciclo E2E.

ConversationManager: inicialización, gestión de contexto, integración FSM.

FSM: todas las transiciones y triggers fundamentales, error y reset.

Persistencia: guardado y recuperación de contexto.

Todos los tests pasan en CI antes de avanzar a agentes, asegurando integridad y evolución.

Ejemplo de uso
python
from src.theaia.core.router import CoreRouter

router = CoreRouter()
resp, state, ctx = router.handle("user1", "Quiero agendar reunión")
print(resp)    # Mensaje de desambiguación o delegación
Diagrama de módulos
text
CoreRouter
   └─ ConversationManager
         └─ ConversationStateMachine (FSM)
               └─ Agentes (Agenda, Notas, ...)
Recomendaciones
Antes de ampliar agentes/funcionalidades, asegúrate siempre que TODOS los tests core pasan y la persistencia funciona.

Documenta los cambios en el changelog por hito/ciclo para trazabilidad.