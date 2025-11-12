src/ml/ - Machine Learning Module
Módulo NLP y Machine Learning (H06)

📋 Overview
PLACEHOLDER H06 - Este módulo se implementará en H06 (24-27 Nov).

Funcionalidades ML/NLP para THEA IA:

🧠 NLP Service: Procesamiento lenguaje natural

🎯 Intent Classification: Clasificar intención usuario

📝 Entity Extraction: Extraer entidades (fechas, nombres, etc)

🤖 ML Models: Modelos entrenados custom

🎯 Propósito (H06)
Mejorar inteligencia conversacional:

Entender lenguaje natural flexible

Clasificar intención sin comandos rígidos

Extraer información automáticamente

Personalización por usuario

📁 Estructura Planificada (H06)
text
src/ml/
├── __init__.py
├── nlp_service.py          # Servicio NLP principal
├── intent_classifier.py    # Clasificación intenciones
├── entity_extractor.py     # Extracción entidades (NER)
├── models/                 # Modelos entrenados
│   ├── intent_model.pkl
│   └── ner_model.pkl
├── training/               # Scripts entrenamiento
│   ├── train_intent.py
│   └── train_ner.py
└── README.md
📦 Dependencias Planificadas
text
spacy==3.7.2                # NLP framework
es-core-news-sm==3.7.0      # Spanish model
scikit-learn==1.3.2         # ML tradicional
numpy==1.26.2
💡 Uso Planificado (H06)
python
# En CoreManager (H06)
from src.ml import NLPService

nlp = NLPService()

# Clasificar intención
intent = nlp.classify_intent("recuérdame reunión mañana")
# → "create_reminder"

# Extraer entidades
entities = nlp.extract_entities("reunión mañana 15:00")
# → {"event": "reunión", "datetime": "tomorrow 15:00"}

# Process completo
result = nlp.process("recuérdame reunión mañana 15:00")
# → {
#     "intent": "create_reminder",
#     "entities": {
#         "title": "reunión",
#         "datetime": datetime(2025, 11, 12, 15, 0)
#     },
#     "confidence": 0.92
# }
🎯 Features H06
Intent Classification:
Intents soportados:

create_reminder - Crear recordatorio

create_note - Crear nota

create_event - Crear evento

create_task - Crear tarea

query - Consultar información

help - Ayuda

Entity Extraction:
Entities extraídas:

datetime - Fechas y horas

event_name / title - Nombre evento/recordatorio

priority - Prioridad (low, medium, high)

tags - Hashtags o categorías

location - Ubicación

🔄 Flujo (H06)
text
User Message: "recuérdame reunión mañana 15:00"
        ↓
NLPService.process()
        ↓
    ┌───┴───┐
    ↓       ↓
Intent   Entities
"create" {"title": "reunión",
reminder  "datetime": ...}
    ↓       ↓
    └───┬───┘
        ↓
CoreManager → ReminderAgent
        ↓
   Create Reminder
📈 Métricas Objetivo (H06)
Métrica	Target	Notas
Intent Accuracy	>85%	Test set etiquetado
Entity Precision	>80%	Datetime crítico
Latency	<100ms	Process completo
Memory	<100MB	spaCy model sm
⚠️ Antes de H06
NO IMPLEMENTAR ESTE MÓDULO ANTES DE H06.

En H02-H05 usar:

Regex patterns para intent classification

Keywords para entity extraction

Reglas simples hardcoded

python
# H02-H05: Regex simple
if "recuerd" in message.lower() or "recordatorio" in message.lower():
    intent = "create_reminder"

# H06+: NLP
intent = nlp.classify_intent(message)
🔮 Roadmap
H06 (24-27 Nov):
spaCy NLP Service

Intent classification >85%

Entity extraction básico

Fallback a reglas simples

H09 (Ene 2026):
Custom trained models con datos THEA IA

Context-aware processing

Multilingual support (es, en)

Sentiment analysis

H12+ (Mar 2026):
User-specific learning

Advanced NER

Summarization

Question answering

🧪 Testing (H06)
python
# tests/unit/test_ml/test_intent_classifier.py
def test_intent_reminder():
    classifier = IntentClassifier()
    
    texts = [
        "recuérdame reunión",
        "recordatorio mañana",
        "avísame cuando"
    ]
    
    for text in texts:
        intent = classifier.classify(text)
        assert intent == "create_reminder"

def test_intent_confidence():
    classifier = IntentClassifier()
    confidence = classifier.confidence("recuérdame reunión")
    assert confidence > 0.7  # High confidence
📚 Recursos
spaCy Docs

spaCy Spanish Models

spaCy Training

🎯 Decisiones Técnicas
¿Por qué spaCy vs transformers?
spaCy más rápido (<100ms)

Menor memoria (~50MB vs ~500MB)

Suficiente para casos uso THEA IA

Transformers si necesario en H09+

¿Por qué no implementar antes H06?
Reglas simples suficientes para MVP (H02-H05)

NLP añade complejidad

Mejor optimizar primero flujos básicos

Evaluar necesidad real con usuarios

⏭️ Próximos Pasos
✅ H02-H05: Implementar con regex (simple, funcional)

📊 Evaluar: ¿Usuarios piden más flexibilidad?

🎯 H06: Si necesario, implementar NLP

📈 Medir: Accuracy antes/después NLP

Estado: Placeholder
Implementar en: H06 (24-27 Nov 2025)
Versión: 0.1.0
Última actualización: 11 Nov 2025
Responsable: Álvaro Fernández Mota