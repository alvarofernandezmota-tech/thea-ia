# 📋 CHECKLIST MASTER H03 — CoreRouter & FSM Integration

**Proyecto:** THEA-IA  
**Hito:** H03 - FSM Avanzado & CoreRouter Integration  
**Versión:** v1.0.0  
**Fecha creación:** 20 Noviembre 2025  
**Responsable:** Álvaro Fernández Mota (CEO THEA-IA)  
**Tipo:** GUÍA PERMANENTE DE REFERENCIA

---

## 🎯 OBJETIVO H03

Integrar CoreRouter con TelegramAdapter, mejorar FSM Engine v2 con callbacks avanzados, implementar procesamiento NLP básico con spaCy para lograr primera conversación inteligente end-to-end.

**Pipeline completo:**
Usuario Telegram → TelegramAdapter → CoreRouter → Intent Detection →
Entity Extraction → FSM Engine → Agent Handler → Database → Response

text

---

## 📊 MÉTRICAS OBJETIVO FINAL

| Métrica | Valor Objetivo | Verificación |
|---------|----------------|--------------|
| Duración total | 36-40h | 4 fases secuenciales |
| Tests nuevos | 50 tests | 100% PASSING |
| Coverage global | ≥80% | pytest-cov |
| Performance CoreRouter | <100ms | ProcessedMessage.processing_time_ms |
| Performance E2E | <500ms | Integration tests |
| Intent accuracy | ≥80% | Test set 100 ejemplos |
| Entity accuracy | ≥90% | Ya existe (H03 anterior) |

---

## 🗂️ ESTRUCTURA COMPLETA H03

H03 TOTAL: 36-40h | 50 tests
│
├─ FASE 1: Core Components (10h) | 14 tests
│ ├─ CoreRouter v2 (6h) | 8 tests
│ └─ FSM Engine v2 (4h) | 6 tests
│
├─ FASE 2: NLP Intelligence (8h) | 10 tests
│ ├─ Setup spaCy (1h)
│ ├─ Intent Detector (5h)
│ └─ Tests & Validation (2h) | 10 tests
│
├─ FASE 3: Integration Layer (8h) | 14 tests
│ ├─ Entity Pipeline (4h) | 8 tests
│ └─ Context Manager v2 (4h) | 6 tests
│
└─ FASE 4: E2E Validation (8-10h) | 12 tests
├─ Integration Tests (6h) | 12 tests
└─ Demo NLP Live (2-3h)

text

---

## 🔵 FASE 1: CORE COMPONENTS (10h | 14 tests)

**Objetivo:** Pipeline CoreRouter completo + FSM con callbacks

**Dependencias satisfechas:**
- ✅ H02 Database Layer operativo
- ✅ H02 TelegramAdapter funcional
- ✅ Entity Extractors H03 anterior (96% avg coverage)

---

### BLOQUE 1.1: CoreRouter v2 (6h | 8 tests)

**Archivos:**
- Código: `src/theaia/core/router.py`
- Tests: `src/theaia/tests/unit/core/test_router.py`

#### TAREA 1.1.1: Pipeline completo (2h)

**Componentes a implementar:**
1. Message & ProcessedMessage dataclasses
2. CoreRouter.process() - pipeline principal
3. _preprocess() - normalización texto
4. _detect_intent() - detección con mock/real
5. _extract_entities() - extracción con mock/real
6. _route_to_agent() - mapeo intent→agent
7. Performance tracking
8. Error handling

**Mapping intent→agent:**
{
"create_event": "EventsAgent",
"edit_event": "EventsAgent",
"delete_event": "EventsAgent",
"create_note": "NotesAgent",
"search_notes": "NotesAgent",
"query_agenda": "AgendaAgent",
"get_reminders": "AgendaAgent",
"help": "HelpAgent",
"*": "FallbackAgent"
}

text

