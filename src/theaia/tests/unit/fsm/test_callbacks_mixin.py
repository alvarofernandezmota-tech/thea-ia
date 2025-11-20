"""
Tests para FSM Callbacks Mixin - H03 Advanced Callbacks System
Verifica pre/post/error callbacks y context injection.

H03 FASE 1 - BLOQUE 1.2 - TAREA 1.2.1 (Tests)
"""

import pytest
from src.theaia.core.fsm.state_machine import ConversationStateMachine
from src.theaia.core.fsm.callbacks_mixin import CallbacksMixin


class TestCallbacksRegistration:
    """Tests de registro de callbacks."""
    
    def test_register_pre_callback(self):
        """Verifica registro de pre-callback."""
        fsm = ConversationStateMachine("test_user")
        
        def my_pre_callback(from_state, to_state, context):
            return True
        
        fsm.register_pre_callback("delegate_to_agent", my_pre_callback)
        
        assert "delegate_to_agent" in fsm._pre_callbacks
        assert my_pre_callback in fsm._pre_callbacks["delegate_to_agent"]
    
    def test_register_post_callback(self):
        """Verifica registro de post-callback."""
        fsm = ConversationStateMachine("test_user")
        
        def my_post_callback(from_state, to_state, context):
            pass
        
        fsm.register_post_callback("delegate_to_agent", my_post_callback)
        
        assert "delegate_to_agent" in fsm._post_callbacks
        assert my_post_callback in fsm._post_callbacks["delegate_to_agent"]
    
    def test_register_error_callback(self):
        """Verifica registro de error-callback."""
        fsm = ConversationStateMachine("test_user")
        
        def my_error_callback(from_state, to_state, error, context):
            pass
        
        fsm.register_error_callback("delegate_to_agent", my_error_callback)
        
        assert "delegate_to_agent" in fsm._error_callbacks
        assert my_error_callback in fsm._error_callbacks["delegate_to_agent"]
    
    def test_register_universal_pre_callback(self):
        """Verifica registro de universal pre-callback."""
        fsm = ConversationStateMachine("test_user")
        
        def my_universal_callback(from_state, to_state, context):
            return True
        
        fsm.register_universal_pre_callback(my_universal_callback)
        
        assert my_universal_callback in fsm._universal_pre_callbacks
    
    def test_register_universal_post_callback(self):
        """Verifica registro de universal post-callback."""
        fsm = ConversationStateMachine("test_user")
        
        def my_universal_callback(from_state, to_state, context):
            pass
        
        fsm.register_universal_post_callback(my_universal_callback)
        
        assert my_universal_callback in fsm._universal_post_callbacks
    
    def test_register_universal_error_callback(self):
        """Verifica registro de universal error-callback."""
        fsm = ConversationStateMachine("test_user")
        
        def my_universal_callback(from_state, to_state, error, context):
            pass
        
        fsm.register_universal_error_callback(my_universal_callback)
        
        assert my_universal_callback in fsm._universal_error_callbacks


class TestCallbacksExecution:
    """Tests de ejecución de callbacks."""
    
    def test_pre_callback_allows_transition(self):
        """Verifica que pre-callback puede permitir transición."""
        fsm = ConversationStateMachine("test_user")
        
        callback_executed = []
        
        def my_pre_callback(from_state, to_state, context):
            callback_executed.append(True)
            return True  # Permitir transición
        
        fsm.register_pre_callback("request_disambiguation", my_pre_callback)
        
        # Ejecutar pre-callbacks
        result = fsm._execute_pre_callbacks("request_disambiguation", "initial", "awaiting_disambiguation", {})
        
        assert result is True
        assert len(callback_executed) > 0
    
    def test_pre_callback_cancels_transition(self):
        """Verifica que pre-callback puede cancelar transición."""
        fsm = ConversationStateMachine("test_user")
        
        def my_pre_callback(from_state, to_state, context):
            return False  # Cancelar transición
        
        fsm.register_pre_callback("request_disambiguation", my_pre_callback)
        
        # Ejecutar pre-callbacks
        result = fsm._execute_pre_callbacks("request_disambiguation", "initial", "awaiting_disambiguation", {})
        
        assert result is False
    
    def test_post_callback_execution(self):
        """Verifica ejecución de post-callback."""
        fsm = ConversationStateMachine("test_user")
        
        callback_executed = []
        
        def my_post_callback(from_state, to_state, context):
            callback_executed.append((from_state, to_state))
        
        fsm.register_post_callback("request_disambiguation", my_post_callback)
        
        # Ejecutar post-callbacks
        fsm._execute_post_callbacks("request_disambiguation", "initial", "awaiting_disambiguation", {})
        
        assert len(callback_executed) > 0
        assert callback_executed[0] == ("initial", "awaiting_disambiguation")
    
    def test_error_callback_execution(self):
        """Verifica ejecución de error-callback."""
        fsm = ConversationStateMachine("test_user")
        
        callback_executed = []
        test_error = ValueError("Test error")
        
        def my_error_callback(from_state, to_state, error, context):
            callback_executed.append((from_state, to_state, type(error).__name__))
        
        fsm.register_error_callback("request_disambiguation", my_error_callback)
        
        # Ejecutar error-callbacks
        fsm._execute_error_callbacks("request_disambiguation", "initial", "awaiting_disambiguation", test_error, {})
        
        assert len(callback_executed) > 0
        assert callback_executed[0][2] == "ValueError"


class TestUniversalCallbacks:
    """Tests de universal callbacks."""
    
    def test_universal_pre_callback_executed(self):
        """Verifica que universal pre-callback se ejecuta."""
        fsm = ConversationStateMachine("test_user")
        
        callback_executed = []
        
        def my_universal_callback(from_state, to_state, context):
            callback_executed.append(True)
            return True
        
        fsm.register_universal_pre_callback(my_universal_callback)
        
        # Ejecutar pre-callbacks
        fsm._execute_pre_callbacks("any_transition", "state1", "state2", {})
        
        assert len(callback_executed) > 0
    
    def test_universal_post_callback_executed(self):
        """Verifica que universal post-callback se ejecuta."""
        fsm = ConversationStateMachine("test_user")
        
        callback_executed = []
        
        def my_universal_callback(from_state, to_state, context):
            callback_executed.append(True)
        
        fsm.register_universal_post_callback(my_universal_callback)
        
        # Ejecutar post-callbacks
        fsm._execute_post_callbacks("any_transition", "state1", "state2", {})
        
        assert len(callback_executed) > 0
    
    def test_universal_error_callback_executed(self):
        """Verifica que universal error-callback se ejecuta."""
        fsm = ConversationStateMachine("test_user")
        
        callback_executed = []
        test_error = RuntimeError("Test error")
        
        def my_universal_callback(from_state, to_state, error, context):
            callback_executed.append(True)
        
        fsm.register_universal_error_callback(my_universal_callback)
        
        # Ejecutar error-callbacks
        fsm._execute_error_callbacks("any_transition", "state1", "state2", test_error, {})
        
        assert len(callback_executed) > 0


class TestContextInjection:
    """Tests de context injection en callbacks."""
    
    def test_context_available_in_pre_callback(self):
        """Verifica que context está disponible en pre-callback."""
        fsm = ConversationStateMachine("test_user")
        fsm.update_context(test_key="test_value")
        
        context_received = []
        
        def my_pre_callback(from_state, to_state, context):
            context_received.append(context)
            return True
        
        fsm.register_pre_callback("request_disambiguation", my_pre_callback)
        
        fsm._execute_pre_callbacks("request_disambiguation", "initial", "awaiting_disambiguation", fsm.context)
        
        assert len(context_received) > 0
        # El context debería contener los datos del FSM
        assert isinstance(context_received[0], dict)
    
    def test_context_available_in_post_callback(self):
        """Verifica que context está disponible en post-callback."""
        fsm = ConversationStateMachine("test_user")
        fsm.update_context(stage="processing")
        
        context_received = []
        
        def my_post_callback(from_state, to_state, context):
            context_received.append(context)
        
        fsm.register_post_callback("request_disambiguation", my_post_callback)
        
        fsm._execute_post_callbacks("request_disambiguation", "initial", "awaiting_disambiguation", fsm.context)
        
        assert len(context_received) > 0
        assert isinstance(context_received[0], dict)
    
    def test_context_modification_in_callback(self):
        """Verifica que callbacks pueden modificar context."""
        fsm = ConversationStateMachine("test_user")
        
        def my_post_callback(from_state, to_state, context):
            context["callback_executed"] = True
        
        fsm.register_post_callback("request_disambiguation", my_post_callback)
        
        initial_context = dict(fsm.context)
        fsm._execute_post_callbacks("request_disambiguation", "initial", "awaiting_disambiguation", fsm.context)
        
        # El context en el diccionario se modificó
        assert fsm.context.get("callback_executed") is True


class TestFSMCallbacksIntegration:
    """Tests de integración FSM + callbacks."""
    
    def test_fsm_has_callbacks_mixin(self):
        """Verifica que FSM hereda de CallbacksMixin."""
        fsm = ConversationStateMachine("test_user")
        
        assert isinstance(fsm, CallbacksMixin)
        assert hasattr(fsm, 'register_pre_callback')
        assert hasattr(fsm, 'register_post_callback')
        assert hasattr(fsm, 'register_error_callback')
    
    def test_callbacks_initialized_empty(self):
        """Verifica que callbacks se inicializan vacíos."""
        fsm = ConversationStateMachine("test_user")
        
        assert len(fsm._pre_callbacks) == 0
        assert len(fsm._post_callbacks) == 0
        assert len(fsm._error_callbacks) == 0
    
    def test_universal_callbacks_initialized(self):
        """Verifica que universal callbacks se inicializan."""
        fsm = ConversationStateMachine("test_user")
        
        # Deberían estar vacíos inicialmente (a menos que ConversationStateMachine los registre)
        # pero la lista debería existir
        assert isinstance(fsm._universal_pre_callbacks, list)
        assert isinstance(fsm._universal_post_callbacks, list)
        assert isinstance(fsm._universal_error_callbacks, list)
    
    def test_fsm_h03_callbacks_registered(self):
        """Verifica que ConversationStateMachine registra callbacks H03."""
        fsm = ConversationStateMachine("test_user")
        
        # ConversationStateMachine debería registrar callbacks H03 en __init__
        # Verificamos que hay al menos 1 callback universal registrado
        assert len(fsm._universal_pre_callbacks) >= 1
        assert len(fsm._universal_post_callbacks) >= 1
        assert len(fsm._universal_error_callbacks) >= 1


# ==================== FIXTURES ====================

@pytest.fixture
def fsm():
    """Fixture que retorna FSM limpio."""
    return ConversationStateMachine("test_user")

@pytest.fixture
def callbacks_tracker():
    """Fixture que retorna dict para trackear callbacks."""
    return {
        "pre_executed": [],
        "post_executed": [],
        "error_executed": []
    }
