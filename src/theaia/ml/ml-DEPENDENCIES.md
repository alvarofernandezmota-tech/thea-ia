Dependencias - src/ml/
Módulo: ML/NLP
Versión actual: 0.1.0 (H01 - Placeholder)
Próxima versión: 0.6.0 (H06 - Primera Implementación)

⚠️ PLACEHOLDER - NO instalar deps antes H06

📦 Dependencias Python
H06 (24-27 Nov): NLP Base
Producción:
text
# NLP Framework
spacy==3.7.2                    # NLP core
es-core-news-sm==3.7.0          # Spanish model (small)

# Machine Learning
scikit-learn==1.3.2             # ML utilities
numpy==1.26.2                   # Array operations
Desarrollo:
text
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
Instalación spaCy model:
bash
# Después instalar spacy
python -m spacy download es_core_news_sm
H09 (Ene 2026): Advanced NLP
Adicionales Producción:
text
# Transformers (si necesario)
transformers==4.35.0            # BERT, GPT models
torch==2.1.0                    # PyTorch (backend transformers)

# Additional ML
pandas==2.1.4                   # Data manipulation
joblib==1.3.2                   # Model persistence
🔗 Dependencias Internas (THEA IA)
Módulos que usa ml/:
python
# Ninguna dependencia interna
# ML es módulo independiente
Módulos que usan ml/:
python
# src/core/ (CoreManager)
from src.ml import NLPService

nlp = NLPService()
result = nlp.process("recuérdame reunión mañana")
# → {"intent": "create_reminder", "entities": {...}}
🔐 Variables de Entorno
Ninguna - Este módulo no requiere variables entorno.

Configuración hardcoded o en src/config/constants.py.

📊 Tabla Resumen Dependencias
Hito	Deps Producción	Deps Desarrollo	Size Download
H06	4 + 1 model	2	~50MB (spaCy sm)
H09	+3	0	~500MB (transformers)
🚀 Instalación Dependencias (H06)
⚠️ NO INSTALAR ANTES DE H06
bash
# Cuando llegue H06:

# Instalar spaCy
pip install spacy==3.7.2

# Descargar modelo español
python -m spacy download es_core_news_sm

# Verificar
python -c "import spacy; nlp = spacy.load('es_core_news_sm'); print('OK')"

# Instalar ML deps
pip install scikit-learn==1.3.2 numpy==1.26.2

# Verificar todo
python -c "
import spacy
import sklearn
import numpy
print('All OK')
"
🧪 Testing (H06)
Test NLP Service:
python
# tests/unit/test_ml/test_nlp_service.py
import pytest
from src.ml import NLPService

def test_nlp_service_singleton():
    """NLPService es singleton"""
    nlp1 = NLPService()
    nlp2 = NLPService()
    assert nlp1 is nlp2

def test_nlp_service_process():
    """Process retorna intent y entities"""
    nlp = NLPService()
    result = nlp.process("recuérdame reunión mañana 15:00")
    
    assert "intent" in result
    assert "entities" in result
    assert result["intent"] == "create_reminder"
Test Intent Classification:
python
def test_intent_classification_reminder():
    """Clasifica reminder correctamente"""
    from src.ml.intent_classifier import IntentClassifier
    
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
    """Confidence score correcto"""
    classifier = IntentClassifier()
    
    confidence = classifier.confidence("recuérdame reunión mañana")
    assert 0 <= confidence <= 1
    assert confidence > 0.7  # High confidence
⚠️ Troubleshooting (H06)
1. spaCy model no encontrado
python
# Error: Can't find model 'es_core_news_sm'

# Solución:
python -m spacy download es_core_news_sm

# O especificar path
nlp = spacy.load("/path/to/es_core_news_sm")
2. Memory issues con model grande
python
# Problema: Model 'lg' usa mucha RAM

# Solución: Usar model 'sm' (small)
# es_core_news_sm: ~50MB RAM
# es_core_news_md: ~200MB RAM
# es_core_news_lg: ~500MB RAM

# Para THEA IA: 'sm' es suficiente
3. Latency alta
python
# Problema: process() toma >100ms

# Solución 1: Cache results comunes
from functools import lru_cache

@lru_cache(maxsize=128)
def classify_cached(text: str) -> str:
    return classifier.classify(text)

# Solución 2: Async processing
async def process_async(text: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, nlp.process, text)
📈 Performance
Benchmarks Target (H06):
Operación	Target	Notas
Load model	<2s	Startup
classify_intent	<50ms	Per query
extract_entities	<50ms	Per query
process (total)	<100ms	Intent + entities
Memory:
Model	RAM	Notas
es_core_news_sm	~50MB	Recomendado
es_core_news_md	~200MB	Si necesario
es_core_news_lg	~500MB	Overkill
📚 Recursos
Documentación Oficial:
spaCy Docs

spaCy Spanish Models

spaCy Usage

Tutoriales:
spaCy 101

Custom NER

Text Classification

🔄 Actualización Dependencias
Política:
spaCy: Actualizar major/minor con cuidado (breaking changes)

spaCy models: Actualizar cuando spaCy actualice

scikit-learn: Actualizar cada 6 meses

Comando:
bash
# Ver outdated
pip list --outdated | grep -E "spacy|sklearn"

# Actualizar spaCy
pip install --upgrade spacy

# Re-download model (si necesario)
python -m spacy download es_core_news_sm --upgrade

# Verificar no rompe
pytest src/tests/unit/test_ml/ -v
🎯 Checklist H06
Antes de implementar:

 H02-H05 completos (regex funciona)

 Decision: ¿Realmente necesitamos NLP o regex suficiente?

 Benchmarks regex vs NLP (accuracy, latency)

Durante implementación:

 spaCy instalado

 Model descargado

 Tests >80% coverage

 Accuracy >85%

 Latency <100ms

 Fallback logic funciona

 Memory usage aceptable

⚠️ RECUERDA: NO INSTALAR ANTES DE H06

Usar regex simple en H02-H05.

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota