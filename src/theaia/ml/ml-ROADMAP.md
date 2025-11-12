Roadmap - src/ml/
Módulo: ML/NLP (Machine Learning)
Versión actual: 0.1.0 (H01 - Placeholder)
Próxima versión: 0.6.0 (H06 - Primera Implementación)

📊 Estado Actual (11 Nov 2025 - H01)
Completado ✅
Estructura módulo definida

Dependencias identificadas

Documentación placeholder completa

Pendiente ⏳
TODO en H06 - Este módulo NO se implementa antes de H06

⏸️ H02-H05: NO IMPLEMENTAR
Este módulo es placeholder hasta H06.

En H02-H05 usar:

Regex patterns para intent classification

Keywords para entity extraction

Reglas simples hardcoded

🎯 H06 (24-27 Nov 2025): NLP Implementation
Objetivo: Inteligencia conversacional con NLP

Día 1 (24 Nov):
NLP Service Base:

nlp_service.py

Clase NLPService(singleton)

Load spaCy model

Basic preprocessing

Intent Classification:

intent_classifier.py

Clasificar: create_reminder, create_note, create_event, create_task, query, help

Train con ejemplos etiquetados

Accuracy >85%

Día 2 (25 Nov):
Entity Extraction:

entity_extractor.py

Extraer: datetime, event_name, priority, tags

spaCy NER + custom patterns

Context-aware extraction

Día 3 (26-27 Nov):
Integration:

Integrar con CoreManager

Replace regex logic con NLP

Fallback a reglas si confidence baja

Tests NLP pipeline

Criterios Done H06:
✅ spaCy model cargado

✅ Intent classification >85% accuracy

✅ Entity extraction funciona

✅ Integration CoreManager OK

✅ Fallback logic funciona

✅ Performance <100ms per query

✅ Tests >80% coverage

🔮 H09 (Ene 2026): Advanced NLP
Fine-tuning:

Custom spaCy model entrenado con datos THEA IA

User-specific patterns learning

Multilingual support (es, en)

Advanced Features:

Context-aware responses

Sentiment analysis

Summarization

Question answering

📈 Métricas de Éxito
Hito	Features	Accuracy	Latency
H06	Intent + Entities	>85%	<100ms
H09	+ Context	>90%	<100ms
H12	+ Custom models	>95%	<50ms
🚧 Riesgos
Riesgo 1: Accuracy insuficiente
Mitigación: Fallback a reglas simples

Riesgo 2: Latency alta
Mitigación: Model caching, async loading

Riesgo 3: Memory footprint grande
Mitigación: Small spaCy models (sm vs lg)

📝 Decisiones Técnicas
¿Por qué spaCy vs transformers?
spaCy más rápido

Menor memoria

Suficiente para casos uso THEA IA

Transformers si necesario en H09+

¿Por qué no implementar antes H06?
Reglas simples suficientes para MVP

NLP añade complejidad

Mejor optimizar primero flujos básicos

Última actualización: 11 Nov 2025
Próxima revisión: H06 start (24 Nov 2025)
Responsable: Álvaro Fernández Mota