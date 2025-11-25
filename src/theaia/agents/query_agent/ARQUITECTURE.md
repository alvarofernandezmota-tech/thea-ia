# QueryAgent - Arquitectura Técnica

Documentación técnica detallada de la arquitectura, decisiones de diseño y patrones implementados.

## 📋 Índice

- [Visión General](#visión-general)
- [Componentes](#componentes)
- [Flujo de Datos](#flujo-de-datos)
- [Decisiones de Diseño](#decisiones-de-diseño)
- [Patrones Implementados](#patrones-implementados)
- [Limitaciones Actuales](#limitaciones-actuales)

---

## 🎯 Visión General

QueryAgent implementa un **stateless query handler** para consultas multi-dominio (eventos, notas, recordatorios) usando detección basada en keywords y regex.

### Principios Arquitectónicos

1. **Stateless**: No requiere FSM (consultas son atómicas)
2. **Single Responsibility**: Una query = una respuesta
3. **Extensible**: Fácil agregar nuevos tipos de query
4. **Testeable**: Lógica desacoplada de DB

---

## 🧩 Componentes

### 1. QueryAgent (handler.py)

**Responsabilidad**: Entry point y delegación

class QueryAgent(BaseAgent):
def init(self, user_id: str):
self.user_id = user_id
self.conversation_manager = QueryConversationManager(user_id)

text
def handle(self, user_id, message, context):
    # Delega a conversation manager
    return self.conversation_manager.handle_message(
        user_id, message, context
    )
text

**Decisión**: Patrón Facade - oculta complejidad del manager

### 2. QueryConversationManager (query_conversation_manager.py)

**Responsabilidad**: Lógica de detección y routing

class QueryConversationManager:
def handle_message(self, user_id, message, context):
# 1. Detectar tipo de query
if self._is_event_query(message):
response = self._handle_event_query(message)

text
    # 2. Formatear respuesta
    # 3. Return con state
    return response, "completed", context
text

**Métodos Principales**:

| Método | Propósito | Input | Output |
|--------|-----------|-------|--------|
| `handle_message()` | Orchestrator | message, context | response, state, context |
| `_is_event_query()` | Detector | message | bool |
| `_handle_event_query()` | Handler | message | str |
| `_extract_search_term()` | Extractor | message | str |

---

## 🔄 Flujo de Datos

### Flujo Completo

┌─────────────────────────────────────────────────────────┐
│ Usuario: "¿qué eventos tengo hoy?" │
└────────────────┬────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────┐
│ QueryAgent.handle(message, context) │
└────────────────┬────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────┐
│ QueryConversationManager.handle_message() │
│ ├─ message_lower = message.lower() │
│ ├─ Detección de tipo: │
│ │ ├─ _is_event_query() → True ✓ │
│ │ ├─ _is_note_query() → False │
│ │ └─ ... │
│ └─ Routing: _handle_event_query() │
└────────────────┬────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────┐
│ _handle_event_query(message_lower) │
│ ├─ if 'hoy' in message: ✓ │
│ └─ return "📅 Eventos de hoy: ..." │
└────────────────┬────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────┐
│ Return (response, "completed", context) │
└─────────────────────────────────────────────────────────┘

text

### Detección en Cascada

Orden de evaluación (priority)
_is_event_query() # Alta prioridad (temporal keywords)

_is_note_query() # Media prioridad (domain specific)

_is_reminder_query() # Media prioridad

_is_statistics_query() # Baja prioridad (generic)

_handle_generic_query() # Fallback

text

---

## 🧠 Decisiones de Diseño

### 1. ¿Por Qué Stateless?

**Decisión**: NO usar FSM para QueryAgent

**Razones**:
QueryAgent: Una query = una respuesta
Usuario: "¿qué tengo hoy?"
Sistema: "Eventos de hoy: ..."

↑ Conversación terminada (no multi-turn)
vs
AgendaAgent: Multi-turn conversation
Usuario: "crear evento"
Sistema: "¿Título?"
Usuario: "Reunión"
Sistema: "¿Cuándo?"

↑ Requiere FSM (estado conversacional)
text

**Ventajas**:
- ✅ Código más simple (no state transitions)
- ✅ Tests más fáciles (no setup FSM)
- ✅ Menor overhead (no state tracking)
- ✅ Más rápido (direct response)

**Trade-offs**:
- ⚠️ No soporta queries multi-turn
- ⚠️ No puede pedir clarificación

### 2. Detección Basada en Keywords

**Decisión**: Regex + keyword matching (no ML)

**Implementación**:
def _is_event_query(self, message: str) -> bool:
keywords = ['evento', 'eventos', 'reunión', 'cita', 'agenda']
time_keywords = ['hoy', 'mañana', 'semana', 'próximo']
return any(kw in message for kw in keywords) or
any(kw in message for kw in time_keywords)

text

**Por qué NO ML**:
- ✅ Queries tienen patrones predecibles
- ✅ Keywords en español bien definidos
- ✅ Más rápido que ML (< 1ms)
- ✅ Fácil debug (transparent logic)

**Cuándo migrar a ML** (H06):
- Queries ambiguas aumentan
- Multi-lenguaje (English, French)
- Semantic search necesario

### 3. Mock Responses (Temporal)

**Decisión**: Mock responses en lugar de DB queries

**Razones**:
ACTUAL (v0.9.0):
return "📅 Eventos de hoy: Consultando tu agenda..."

FUTURO (v1.0.0 - H05):
events = await event_repo.get_today(user_id)
return self._format_events(events)

text

**Por qué diferir**:
- Import circular detectado
- Session management no claro
- Mejor timing: H05 (LangChain + DB refactor)

**Impacto**:
- Tests pasan ✅ (mock responses válidas)
- UX aceptable para beta
- Real data en H05

---

## 🎨 Patrones Implementados

### 1. Facade Pattern

class QueryAgent:
def init(self, user_id):
self.manager = QueryConversationManager(user_id)

text
def handle(self, message, context):
    return self.manager.handle_message(message, context)
    # ↑ Oculta complejidad del manager
text

### 2. Strategy Pattern (Implicit)

Cada tipo de query = estrategia diferente
strategies = {
'event': self._handle_event_query,
'note': self._handle_note_query,
'reminder': self._handle_reminder_query,
'stats': self._handle_statistics
}

text

### 3. Template Method Pattern

def _handle_X_query(self, message):
# 1. Detectar sub-tipo (template)
if 'pattern1' in message:
return self._format_response_type1()
elif 'pattern2' in message:
return self._format_response_type2()
# 2. Fallback
return self._default_response()

text

---

## ⚠️ Limitaciones Actuales

### Technical Debt

**1. Mock Responses (10%)**
Limitación:
return "Consultando tu agenda..." # No datos reales

Solución (H05):
events = await event_repo.get_today(user_id)
return self._format_events(events)

text

**2. No Session Management**
Problema:
No hay patrón claro para crear sessions
Solución (H05):
Unificar session factory en H05 refactor
text

**3. Sync Code (No Async)**
Actual:
def _handle_event_query(self, message):

Futuro:
async def _handle_event_query(self, message, user_id):
await event_repo.get_today(user_id)

text

### Limitaciones de Diseño

**1. No Multi-Turn**
❌ NO SOPORTADO:
Usuario: "eventos"
Sistema: "¿De qué día?"
Usuario: "hoy"

✅ SOPORTADO:
Usuario: "eventos de hoy"
Sistema: "Eventos: ..."

text

**2. No Clarificación**
❌ NO SOPORTADO:
Usuario: "eventos" (ambiguo)
Sistema: "¿Qué día: hoy, mañana, semana?"

✅ ACTUAL:
Usuario: "eventos" (ambiguo)
Sistema: "Buscando en tu calendario..."

text

**3. No Context Awareness**
❌ NO SOPORTADO:
Usuario: "¿y de notas?" (referencia previa)

✅ SOPORTADO:
Usuario: "¿cuántas notas tengo?" (query explícita)

text

---

## 🔮 Evolución Futura

### H05 (Dec 2025): DB Integration

ANTES:
def _handle_event_query(self, message):
return "Mock response"

DESPUÉS:
async def _handle_event_query(self, message, user_id, tenant_id):
event_repo = await self._get_event_repo()
events = await event_repo.get_today(user_id)
return self._format_events(events)

text

### H06 (Dec 2025): ML Enhancement

Agregar intent detector ML
from src.theaia.ml.intent_detector import IntentDetector

class QueryConversationManager:
def init(self):
self.intent_detector = IntentDetector()

text
async def handle_message(self, message):
    intent = await self.intent_detector.predict(message)
    # Use ML intent instead of keywords
text

### H12 (Mar 2026): Multi-lenguaje

Auto-detect language
from src.theaia.ml.language_detector import LanguageDetector

class QueryConversationManager:
def init(self):
self.lang_detector = LanguageDetector()

text
async def handle_message(self, message):
    lang = self.lang_detector.detect(message)
    # Use lang-specific keywords
text

---

## 📞 Referencias

- [README.md](./README.md) - User documentation
- [TESTING.md](./TESTING.md) - Testing guide
- [Technical Debt Issue](../../../docs/technical-debt/query-agent-db-integration.md)

**Última actualización**: 2025-11-25  
**Versión**: v0.9.0  
**Autor**: THEA-IA Development Team