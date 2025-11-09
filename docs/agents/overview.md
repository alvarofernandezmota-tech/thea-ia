🤖 Agents System Overview — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Visión general del sistema multi-agente de THEA IA: arquitectura, catálogo de agentes, ciclo de vida, comunicación y orquestación.

Audiencia:

Desarrolladores trabajando con agentes

Arquitectos entendiendo el sistema

Usuarios integrando nuevos agentes

Auditores validando comportamiento multi-agente

🎯 Filosofía multi-agente THEA IA
THEA IA implementa un sistema de agentes especializados, cada uno con responsabilidad específica:

🎯 Especialización: Cada agente domina su dominio

🔄 Comunicación: Agentes colaboran vía FSM central

📊 Orquestación: FSM (Finite State Machine) coordina

🧠 Inteligencia: Cada agente entiende su contexto

Flujo arquitectónico
text
Entrada (Usuario/Adapter)
           ↓
    ┌──────────────┐
    │  FSM Engine  │ ← Orquestador central
    └──────────────┘
           ↓
    ┌──────────────────────────────────┐
    │   Agentes Especializados         │
    ├──────────────────────────────────┤
    │ • Agenda (eventos)               │
    │ • Note (notas)                   │
    │ • Query (búsquedas)              │
    │ • Event (procesamiento eventos)  │
    │ • Scheduler (tareas periódicas)  │
    │ • ... más                        │
    └──────────────────────────────────┘
           ↓
    Salida (Respuesta/Acción)
📚 Catálogo de agentes
Agentes actuales
Agente	Responsabilidad	Rol	Prioridad
Agenda	Crear, listar, modificar eventos	Core	🔴 Alta
Note	Crear, buscar, organizar notas	Core	🔴 Alta
Event	Procesar eventos del sistema	Core	🔴 Alta
Query	Búsquedas inteligentes (NLP)	Core	🔴 Alta
Reminder	Recordatorios y notificaciones	Util	🟡 Media
Scheduler	Tareas periódicas/recurrentes	Util	🟡 Media
Help	Asistencia y documentación	Soporte	🟠 Baja
Fallback	Manejo de errores/unknowns	Soporte	🟠 Baja
Estados de agentes
✅ Activo: Procesando solicitudes

🔄 En Processing: Ejecutando tarea

⏸️ En Espera: Esperando feedback

❌ Error: Fallo en procesamiento

🛑 Deshabilitado: Temporalmente fuera de servicio

🔄 Ciclo de vida de un agente
1. Inicialización
python
agent = AgendaAgent()
agent.initialize()  # Carga configuración, modelos, BD
Qué ocurre:

Cargar configuración del agente

Instanciar modelos ML/dependencias

Conectar a BD/APIs

Estado = "ready"

2. Registro en FSM
python
fsm = FSMEngine()
fsm.register_agent('agenda', agent)
Qué ocurre:

FSM conoce qué agentes disponibles

Se establece comunicación bidireccional

Agente entra en pool disponible

3. Activación por FSM
python
fsm.route_to_agent('agenda', task_data)
Qué ocurre:

FSM selecciona agente apropiado

Pasa datos y contexto

Agente entra en estado "processing"

4. Procesamiento
python
result = agent.process(task_data)
Qué ocurre:

Agente ejecuta su lógica

Valida entrada

Ejecuta tarea (crear evento, buscar, etc.)

Retorna resultado

5. Retorno a FSM
python
fsm.handle_result(result)
Qué ocurre:

FSM recibe resultado

Valida éxito/error

Continúa flujo o eskalación

Comunica resultado al usuario

6. Cierre (teardown)
python
agent.shutdown()
Qué ocurre:

Liberar recursos

Cerrar conexiones

Guardar estado (si necesario)

🗣️ Comunicación entre agentes
Patrón: FSM-mediado
text
Agent A                FSM Engine             Agent B
  │                       │                      │
  ├─ Resultado ────────>  │                      │
  │                       ├─ Necesita B ────>   │
  │                       │                      ├─ Procesa
  │                       │  <─ Resultado ───┤
  │  <─ Integración ───┤
  │
Nunca: Agent A ↔️ Agent B directamente
Siempre: Agent A ↔️ FSM ↔️ Agent B

Ejemplo: Crear evento y guardar nota
python
# 1. Usuario: "Crear evento y toma nota de asuntos"
# 2. FSM: Ruta a Agenda
# 3. Agenda: Crea evento → Retorna event_id
# 4. FSM: Ruta a Note con contexto de evento
# 5. Note: Crea nota con ref a event_id
# 6. FSM: Retorna resultado integrado
🎛️ Configuración de agentes
Cada agente tiene archivo de configuración:

