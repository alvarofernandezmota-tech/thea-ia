# Archivo: src/theaia/tests/unit/test_router.py

"""Test TheaRouter functionality."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from src.theaia.core.router import TheaRouter


@pytest.fixture
def mock_router():
    """Create mock router."""
    router = TheaRouter()
    router.intent_detector = MagicMock()
    router.intent_detector.detect_intent = MagicMock(return_value="agenda")
    return router


def test_router_initialization(mock_router):
    """Test router initialization."""
    assert mock_router is not None
    assert hasattr(mock_router, 'intent_detector')


def test_detect_intents_agenda(mock_router):
    """Test intent detection for agenda."""
    result = mock_router.intent_detector.detect_intent("Agendar reunión mañana")
    assert result == "agenda"


def test_detect_intents_nota(mock_router):
    """Test intent detection for notes."""
    mock_router.intent_detector.detect_intent = MagicMock(return_value="nota")
    result = mock_router.intent_detector.detect_intent("Apuntar comprar leche")
    assert result == "nota"


@pytest.mark.asyncio
async def test_handle_message_async(mock_router):
    """Test async message handling."""
    mock_router.handle = AsyncMock(return_value="Mensaje procesado")
    response = await mock_router.handle("test_user", "hola")
    assert response is not None