**Criterios de aceptación:**
- [ ] Pipeline ejecuta: preprocess → intent → entities → routing
- [ ] Performance <100ms medido
- [ ] Error handling con fallback
- [ ] Logging en cada paso

---

#### TAREA 1.1.2: Integration Entity Extractors (2h)

**Extractors a usar (H03 anterior completado):**
- DateTimeExtractor (91% coverage, 15 tests) ✅
- LocationExtractor (100% coverage, 18 tests) ✅
- PersonNameExtractor (98% coverage, 18 tests) ✅

**Implementar EntityExtractionPipeline:**

class EntityExtractionPipeline:
"""Composition de extractors con intent-aware logic."""

text
def __init__(self):
    self.date_extractor = DateTimeExtractor()
    self.location_extractor = LocationExtractor()
    self.person_extractor = PersonNameExtractor()

async def extract(self, text: str, intent: str) -> Dict:
    """
    Intent-aware extraction:
    - create_event → date + location
    - create_note → person + location
    - query_agenda → date
    - fallback → date (siempre útil para contexto)
    """
    entities = {}
    
    if intent == "create_event":
        entities["dates"] = self.date_extractor.extract(text)
        entities["locations"] = self.location_extractor.extract(text)
    
    elif intent == "create_note":
        entities["persons"] = self.person_extractor.extract(text)
        entities["locations"] = self.location_extractor.extract(text)
    
    elif intent == "query_agenda":
        entities["dates"] = self.date_extractor.extract(text)
    
    # Fallback: siempre intenta dates
    if "dates" not in entities:
        dates = self.date_extractor.extract(text)
        if dates:
            entities["dates"] = dates
    
    return entities
text

**Criterios de aceptación:**
- [ ] 3 extractors importados correctamente
- [ ] Intent-aware logic implementado
- [ ] Fallback a dates siempre
- [ ] Retorna dict (nunca None)

---

#### TAREA 1.1.3: Tests CoreRouter (2h)

**8 tests unitarios:**

test_router.py
@pytest.mark.asyncio
async def test_process_complete_pipeline():
"""Test pipeline completo sin errores."""
pass

@pytest.mark.asyncio
async def test_detect_intent_create_event():
"""Test: 'crear evento mañana' → create_event."""
pass

@pytest.mark.asyncio
async def test_detect_intent_create_note():
"""Test: 'nueva nota' → create_note."""
pass

@pytest.mark.asyncio
async def test_extract_entities_with_dates():
"""Test extracción fechas con DateTimeExtractor."""
pass

@pytest.mark.asyncio
async def test_route_to_correct_agent():
"""Test routing 9 intents a 5 agentes."""
pass

@pytest.mark.asyncio
async def test_performance_under_100ms():
"""Test performance <100ms."""
pass

@pytest.mark.asyncio
async def test_error_handling_empty_message():
"""Test mensaje vacío → ValueError."""
pass

@pytest.mark.asyncio
async def test_fallback_unknown_intent():
"""Test intent desconocido → FallbackAgent."""
pass

text

**Criterios de aceptación:**
- [ ] 8/8 tests PASSING
- [ ] Coverage ≥80% router.py
- [ ] `pytest -v test_router.py` → ALL GREEN

---

**ENTREGABLE BLOQUE 1.1:**
✅ CoreRouter.process() funcional
✅ EntityExtractionPipeline integrado
✅ 8/8 tests PASSING
✅ Coverage ≥80%
✅ Performance <100ms verificado
✅ Commit: "feat(h03): CoreRouter v2 pipeline - 8/8 tests"

text

---

### BLOQUE 1.2: FSM Engine v2 (4h | 6 tests)

**Archivos:**
- Código: `src/theaia/core/fsm/state_machine.py`
- Tests: `src/theaia/tests/unit/core/fsm/test_state_machine_v2.py`

#### TAREA 1.2.1: Callbacks (2h)

**Implementar 3 tipos de callbacks:**

from typing import Callable, List, Dict
from enum import Enum

