Estructura Planificada - src/ml/
Módulo: ML/NLP
Propósito: Inteligencia conversacional
Patrón: Singleton NLP Service

⚠️ PLACEHOLDER - NO implementar antes H06

📋 Estado Actual (11 Nov 2025 - H01)
text
src/ml/
├── __init__.py (placeholder)
├── README.md ✅
├── ROADMAP.md ✅
├── CHANGELOG.md ✅
├── STRUCTURE.md ✅ (este archivo)
└── DEPENDENCIES.md ✅
Estado: Placeholder, sin implementación

🎯 H06 (24-27 Nov): NLP Implementation
Estructura Objetivo:
text
src/ml/
│
├── __init__.py
│   # Exports: NLPService
│   from .nlp_service import NLPService
│
├── nlp_service.py ← 🆕 H06 DÍA 1
│   # Servicio NLP principal
│   #
│   # class NLPService:
│   #     """Singleton NLP service"""
│   #     _instance = None
│   #     
│   #     def __init__(self):
│   #         self.nlp = spacy.load("es_core_news_sm")
│   #         self.intent_classifier = IntentClassifier()
│   #         self.entity_extractor = EntityExtractor()
│   #     
│   #     def process(self, text: str) -> dict:
│   #         """Procesa texto y retorna intent + entities"""
│   #         intent = self.intent_classifier.classify(text)
│   #         entities = self.entity_extractor.extract(text)
│   #         return {"intent": intent, "entities": entities}
│
├── intent_classifier.py ← 🆕 H06 DÍA 1
│   # Clasificación intención
│   #
│   # class IntentClassifier:
│   #     def __init__(self):
│   #         self.model = self._load_model()
│   #     
│   #     def classify(self, text: str) -> str:
│   #         """
│   #         Clasifica intención usuario.
│   #         
│   #         Returns:
│   #             - "create_reminder"
│   #             - "create_note"
│   #             - "create_event"
│   #             - "create_task"
│   #             - "query"
│   #             - "help"
│   #         """
│   #         pass
│   #     
│   #     def confidence(self, text: str) -> float:
│   #         """Retorna confidence score 0-1"""
│   #         pass
│
├── entity_extractor.py ← 🆕 H06 DÍA 2
│   # Extracción entidades (NER)
│   #
│   # class EntityExtractor:
│   #     def __init__(self):
│   #         self.nlp = spacy.load("es_core_news_sm")
│   #     
│   #     def extract(self, text: str) -> dict:
│   #         """
│   #         Extrae entidades del texto.
│   #         
│   #         Returns:
│   #             {
│   #                 "datetime": datetime | None,
│   #                 "event_name": str | None,
│   #                 "priority": str | None,
│   #                 "tags": list[str],
│   #                 "location": str | None
│   #             }
│   #         """
│   #         pass
│
├── models/ ← 🆕 H06 DÍA 1
│   │
│   ├── intent_model.pkl
│   │   # Modelo entrenado intent classification
│   │
│   └── training_data.json
│       # Ejemplos etiquetados para training
│       # [
│       #   {"text": "recuérdame reunión mañana", "intent": "create_reminder"},
│       #   {"text": "nota importante", "intent": "create_note"},
│       #   ...
│       # ]
│
├── training/ ← 🆕 H06 DÍA 3 (opcional)
│   │
│   ├── train_intent.py
│   │   # Script entrenar modelo intent
│   │
│   └── evaluate.py
│       # Script evaluar accuracy
│
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── STRUCTURE.md (este archivo)
└── DEPENDENCIES.md
📐 Arquitectura
text
User Message → NLPService.process()
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
IntentClassifier        EntityExtractor
        ↓                       ↓
  "create_reminder"    {"datetime": ..., "title": ...}
        ↓                       ↓
        └───────────┬───────────┘
                    ↓
            CoreManager router
                    ↓
            Appropriate Agent
🔗 Dependencias Internas
text
src/ml/ depende de:
└── [Ninguna - módulo independiente]
text
src/ml/ es usado por:
└── src/core/ (CoreManager usa NLPService)
📊 Métricas H06
Archivos: 3-4 archivos Python

LOC: ~400

Tests LOC: ~300

Accuracy: >85%

Latency: <100ms

🎯 Criterios Completitud H06
✅ spaCy model cargado

✅ Intent classification funciona

✅ Entity extraction funciona

✅ Accuracy >85%

✅ Latency <100ms

✅ Fallback a reglas simples

✅ Tests >80% coverage

✅ Integration CoreManager OK

⚠️ NO IMPLEMENTAR ANTES DE H06

En H02-H05: Usar regex + keywords simples

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota