"""
Tests para Context Merging Engine - H03 Advanced Context Management
Verifica estrategias de merge y context management.

H03 FASE 1 - BLOQUE 1.2 - TAREA 1.2.3
"""

import pytest
from src.theaia.core.fsm.context_merging import ContextMergingEngine, MergeStrategy
from src.theaia.core.fsm.state_machine import ConversationStateMachine


class TestMergeStrategies:
    """Tests de estrategias de merge."""
    
    def test_merge_overwrite_strategy(self):
        """Verifica estrategia OVERWRITE."""
        engine = ContextMergingEngine()
        
        old_ctx = {"key1": "old_value", "key2": "keep"}
        new_ctx = {"key1": "new_value", "key3": "added"}
        
        result = engine.merge(old_ctx, new_ctx, strategy="overwrite")
        
        assert result["key1"] == "new_value"  # Sobrescrito
        assert result["key2"] == "keep"       # Mantenido
        assert result["key3"] == "added"      # Añadido
    
    def test_merge_append_strategy_lists(self):
        """Verifica estrategia APPEND para listas."""
        engine = ContextMergingEngine()
        
        old_ctx = {"messages": [1, 2], "user": "test"}
        new_ctx = {"messages": [3, 4], "user": "updated"}
        
        result = engine.merge(old_ctx, new_ctx, strategy="append")
        
        assert set(result["messages"]) == {1, 2, 3, 4}  # Merged sin duplicados
        assert result["user"] == "updated"  # Sobrescrito (no lista)
    
    def test_merge_append_strategy_no_duplicates(self):
        """Verifica que APPEND evita duplicados."""
        engine = ContextMergingEngine()
        
        old_ctx = {"items": [1, 2, 3]}
        new_ctx = {"items": [2, 3, 4]}
        
        result = engine.merge(old_ctx, new_ctx, strategy="append")
        
        assert set(result["items"]) == {1, 2, 3, 4}
        assert len(result["items"]) == 4  # Sin duplicados
    
    def test_merge_recursive_strategy_dicts(self):
        """Verifica estrategia MERGE recursiva para dicts."""
        engine = ContextMergingEngine()
        
        old_ctx = {
            "user": {"name": "John", "age": 30},
            "settings": {"theme": "dark"}
        }
        new_ctx = {
            "user": {"age": 31, "city": "NYC"},
            "settings": {"lang": "en"}
        }
        
        result = engine.merge(old_ctx, new_ctx, strategy="merge")
        
        assert result["user"]["name"] == "John"      # Mantenido
        assert result["user"]["age"] == 31           # Actualizado
        assert result["user"]["city"] == "NYC"       # Añadido
        assert result["settings"]["theme"] == "dark" # Mantenido
        assert result["settings"]["lang"] == "en"    # Añadido
    
    def test_merge_recursive_strategy_lists(self):
        """Verifica estrategia MERGE para listas (append)."""
        engine = ContextMergingEngine()
        
        old_ctx = {"history": [1, 2]}
        new_ctx = {"history": [3, 4]}
        
        result = engine.merge(old_ctx, new_ctx, strategy="merge")
        
        assert result["history"] == [1, 2, 3, 4]
    
    def test_merge_windowing_strategy(self):
        """Verifica estrategia WINDOWING (limita histórico)."""
        engine = ContextMergingEngine(max_history=3)
        
        old_ctx = {"messages": [1, 2, 3, 4, 5]}
        new_ctx = {"messages": [6, 7]}
        
        result = engine.merge(old_ctx, new_ctx, strategy="windowing")
        
        # Debe mantener solo últimos 3 elementos después de merge
        assert len(result["messages"]) == 3
        assert result["messages"] == [5, 6, 7]


class TestContextWindowing:
    """Tests de windowing."""
    
    def test_apply_windowing_to_lists(self):
        """Verifica windowing aplicado a listas."""
        engine = ContextMergingEngine(max_history=5)
        
        context = {
            "messages": [1, 2, 3, 4, 5, 6, 7, 8],
            "events": [1, 2, 3],
            "user": "test"
        }
        
        result = engine.apply_windowing(context)
        
        assert len(result["messages"]) == 5
        assert result["messages"] == [4, 5, 6, 7, 8]  # Últimos 5
        assert result["events"] == [1, 2, 3]          # Sin cambio (≤5)
        assert result["user"] == "test"               # Sin cambio (no lista)
    
    def test_apply_windowing_specific_keys(self):
        """Verifica windowing solo en keys específicas."""
        engine = ContextMergingEngine(max_history=2)
        
        context = {
            "messages": [1, 2, 3, 4],
            "events": [1, 2, 3, 4]
        }
        
        result = engine.apply_windowing(context, keys=["messages"])
        
        assert result["messages"] == [3, 4]  # Windowed
        assert result["events"] == [1, 2, 3, 4]  # No tocado


class TestContextIsolation:
    """Tests de aislamiento de contexto."""
    
    def test_create_isolated_context(self):
        """Verifica creación de context aislado."""
        engine = ContextMergingEngine()
        
        context = engine.create_isolated_context("user123")
        
        assert context["user_id"] == "user123"
        assert "session_start" in context
        assert context["message_history"] == []
    
    def test_create_isolated_context_with_base(self):
        """Verifica context aislado con base context."""
        engine = ContextMergingEngine()
        
        base = {"setting": "value"}
        context = engine.create_isolated_context("user456", base_context=base)
        
        assert context["user_id"] == "user456"
        assert context["setting"] == "value"
        assert "session_start" in context


class TestContextUtilities:
    """Tests de utilidades de context."""
    
    def test_get_context_stats(self):
        """Verifica estadísticas de context."""
        engine = ContextMergingEngine()
        
        context = {
            "key1": "value",
            "list1": [1, 2, 3],
            "dict1": {"nested": "value"},
            "list2": [4, 5]
        }
        
        stats = engine.get_context_stats(context)
        
        assert stats["total_keys"] == 4
        assert stats["lists"] == 2
        assert stats["dicts"] == 1
        assert stats["total_list_items"] == 5
    
    def test_prune_context(self):
        """Verifica poda de context."""
        engine = ContextMergingEngine()
        
        context = {
            "keep1": "value1",
            "keep2": "value2",
            "remove1": "value3",
            "remove2": "value4"
        }
        
        result = engine.prune_context(context, keep_keys=["keep1", "keep2"])
        
        assert len(result) == 2
        assert "keep1" in result
        assert "keep2" in result
        assert "remove1" not in result
        assert "remove2" not in result


class TestFSMIntegration:
    """Tests de integración con FSM."""
    
    def test_fsm_has_context_merging_engine(self):
        """Verifica que FSM tiene ContextMergingEngine."""
        fsm = ConversationStateMachine("test_user")
        
        assert hasattr(fsm, 'context_merging_engine')
        assert isinstance(fsm.context_merging_engine, ContextMergingEngine)
    
    def test_fsm_merge_context(self):
        """Verifica método merge_context en FSM."""
        fsm = ConversationStateMachine("test_user")
        fsm.context = {"old": "value"}
        
        new_ctx = {"new": "data"}
        result = fsm.merge_context(new_ctx, strategy="merge")
        
        assert result["old"] == "value"
        assert result["new"] == "data"
        assert fsm.context == result  # Context actualizado
    
    def test_fsm_get_context_stats(self):
        """Verifica método get_context_stats en FSM."""
        fsm = ConversationStateMachine("test_user")
        fsm.context = {
            "list1": [1, 2],
            "dict1": {"key": "value"}
        }
        
        stats = fsm.get_context_stats()
        
        assert stats["total_keys"] == 2
        assert stats["lists"] == 1
        assert stats["dicts"] == 1
    
    def test_fsm_prune_context(self):
        """Verifica método prune_context en FSM."""
        fsm = ConversationStateMachine("test_user")
        fsm.context = {
            "keep": "this",
            "remove": "that"
        }
        
        fsm.prune_context(["keep"])
        
        assert len(fsm.context) == 1
        assert "keep" in fsm.context
        assert "remove" not in fsm.context


class TestEngineInitialization:
    """Tests de inicialización del engine."""
    
    def test_engine_default_max_history(self):
        """Verifica max_history por defecto."""
        engine = ContextMergingEngine()
        
        assert engine.max_history == 10
    
    def test_engine_custom_max_history(self):
        """Verifica max_history personalizado."""
        engine = ContextMergingEngine(max_history=5)
        
        assert engine.max_history == 5


# ==================== FIXTURES ====================

@pytest.fixture
def engine():
    """Fixture que retorna ContextMergingEngine limpio."""
    return ContextMergingEngine(max_history=10)

@pytest.fixture
def fsm():
    """Fixture que retorna FSM limpio."""
    return ConversationStateMachine("test_user")
