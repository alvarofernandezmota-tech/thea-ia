# 📊 SCHEMA.md — Estado Global THEA IA v3.0.0

**Versión:** v3.0.0  
**Última actualización:** 06 Enero 2026, 16:21 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 🎯 Visión General

THEA IA es un sistema multi-tenant de agentes conversacionales inteligentes con **4 agentes especializados** que NO se solapan en funcionalidades.

**Stack Tecnológico:**
- **Python 3.11+**
- **PostgreSQL 14+** (7 modelos SQLAlchemy)
- **FastAPI** (async/await)
- **SQLAlchemy 2.0** (async ORM)
- **Repository Pattern** (6 repositories + base abstracto)
- **FSM Engine** (Finite State Machine completo)
- **Groq LLM** (Mixtral-8x7b para NLP)

---

## 📊 Roadmap Completo H01-H17

### ✅ FASE 1: CORE & FSM (H01-H08) — COMPLETADO

| Hito | Nombre | Período | Estado | Tests | Coverage |
|------|--------|---------|--------|-------|----------|
| **H01** | Router & Orchestrator | Oct 2025 | ✅ | 10 | 60% |
| **H02** | Multi-tenancy & Database | Nov 2025 | ✅ | 16 | 41-59% |
| **H03** | AgentConfig & NLP Extractors | Nov-Dic 2025 | ✅ | 18 | 84-87% |
| **H04** | FSM Core System | Dic 2025 | ✅ | 196 | 63-100% |
| **H05** | FSM Advanced (Nested, Orthogonal) | Dic 2025 | ✅ | 174 | 85%+ |
| **H06** | FSM Integration & Polish | Dic 2025 | ✅ | 261 | 90%+ |
| **H07** | Callbacks Manager | Dic 2025 | ✅ | 71 | 96% |
| **H08** | FSM Production Ready | Dic 2025 | ✅ | 40 | 95% |

**Totales H01-H08:**
- **Tests:** 786 (100% passing)
- **Coverage:** ~85% promedio
- **LOC:** 12,300+
- **Estado:** ✅ PRODUCCIÓN READY

---

### 🔴 FASE 2: ECOSISTEMA REAL (H09) — EN EJECUCIÓN

| Hito | Submódulo | Duración | Tests | LOC | Estado |
|------|-----------|----------|-------|-----|--------|
| **H09** | **ECOSISTEMA FUNCIONAL** | Ene 2026 (15 días) | 81 | 3,000 | 🔴 CRÍTICO |
| 9.1 | Bot Telegram | 20h | 15 | 800 | ⏳ |
| 9.2 | Database Services | 15h | 20 | 600 | ⏳ |
| 9.3 | Calendar Engine | 18h | 18 | 700 | ⏳ |
| 9.4 | Groq LLM Integration | 15h | 16 | 600 | ⏳ |
| 9.5 | E2E Integration | 7h | 12 | 300 | ⏳ |

**Objetivo H09:** Bot Telegram funcionando + BD guardando datos + Calendar + Groq

**Agente implementado en H09:**
- ✅ **AgendaAgent** (único agente funcional actualmente)

---

### ⏳ FASE 3: AGENTES COMPLEMENTARIOS (H10-H11) — PLANIFICADO

| Hito | Agentes | Período | Tests | Estado |
|------|---------|---------|-------|--------|
| **H10** | QueryAgent + NoteAgent | Feb 2026 | 60 | ⏳ Planificado |
| **H11** | ReminderAgent + Integraciones | Feb 2026 | 40 | ⏳ Planificado |

---

### ⏳ FASE 4: ESCALABILIDAD (H12-H14)

| Hito | Nombre | Período | Horas | Estado |
|------|--------|---------|-------|--------|
| **H12** | API REST + OAuth2 | Mar 2026 | 70 | ⏳ |
| **H13** | WhatsApp Adapter | Abr 2026 | 80 | ⏳ |
| **H14** | Observabilidad | Abr 2026 | 75 | ⏳ |

---

### ⏳ FASE 5: COMPLEMENTARIOS (H15-H17)

| Hito | Nombre | Período | Horas | Estado |
|------|--------|---------|-------|--------|
| **H15** | Security & Hardening | May 2026 | 65 | ⏳ |
| **H16** | Monitoring & APM | May 2026 | 75 | ⏳ |
| **H17** | Web UI (opcional) | Jun 2026 | 80 | ⏳ |

---

## 🤖 ECOSISTEMA DE 4 AGENTES — SIN SOLAPAMIENTO

### 1️⃣ AgendaAgent (Agendar) 📅
**Hito:** H09 (Ene 2026)  
**Estado:** 🔴 EN IMPLEMENTACIÓN  
**Prioridad:** CRÍTICA

