# 🔍 AUDITORÍA ML COMPONENTS - THEA IA

**Fecha:** 03 Diciembre 2025  
**Versión:** 1.0  
**Auditor:** Equipo THEA IA (Perplexity AI + Lead Developer)  
**Objetivo:** Analizar componentes Machine Learning para MVP

---

## 📊 RESUMEN EJECUTIVO

### Componentes Analizados: 4

| Componente | LOC | Estado | Decisión |
|------------|-----|--------|----------|
| **EntityExtractor** | 150 | ✅ BUENO | 🟢 MANTENER |
| **IntentDetector (nuevo)** | 250 | ✅ BUENO | 🟢 MANTENER |
| **IntentDetector (legacy)** | 80 | ⚠️ LEGACY | 🔴 DELETE |
| **NLPPipeline** | 25 | ✅ BUENO | 🟢 OPTIMIZAR |

### Decisiones Tomadas: 4

- 🟢 **MANTENER:** 2 componentes (EntityExtractor, IntentDetector nuevo)
- 🟢 **OPTIMIZAR:** 1 componente (NLPPipeline)
- 🔴 **DELETE:** 1 componente (IntentDetector legacy)

### Hallazgos Clave

- ✅ **ML components bien implementados** (spaCy + sklearn)
- 🔴 **Duplicación crítica** - 2 Intent Detectors diferentes
- ✅ **Training data completo** - 320 ejemplos, 8 intents
- ⚠️ **Threshold bajo** - 0.3 (debería ser 0.5)
- ✅ **Hybrid approach** - ML + regex fallback

---

## 🎯 MATRIZ DE DECISIONES

| Componente | LOC | Modelo | Training | Tests | MVP? | Decisión | Prioridad |
|------------|-----|--------|----------|-------|------|----------|-----------|
| **EntityExtractor** | 150 | spaCy NER | N/A | ❓ | ✅ SÍ | 🟢 MANTENER | P0 |
| **IntentDetector (nuevo)** | 250 | TF-IDF + LogReg | 320 ejs | ❓ | ✅ SÍ | 🟢 MANTENER | P0 |
| **IntentDetector (legacy)** | 80 | LinearSVC | 8 ejs | ❓ | ❌ NO | 🔴 DELETE | - |
| **NLPPipeline** | 25 | Wrapper | N/A | ❓ | ✅ SÍ | 🟢 OPTIMIZAR | P1 |

**Leyenda:**
- P0 = Prioridad crítica MVP
- P1 = Prioridad alta MVP

---

## 📋 ANÁLISIS DETALLADO POR COMPONENTE

### 1. EntityExtractor ✅ MVP

**Ubicación:** `src/theaia/ml/entity_extractor/pipeline.py`

**Estado Actual:**
- **LOC:** 150 líneas
- **Modelo:** spaCy `es_core_news_sm` (NER español)
- **Fallback:** Regex patterns personalizados
- **Tests:** ❓ Desconocido

**Funcionalidad:**
class EntityExtractor:
def init(self):
try:
self.nlp = spacy.load("es_core_news_sm") # ✅ ML
except:
self.nlp = None # ⚠️ Silent fallback

text
    # Custom patterns
    self.date_patterns = [...]  # 10+ patterns
    self.time_patterns = [...]  # 8+ patterns

def extract(self, text: str) -> Dict:
    # 1. spaCy NER (ML)
    entities = {'DATE': [], 'TIME': [], 'PERSON': [], 'LOCATION': []}
    
    # 2. Custom regex (fallback)
    # Patterns para fechas/tiempos en español
text

**Capacidades:**
- ✅ **4 tipos de entidades:** DATE, TIME, PERSON, LOCATION
- ✅ **Hybrid approach:** spaCy NER + regex patterns
- ✅ **Confidence scores:** 0.85-0.95
- ✅ **Batch processing:** `extract_batch()`
- ✅ **Intent-aware:** `extract_intent_aware()`

