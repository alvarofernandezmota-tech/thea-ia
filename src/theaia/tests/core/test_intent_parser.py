"""
Tests para CoreIntentParser
"""

import pytest
from src.theaia.core.intent_parser import CoreIntentParser


@pytest.mark.asyncio
async def test_detect_create_event_intent():
    """Test detección de intent crear evento."""
    parser = CoreIntentParser()
    
    messages = [
        "crear evento mañana a las 3pm",
        "agendar reunión el viernes",
        "programar cita con el doctor"
    ]
    
    for msg in messages:
        intent = await parser.detect_intent(msg)
        assert intent == "create_event"


@pytest.mark.asyncio
async def test_detect_query_events_intent():
    """Test detección de intent listar eventos."""
    parser = CoreIntentParser()
    
    messages = [
        "mostrar mis eventos",
        "listar citas de hoy",
        "ver mi agenda"
    ]
    
    for msg in messages:
        intent = await parser.detect_intent(msg)
        assert intent == "query_events"


@pytest.mark.asyncio
async def test_detect_unknown_intent():
    """Test detección de intent desconocido."""
    parser = CoreIntentParser()
    
    intent = await parser.detect_intent("xyz abc 123")
    assert intent == "unknown"


@pytest.mark.asyncio
async def test_detect_with_confidence():
    """Test detección con score de confianza."""
    parser = CoreIntentParser()
    
    result = await parser.detect_intent_with_confidence(
        "crear evento mañana"
    )
    
    assert result.intent == "create_event"
    assert result.confidence > 0.5
    assert isinstance(result.matched_keywords, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