text
# config/agents/agenda.yaml
agent:
  name: "Agenda"
  version: "1.0"
  enabled: true
  timeout: 30  # segundos

capabilities:
  - create_event
  - list_events
  - modify_event
  - delete_event

models:
  nlp: "bert-base-uncased"
  ner: "dbmdz/bert-base-german-cased"

database:
  table: "events"
  cache_ttl: 3600

external_apis:
  calendar:
    url: "https://api.calendar.com"
    timeout: 10
📊 Métricas de agentes
Monitoreadas automáticamente:

Métrica	Propósito
Response time	Velocidad de procesamiento
Success rate	% de éxito vs errores
Error rate	% de errores
Avg accuracy	Precisión predicciones (si ML)
Cache hit rate	Eficiencia de caché
Acceso:

bash
# Ver métricas
GET /api/agents/metrics

# Por agente
GET /api/agents/agenda/metrics
🔐 Seguridad y aislamiento
Principios
Aislamiento de proceso: Cada agente ≈ contexto aislado

Validación entrada: Sanitizar datos antes de procesar

Rate limiting: Throttle por usuario/agente

Timeouts: Prevenir bloqueos

Error handling: Nunca exponer detalles internos

Logging: Auditoría completa

Ejemplo: Rate limit
python
# Max 100 solicitudes por minuto por usuario
@rate_limit(requests=100, window=60)
def process(self, task_data):
    ...
📚 Estructura de archivos
text
src/theaia/agents/
├── __init__.py
├── base.py                    # Clase base abstracta
├── agenda.py                  # Agente Agenda
├── note.py                    # Agente Note
├── event.py                   # Agente Event
├── query.py                   # Agente Query
├── reminder.py                # Agente Reminder
├── scheduler.py               # Agente Scheduler
├── help.py                    # Agente Help
├── fallback.py                # Agente Fallback
├── config/                    # Configuraciones YAML
│   ├── agenda.yaml
│   ├── note.yaml
│   └── ...
└── models/                    # Modelos ML específicos
    ├── intent_classifier.py
    └── ...

docs/agents/
├── overview.md  ← Estás aquí
├── agent_agenda.md
├── agent_note.md
├── ...
└── best_practices.md
🔗 Referencia rápida por agente
Agente	Docs	Casos de uso
Agenda	agent_agenda.md	Crear, listar, modificar eventos
Note	agent_note.md	Tomar y organizar notas
Event	agent_event.md	Procesar eventos del sistema
Query	agent_query.md	Búsquedas inteligentes
Reminder	agent_reminder.md	Recordatorios
Scheduler	agent_scheduler.md	Tareas periódicas
Help	agent_help.md	Asistencia
Fallback	agent_fallback.md	Manejo errores
🎓 Cómo crear un nuevo agente
Pasos resumidos
Heredar de BaseAgent

python
from src.theaia.agents.base import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyAgent")
Implementar métodos clave

python
def initialize(self):
    # Carga recursos
    pass

def process(self, task_data):
    # Lógica principal
    return result

def shutdown(self):
    # Limpieza
    pass
Crear configuración YAML

text
agent:
  name: "MyAgent"
  enabled: true
Registrar en FSM

python
fsm.register_agent('myagent', MyAgent())
Ver best_practices.md para detalles.

✅ Checklist de validación de agentes
 Hereda de BaseAgent

 Implementa initialize(), process(), shutdown()

 Tiene configuración YAML

 Documentación README en docs/agents/agent_xxx.md

 Tests unitarios en src/theaia/tests/unit/test_agents_xxx.py

 Tests integración con FSM

 Rate limiting configurado

 Error handling robusto

 Logging en todos los pasos clave

 Validación de entrada

 Métricas registradas

 Seguridad auditada

🔗 Enlaces relacionados
FSM Engine — Orquestador central

Testing de Agentes — Cómo testear

Best Practices — Convenciones y patrones

Architecture Decisions — Decisiones arquitectónicas

📌 Meta-información
Campo	Valor
Archivo	docs/agents/overview.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	Agents Team / CEO
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.3 (docs/agents/)

Sigue estándar THEA IA: Modular, auditable, escalable

Arquitectura validada y documentada

Cambios deben reflejarse en CHANGELOG

Validado en sesión 35

Nota: Sistema de agentes es el corazón de THEA IA. Cualquier cambio arquitectónico requiere revisión y actualización de todos estos documentos.