**Problemas:**
1. ⚠️ **Silent fallback** si spaCy no instalado
2. ⚠️ **No logging** de errores
3. ❓ **No tests unitarios** (probablemente)

**Decisión:** 🟢 **MANTENER Y MEJORAR**

**Plan FASE 2:**
Target: Añadir robustez y tests
class EntityExtractor:
def init(self, logger=None):
self.logger = logger or logging.getLogger(name)

text
    try:
        self.nlp = spacy.load("es_core_news_sm")
        self.logger.info("✅ spaCy model loaded")
    except Exception as e:
        self.logger.warning(f"⚠️ spaCy not available: {e}")
        self.nlp = None

def extract(self, text: str) -> Dict:
    if not self.nlp:
        self.logger.debug("Using regex-only extraction")
    # ... resto del código
text

**Añadir:**
- ✅ Logging (warnings si spaCy falla)
- ✅ 10 tests unitarios (spaCy + regex)
- ✅ Test fallback si spaCy no disponible
- ✅ Validación de input

**Target:** Tests 0 → 10+

---

### 2. IntentDetector (NUEVO) ✅ MVP

**Ubicación:** `src/theaia/ml/intent_detector/detector.py`

**Estado Actual:**
- **LOC:** 250 líneas
- **Modelo:** TF-IDF + Logistic Regression
- **Training:** 320 ejemplos (40 por intent)
- **Intents:** 8 (create_event, create_note, create_reminder, query_agenda, help, schedule_task, fallback, delete_item)
- **Threshold:** 0.3 (⚠️ bajo)
- **Tests:** ❓ Desconocido

**Arquitectura:**
class IntentDetector:
def init(self, confidence_threshold: float = 0.3):
self.vectorizer = TfidfVectorizer(
max_features=500,
ngram_range=(1, 2), # Unigrams + bigrams
lowercase=True,
strip_accents=None,
analyzer='word'
)

text
    self.classifier = LogisticRegression(
        max_iter=1000,
        random_state=42,
        multi_class='multinomial',
        solver='lbfgs'
    )
    
    self.confidence_threshold = 0.3  # ⚠️ BAJO
text

**Funcionalidad:**
- ✅ **train()** - Entrena modelo con training data
- ✅ **predict()** - Predice intent con confidence
- ✅ **predict_batch()** - Predicción múltiple
- ✅ **predict_top_n()** - Top N intents más probables
- ✅ **save() / load()** - Persistencia del modelo
- ✅ **get_feature_importance()** - Palabras importantes por intent

**Training Data:**
TRAINING_DATA = {
"create_event": 40 ejemplos,
"create_note": 40 ejemplos,
"create_reminder": 40 ejemplos,
"query_agenda": 40 ejemplos,
"help": 40 ejemplos,
"schedule_task": 40 ejemplos,
"fallback": 40 ejemplos,
"delete_item": 40 ejemplos,
}

Total: 320 ejemplos
text

**Métricas Entrenamiento:**
- ✅ **Train/Test split:** 80/20
- ✅ **Stratified sampling**
- ✅ **Classification report**
- ✅ **Accuracy score**

**Problemas:**
1. ⚠️ **Threshold 0.3 muy bajo** (debería ser 0.5)
2. ⚠️ **Entrena cada vez** (no carga modelo pre-entrenado)
3. ❓ **No tests unitarios** con training data
4. ⚠️ **No validation set** (solo train/test)

**Decisión:** 🟢 **MANTENER Y MEJORAR**

**Plan FASE 2:**
Cambios recomendados
class IntentDetector:
def init(self, confidence_threshold: float = 0.5): # ✅ Subir threshold
# ... configuración
self.confidence_threshold = 0.5 # NUEVO (era 0.3)

text
def train(self, test_size: float = 0.2, val_size: float = 0.1):
    # ✅ NUEVO: Añadir validation set
    X_train, X_temp, y_train, y_temp = train_test_split(...)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, ...)
    
    # Entrenar y validar
    # ...