class CallbackType(Enum):
PRE_TRANSITION = "pre" # Validación antes
POST_TRANSITION = "post" # Side effects después
ON_ERROR = "error" # Manejo errores

class FSMEngine:
"""FSM con callbacks pre/post/error."""

text
def __init__(self, conversation_repo):
    self.conversation_repo = conversation_repo
    self.callbacks: Dict[CallbackType, List[Callable]] = {
        CallbackType.PRE_TRANSITION: [],
        CallbackType.POST_TRANSITION: [],
        CallbackType.ON_ERROR: []
    }

def register_callback(self, callback_type: CallbackType, callback: Callable):
    """Registra callback por tipo."""
    self.callbacks[callback_type].append(callback)

async def transition(
    self, 
    conversation_id: int,
    tenant_id: str,
    new_state: str,
    context_update: Dict
) -> bool:
    """
    Transición con callbacks.
    
    Flow:
    1. Pre-callbacks (validación) → si False, bloquea
    2. Get conversation actual
    3. Merge context
    4. Update state en DB
    5. Post-callbacks (side effects)
    6. On error: error callbacks
    """
    try:
        # 1. Pre-callbacks
        for callback in self.callbacks[CallbackType.PRE_TRANSITION]:
            valid = await callback(conversation_id, new_state, context_update)
            if not valid:
                raise ValueError(f"Pre-callback blocked transition")
        
        # 2. Get conversation
        conv = await self.conversation_repo.get_by_id(conversation_id, tenant_id)
        if not conv:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # 3. Merge context
        merged_context = self._merge_context(conv.context_data, context_update)
        
        # 4. Update state
        updated_conv = await self.conversation_repo.update_state(
            conversation_id, tenant_id, new_state, merged_context
        )
        
        # 5. Post-callbacks
        for callback in self.callbacks[CallbackType.POST_TRANSITION]:
            await callback(updated_conv)
        
        return True
    
    except Exception as e:
        # 6. Error callbacks
        for callback in self.callbacks[CallbackType.ON_ERROR]:
            await callback(conversation_id, e)
        raise
text

**Criterios de aceptación:**
- [ ] 3 tipos callbacks implementados
- [ ] Pre-callback puede bloquear transición
- [ ] Post-callbacks solo si éxito
- [ ] Error-callbacks si falla

---

#### TAREA 1.2.2: Context merging (1h)

def _merge_context(self, current: Dict, update: Dict) -> Dict:
"""
Merge inteligente preservando historial.

text
Rules:
- Nested dicts merge recursivo
- Listas se reemplazan (no append)
- None values se ignoran
"""
if not current:
    return update

merged = current.copy()

for key, value in update.items():
    if value is None:
        continue
    
    if isinstance(merged.get(key), dict) and isinstance(value, dict):
        # Recursive merge
        merged[key] = self._merge_context(merged[key], value)
    else:
        # Replace
        merged[key] = value

return merged
text

**Criterios de aceptación:**
- [ ] Merge recursivo para nested dicts
- [ ] Preserva keys no actualizados
- [ ] Ignora None values

---

#### TAREA 1.2.3: Tests FSM v2 (1h)

**6 tests:**

@pytest.mark.asyncio
async def test_basic_transition():
"""Test transición básica exitosa."""
pass

@pytest.mark.asyncio
async def test_pre_callback_blocks_transition():
"""Test pre-callback False bloquea."""
pass

@pytest.mark.asyncio
async def test_post_callback_executes_on_success():
"""Test post-callback solo si éxito."""
pass

@pytest.mark.asyncio
async def test_error_callback_on_failure():
"""Test error-callback si falla."""
pass

@pytest.mark.asyncio
async def test_context_merge_nested_dicts():
"""Test merge recursivo."""
pass

@pytest.mark.asyncio
async def test_multiple_callbacks_execute_order():
"""Test orden ejecución múltiples callbacks."""
pass

text

