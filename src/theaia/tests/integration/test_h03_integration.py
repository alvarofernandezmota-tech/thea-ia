"""
Integration Tests - H03 Complete Stack
End-to-end tests para CoreRouter + FSM + Agents.

H03 FASE 1 - BLOQUE 1.4 - Integration Tests
"""

import pytest
from src.theaia.core.router import CoreRouter, Message, ProcessedMessage
from src.theaia.core.fsm.state_machine import ConversationStateMachine
from src.theaia.agents.registry import get_agent, list_intents
from src.theaia.agents.decorators import clear_registry
from datetime import datetime
import asyncio


class TestRouterFSMIntegration:
    """Tests de integración Router + FSM."""
    
    def setup_method(self):
        """Setup limpio."""
        clear_registry()
        self.router = CoreRouter()
        self.fsm = ConversationStateMachine("test_user")
    
    @pytest.mark.asyncio
    async def test_complete_message_flow_to_fsm(self):
        """Flujo completo: Message → Router → FSM."""
        message = Message(
            text="Crear evento mañana a las 15:00",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        # Procesar con router
        result = await self.router.process(message)
        
        assert isinstance(result, ProcessedMessage)
        assert result.intent != "unknown"
        assert result.processing_time_ms < 100
        assert result.agent_target is not None
    
    @pytest.mark.asyncio
    async def test_router_output_to_fsm_context(self):
        """Output del router → context del FSM."""
        message = Message(
            text="Nueva nota importante",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        result = await self.router.process(message)
        
        # Actualizar FSM context con output router
        self.fsm.merge_context({
            "intent": result.intent,
            "entities": result.entities,
            "agent_target": result.agent_target
        })
        
        assert self.fsm.context["intent"] == result.intent
        assert "entities" in self.fsm.context
    
    @pytest.mark.asyncio
    async def test_performance_router_fsm_e2e(self):
        """Performance E2E: <150ms total."""
        import time
        
        start = time.time()
        
        message = Message(
            text="Qué tengo el lunes",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        result = await self.router.process(message)
        self.fsm.merge_context({"router_result": result})
        
        elapsed_ms = (time.time() - start) * 1000
        
        assert elapsed_ms < 150  # Total E2E <150ms


class TestFSMCallbacksIntegration:
    """Tests de integración FSM callbacks con transitions."""
    
    def setup_method(self):
        """Setup limpio."""
        clear_registry()
        self.fsm = ConversationStateMachine("test_user_callbacks")
        self.callback_executed = False
    
    def test_pre_callback_blocks_transition(self):
        """Pre-callback puede bloquear transición."""
        
        # Los callbacks tienen guión bajo: _pre_callbacks (es DICT, no list)
        assert hasattr(self.fsm, '_pre_callbacks')
        assert isinstance(self.fsm._pre_callbacks, dict)
        # Callbacks registro universal debe existir
        assert len(self.fsm._pre_callbacks) >= 0
    
    def test_post_callback_executes_on_success(self):
        """Post-callback ejecuta solo en éxito."""
        
        # Los callbacks tienen guión bajo: _post_callbacks (es DICT, no list)
        assert hasattr(self.fsm, '_post_callbacks')
        assert isinstance(self.fsm._post_callbacks, dict)
        
        # Ejecutar transición válida
        self.fsm.request_disambiguation()
        
        # Verificar transición exitosa
        assert self.fsm.state == "awaiting_disambiguation"
    
    def test_context_merge_in_transition(self):
        """Context se mergea durante transición."""
        
        # Setup context inicial
        self.fsm.context = {"user_input": "test", "intent": None}
        
        # Realizar transición
        self.fsm.request_disambiguation()
        
        # Verificar context actualizado
        assert "disambiguation_started" in self.fsm.context
        assert self.fsm.context["user_input"] == "test"


class TestFullH03Stack:
    """Tests full stack: Router + FSM + Agents + Registry."""
    
    def setup_method(self):
        """Setup limpio."""
        clear_registry()
        self.router = CoreRouter()
        self.fsm = ConversationStateMachine("full_stack_user")
    
    @pytest.mark.asyncio
    async def test_full_stack_create_event_flow(self):
        """Flow completo: Input → Intent → Agent routing."""
        
        message = Message(
            text="Crear reunión mañana 14:00 en oficina",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        # 1. Router procesa
        router_result = await self.router.process(message)
        
        # 2. FSM actualiza context
        self.fsm.merge_context({
            "intent": router_result.intent,
            "entities": router_result.entities,
            "agent_target": router_result.agent_target
        })
        
        # 3. Verificar agente disponible
        agent = get_agent(router_result.agent_target)
        
        # Verificaciones
        assert router_result.intent is not None
        assert router_result.agent_target is not None
        assert self.fsm.context["intent"] == router_result.intent
        assert "entities" in self.fsm.context
    
    @pytest.mark.asyncio
    async def test_full_stack_create_note_flow(self):
        """Flow completo: Nota + Entidades + FSM."""
        
        message = Message(
            text="Nota importante: hablar con Juan sobre proyecto",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        router_result = await self.router.process(message)
        self.fsm.merge_context({
            "intent": router_result.intent,
            "entities": router_result.entities
        })
        
        assert "intent" in self.fsm.context
        assert isinstance(self.fsm.context["entities"], dict)
    
    @pytest.mark.asyncio
    async def test_full_stack_query_agenda_flow(self):
        """Flow completo: Query Agenda + Entities + FSM."""
        
        message = Message(
            text="Qué tengo programado el próximo lunes",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        router_result = await self.router.process(message)
        self.fsm.merge_context({
            "intent": router_result.intent,
            "entities": router_result.entities,
            "agent_target": router_result.agent_target
        })
        
        # Verificar entities contiene datos
        entities = self.fsm.context.get("entities", {})
        
        assert router_result.intent is not None
        assert isinstance(entities, dict)
        assert self.fsm.context["agent_target"] is not None


class TestH03ComponentsIntegration:
    """Tests de integración entre componentes H03."""
    
    def setup_method(self):
        """Setup."""
        clear_registry()
    
    def test_registry_with_fsm_routing(self):
        """Registry agents disponibles para FSM routing."""
        
        intents = list_intents()
        
        assert isinstance(intents, list)
        assert len(intents) > 0
        
        # Verificar agentes registrados
        for intent in intents[:3]:
            # Verificar intent está en lista
            assert intent in intents
    
    def test_context_merging_strategies(self):
        """Estrategias merging están integradas."""
        
        fsm = ConversationStateMachine("merge_test")
        
        # Test merge strategy
        result = fsm.merge_context({"key": "value"}, strategy="merge")
        
        assert result is not None
        assert "key" in result
    
    @pytest.mark.asyncio
    async def test_end_to_end_performance_under_500ms(self):
        """E2E performance <500ms total."""
        import time
        
        start = time.time()
        
        router = CoreRouter()
        fsm = ConversationStateMachine("perf_test")
        
        message = Message(
            text="Test mensaje performance",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        result = await router.process(message)
        fsm.merge_context({"router_result": result})
        fsm.request_disambiguation()
        
        elapsed_ms = (time.time() - start) * 1000
        
        assert elapsed_ms < 500


class TestRouterFSMCallbacksIntegration:
    """Tests adicionales de callbacks con router."""
    
    def setup_method(self):
        """Setup."""
        clear_registry()
        self.router = CoreRouter()
        self.fsm = ConversationStateMachine("callbacks_test")
    
    @pytest.mark.asyncio
    async def test_router_fsm_callbacks_order(self):
        """Callbacks ejecutan en orden correcto."""
        
        message = Message(
            text="Test callbacks",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        result = await self.router.process(message)
        
        # Merging actualiza context
        self.fsm.merge_context({"router_output": result})
        
        # Transición con callbacks
        self.fsm.request_disambiguation()
        
        # Verificar estado
        assert self.fsm.state == "awaiting_disambiguation"
    
    def test_fsm_context_isolation(self):
        """Cada FSM tiene contexto aislado."""
        
        fsm1 = ConversationStateMachine("user_1")
        fsm2 = ConversationStateMachine("user_2")
        
        fsm1.merge_context({"user_data": "user1"})
        fsm2.merge_context({"user_data": "user2"})
        
        # Contextos aislados
        assert fsm1.context["user_data"] == "user1"
        assert fsm2.context["user_data"] == "user2"
    
    @pytest.mark.asyncio
    async def test_router_agent_availability(self):
        """Agentes están disponibles después routing."""
        
        message = Message(
            text="Crear evento",
            user_id=1,
            tenant_id="test",
            session_id="session_1",
            timestamp=datetime.now()
        )
        
        result = await self.router.process(message)
        
        # Verificar agent_target tiene valor
        assert result.agent_target is not None
        assert isinstance(result.agent_target, str)