text

**Añadir:**
- ✅ Subir threshold 0.3 → 0.5
- ✅ Validation set (train/val/test: 70/15/15)
- ✅ 15 tests unitarios
- ✅ Cachear modelo entrenado
- ✅ Cross-validation

**Target:** Threshold 0.5, Tests 0 → 15+

---

### 3. IntentDetector (LEGACY) ❌ ELIMINAR

**Ubicación:** `src/theaia/ml/intent_detector/intent_detector_fallback.py`

**Estado Actual:**
- **LOC:** 80 líneas
- **Modelo:** LinearSVC (legacy)
- **Training:** 8 ejemplos (insuficiente)
- **Fallback:** Keywords hardcoded
- **Tests:** ❓ Desconocido

**Arquitectura:**
class IntentDetector:
def init(self, model_filename: str = "model_intent.pkl"):
# Carga modelo LinearSVC viejo
self.model = joblib.load(model_path)

text
    # Keywords hardcoded
    self.keywords = {
        "nota": ["nota", "anota", "apunta", ...],
        "ayuda": ["ayuda", "help", ...],
        "evento": ["evento", "cita", ...],
        # ... etc
    }

def detect(self, text: str) -> str:
    # 1. Intenta ML
    if self.model:
        intent = self.model.predict([text])
    
    # 2. Fallback a keywords
    for intent, kws in self.keywords.items():
        if any(kw in msg for kw in kws):
            return intent
text

**PROBLEMA CRÍTICO:** 🔴 **DUPLICACIÓN**

| Aspecto | IntentDetector NUEVO | IntentDetector LEGACY |
|---------|---------------------|----------------------|
| **Modelo** | TF-IDF + LogReg | LinearSVC |
| **Training** | 320 ejemplos | 8 ejemplos |
| **Threshold** | 0.3 configurable | No configurable |
| **Fallback** | fallback intent | Keywords |
| **Usado por** | Router nuevo (H03) | Router antiguo |
| **Estado** | ✅ Activo | ⚠️ Obsoleto |

**Razón Eliminación:**
1. 🔴 **Duplicación** - 2 detectores haciendo lo mismo
2. ⚠️ **Training insuficiente** - Solo 8 ejemplos vs 320
3. ⚠️ **Keywords hardcoded** - No escalable
4. ⚠️ **Modelo viejo** - LinearSVC menos robusto que LogReg
5. ✅ **Nuevo es superior** - Mejor arquitectura, más datos

**Decisión:** 🔴 **DELETE COMPLETO**

**Plan FASE 2:**
Eliminar archivo legacy
rm src/theaia/ml/intent_detector/intent_detector_fallback.py

Actualizar imports en router antiguo
Cambiar de legacy a nuevo detector
text

**Action:**
- 🔴 DELETE archivo completo
- 🔴 Actualizar imports router antiguo
- ✅ Migrar a IntentDetector nuevo

---

### 4. NLPPipeline 🟢 OPTIMIZAR

**Ubicación:** `src/theaia/ml/intent_detector/router_integration.py`

**Estado Actual:**
- **LOC:** 25 líneas
- **Función:** Wrapper unificado Intent + Entities
- **Tests:** ❓ Desconocido

**Arquitectura:**
class NLPPipeline:
def init(self, confidence_threshold: float = 0.3):
# ⚠️ Entrena cada vez (ineficiente)
self.intent_detector = create_and_train_detector(
confidence_threshold,
verbose=False
)
self.entity_extractor = EntityExtractor()

text
def process(self, text: str) -> Dict:
    # 1. Detectar intent
    intent, confidence = self.intent_detector.predict(text)
    
    # 2. Extraer entidades
    entities = self.entity_extractor.extract(text)
    
    # 3. Retornar todo junto
    return {
        'intent': intent,
        'confidence': confidence,
        'entities': entities,
        'text': text
    }

