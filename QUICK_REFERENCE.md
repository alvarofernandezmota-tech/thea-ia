# 📄 QUICK REFERENCE - Status A.4-A.7

**Última Actualización:** 09 Dic 2025, 20:33 CET

---

## ✅ A.4-A.5 STATUS

```
✅ A.4 Context Manager       - COMPLETADO (8/8 tests)
✅ A.5 DateTime Parser        - COMPLETADO (18/18 tests)  
😈 A.6 Intent Detection     - PENDIENTE
😈 A.7 Event Agent          - PENDIENTE
```

---

## 📋 DOCUMENTACIÓN DISPONIBLE

| Archivo | Contenido | Estado |
|---------|----------|--------|
| `HITOS_A4_A5_CIERRE.md` | Cierre detallado de A.4-A.5 | ✅ V1.0 |
| `HITOS_A6_A7_PLAN.md` | Plan detallado para A.6-A.7 | ✅ V1.0 |
| `QUICK_REFERENCE.md` | Este archivo | 🔄 Live |

---

## 💻 API DISPONIBLE (A.4-A.5)

### Imports Básicos

```python
# Context Manager
from src.theaia.agents.agenda_agent.context_manager import (
    ConversationContext,
    ContextManagerFactory,
    ExtractedEntities,
    Message
)

# DateTime Parser
from src.theaia.agents.agenda_agent.datetime_parser import DateTimeParser
```

### Uso Rápido

```python
# 1. Crear contexto
factory = ContextManagerFactory()
context = factory.get_or_create_context("user_123")

# 2. Añadir mensaje
context.add_message(
    text="Agendar reunión mañana a las 3pm con Juan",
    intent="create_event",
    confidence=0.95,
    entities={"title": "Reunión", "participants": ["Juan"]}
)

# 3. Obtener entidades acumuladas
entities = context.get_accumulated_entities()
print(entities["title"])          # "Reunión"
print(entities["participants"])  # ["Juan"]

# 4. Parsear fechas/horas
parser = DateTimeParser(timezone="Europe/Madrid")
date = parser.parse_datetime("mañana")
time = parser.extract_time("a las 3pm")
participants = parser.extract_participants("con Juan y María")

# 5. Ver historial
history = context.get_conversation_history()
print(history)
# [14:23:45] Usuario: Agendar...
# [14:23:50] Agente: ¿A qué hora?
```

---

## 📝 CHECKLISTS RÁPIDOS

### Antes de Empezar A.6

- [ ] Leí `HITOS_A4_A5_CIERRE.md` completo
- [ ] Leí `HITOS_A6_A7_PLAN.md` completo
- [ ] Entiendo la API de `ConversationContext`
- [ ] Entiendo la API de `DateTimeParser`
- [ ] Ejecuté los tests de A.4-A.5 localmente
- [ ] Configuré PyCharm/VSCode con pytest

### Estructura de A.6 (Intent Detection)

```
A.6 Cosas a Crear:
✅ intent_detector.py          - Clase IntentDetector
✅ intent_router.py            - Clase IntentRouter
✅ test_intent_detection.py    - Tests para detector
✅ test_intent_routing.py      - Tests para router

A.6 No Tocar:
✅ context_manager.py          - ❌ READONLY (viene de A.4)
✅ datetime_parser.py          - ❌ READONLY (viene de A.5)
✅ Fixtures de A.4-A.5         - ❌ READONLY
```

### Estructura de A.7 (Event Agent)

```
A.7 Cosas a Crear:
✅ event_service.py            - Clase EventService (CRUD)
✅ event_validator.py          - Clase EventValidator
✅ event_handler.py            - Clase EventHandler
✅ test_event_service.py       - Tests para service
✅ test_event_validation.py    - Tests para validator
✅ test_event_crud.py          - Tests para CRUD

A.7 No Tocar:
✅ Todo lo anterior (A.4-A.6) - ❌ READONLY
```

---

## 📈 MÉTRICAS ACTUALES

### Tests
```
A.4: 8/8 tests ✅
A.5: 18/18 tests ✅
---
Total: 26/26 tests ✅ (100%)
```

### Coverage
```
A.4: ~45%
A.5: ~47%

Promedio: ~46%
Objetivo: >45% ✅
```

### Tiempo de Ejecución
```
A.4: ~3.5s
A.5: ~6.5s
---
Total: ~10s
```

---

## 🚋 WORKFLOW RECOMENDADO

### Para A.6 (Intent Detection)

```bash
# 1. Crear rama
git checkout -b feature/A6-intent-detection

# 2. Crear tests primero (TDD)
echo "# Tests" > test_intent_detection.py

# 3. Implementar intent_detector.py
# 4. Implementar intent_router.py

# 5. Ejecutar tests
python -m pytest src/theaia/agents/agenda_agent/tests/ -v

# 6. Commit
git commit -m "feat: A.6 - Intent detection complete"

# 7. PR & Merge
```

### Para A.7 (Event Agent)

```bash
# 1. Crear rama
git checkout -b feature/A7-event-agent

# 2. Crear service first
echo "# Service" > event_service.py

# 3. Crear validator
# 4. Crear handler

# 5. Ejecutar tests
python -m pytest src/theaia/agents/agenda_agent/tests/ -v

# 6. Commit & Merge
```

---

## 💡 TIPS & GOTCHAS

### Context Manager

```python
# ✅ CORRECTO
context.add_message(
    text=user_input,
    intent="create_event",
    confidence=0.95,
    entities={"title": "Evento"}
)

# ❌ INCORRECTO
context.add_message(
    text=user_input,
    # intent falta
    entities={...}
)
```

### DateTime Parser

```python
# ✅ CORRECTO - con base_date
date = parser.parse_datetime("mañana", 
    base_date=datetime(2025, 12, 9))

# ❌ INCORRECTO - sin base_date puede ser impreciso
date = parser.parse_datetime("mañana")
```

### Fixtures en Tests

```python
# ✅ CORRECTO - usar fixtures
def test_something(context, datetime_parser):
    # context y datetime_parser ya configurados
    pass

# ❌ INCORRECTO - crear manualmente
def test_something():
    context = ConversationContext()  # Evitar
```

---

## 📱 TABLA COMPARATIVA A.4-A.7

| Aspecto | A.4 | A.5 | A.6 | A.7 |
|--------|-----|-----|-----|-----|
| **Tests** | 8 | 18 | 8-10 | 12-15 |
| **Coverage** | 45% | 47% | TBD | TBD |
| **Módulos** | 5 | 1 | 2 | 4 |
| **Depends On** | - | A.4 | A.4-A.5 | A.4-A.6 |
| **Status** | ✅ Done | ✅ Done | 😈 Pending | 😈 Pending |
| **Estimated Days** | 2 | 1 | 1 | 1.5 |

---

## 🔗 Enlaces ÚTiles

- [Cierre A.4-A.5](./HITOS_A4_A5_CIERRE.md) - Documentación completa
- [Plan A.6-A.7](./HITOS_A6_A7_PLAN.md) - Especificaciones detalladas
- [Tests A.4-A.5](./src/theaia/agents/agenda_agent/tests/test_agenda_integration.py) - Tests actuales

---

**✅ Listo para empezar A.6**

Cualquier pregunta: Revisar documentación relevante arriba o abrir issue en GitHub.