**Criterios de aceptación:**
- [ ] 6/6 tests PASSING
- [ ] Coverage ≥85% state_machine.py

---

**ENTREGABLE BLOQUE 1.2:**
✅ FSM con callbacks pre/post/error
✅ Context merging inteligente
✅ 6/6 tests PASSING
✅ Coverage ≥85%
✅ Commit: "feat(h03): FSM Engine v2 callbacks - 6/6 tests"

text

---

**CHECKPOINT FASE 1:**
✅ CoreRouter v2: 6h | 8/8 tests
✅ FSM Engine v2: 4h | 6/6 tests
✅ TOTAL FASE 1: 10h | 14/14 tests PASSING
✅ Coverage ≥80% ambos componentes
✅ Performance <100ms CoreRouter verificado
✅ 2 commits exitosos
→ LISTO PARA FASE 2

text

---

## 🔵 FASE 2: NLP INTELLIGENCE (8h | 10 tests)

**Objetivo:** Intent Detector real con spaCy + español

---

### BLOQUE 2.1: Setup spaCy (1h)

#### TAREA 2.1.1: Instalación (30min)

Install spaCy
pip install spacy>=3.7.0

Download Spanish model
python -m spacy download es_core_news_sm

Verify
python -c "import spacy; nlp = spacy.load('es_core_news_sm'); print('✅ OK')"

Update requirements.txt
echo "spacy>=3.7.0" >> requirements.txt

text

**Criterios de aceptación:**
- [ ] spaCy instalado (≥3.7.0)
- [ ] Modelo español descargado
- [ ] Verificación exitosa
- [ ] requirements.txt actualizado

---

#### TAREA 2.1.2: Estructura ML (30min)

mkdir -p src/theaia/ml/intent_detector
touch src/theaia/ml/init.py
touch src/theaia/ml/intent_detector/init.py
touch src/theaia/ml/intent_detector/detector_v2.py
touch src/theaia/ml/intent_detector/training_data.py

text

**Criterios de aceptación:**
- [ ] Estructura `ml/` creada
- [ ] `__init__.py` en cada dir
- [ ] Archivos base creados

---

### BLOQUE 2.2: Intent Detector (5h)

**Archivos:**
- `src/theaia/ml/intent_detector/training_data.py`
- `src/theaia/ml/intent_detector/detector_v2.py`

#### TAREA 2.2.1: Training data (1h)

**9 intents con 50+ ejemplos cada uno:**

training_data.py
TRAINING_DATA = {
"create_event": [
"crear reunión mañana 15:00",
"agendar evento viernes",
"quiero crear cita médica",
"programar meeting lunes",
"nuevo evento jueves 10am",
# ... 45 más
],
"create_note": [
"crear nota importante",
"anotar idea proyecto",
"guardar recordatorio",
"nueva nota reunión",
# ... 46 más
],
"query_agenda": [
"qué tengo mañana",
"agenda próxima semana",
"eventos hoy",
"mi calendario jueves",
# ... 46 más
],
"help": [
"ayuda",
"cómo funciona",
"qué puedes hacer",
# ... 47 más
],
"greeting": [
"hola",
"buenos días",
"qué tal",
# ... 47 más
],
"farewell": [
"adiós",
"hasta luego",
"nos vemos",
# ... 47 más
],
"cancel": [
"cancelar",
"abortar",
"no quiero",
# ... 47 más
],
"confirm": [
"sí",
"confirmar",
"correcto",
# ... 47 más
],
"fallback": [
"sdkfjsdkfj",
"???",
"12345",
# ... 47 más
]
}

text

**Criterios de aceptación:**
- [ ] 9 intents definidos
- [ ] 50+ ejemplos por intent
- [ ] Variaciones naturales
- [ ] Casos edge incluidos

---

#### TAREA 2.2.2: Detector con spaCy (3h)

detector_v2.py
import spacy
from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class IntentDetectorV2:
"""Intent detector con spaCy + sklearn."""