def process_batch(self, texts: list) -> list:
    return [self.process(text) for text in texts]
text

**Funcionalidad:**
- ✅ **API unificada** - Intent + Entities en un llamado
- ✅ **Batch processing** - Múltiples textos
- ✅ **Simple integration** - Fácil de usar

**Problemas:**
1. ⚠️ **Entrena cada vez** - `create_and_train_detector()` en `__init__`
2. ⚠️ **No lazy loading** - Carga spaCy siempre
3. ⚠️ **No caching** - Re-entrena modelo cada instancia
4. ❓ **No tests E2E** pipeline completo

**Decisión:** 🟢 **MANTENER Y OPTIMIZAR**

**Plan FASE 2:**
Target: Cachear modelo y lazy loading
class NLPPipeline:
_cached_intent_detector = None # ✅ NUEVO: Cache class-level

text
def __init__(self, confidence_threshold: float = 0.5):
    # ✅ NUEVO: Cargar modelo pre-entrenado
    if NLPPipeline._cached_intent_detector is None:
        model_path = "models/intent_detector.pkl"
        if os.path.exists(model_path):
            self.intent_detector = IntentDetector()
            self.intent_detector.load(model_path)
            NLPPipeline._cached_intent_detector = self.intent_detector
        else:
            # Entrenar solo si no existe modelo
            self.intent_detector = create_and_train_detector(...)
            self.intent_detector.save(model_path)
    else:
        self.intent_detector = NLPPipeline._cached_intent_detector
    
    # ✅ NUEVO: Lazy loading EntityExtractor
    self.entity_extractor = None

def _get_entity_extractor(self):
    if self.entity_extractor is None:
        self.entity_extractor = EntityExtractor()
    return self.entity_extractor

def process(self, text: str) -> Dict:
    intent, confidence = self.intent_detector.predict(text)
    entities = self._get_entity_extractor().extract(text)
    return {...}
text

**Añadir:**
- ✅ Cachear modelo entrenado (class-level)
- ✅ Lazy loading EntityExtractor
- ✅ Pre-entrenar modelo en CI/CD
- ✅ 8 tests E2E pipeline completo
- ✅ Benchmarking performance

**Target:** Performance boost 10x, Tests 0 → 8+

---

## 📊 HALLAZGOS GENERALES

### Fortalezas ✅

1. **Arquitectura sólida** - spaCy + sklearn bien integrados
2. **Hybrid approach** - ML + regex fallback robusto
3. **Training data completo** - 320 ejemplos, 8 intents
4. **API simple** - NLPPipeline fácil de usar
5. **Modularidad** - Componentes bien separados

### Debilidades ⚠️

1. **Duplicación crítica** - 2 Intent Detectors
2. **Threshold bajo** - 0.3 debería ser 0.5
3. **No caching** - Entrena modelo cada vez
4. **Tests ausentes** - Coverage probablemente 0%
5. **Silent failures** - No logging de errores

### Riesgos 🔴

1. **Confusión arquitectura** - ¿Cuál detector usar?
2. **Performance** - Entrena cada instancia (lento)
3. **Mantenibilidad** - Legacy code sin tests
4. **Escalabilidad** - Keywords hardcoded no escalan

---

## 🎯 ROADMAP MVP - ML COMPONENTS

### FASE 2 (H04-H05) - Limpieza y Tests

**H04.1 — Delete Legacy IntentDetector**
- 🔴 Eliminar `intent_detector_fallback.py`
- 🔴 Actualizar imports router antiguo
- ✅ Migrar a detector nuevo

**H04.2 — Optimizar NLPPipeline**
- ✅ Cachear modelo entrenado
- ✅ Lazy loading EntityExtractor
- ✅ Pre-entrenar modelo en CI/CD
- ✅ Benchmarking

