Changelog - src/ml/
Placeholder Module - No se implementa hasta H06

[Unreleased]
Planificado para H06 (24-27 Nov 2025)
NLP Service base (spaCy)

Intent classification

Entity extraction (NER)

Integration con CoreManager

Planificado para H09 (Ene 2026)
Custom trained models

Context-aware processing

Multilingual support

Sentiment analysis

[0.6.0] - 2025-11-27 (H06 Target)
Added
nlp_service.py:

NLPService clase singleton

Load spaCy model (es_core_news_sm)

Text preprocessing pipeline

intent_classifier.py:

classify_intent(text) → str

Train con ejemplos etiquetados

Intents: create_reminder, create_note, create_event, create_task, query, help

Accuracy target: >85%

entity_extractor.py:

extract_entities(text) → dict

Entities: datetime, event_name, priority, tags, location

spaCy NER + custom patterns

Context-aware extraction

Tests:

test_nlp_service.py

test_intent_classifier.py

test_entity_extractor.py

Coverage >80%

Dependencies
spacy==3.7.2

es-core-news-sm (spaCy model)

[0.1.0] - 2025-11-03 (H01)
Added
Estructura placeholder

Documentación:

README.md (placeholder)

ROADMAP.md

CHANGELOG.md (este archivo)

STRUCTURE.md

DEPENDENCIES.md

Planning
H06: NLP implementation

H09: Advanced NLP

Nota: Este módulo es placeholder hasta H06. No implementar antes.

Última actualización: 11 Nov 2025
Responsable: Álvaro Fernández Mota