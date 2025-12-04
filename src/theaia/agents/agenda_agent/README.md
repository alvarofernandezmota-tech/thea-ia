# 📅 AgendaAgent

**Sistema inteligente de gestión de agenda con NLP, FSM y conversaciones multi-turno.**

---

## 🎯 Descripción

AgendaAgent es un agente conversacional avanzado que permite a los usuarios gestionar su calendario mediante lenguaje natural. Detecta intenciones, extrae información temporal, y mantiene conversaciones contextuales para completar solicitudes.

### Características principales:
- ✅ **NLP Simple:** Detección de intents con diccionario (sin IA costosa)
- ✅ **DateTime Parser:** Parseo de fechas naturales en español e inglés
- ✅ **FSM Robusto:** Máquina de estados con transitions library
- ✅ **Conversaciones Multi-turno:** Gestión de contexto entre mensajes
- ✅ **Respuestas Formateadas:** Mensajes bonitos con emojis
- ✅ **Persistencia:** Guarda eventos en base de datos
- ✅ **Multi-tenant:** Soporte para múltiples organizaciones

---

## 🏗️ Arquitectura

┌─────────────────────────────────────────────────────────┐
│ handler.py │
│ (Punto de entrada) │
└──────────────────────┬──────────────────────────────────┘
│
┌─────────────┴─────────────┐
│ │
┌────────▼─────────┐ ┌─────────▼──────────┐
│ Orchestrator │ │ Conversation │
│ │◄────►│ Manager │
│ - Coordina flujo │ │ │
│ - Valida datos │ │ - Multi-turno │
│ - Ejecuta acción │ │ - FSM states │
└────────┬─────────┘ │ - Contexto │
│ └────────────────────┘
│
┌────┴────┐
│ │
┌───▼───┐ ┌──▼────────┐
│NLP │ │DateTime │
│Engine │ │Parser │
└───┬───┘ └──┬────────┘
│ │
└────┬───┘
│
┌────▼────────┐
│EventService │
│EventTools │
└─────┬───────┘
│
┌─────▼────────┐
│ Database │
└──────────────┘

text

---

## 📦 Componentes

### **1. Parsing & NLP**

#### `intent_parser.py`
Parser basado en regex para detección de intents.

**Intents soportados:**
- `create_event` - Crear evento
- `update_event` - Modificar evento
- `delete_event` - Eliminar evento
- `query_events` - Listar eventos
- `mark_complete` - Marcar como completado

**Ejemplo:**
parser = AgendaIntentParser()
intent = await parser.detect_intent("crear reunión mañana")

→ "create_event"
entities = await parser.extract_entities(message, intent)

→ {"title": "reunión", "datetime_str": "mañana"}
text

#### `datetime_parser.py`
Parser de expresiones temporales naturales.

**Formatos soportados:**
- Relativos: "en 2 horas", "mañana", "pasado mañana"
- Absolutos: "el viernes", "05/12/2025"
- Horas: "a las 3pm", "at 15:00"

**Ejemplo:**
parser = DateTimeParser(timezone="UTC")
dt = parser.parse("mañana a las 3pm")

→ datetime(2025, 12, 05, 15, 0, 0)
duration = parser.parse_duration("2 horas")

→ timedelta(hours=2)
text

#### `nlp_engine.py`
Motor NLP simple basado en diccionarios (sin IA).

**Características:**
- Score-based intent matching
- Sinónimos y variaciones
- Sugerencias de información faltante
- Hints para entity extraction

**Ejemplo:**
nlp = SimpleNLPEngine()
intent = await nlp.detect_intent("quiero agendar una cita")

→ "create_event"
match = await nlp.detect_intent_with_confidence(message)

→ IntentMatch(intent="create_event", confidence=0.9, matched_keywords=["agendar", "cita"])
text

---

### **2. Orquestación & FSM**

#### `orchestrator.py`
Coordina el flujo completo de procesamiento.

**Flujo:**
1. Parse intent (NLP + regex fallback)
2. Extract entities
3. Parse datetime si presente
4. Validar completitud
5. Ejecutar acción o pedir información faltante

**Ejemplo:**
orchestrator = AgendaOrchestrator(event_service, event_tools, timezone="UTC")

result = await orchestrator.process_message(
message="crear reunión mañana a las 3pm",
context={"user_id": 1, "tenant_id": "default"}
)

→ {"success": True, "response": "✅ Evento creado...", ...}
text

#### `conversation_manager.py`
Gestiona conversaciones multi-turno.

**Características:**
- Mantiene estado de conversación
- Almacena información parcial
- Genera prompts contextuales
- Integrado con FSM

**Ejemplo:**
manager = ConversationManager()

Iniciar conversación
conv_id = manager.start_conversation(
user_id=1,
intent="create_event",
partial_entities={"title": "Reunión"},
missing_fields=["datetime_str"]
)

Actualizar con nueva información
manager.update_conversation(conv_id, new_entities={"datetime_str": "mañana"})

Verificar completitud
is_complete = manager.is_conversation_complete(conv_id)

text

#### `fsm_machine.py`
Máquina de estados finitos con transitions library.

