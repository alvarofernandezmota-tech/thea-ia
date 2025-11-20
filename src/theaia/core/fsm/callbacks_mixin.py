"""
FSM Callbacks Mixin - H03 Advanced Callbacks System
Añade pre/post/error callbacks con context injection a FSM existente.

H03 FASE 1 - BLOQUE 1.2 - TAREA 1.2.1
"""

from typing import Callable, Dict, Any, Optional, List
from abc import ABC
import logging

logger = logging.getLogger(__name__)


class CallbacksMixin(ABC):
    """
    Mixin que añade sistema de callbacks avanzado a FSM.
    
    Features H03:
    - Pre-transition callbacks (ejecutan antes de transición)
    - Post-transition callbacks (ejecutan después de transición exitosa)
    - Error callbacks (manejan errores en transición)
    - Context injection (callbacks reciben y pueden modificar context)
    - Callback registration system
    
    Usage:
        class MyFSM(CallbacksMixin, BaseStateMachine):
            def __init__(self, user_id):
                super().__init__(user_id)
                self.register_pre_callback("my_transition", self._validate_before)
                self.register_post_callback("my_transition", self._update_after)
    """
    
    def __init__(self, *args, **kwargs):
        """Inicializa sistema de callbacks."""
        super().__init__(*args, **kwargs)
        
        # Callback registries
        self._pre_callbacks: Dict[str, List[Callable]] = {}
        self._post_callbacks: Dict[str, List[Callable]] = {}
        self._error_callbacks: Dict[str, List[Callable]] = {}
        
        # Universal callbacks (aplican a TODAS las transiciones)
        self._universal_pre_callbacks: List[Callable] = []
        self._universal_post_callbacks: List[Callable] = []
        self._universal_error_callbacks: List[Callable] = []
        
        logger.debug(f"[CallbacksMixin] Initialized for {getattr(self, 'user_id', 'unknown')}")
    
    # ==================== CALLBACK REGISTRATION ====================
    
    def register_pre_callback(self, transition: str, callback: Callable):
        """
        Registra callback que se ejecuta ANTES de transición.
        
        Args:
            transition: Nombre de la transición (ej: "delegate_to_agent")
            callback: Función callback(from_state, to_state, context) -> bool
                     Debe retornar True para permitir transición, False para cancelar
        """
        if transition not in self._pre_callbacks:
            self._pre_callbacks[transition] = []
        self._pre_callbacks[transition].append(callback)
        logger.debug(f"[CallbacksMixin] Registered pre-callback for '{transition}'")
    
    def register_post_callback(self, transition: str, callback: Callable):
        """
        Registra callback que se ejecuta DESPUÉS de transición exitosa.
        
        Args:
            transition: Nombre de la transición
            callback: Función callback(from_state, to_state, context) -> None
        """
        if transition not in self._post_callbacks:
            self._post_callbacks[transition] = []
        self._post_callbacks[transition].append(callback)
        logger.debug(f"[CallbacksMixin] Registered post-callback for '{transition}'")
    
    def register_error_callback(self, transition: str, callback: Callable):
        """
        Registra callback que se ejecuta si transición FALLA.
        
        Args:
            transition: Nombre de la transición
            callback: Función callback(from_state, to_state, error, context) -> None
        """
        if transition not in self._error_callbacks:
            self._error_callbacks[transition] = []
        self._error_callbacks[transition].append(callback)
        logger.debug(f"[CallbacksMixin] Registered error-callback for '{transition}'")
    
    def register_universal_pre_callback(self, callback: Callable):
        """Registra callback que se ejecuta ANTES de CUALQUIER transición."""
        self._universal_pre_callbacks.append(callback)
        logger.debug(f"[CallbacksMixin] Registered universal pre-callback")
    
    def register_universal_post_callback(self, callback: Callable):
        """Registra callback que se ejecuta DESPUÉS de CUALQUIER transición exitosa."""
        self._universal_post_callbacks.append(callback)
        logger.debug(f"[CallbacksMixin] Registered universal post-callback")
    
    def register_universal_error_callback(self, callback: Callable):
        """Registra callback que se ejecuta si CUALQUIER transición falla."""
        self._universal_error_callbacks.append(callback)
        logger.debug(f"[CallbacksMixin] Registered universal error-callback")
    
    # ==================== CALLBACK EXECUTION ====================
    
    def _execute_pre_callbacks(self, transition: str, from_state: str, to_state: str, context: Dict[str, Any]) -> bool:
        """
        Ejecuta pre-callbacks (universales + específicos).
        
        Returns:
            bool: True si transición debe proceder, False si debe cancelarse
        """
        # Universal pre-callbacks
        for callback in self._universal_pre_callbacks:
            try:
                result = callback(from_state, to_state, context)
                if result is False:
                    logger.warning(f"[CallbacksMixin] Universal pre-callback cancelled transition '{transition}'")
                    return False
            except Exception as e:
                logger.error(f"[CallbacksMixin] Universal pre-callback error: {e}", exc_info=True)
                return False
        
        # Specific pre-callbacks
        if transition in self._pre_callbacks:
            for callback in self._pre_callbacks[transition]:
                try:
                    result = callback(from_state, to_state, context)
                    if result is False:
                        logger.warning(f"[CallbacksMixin] Pre-callback cancelled transition '{transition}'")
                        return False
                except Exception as e:
                    logger.error(f"[CallbacksMixin] Pre-callback error for '{transition}': {e}", exc_info=True)
                    return False
        
        return True
    
    def _execute_post_callbacks(self, transition: str, from_state: str, to_state: str, context: Dict[str, Any]):
        """Ejecuta post-callbacks (universales + específicos)."""
        # Universal post-callbacks
        for callback in self._universal_post_callbacks:
            try:
                callback(from_state, to_state, context)
            except Exception as e:
                logger.error(f"[CallbacksMixin] Universal post-callback error: {e}", exc_info=True)
        
        # Specific post-callbacks
        if transition in self._post_callbacks:
            for callback in self._post_callbacks[transition]:
                try:
                    callback(from_state, to_state, context)
                except Exception as e:
                    logger.error(f"[CallbacksMixin] Post-callback error for '{transition}': {e}", exc_info=True)
    
    def _execute_error_callbacks(self, transition: str, from_state: str, to_state: str, error: Exception, context: Dict[str, Any]):
        """Ejecuta error-callbacks (universales + específicos)."""
        # Universal error-callbacks
        for callback in self._universal_error_callbacks:
            try:
                callback(from_state, to_state, error, context)
            except Exception as e:
                logger.error(f"[CallbacksMixin] Universal error-callback failed: {e}", exc_info=True)
        
        # Specific error-callbacks
        if transition in self._error_callbacks:
            for callback in self._error_callbacks[transition]:
                try:
                    callback(from_state, to_state, error, context)
                except Exception as e:
                    logger.error(f"[CallbacksMixin] Error-callback failed for '{transition}': {e}", exc_info=True)
    
    # ==================== TRANSITION WITH CALLBACKS ====================
    
    def transition_with_callbacks(self, trigger: str, **kwargs):
        """
        Ejecuta transición con sistema completo de callbacks H03.
        
        Args:
            trigger: Nombre de la transición (ej: "delegate_to_agent")
            **kwargs: Argumentos adicionales para la transición
            
        Returns:
            bool: True si transición exitosa, False si falló o fue cancelada
        """
        from_state = self.state
        
        # Determinar to_state (requiere acceso a machine.get_transitions)
        try:
            transitions = [t for t in self.machine.get_triggers(from_state) if t.name == trigger]
            if not transitions:
                logger.warning(f"[CallbacksMixin] No valid transition '{trigger}' from '{from_state}'")
                return False
            to_state = transitions[0].dest if hasattr(transitions[0], 'dest') else "unknown"
        except Exception:
            to_state = "unknown"
        
        # Get context (asume que FSM tiene self.context)
        context = getattr(self, 'context', {})
        
        # PRE-CALLBACKS
        if not self._execute_pre_callbacks(trigger, from_state, to_state, context):
            logger.info(f"[CallbacksMixin] Transition '{trigger}' cancelled by pre-callback")
            return False
        
        # EXECUTE TRANSITION
        try:
            # Llama al trigger del FSM original
            trigger_method = getattr(self, trigger, None)
            if not trigger_method:
                raise AttributeError(f"Trigger '{trigger}' not found")
            
            result = trigger_method(**kwargs)
            
            # POST-CALLBACKS
            self._execute_post_callbacks(trigger, from_state, self.state, context)
            
            logger.info(f"[CallbacksMixin] Transition '{trigger}' completed: {from_state} → {self.state}")
            return True
        
        except Exception as e:
            # ERROR-CALLBACKS
            self._execute_error_callbacks(trigger, from_state, to_state, e, context)
            logger.error(f"[CallbacksMixin] Transition '{trigger}' failed: {e}", exc_info=True)
            return False