text
def __init__(self):
    self.nlp = spacy.load("es_core_news_sm")
    self.vectorizer = TfidfVectorizer()
    self.classifier = MultinomialNB()
    self.intents = []
    self.trained = False

def train(self, training_data: Dict[str, List[str]]):
    """Entrena clasificador."""
    texts = []
    labels = []
    
    for intent, examples in training_data.items():
        texts.extend(examples)
        labels.extend([intent] * len(examples))
    
    # Vectorize con TF-IDF
    X = self.vectorizer.fit_transform(texts)
    
    # Train Naive Bayes
    self.classifier.fit(X, labels)
    
    self.intents = list(training_data.keys())
    self.trained = True

async def detect(self, text: str) -> Tuple[str, float]:
    """Detecta intent con confidence."""
    if not self.trained:
        return ("fallback", 0.0)
    
    # Preprocess con spaCy
    doc = self.nlp(text.lower())
    clean = " ".join([t.lemma_ for t in doc if not t.is_stop])
    
    # Vectorize
    X = self.vectorizer.transform([clean])
    
    # Predict
    proba = self.classifier.predict_proba(X)
    idx = proba.argmax()
    confidence = float(proba[idx])
    intent = self.classifier.classes_[idx]
    
    return (intent, confidence)
text

**Criterios de aceptación:**
- [ ] spaCy preprocesa (lemma + stop words)
- [ ] TF-IDF vectorization
- [ ] Naive Bayes classification
- [ ] Confidence 0-1
- [ ] Async interface

---

#### TAREA 2.2.3: Integration CoreRouter (1h)

Actualizar router.py
from theaia.ml.intent_detector.detector_v2 import IntentDetectorV2
from theaia.ml.intent_detector.training_data import TRAINING_DATA

class CoreRouter:
def init(self):
# Intent detector real
self.intent_detector = IntentDetectorV2()
self.intent_detector.train(TRAINING_DATA)

text
    # Entity pipeline
    self.entity_extractor = EntityExtractionPipeline()
text

**Criterios de aceptación:**
- [ ] CoreRouter usa IntentDetectorV2
- [ ] Training ejecuta en __init__
- [ ] No más mock en detect

---

### BLOQUE 2.3: Tests & Validation (2h)

**Archivos:**
- `src/theaia/tests/unit/ml/test_intent_detector_v2.py`

**10 tests:**

@pytest.mark.asyncio
async def test_detect_create_event():
"""'reunión mañana' → create_event, conf>0.8"""
pass

@pytest.mark.asyncio
async def test_detect_create_note():
"""'anotar' → create_note"""
pass

@pytest.mark.asyncio
async def test_detect_query_agenda():
"""'qué tengo hoy' → query_agenda"""
pass

@pytest.mark.asyncio
async def test_detect_help():
"""'ayuda' → help"""
pass

@pytest.mark.asyncio
async def test_detect_greeting():
"""'hola' → greeting"""
pass

@pytest.mark.asyncio
async def test_confidence_scoring():
"""Confidence entre 0-1"""
pass

@pytest.mark.asyncio
async def test_fallback_unknown():
"""'sdkfjsdkfj' → fallback"""
pass

@pytest.mark.asyncio
async def test_accuracy_80_percent():
"""Accuracy ≥80% en test set 100 ejemplos"""
pass

@pytest.mark.asyncio
async def test_spacy_preprocessing():
"""Lemmatization + stop words"""
pass

@pytest.mark.asyncio
async def test_training_all_intents():
"""9 intents entrenados"""
pass

text

**Criterios de aceptación:**
- [ ] 10/10 tests PASSING
- [ ] Accuracy ≥80% verificado
- [ ] Coverage ≥80%

---

**CHECKPOINT FASE 2:**
✅ Setup spaCy: 1h
✅ Intent Detector: 5h
✅ Tests: 2h | 10/10 tests PASSING
✅ TOTAL FASE 2: 8h | 10/10 tests
✅ Accuracy ≥80% documentado
✅ 3 commits exitosos
→ LISTO PARA FASE 3

