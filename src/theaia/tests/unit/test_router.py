"""
Test TheaRouter functionality.
Tests legacy + H03 improvements (pipeline, entities, performance).
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timezone
from src.theaia.core.router import TheaRouter, Message, ProcessedMessage, preprocess_text


# ==================== TESTS LEGACY (tus tests actuales) ====================

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


# ==================== TESTS H03 NUEVOS ====================

class TestH03Dataclasses:
    """Tests de dataclasses H03 (Message, ProcessedMessage)."""
    
    def test_message_dataclass_basic(self):
        """Verifica creación básica de Message."""
        msg = Message(text="hola", user_id="user123")
        
        assert msg.text == "hola"
        assert msg.user_id == "user123"
        assert msg.tenant_id == "default"
        assert msg.session_id == "user123"
        assert isinstance(msg.timestamp, datetime)
    
    def test_message_dataclass_full(self):
        """Verifica Message con todos los campos."""
        ts = datetime.now(timezone.utc)
        msg = Message(
            text="test message",
            user_id="user456",
            tenant_id="tenant1",
            session_id="session1",
            timestamp=ts,
            metadata={"key": "value"}
        )
        
        assert msg.text == "test message"
        assert msg.user_id == "user456"
        assert msg.tenant_id == "tenant1"
        assert msg.session_id == "session1"
        assert msg.timestamp == ts
        assert msg.metadata == {"key": "value"}
    
    def test_processed_message_dataclass(self):
        """Verifica ProcessedMessage."""
        pm = ProcessedMessage(
            intent="nota",
            entities={"persons": ["Juan"]},
            confidence=0.8,
            agent_target="NoteAgent",
            processing_time_ms=15,
            original_text="crear nota con Juan"
        )
        
        assert pm.intent == "nota"
        assert pm.entities == {"persons": ["Juan"]}
        assert pm.confidence == 0.8
        assert pm.agent_target == "NoteAgent"
        assert pm.processing_time_ms == 15
        assert pm.original_text == "crear nota con Juan"


class TestH03Preprocessing:
    """Tests de función preprocess_text H03."""
    
    def test_preprocess_lowercase(self):
        """Verifica conversión a lowercase."""
        result = preprocess_text("HOLA MUNDO")
        assert result == "hola mundo"
    
    def test_preprocess_strip(self):
        """Verifica strip de espacios."""
        result = preprocess_text("  hola  ")
        assert result == "hola"
    
    def test_preprocess_normalize_spaces(self):
        """Verifica normalización de múltiples espacios."""
        result = preprocess_text("hola    mundo   test")
        assert result == "hola mundo test"
    
    def test_preprocess_empty(self):
        """Verifica manejo de string vacío."""
        result = preprocess_text("")
        assert result == ""
    
    def test_preprocess_none(self):
        """Verifica manejo de None."""
        result = preprocess_text(None)
        assert result == ""


class TestH03RouterHandle:
    """Tests del método handle() con mejoras H03."""
    
    def test_handle_returns_structured_response(self):
        """Verifica que handle() retorna response estructurado H03."""
        router = TheaRouter()
        result = router.handle("test_user", "crear nota test")
        
        # Campos obligatorios H03
        assert "status" in result
        assert "message" in result
        assert "state" in result
        assert "intent" in result
        assert "entities" in result
        assert "processing_time_ms" in result
        assert "original_text" in result
        assert "cleaned_text" in result
        assert "confidence" in result
        assert "agent" in result
    
    def test_handle_performance_tracking(self):
        """Verifica que se trackea performance H03."""
        router = TheaRouter()
        result = router.handle("test_user", "hola")
        
        assert "processing_time_ms" in result
        assert isinstance(result["processing_time_ms"], int)
        assert result["processing_time_ms"] >= 0
    
    def test_handle_preprocessing_applied(self):
        """Verifica que preprocessing se aplica."""
        router = TheaRouter()
        result = router.handle("test_user", "  CREAR  NOTA   ")
        
        assert result["cleaned_text"] == "crear nota"
        assert result["original_text"] == "  CREAR  NOTA   "
    
    def test_handle_with_entities(self):
        """Verifica extracción de entities H03."""
        router = TheaRouter()
        result = router.handle("test_user", "crear nota reunión con Juan mañana")
        
        assert "entities" in result
        assert isinstance(result["entities"], dict)


class TestH03ProcessAsync:
    """Tests del método process() async H03."""
    
    @pytest.mark.asyncio
    async def test_process_async_returns_processed_message(self):
        """Verifica que process() retorna ProcessedMessage."""
        router = TheaRouter()
        msg = Message(text="crear nota test", user_id="test_user")
        
        result = await router.process(msg)
        
        assert isinstance(result, ProcessedMessage)
        assert result.intent is not None
        assert isinstance(result.entities, dict)
        assert result.confidence >= 0.0
        assert result.processing_time_ms >= 0
        assert result.original_text == "crear nota test"
    
    @pytest.mark.asyncio
    async def test_process_has_all_fields(self):
        """Verifica que ProcessedMessage tiene todos los campos."""
        router = TheaRouter()
        msg = Message(text="hola", user_id="user123")
        
        result = await router.process(msg)
        
        assert hasattr(result, "intent")
        assert hasattr(result, "entities")
        assert hasattr(result, "confidence")
        assert hasattr(result, "agent_target")
        assert hasattr(result, "processing_time_ms")
        assert hasattr(result, "original_text")
        assert hasattr(result, "fsm_state")
        assert hasattr(result, "status")


class TestH03ErrorHandling:
    """Tests de manejo de errores H03."""
    
    def test_handle_empty_message(self):
        """Verifica manejo de mensaje vacío."""
        router = TheaRouter()
        result = router.handle("test_user", "")
        
        # Debe manejar mensaje vacío sin crash
        assert "status" in result
        assert "intent" in result
    
    def test_handle_special_characters(self):
        """Verifica manejo de caracteres especiales."""
        router = TheaRouter()
        result = router.handle("test_user", "!@#$%^&*()")
        
        # No debe crashear
        assert "status" in result
        assert "intent" in result


# ==================== FIXTURES ADICIONALES ====================

@pytest.fixture
def router():
    """Fixture que retorna router limpio (sin mocks)."""
    return TheaRouter()

@pytest.fixture
def sample_message():
    """Fixture que retorna mensaje de ejemplo."""
    return Message(
        text="crear nota reunión con Juan",
        user_id="test_user"
    )
