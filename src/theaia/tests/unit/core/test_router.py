"""
Tests para TheaRouter v2.0 - H03 Hito 1
8 tests críticos de router
"""

import pytest
import asyncio
from datetime import datetime, timezone
from src.theaia.core.router import (
    TheaRouter, CoreRouter, Message, ProcessedMessage, preprocess_text
)


@pytest.fixture
def router():
    """Fixture: Router inicializado."""
    return TheaRouter()


class TestTheaRouter:
    """Suite de tests para TheaRouter v2.0."""
    
    def test_router_initialization(self, router):
        """Test 1: Router inicializa correctamente."""
        assert router is not None
        assert router.message_count == 0
        assert isinstance(router.agents, dict)
        assert len(router.get_available_agents()) >= 0
    
    def test_preprocess_text_basic(self):
        """Test 2: Preprocess limpia texto correctamente."""
        result = preprocess_text("  HOLA   MUNDO  ")
        assert result == "hola mundo"
    
    def test_preprocess_text_spanish_chars(self):
        """Test 3: Preprocess mantiene caracteres españoles."""
        result = preprocess_text("¿Qué hay mañana?")
        assert "qué" in result
        assert "mañana" in result
    
    def test_preprocess_empty_text(self):
        """Test 4: Preprocess maneja texto vacío."""
        assert preprocess_text("") == ""
        assert preprocess_text("   ") == ""
        assert preprocess_text(None) == ""
    
    @pytest.mark.asyncio
    async def test_process_message_basic(self, router):
        """Test 5: Procesa mensaje básico."""
        message = Message(
            text="Hola router",
            user_id="user123",
            tenant_id="default",
            session_id="session123",
            timestamp=datetime.now(timezone.utc)
        )
        
        result = await router.process(message)
        
        assert isinstance(result, ProcessedMessage)
        assert result.original_text == "Hola router"
        assert result.status in ["ok", "error"]
    
    @pytest.mark.asyncio
    async def test_process_empty_message(self, router):
        """Test 6: Maneja mensaje vacío."""
        message = Message(
            text="",
            user_id="user123",
            tenant_id="default"
        )
        
        result = await router.process(message)
        
        assert result.status == "error"
        assert result.intent == "unknown"
    
    def test_handle_sync_method(self, router):
        """Test 7: Método handle() síncrono funciona."""
        result = router.handle(
            user_id="user123",
            message="Test message"
        )
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "message" in result
        assert "cleaned_text" in result
    
    def test_get_stats(self, router):
        """Test 8: Retorna estadísticas correctamente."""
        stats = router.get_stats()
        
        assert isinstance(stats, dict)
        assert "message_count" in stats
        assert "version" in stats
        assert stats["version"] == "2.0"
        assert stats["router_type"] == "TheaRouter"


class TestCoreRouterAlias:
    """Test que CoreRouter alias funciona correctamente."""
    
    def test_corerouter_alias_exists(self):
        """Test: CoreRouter alias está disponible."""
        assert CoreRouter is not None
        assert CoreRouter == TheaRouter
    
    def test_corerouter_initialization(self):
        """Test: CoreRouter alias inicializa igual que TheaRouter."""
        router = CoreRouter()
        assert isinstance(router, TheaRouter)
        assert router.message_count == 0


class TestMessageDataclass:
    """Tests para Message dataclass."""
    
    def test_message_creation_minimal(self):
        """Test: Crea mensaje con parámetros mínimos."""
        msg = Message(
            text="Test",
            user_id="user1"
        )
        
        assert msg.text == "Test"
        assert msg.user_id == "user1"
        assert msg.tenant_id == "default"
        assert msg.timestamp is not None
    
    def test_message_creation_full(self):
        """Test: Crea mensaje con todos los parámetros."""
        ts = datetime.now(timezone.utc)
        msg = Message(
            text="Test",
            user_id="user1",
            tenant_id="custom",
            session_id="sess1",
            timestamp=ts,
            metadata={"key": "value"}
        )
        
        assert msg.metadata == {"key": "value"}
        assert msg.session_id == "sess1"


class TestProcessedMessageDataclass:
    """Tests para ProcessedMessage dataclass."""
    
    def test_processed_message_creation(self):
        """Test: Crea ProcessedMessage correctamente."""
        msg = ProcessedMessage(
            intent="test_intent",
            entities={"key": "value"},
            confidence=0.95,
            agent_target="test_agent"
        )
        
        assert msg.intent == "test_intent"
        assert msg.confidence == 0.95
        assert msg.status == "ok"
        assert msg.fsm_state == "idle"


class TestRouterIntegration:
    """Tests de integración router end-to-end."""
    
    @pytest.mark.asyncio
    async def test_router_message_count_increments(self, router):
        """Test: Contador de mensajes incrementa."""
        assert router.message_count == 0
        
        msg = Message(text="Test1", user_id="u1")
        await router.process(msg)
        assert router.message_count == 1
        
        msg = Message(text="Test2", user_id="u2")
        await router.process(msg)
        assert router.message_count == 2
    
    def test_router_sync_message_count(self, router):
        """Test: Contador incrementa en modo sync también."""
        assert router.message_count == 0
        
        router.handle("user1", "Test1")
        assert router.message_count == 1
        
        router.handle("user2", "Test2")
        assert router.message_count == 2