text

---

## 🔵 FASE 3: INTEGRATION LAYER (8h | 14 tests)

**Objetivo:** Entity pipeline composition + Context Manager v2

---

### BLOQUE 3.1: Entity Pipeline (4h | 8 tests)

**Ya tenemos extractors (H03 anterior):**
- ✅ DateTimeExtractor (91%)
- ✅ LocationExtractor (100%)
- ✅ PersonNameExtractor (98%)

**Solo falta:**
- Composition pipeline
- Integration con CoreRouter
- Tests integration

#### TAREA 3.1.1: Composition pipeline (2h)

src/theaia/ml/entity_extractor/pipeline.py
class EntityExtractionPipeline:
"""Composition con intent-aware extraction."""

text
def __init__(self):
    self.date_extractor = DateTimeExtractor()
    self.location_extractor = LocationExtractor()
    self.person_extractor = PersonNameExtractor()

async def extract(self, text: str, intent: str) -> Dict:
    """Intent-aware extraction."""
    entities = {}
    
    if intent == "create_event":
        entities["dates"] = self.date_extractor.extract(text)
        entities["locations"] = self.location_extractor.extract(text)
    elif intent == "create_note":
        entities["persons"] = self.person_extractor.extract(text)
        entities["locations"] = self.location_extractor.extract(text)
    elif intent == "query_agenda":
        entities["dates"] = self.date_extractor.extract(text)
    
    # Fallback dates
    if "dates" not in entities:
        dates = self.date_extractor.extract(text)
        if dates:
            entities["dates"] = dates
    
    return entities
text

**Criterios:**
- [ ] Intent-aware implementado
- [ ] Fallback dates siempre
- [ ] Retorna dict (no None)

---

#### TAREA 3.1.2: Integration CoreRouter (1h)

Actualizar router.py
self.entity_extractor = EntityExtractionPipeline()

text

---

#### TAREA 3.1.3: Tests (1h)

**8 tests:**

async def test_pipeline_create_event_extracts_date_location()
async def test_pipeline_create_note_extracts_person_location()
async def test_pipeline_query_agenda_extracts_date()
async def test_pipeline_fallback_always_tries_dates()
async def test_pipeline_empty_results_not_none()
async def test_pipeline_composition_all_extractors()
async def test_pipeline_async_execution()
async def test_pipeline_router_integration()

text

**Criterios:**
- [ ] 8/8 tests PASSING
- [ ] Coverage ≥80%

---

### BLOQUE 3.2: Context Manager v2 (4h | 6 tests)

#### TAREA 3.2.1: Persistencia PostgreSQL (2h)

src/theaia/core/context_manager.py
class ContextManagerV2:
"""Context manager con persistencia DB."""

text
def __init__(self, conversation_repo):
    self.repo = conversation_repo
    self.cache: Dict[str, Context] = {}

async def load_context(
    self, 
    session_id: str, 
    user_id: int, 
    tenant_id: str
) -> Context:
    """Load desde DB o cache."""
    # Check cache
    if session_id in self.cache:
        return self.cache[session_id]
    
    # Load DB
    conv = await self.repo.get_by_session(session_id, tenant_id)
    
    if conv:
        context = self._conversation_to_context(conv)
    else:
        context = Context(
            user_id=user_id,
            tenant_id=tenant_id,
            session_id=session_id,
            state="idle",
            data={},
            history=[]
        )
    
    self.cache[session_id] = context
    return context

async def save_context(self, context: Context):
    """Save a DB y cache."""
    await self.repo.update_context(
        context.session_id,
        context.tenant_id,
        context.state,
        context.data,
        context.history
    )
    self.cache[context.session_id] = context
text

**Criterios:**
- [ ] Load desde DB o cache
- [ ] Save a DB y cache
- [ ] Session cache para performance