**H05 — Tests Unitarios ML**
- ✅ 10 tests EntityExtractor
- ✅ 15 tests IntentDetector
- ✅ 8 tests NLPPipeline E2E
- Target: Coverage 85%+

---

### FASE 3 (H06-H10) - Mejoras y Robustez

**H06 — Logging y Monitoreo**
- ✅ Logging completo EntityExtractor
- ✅ Logging completo IntentDetector
- ✅ Métricas de confianza

**H07 — Threshold Optimization**
- ✅ Subir threshold 0.3 → 0.5
- ✅ Validation set (train/val/test)
- ✅ Cross-validation

**H08 — Feature Engineering**
- ✅ Añadir n-grams adicionales
- ✅ Experimentar con modelos (RF, XGBoost)
- ✅ Hyperparameter tuning

---

### FASE 4 (POST-MVP) - Escalabilidad

**Features avanzados:**
- 🟡 Contextual embeddings (BERT español)
- 🟡 Active learning (feedback loop)
- 🟡 Multi-language support
- 🟡 Entity linking (knowledge graph)
- 🟡 Intent disambiguation

---

## 📈 MÉTRICAS ÉXITO MVP

### Coverage Targets

| Componente | Actual | Target MVP | Target POST-MVP |
|------------|--------|------------|-----------------|
| **EntityExtractor** | ❓ 0%? | 85%+ | 95%+ |
| **IntentDetector** | ❓ 0%? | 85%+ | 95%+ |
| **NLPPipeline** | ❓ 0%? | 85%+ | 95%+ |

### Performance Targets

| Métrica | Actual | Target MVP |
|---------|--------|------------|
| **Intent Accuracy** | ❓ | 90%+ |
| **Entity Precision** | ❓ | 85%+ |
| **Inference Time** | ❓ | <50ms |
| **Model Load Time** | ❓ | <1s |

### Quality Targets

| Aspecto | Actual | Target MVP |
|---------|--------|------------|
| **Tests Unitarios** | ❓ 0 | 33+ |
| **Logging** | ❌ NO | ✅ SÍ |
| **Caching** | ❌ NO | ✅ SÍ |
| **Documentation** | ⚠️ Parcial | ✅ Completa |

---

## 💡 CONCLUSIONES

### Estado General: 🟢 **BUENO CON MEJORAS NECESARIAS**

**Los componentes ML están bien diseñados** pero requieren:
1. 🔴 **Eliminar duplicación** (2 Intent Detectors)
2. 🟢 **Optimizar performance** (caching)
3. ✅ **Añadir tests** (coverage 0% → 85%+)
4. ✅ **Mejorar robustez** (logging, threshold)

### Prioridades Inmediatas

1. **P0 - DELETE Legacy IntentDetector** (bloquea arquitectura)
2. **P0 - Cachear modelo** (bloquea performance)
3. **P1 - Tests unitarios** (bloquea confiabilidad)
4. **P1 - Subir threshold** (mejora accuracy)

### Micro-recompensas Completadas

- ✅ **BLOQUE 1.2 completado** (+3 puntos)
- ✅ **4 componentes auditados**
- ✅ **Duplicación detectada**
- ✅ **Roadmap ML definido**

---

## 📝 PRÓXIMOS PASOS

**Inmediato (siguiente sesión):**
- [ ] BLOQUE 1.3 — Auditoría Adapters (2 puntos)
- [ ] BLOQUE 1.4 — Auditoría Core (2 puntos)

**FASE 2 (H04-H05):**
- [ ] Delete Legacy IntentDetector
- [ ] Optimizar NLPPipeline
- [ ] Tests Unitarios ML (33+)

**FASE 3 (H06-H10):**
- [ ] Logging y monitoreo
- [ ] Threshold optimization
- [ ] Feature engineering

---

**Auditoría ML completada. Sistema ML bien diseñado, requiere limpieza y tests.** 🎯

---

**Progreso FASE 1:** 11/15 puntos (73.3%)