**Estados:**
- `IDLE` - Estado inicial
- `AWAITING_EVENT_DETAILS` - Esperando título
- `AWAITING_TIME` - Esperando fecha/hora
- `AWAITING_EVENT_SELECTION` - Esperando selección
- `AWAITING_CONFIRMATION` - Esperando confirmación
- `PROCESSING` - Procesando acción
- `COMPLETED` - Acción completada
- `ERROR` - Error en proceso

**Ejemplo:**
fsm = AgendaFSM()
fsm.start_create_event()

Estado: IDLE → AWAITING_EVENT_DETAILS
fsm.update_context("title", "Reunión")
fsm.provide_details()

Estado: AWAITING_EVENT_DETAILS → AWAITING_TIME
text

---

### **3. Presentación**

#### `response_formatter.py`
Formatea respuestas bonitas con emojis.

**Métodos:**
- `format_event_created()` - Confirmación de creación
- `format_event_list()` - Lista de eventos
- `format_error()` - Mensajes de error
- `format_missing_info_prompt()` - Solicitudes de info

**Ejemplo:**
formatter = ResponseFormatter(language="es")

response = formatter.format_event_created(event)

→ "✅ Evento creado exitosamente\n📝 Título: Reunión\n📅 Fecha: ..."
text

#### `handler.py`
Punto de entrada principal del agente.

**Uso:**
from sqlalchemy.ext.asyncio import AsyncSession

agent = AgendaAgent(
session=session,
timezone="Europe/Madrid",
language="es"
)

response = await agent.handle_message(
message="crear reunión mañana a las 3pm con Juan",
context={
"user_id": 1,
"tenant_id": "default"
}
)

text

---

### **4. Capas Base**

#### `model/agent_states.py`
Enumeración de estados FSM.

#### `schemas/event_schema.py`
Validaciones Pydantic para eventos.

#### `services/event_service.py`
Lógica de negocio para eventos.

#### `tools/event_tools.py`
Herramientas CrewAI para operaciones.

---

## 🚀 Uso

### **Ejemplo básico:**

from sqlalchemy.ext.asyncio import AsyncSession
from src.theaia.agents.agenda_agent import AgendaAgent

async def process_agenda_message(session: AsyncSession, message: str, user_id: int):
# Crear agente
agent = AgendaAgent(
session=session,
timezone="Europe/Madrid",
language="es"
)

text
# Procesar mensaje
response = await agent.handle_message(
    message=message,
    context={
        "user_id": user_id,
        "tenant_id": "default"
    }
)

return response
text

### **Ejemplos de mensajes soportados:**

**Crear eventos:**
"crear reunión mañana a las 3pm"
"agendar cita con Juan el viernes"
"tengo reunión pasado mañana"

text

**Listar eventos:**
"mostrar mis eventos"
"qué tengo hoy"
"mis próximos eventos"

text

**Modificar eventos:**
"modificar evento #5"
"cambiar reunión a las 4pm"

text

**Eliminar eventos:**
"eliminar evento #3"
"cancelar reunión de mañana"

text

---

## 🧪 Tests

**Ejecutar tests de compilación:**
python -m pytest tests/agents/agenda_agent/test_compilation.py -v

text

**Ejecutar tests de integración:**
python -m pytest tests/agents/agenda_agent/test_agenda_integration.py -v

text

**Cobertura:**
pytest --cov=src.theaia.agents.agenda_agent tests/agents/agenda_agent/

text

---

## 📊 Estadísticas

- **Líneas de código:** ~2,500
- **Módulos:** 12
- **Tests:** 19 (9 compilación + 10 integración)
- **Cobertura:** ~40% (suficiente para MVP)
- **Intents soportados:** 5
- **Idiomas:** Español e Inglés

---

## 🔧 Configuración

### **Dependencias:**

requirements.txt
python-dateutil>=2.8.2
pytz>=2023.3
transitions>=0.9.0

text

### **Variables de entorno:**

.env
AGENDA_TIMEZONE=Europe/Madrid
AGENDA_LANGUAGE=es

text

---

## 🗺️ Roadmap

### **v1.0 (Actual) - MVP Funcional** ✅
- ✅ NLP simple con diccionarios
- ✅ FSM con transitions
- ✅ DateTime parsing
- ✅ Conversaciones multi-turno
- ✅ CRUD de eventos

### **v1.1 (Próximo)**
- 🔜 Integración con router principal
- 🔜 Redis para persistencia de conversaciones
- 🔜 Webhooks para recordatorios
- 🔜 Soporte para eventos recurrentes

### **v2.0 (Futuro)**
- 🔮 NLP con LLM (OpenAI/Claude)
- 🔮 CrewAI agent completo
- 🔮 Integración con Google Calendar
- 🔮 Análisis de disponibilidad inteligente

---

## 👥 Autores

**Álvaro Fernández Mota** - CEO THEA IA  
Filosofía TRES: Álvaro + Jarvis + THEA IA

---

## 📄 Licencia

Propiedad de THEA IA © 2025

---

## 🆘 Soporte

Para dudas o problemas:
- Email: alvaro@thea-ia.com
- Docs: [Documentación interna]

---

## 🎯 Estado del Proyecto

**✅ FUNCIONAL Y TESTEADO**

Última actualización: 04 Diciembre 2025