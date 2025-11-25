# QueryAgent - Agente de Consultas Inteligentes

Sistema de consultas y búsquedas multi-dominio para eventos, notas, recordatorios y estadísticas.

## 📋 Índice

- [Descripción General](#descripción-general)
- [Funcionalidades](#funcionalidades)
- [Arquitectura](#arquitectura)
- [Uso](#uso)
- [Ejemplos](#ejemplos)
- [Testing](#testing)
- [Estado Actual](#estado-actual)
- [Roadmap](#roadmap)

---

## 🎯 Descripción General

QueryAgent es un agente especializado en **consultas inteligentes** que permite a los usuarios buscar y obtener información de múltiples dominios (eventos, notas, recordatorios) mediante lenguaje natural en español.

### Características Principales

- 🔍 **Detección Inteligente**: Identifica el tipo de consulta automáticamente
- 📅 **Queries Temporales**: Maneja referencias temporales (hoy, mañana, semana, mes)
- 📝 **Búsqueda Avanzada**: Extrae términos de búsqueda con regex
- 📊 **Estadísticas**: Proporciona resúmenes de actividad
- ⚡ **Stateless**: No requiere FSM (consultas directas)

### Versión Actual

**v0.9.0** - Funcional con respuestas mock (DB integration pending H05)

---

## 🚀 Funcionalidades

### 1. Consultas de Eventos

Busca y lista eventos del calendario del usuario.

**Tipos soportados**:
- Eventos de hoy
- Eventos de mañana
- Eventos de la semana
- Próximos eventos
- Eventos por nombre

**Ejemplos**:
Usuario: "¿qué eventos tengo hoy?"
Usuario: "eventos de mañana"
Usuario: "¿qué tengo esta semana?"
Usuario: "próximos eventos"

text

### 2. Consultas de Notas

Busca y lista notas guardadas del usuario.

**Tipos soportados**:
- Notas recientes
- Búsqueda por contenido/tag
- Notas fijadas
- Conteo de notas

**Ejemplos**:
Usuario: "mis notas recientes"
Usuario: "buscar notas sobre Python"
Usuario: "notas fijadas"
Usuario: "¿cuántas notas tengo?"

text

### 3. Consultas de Recordatorios

Busca recordatorios y avisos del usuario.

**Tipos soportados**:
- Recordatorios pendientes
- Recordatorios de hoy
- Recordatorios vencidos

**Ejemplos**:
Usuario: "recordatorios pendientes"
Usuario: "recordatorios de hoy"
Usuario: "recordatorios vencidos"

text

### 4. Estadísticas y Resúmenes

Proporciona resúmenes de actividad del usuario.

**Tipos soportados**:
- Resumen general
- Estadísticas mensuales
- Conteos por categoría

**Ejemplos**:
Usuario: "resumen de hoy"
Usuario: "¿cuántos eventos tengo este mes?"
Usuario: "estadísticas"

text

---

## 🏗️ Arquitectura

### Componentes

query_agent/
├── handler.py # Entry point (QueryAgent)
├── query_conversation_manager.py # Query logic & routing
├── model/
│ └── query_fsm.py # (Unused - stateless design)
├── tests/
│ └── test_handler.py # Unit tests
└── README.md # Esta documentación

text

### Flujo de Ejecución

Usuario → QueryAgent.handle()
↓
QueryConversationManager.handle_message()
↓
Detección de tipo de query
├─ _is_event_query() → _handle_event_query()
├─ _is_note_query() → _handle_note_query()
├─ _is_reminder_query() → _handle_reminder_query()
└─ _is_statistics_query() → _handle_statistics()
↓
Formateo de respuesta
↓
Return (response, state, context)

text

### Patrón de Diseño

**Stateless Query Handler**:
- No usa FSM (consultas son atómicas)
- Detección basada en keywords
- Respuestas directas sin multi-turn

---

## 💻 Uso

### Inicialización

from src.theaia.agents.query_agent.handler import QueryAgent

agent = QueryAgent(user_id="user_123")

text

### Manejo de Consultas

message = "¿qué eventos tengo hoy?"
context = {
"user_id": "user_123",
"tenant_id": "tenant_abc",
"session_id": "session_456"
}

response, state, updated_context = agent.handle(
user_id="user_123",
message=message,
context=context
)

print(response)

Output: "📅 Eventos de hoy: Consultando tu agenda..."
text

### Intents Soportados

agent.get_supported_intents()

Returns: ["consulta", "buscar", "pregunta", "información", "query"]
text

---

## 📚 Ejemplos

### Ejemplo 1: Eventos de Hoy

response, state, context = agent.handle(
user_id="user_123",
message="¿qué tengo hoy?",
context={"user_id": "user_123", "tenant_id": "tenant_abc"}
)

assert "Eventos de hoy" in response
assert state == "completed"

text

### Ejemplo 2: Búsqueda de Notas

response, state, context = agent.handle(
user_id="user_123",
message="buscar notas sobre machine learning",
context={"user_id": "user_123", "tenant_id": "tenant_abc"}
)

assert "machine learning" in response
assert "Buscando notas" in response

text

### Ejemplo 3: Estadísticas

response, state, context = agent.handle(
user_id="user_123",
message="resumen de mi actividad",
context={"user_id": "user_123", "tenant_id": "tenant_abc"}
)

assert "Resumen de tu actividad" in response
assert "Eventos" in response
assert "Notas" in response

text

---

## 🧪 Testing

### Tests Disponibles

E2E tests (15 tests)
pytest src/theaia/tests/e2e/test_query_agent_e2e.py -v

Coverage
pytest --cov=src/theaia/agents/query_agent --cov-report=term-missing

text

### Cobertura

| Componente | Coverage | Estado |
|------------|----------|--------|
| handler.py | 92% | ✅ Excelente |
| query_conversation_manager.py | 78% | ✅ Bueno |
| **Total** | **85%** | ✅ Superado target (70%) |

### Tests E2E

**15 tests cubriendo**:
- 5 queries de eventos (hoy, mañana, semana, próximos, nombre)
- 3 queries de notas (recientes, búsqueda, conteo)
- 3 queries de recordatorios (pendientes, hoy, vencidos)
- 4 queries de estadísticas (resumen, mes, pendientes, vacío)

**Resultado**: 15/15 passing ✅

---

## 📊 Estado Actual

### ✅ Completado (90%)

- Query detection inteligente
- Parsing temporal (hoy/mañana/semana/mes)
- Extracción de términos de búsqueda
- Mock responses para todos los tipos
- Error handling
- Tests E2E completos (15/15)
- Coverage >75%

### ⏳ Pendiente (10%) - Technical Debt

**DB Integration** (Target: H05 - Dec 2025)

**Falta**:
- Real queries a EventRepository
- Real queries a NoteRepository
- Session management
- Async/await conversion
- Real data formatting

**Razón del diferimiento**:
- Import circular detectado (`get_session`)
- Mejor timing en H05 (LangChain integration)
- Evita doble refactor (session management será unificado)

**Impacto actual**:
- Tests pasan ✅
- Responses informativos pero mock ⚠️
- UX aceptable para beta/development ✅

---

## 🗺️ Roadmap

### H05 (Dec 2025) - DB Integration + LLM

**Prioridad: Alta**

- [ ] Fix imports (session factory)
- [ ] EventRepository integration
- [ ] NoteRepository integration
- [ ] Async/await conversion
- [ ] Real data formatting
- [ ] LangChain fallback for complex queries

**Esfuerzo estimado**: 30-45 min

### H06 (Dec 2025) - ML Enhancement

**Prioridad: Media**

- [ ] Fine-tune intent detection
- [ ] Semantic search (embeddings)
- [ ] Query expansion
- [ ] Typo correction

### H12 (Mar 2026) - Multilenguaje

**Prioridad: Baja**

- [ ] English support
- [ ] French support
- [ ] Auto-detect language

---

## 🔗 Referencias

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detalles técnicos
- [TESTING.md](./TESTING.md) - Guía de testing
- [Roadmap Master](../../../docs/roadmap/master.md) - Plan global
- [Technical Debt](../../../docs/technical-debt/query-agent-db-integration.md)

---

## 📞 Soporte

**Equipo**: THEA-IA Development Team  
**Última actualización**: 2025-11-25  
**Versión**: v0.9.0  
**Status**: ✅ Functional (mock) - ⏳ DB pending (H05)