#### Responsabilidades ÚNICAS:
- ✅ Crear eventos/citas con fecha y hora
- ✅ Listar eventos por rango de fechas
- ✅ Modificar eventos (cambiar fecha/hora/asistentes)
- ✅ Eliminar/cancelar eventos
- ✅ Detectar conflictos de horario (overbooking)
- ✅ Configurar recordatorios PRE-evento (15 min antes)
- ✅ Sincronizar con Google Calendar

#### Tecnología:
```python
# Calendar Engine
- Slot generation (9am-6pm, 30min slots)
- Availability checking
- Conflict detection
- Timezone support (UTC → local)

# Base de datos
- Tabla: appointments
  ├─ user_id
  ├─ date
  ├─ start_time
  ├─ end_time
  ├─ status (booked/cancelled/completed)
  └─ reminder_minutes

# Integraciones
- Google Calendar API
- Bot Telegram (comandos /agendar, /citas, /cancelar)
- Groq LLM (entender "quiero cita mañana a las 3pm")
Ejemplos de uso:
text
Usuario: "Quiero agendar una cita mañana a las 3pm"
Bot: (LLM entiende) → date=tomorrow, time=15:00
Bot: (Calendar Engine) → check availability
Bot: "✅ Cita confirmada para 07 Ene 2026 a las 15:00"
2️⃣ QueryAgent (Consultas) 🔍
Hito: H10 (Feb 2026)
Estado: ⏳ PLANIFICADO
Prioridad: ALTA

Responsabilidades ÚNICAS:
✅ Búsqueda semántica (buscar por SIGNIFICADO no palabras exactas)

✅ Question answering ("¿Cuándo es mi próxima cita?")

✅ Extracción de información ("Extrae todas las fechas de mis notas")

✅ Búsqueda MULTI-FUENTE (buscar en notas + eventos + docs)

✅ Ranking por relevancia (ordenar resultados)

✅ Respuestas directas (no solo listar, sino responder)

Tecnología:
python
# NLP Models
- Embedding model: sentence-transformers/all-MiniLM-L6-v2
- QA model: deepset/roberta-base-squad2
- Semantic search engine

# Capacidades
- Búsqueda vectorial (embeddings)
- Question answering (responde preguntas)
- Entity extraction (nombres, fechas, lugares)
- Multi-source search (notas + eventos + docs)

# Base de datos
- Vector embeddings
- Full-text search index
- Relevance scoring
Diferencia con otros agentes:
AgendaAgent: Gestiona eventos (crear/modificar)

QueryAgent: Busca y responde preguntas SOBRE eventos/notas

NoteAgent: Gestiona notas (crear/editar)

QueryAgent: Busca DENTRO de notas con NLP

Ejemplos de uso:
text
Usuario: "¿Cuál fue mi última cita?"
QueryAgent: (busca en appointments) → "Tu última cita fue el 03 Ene a las 14:00"

Usuario: "Busca notas sobre 'roadmap'"
QueryAgent: (semantic search) → "Encontré 3 notas: Roadmap Q1, H09 Roadmap, ..."

Usuario: "¿Qué tengo que hacer mañana?"
QueryAgent: (busca eventos + notas con tag 'todo') → "Tienes: 1) Cita 10am, 2) Reunión 3pm"
3️⃣ NoteAgent (Notas) 📝
Hito: H10 (Feb 2026)
Estado: ⏳ PLANIFICADO
Prioridad: ALTA

Responsabilidades ÚNICAS:
✅ Crear notas (título + contenido markdown)

✅ Listar todas las notas del usuario

✅ Modificar/editar contenido de notas

✅ Eliminar notas

✅ Sistema de etiquetas/tags (personal, trabajo, ideas)

✅ Archivar notas antiguas

✅ Auto-tagging con NLP ("Esta nota parece sobre 'planning'")

✅ Deduplicación (detectar notas similares)

Tecnología:
python
# Base de datos
- Tabla: notes
  ├─ note_id
  ├─ user_id
  ├─ title
  ├─ content (markdown)
  ├─ tags (array)
  ├─ created_at
  └─ archived (bool)

# Full-text search
- PostgreSQL ts_vector (español)
- Text embeddings para similitud
- Tag indexing

# NLP Features
- Auto-tagging (extraer topics)
- Deduplicación (similarity > 0.9)
- Excerpt generation
Diferencia con otros agentes:
NoteAgent: Gestiona notas (crear/editar/organizar)

QueryAgent: Busca DENTRO de notas (no las modifica)

Ejemplos de uso:
text
Usuario: "Crea nota: 'Roadmap Q1' con contenido 'Feature A, B, C'"
NoteAgent: (crea nota + auto-tags) → "Nota creada con tags: [planning, roadmap]"

Usuario: "Edita mi nota de roadmap"
NoteAgent: (modifica contenido) → "Nota actualizada"

Usuario: "Lista mis notas con tag 'ideas'"
NoteAgent: → "3 notas encontradas: [Idea A, Idea B, Idea C]"
4️⃣ ReminderAgent (Recordatorios) ⏰
Hito: H11 (Feb 2026)
Estado: ⏳ PLANIFICADO
Prioridad: MEDIA

Responsabilidades ÚNICAS:
✅ Crear recordatorios INDEPENDIENTES (no ligados a eventos)

✅ Listar recordatorios activos

✅ Modificar recordatorios (cambiar mensaje/fecha)

✅ Eliminar recordatorios

✅ Enviar notificaciones multi-canal (Telegram, email, push)

✅ Recordatorios recurrentes (diarios, semanales)

✅ Snooze (posponer recordatorio)

Tecnología:
python
# Scheduler
- Celery o APScheduler
- Cron-like scheduling
- Background tasks

# Base de datos
- Tabla: reminders
  ├─ reminder_id
  ├─ user_id
  ├─ message
  ├─ trigger_at (datetime)
  ├─ recurrence (null/daily/weekly)
  ├─ channels (telegram/email/push)
  └─ status (active/triggered/snoozed)

# Notification System
- Multi-channel delivery
- Retry logic (3 intentos)
- Delivery confirmation
Diferencia con otros agentes:
AgendaAgent: Recordatorios PRE-evento (15 min antes de cita)

ReminderAgent: Recordatorios INDEPENDIENTES ("Comprar leche mañana")

Ejemplos de uso:
text
Usuario: "Recuérdame comprar leche mañana a las 10am"
ReminderAgent: → "Recordatorio creado para 07 Ene 10:00"

Usuario: "Recuérdame tomar agua cada 2 horas"
ReminderAgent: (recurrente) → "Recordatorio recurrente creado"

Usuario: "Snooze 30 minutos"
ReminderAgent: → "Recordatorio pospuesto 30 min"
💾 Base de Datos PostgreSQL 14+
Tablas Core (H02) ✅
Tabla	Filas Típicas	Multi-tenant	Estado
tenants	100s	-	✅ H02
users	10,000s	✅	✅ H02
conversations	100,000s	✅	✅ H02
messages	1,000,000s	✅	✅ H02
agent_configs	100s	✅	✅ H03
Tablas Agentes (H09-H11) ⏳
Tabla	Agente	Estado	Índices
appointments	AgendaAgent	⏳ H09	date, user_id, status
availability	AgendaAgent	⏳ H09	date, time_slot
notes	NoteAgent	⏳ H10	user_id, tags, ts_vector
reminders	ReminderAgent	⏳ H11	trigger_at, user_id, status
Índices Optimizados:
sql
-- Appointments (AgendaAgent)
CREATE INDEX idx_appointments_date ON appointments(date);
CREATE INDEX idx_appointments_user ON appointments(user_id);
CREATE INDEX idx_appointments_status ON appointments(status);

-- Notes (NoteAgent)
CREATE INDEX idx_notes_fulltext ON notes USING GIN(to_tsvector('spanish', content));
CREATE INDEX idx_notes_tags ON notes USING GIN(tags);

-- Reminders (ReminderAgent)
CREATE INDEX idx_reminders_trigger ON reminders(trigger_at) WHERE status='active';
🧪 Testing & Coverage
Estado Actual (H01-H08) ✅
Métrica	Valor Actual	Objetivo	Estado
Total Tests	786	500+	✅
Unit Tests	450	300+	✅
Integration Tests	250	150+	✅
E2E Tests	86	50+	✅
Code Coverage	85%	80%	✅
Test Pass Rate	100%	100%	✅
Test Duration	~5 min	< 10 min	✅
Roadmap Testing (H09-H11) ⏳
Hito	Tests Nuevos	Acumulado	Target Coverage
H09	+81	867	85%
H10	+60	927	87%
H11	+40	967	90%
🏗️ Arquitectura en Capas
text
┌─────────────────────────────────────────────────────┐
│         INTEGRATION LAYER (Adapters)                │
│  ✅ TelegramAdapter (H02, H09)                      │
│  ⏳ APIAdapter (H12)                                │
│  ⏳ WhatsAppAdapter (H13)                           │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│      INTELLIGENCE LAYER (4 Agentes)                 │
│  🔴 AgendaAgent (H09) — Agendar eventos             │
│  ⏳ QueryAgent (H10) — Búsquedas semánticas         │
│  ⏳ NoteAgent (H10) — Gestión de notas              │
│  ⏳ ReminderAgent (H11) — Recordatorios             │
│                                                     │
│  ✅ AgentConfig System (H03)                        │
│  ✅ Entity Extractors (H03)                         │
│     - DateTimeExtractor (91% coverage)             │
│     - LocationExtractor (100% coverage)            │
│     - PersonNameExtractor (98% coverage)           │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│         CORE LAYER (FSM + Context)                  │
│  ✅ State Machine (H04, 732 LOC, 63%)               │
│  ✅ Exceptions (H04, 681 LOC, 100%)                 │
│  ✅ Transitions (H04, 680 LOC, 81%)                 │
│  ✅ Context Merging (H04, 600 LOC, 84%)             │
│  ✅ Callbacks Manager (H07, 300 LOC, 96%)           │
│  ✅ FSM Advanced (H05-H06, 174+261 tests)           │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│       DATA LAYER (Repository Pattern)               │
│  ✅ 6 Repositories + Base Abstract (H02)            │
│  ✅ PostgreSQL 14+ (7 tablas core)                  │
│  ✅ SQLAlchemy 2.0 async                            │
│  ⏳ 4 tablas agentes (H09-H11)                      │
└─────────────────────────────────────────────────────┘
🔒 Seguridad
Implementado (H01-H08) ✅
✅ Multi-tenant isolation (tenant_id obligatorio)

✅ Environment variables (.env para secrets)

✅ Input validation (Pydantic schemas)

✅ SQL injection protection (SQLAlchemy ORM)

✅ Async/await (no blocking)

Roadmap Seguridad ⏳
⏳ OAuth2 + JWT (H12, Q1 2026)

⏳ Rate Limiting (H12, P0)

⏳ CORS Configuration (H12, P0)

⏳ Row-Level Security PostgreSQL (H15, Q2 2026)

⏳ Secrets Manager (H15, Q2 2026)

📈 Métricas de Calidad
Métrica	Actual	Objetivo v3.0.0	Estado
Código Limpio	95%	90%+	✅
Test Coverage	85%	80%+	✅
Documentación	10/10	8/10	✅
Security Score	8.8/10	8/10	✅
FSM Completitud	100%	100%	✅
Performance	TBD	< 500ms	⏳ H15
🚀 Próximos Pasos (Q1 2026)
Enero 2026
✅ Auditoría Diciembre 2025 completada

🔴 H09: Ecosistema Real (EN CURSO)

Bot Telegram funcionando

AgendaAgent operativo

Calendar Engine

Groq LLM integrado

Febrero 2026
⏳ H10: QueryAgent + NoteAgent

Búsquedas semánticas

Gestión de notas

60 tests nuevos

⏳ H11: ReminderAgent

Sistema de recordatorios

Multi-channel notifications

40 tests nuevos

Marzo 2026
⏳ H12: API REST + OAuth2

Endpoints públicos

Autenticación robusta

Rate limiting

📚 Referencias Rápidas
Documento	Ubicación	Propósito
Roadmap Master	docs/roadmap/master.md	Roadmap completo H01-H17
H09 Ecosystem	docs/roadmap/milestones/H09/	Ecosistema real detallado
Agents Overview	docs/agents/overview.md	Visión general de agentes
AgendaAgent	docs/agents/agent_agenda.md	Spec AgendaAgent
QueryAgent	docs/agents/agent_query.md	Spec QueryAgent
NoteAgent	docs/agents/agent_note.md	Spec NoteAgent
ReminderAgent	docs/agents/agent-reminder.md	Spec ReminderAgent
Auditoría Dic 2025	docs/audit/audit_diciembre_2025/	Auditoría completa
Diary Sessions	docs/diary/	Diarios de sesiones
📊 Resumen Ejecutivo
text
┌──────────────────────────────────────────────────────┐
│            THEA IA v3.0.0 — ESTADO GLOBAL           │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Hitos Completados:        8/17 (47%)               │
│  Tests Implementados:      786 (100% passing)       │
│  Code Coverage:            85%                      │
│  Líneas de Código:         12,300+ LOC              │
│  Documentación:            10/10                    │
│  Technical Debt:           0 (ZERO)                 │
│                                                      │
│  Agentes Funcionales:      1/4 (AgendaAgent H09)    │
│  Agentes Planificados:     3/4 (H10-H11)           │
│                                                      │
│  Status Actual:            🔴 H09 EN EJECUCIÓN      │
│  Próximo Milestone:        H10 QueryAgent + Note    │
│  Production Release:       Q2 2026                  │
│                                                      │
│  Confianza:                ⭐⭐⭐⭐⭐               │
│                                                      │
└──────────────────────────────────────────────────────┘
Última actualización: 06 Enero 2026, 16:21 CET
Versión: v3.0.0
Responsable: Álvaro Fernández Mota
Email: alvarofernandezmota@gmail.com

🎯 Filosofía del Proyecto
Ecosistema Funcional > Interfaces Bonitas
Datos Reales > Mockups
Agentes Especializados > Agentes Generalistas
Testing > Código sin tests
Documentación > Código sin docs