"""
Tests para CoreNLPEngine
"""

import pytest
from src.theaia.core.nlp_engine import CoreNLPEngine


@pytest.mark.asyncio
async def test_nlp_detect_intent():
    """Test detección de intent básica."""
    nlp = CoreNLPEngine()
    
    intent = await nlp.detect_intent("crear evento mañana")
    assert intent == "create_event"


@pytest.mark.asyncio
async def test_nlp_detect_language():
    """Test detección de idioma."""
    nlp = CoreNLPEngine()
    
    # Español
    lang_es = nlp._detect_language("¿Cómo estás?")
    assert lang_es == "es"
    
    # Inglés (por defecto)
    lang_en = nlp._detect_language("How are you?")
    assert lang_en == "es"  # Default


@pytest.mark.asyncio
async def test_nlp_process_message():
    """Test procesamiento completo de mensaje."""
    nlp = CoreNLPEngine()
    
    result = await nlp.process_message(
        "crear evento reunión mañana"
    )
    
    assert result.intent == "create_event"
    assert result.confidence > 0
    assert result.language == "es"
    assert result.processing_time_ms >= 0
    assert isinstance(result.entities, dict)
    assert isinstance(result.suggestions, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