---

#### TAREA 3.2.2: Context windowing (1h)

async def prune_history(self, context: Context, max_messages: int = 10):
"""Mantiene últimos N mensajes."""
if len(context.history) > max_messages:
context.history = context.history[-max_messages:]
return context

text

---

#### TAREA 3.2.3: Tests (1h)

**6 tests:**

async def test_load_context_from_cache()
async def test_load_context_from_db()
async def test_load_context_create_new()
async def test_save_context_to_db_and_cache()
async def test_context_windowing_prune()
async def test_multi_session_isolation()

text

**Criterios:**
- [ ] 6/6 tests PASSING
- [ ] Coverage ≥80%

---

**CHECKPOINT FASE 3:**
✅ Entity Pipeline: 4h | 8/8 tests
✅ Context Manager v2: 4h | 6/6 tests
✅ TOTAL FASE 3: 8h | 14/14 tests PASSING
✅ 2 commits exitosos
→ LISTO PARA FASE 4

text

---

## 🔵 FASE 4: E2E VALIDATION (8-10h | 12 tests)

**Objetivo:** Integration tests + Demo NLP live

---

### BLOQUE 4.1: Integration Tests (6h | 12 tests)

**Archivos:**
- `src/theaia/tests/integration/test_h03_e2e_flow.py`

**12 tests E2E:**

@pytest.mark.asyncio
async def test_e2e_telegram_to_db_create_event():
"""Telegram → CoreRouter → EventsAgent → DB"""
pass

@pytest.mark.asyncio
async def test_e2e_telegram_to_db_create_note():
"""Telegram → CoreRouter → NotesAgent → DB"""
pass

@pytest.mark.asyncio
async def test_e2e_intent_detection_accuracy():
"""Intent accuracy ≥80% en 100 casos"""
pass

@pytest.mark.asyncio
async def test_e2e_entity_extraction_dates():
"""Entity extraction fechas correcta"""
pass

@pytest.mark.asyncio
async def test_e2e_multi_user_concurrent():
"""5 usuarios simultáneos sin race conditions"""
pass

@pytest.mark.asyncio
async def test_e2e_rate_limiting():
"""10 msg/s max por usuario"""
pass

@pytest.mark.asyncio
async def test_e2e_performance_under_500ms():
"""E2E <500ms por mensaje"""
pass

@pytest.mark.asyncio
async def test_e2e_error_handling_invalid_input():
"""Manejo errores inputs inválidos"""
pass

@pytest.mark.asyncio
async def test_e2e_context_persistence():
"""Context persiste entre sesiones"""
pass

@pytest.mark.asyncio
async def test_e2e_fsm_state_transitions():
"""Transiciones FSM correctas"""
pass

@pytest.mark.asyncio
async def test_e2e_tenant_isolation():
"""Multi-tenant isolation verificado"""
pass

@pytest.mark.asyncio
async def test_e2e_complete_conversation_flow():
"""Conversación completa end-to-end"""
pass

text

**Criterios:**
- [ ] 12/12 tests PASSING
- [ ] Performance <500ms E2E
- [ ] Multi-user verified
- [ ] Tenant isolation verified

---

### BLOQUE 4.2: Demo NLP Live (2-3h)

**Objetivo:** Primera conversación NLP funcional con usuario real

#### TAREA 4.2.1: Deploy completo (30min)

1. Verificar DB
psql -U thea_user -d thea_ia -c "SELECT count(*) FROM users;"

2. Verificar spaCy
python -c "import spacy; nlp = spacy.load('es_core_news_sm'); print('✅')"

3. Run bot
python src/theaia/adapters/telegram/run_bot.py

text

---

#### TAREA 4.2.2: Conversación real (1h)

**Usuario:** Entu (ID: 6961767622, ya registrado)

**Test conversación:**

Usuario: "Hola"
→ Intent: greeting
→ Agent: HelpAgent
→ Response: "¡Hola! ¿En qué puedo ayudarte?"

Usuario: "Quiero crear un evento mañana a las 15:00"
→ Intent: create_event (confidence >0.8)
→ Entities: {dates: ["mañana 15:00"]}
→ Agent: EventsAgent
→ FSM: idle → awaiting_event_details
→ DB: Evento creado
→ Response: "✅ Evento creado para mañana 15:00"

Usuario: "Gracias"
→ Intent: farewell
→ Agent: HelpAgent
→ Response: "¡Hasta luego!"

text

**Verificar en DB:**
SELECT * FROM events WHERE user_id = 6961767622 ORDER BY created_at DESC LIMIT 1;
SELECT * FROM conversations WHERE session_id = 'telegram_6961767622';

text

---

#### TAREA 4.2.3: Documentación demo (30min)

- [ ] Screenshots conversación
- [ ] Métricas performance (processing_time_ms)
- [ ] Video opcional
- [ ] Actualizar DIARY

---

**ENTREGABLE FASE 4:**
✅ 12/12 integration tests PASSING
✅ Demo NLP funcional con usuario real
✅ Evento creado end-to-end verificado
✅ Performance <500ms E2E
✅ Video/screenshots documentados
✅ Commit: "feat(h03): E2E validation complete - 12/12 tests + demo"

text

---

**CHECKPOINT FINAL H03:**
✅ FASE 1: 10h | 14/14 tests ✅
✅ FASE 2: 8h | 10/10 tests ✅
✅ FASE 3: 8h | 14/14 tests ✅
✅ FASE 4: 8h | 12/12 tests ✅
────────────────────────────────
✅ TOTAL: 36-40h | 50/50 tests (100%)
✅ Coverage ≥80% global
✅ Performance <500ms E2E
✅ Demo NLP funcional
✅ Primera conversación inteligente ✅
────────────────────────────────
🎉 H03 100% COMPLETADO

text

---

## 📊 RESUMEN MÉTRICAS FINALES

| Componente | Tests | Coverage | Performance |
|------------|-------|----------|-------------|
| CoreRouter | 8/8 | ≥80% | <100ms |
| FSM Engine v2 | 6/6 | ≥85% | N/A |
| Intent Detector | 10/10 | ≥80% | <50ms |
| Entity Pipeline | 8/8 | ≥80% | <30ms |
| Context Manager | 6/6 | ≥80% | N/A |
| Integration E2E | 12/12 | N/A | <500ms |
| **TOTAL** | **50/50** | **≥80%** | **<500ms** |

---

## 🎯 CRITERIOS DONE H03

**H03 NO se considera DONE hasta:**

- [ ] 50/50 tests PASSING (100%)
- [ ] Coverage ≥80% en TODOS los componentes
- [ ] Performance <100ms CoreRouter verificado
- [ ] Performance <500ms E2E verificado
- [ ] Intent accuracy ≥80% documentado
- [ ] Demo NLP funcional con usuario real
- [ ] Evento creado end-to-end verificado en DB
- [ ] Documentación actualizada (DIARY + README)
- [ ] Todos los commits pusheados a GitHub
- [ ] CHECKLIST_H03_ACTUAL.md actualizado a 100%

---

## 🚀 PRÓXIMO PASO DESPUÉS DE H03

**Una vez H03 100% completado:**

1. Actualizar ROADMAP maestro con H03 ✅
2. Cerrar milestone H03 en GitHub
3. Planificar H04: Persistencia Avanzada (~40h)
4. Actualizar DIARY con métricas H03
5. Celebrar primera conversación NLP inteligente 🎉

---

**Creado:** 20 Noviembre 2025, 23:24 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA-IA)  
**Versión:** v1.0.0  
**Status:** ✅ LISTO PARA USO

---

**Filosofía THEA-IA 100x100:**
> "No decimos completado hasta que TODO esté hecho: tests, coverage, performance, demo y documentación. Sin excepciones."
