# 📄 callbacks_manager.py - HITO 5 (OPCIÓN B: COMPOSICIÓN)

"""
Gestor centralizado de callbacks para ConversationStateMachine.

Arquitectura: Composición (no herencia)
- CallbacksManager es independiente
- Se inyecta en ConversationStateMachine
- Reusable en otras clases (AgentManager, ContextManager, etc)
- Multi-tenant ready (aislado por user_id)

Uso:
    fsm = ConversationStateMachine(user_id="user123")
    fsm.callbacks.register_callback('before_transition', my_callback)
    fsm.callbacks.execute_callbacks('before_transition', from_state, to_state, ...)

Módulo: src/theaia/core/fsm/callbacks_manager.py
Versión: 1.0.0
"""

from typing import Dict, List, Callable, Optional, Any, Tuple
from enum import Enum
import logging
from datetime import datetime
from functools import wraps

from theaia.core.fsm.exceptions import CallbackExecutionError, ErrorCategory


class CallbackEventType(Enum):
    """Tipos de eventos que disparan callbacks."""
    
    BEFORE_TRANSITION = "before_transition"
    """Antes de cualquier transición de estado."""
    
    AFTER_TRANSITION = "after_transition"
    """Después de cualquier transición de estado."""
    
    ON_ENTER_STATE = "on_enter_state"
    """Al entrar a un estado específico: on_enter_<state>."""
    
    ON_EXIT_STATE = "on_exit_state"
    """Al salir de un estado específico: on_exit_<state>."""
    
    ON_CALLBACK_ERROR = "on_callback_error"
    """Cuando un callback falla durante ejecución."""
    
    ON_TRANSITION_ERROR = "on_transition_error"
    """Cuando una transición falla (guard, etc)."""
    
    ON_CONTEXT_CHANGE = "on_context_change"
    """Cuando el contexto FSM cambia."""


class CallbackRecord:
    """Registro de ejecución de callback para auditoría."""
    
    def __init__(
        self,
        event_type: str,
        callback_name: str,
        timestamp: datetime,
        success: bool,
        duration_ms: float,
        error: Optional[Exception] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Inicializar registro de callback.
        
        Args:
            event_type: Tipo de evento (ej: 'before_transition')
            callback_name: Nombre del callback ejecutado
            timestamp: Momento de ejecución
            success: Si la ejecución fue exitosa
            duration_ms: Duración en milisegundos
            error: Excepción si ocurrió
            metadata: Datos adicionales del evento
        """
        self.event_type = event_type
        self.callback_name = callback_name
        self.timestamp = timestamp
        self.success = success
        self.duration_ms = duration_ms
        self.error = error
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para serialización.
        
        Returns:
            Diccionario con datos del registro.
        """
        return {
            'event_type': self.event_type,
            'callback_name': self.callback_name,
            'timestamp': self.timestamp.isoformat(),
            'success': self.success,
            'duration_ms': self.duration_ms,
            'error': str(self.error) if self.error else None,
            'metadata': self.metadata
        }


class CallbacksManager:
    """Gestor centralizado de callbacks para FSM.
    
    Proporciona:
    - Registro de callbacks por evento
    - Ejecución segura con error handling
    - Auditoría y logging
    - Enable/disable por tipos de evento
    - Multi-tenant (aislado por user_id del FSM)
    
    Composición con ConversationStateMachine:
        fsm = ConversationStateMachine(user_id="user123")
        fsm.callbacks.register_callback('before_transition', my_callback)
        fsm.callbacks.execute_callbacks('before_transition', from_state, to_state, ...)
    
    Attributes:
        fsm: Referencia a ConversationStateMachine (inyección de dependencia)
        _registry: Dict[str, List[Callable]] - Callbacks por evento
        _enabled: bool - Si callbacks están habilitados
        _event_enabled: Dict[str, bool] - Por-evento enable/disable
        _history: List[CallbackRecord] - Auditoría de ejecuciones
        _max_history: int - Máximo de registros a mantener (FIFO)
        logger: Logger específico del user_id
    """
    
    def __init__(
        self,
        fsm: 'ConversationStateMachine',
        max_history: int = 1000
    ):
        """Inicializar gestor de callbacks.
        
        Args:
            fsm: Instancia de ConversationStateMachine
            max_history: Máximo número de registros de auditoría (default: 1000)
        
        Raises:
            ValueError: Si fsm es None o max_history < 1
        """
        if fsm is None:
            raise ValueError("FSM cannot be None")
        if max_history < 1:
            raise ValueError("max_history must be >= 1")
        
        self.fsm = fsm
        self._registry: Dict[str, List[Callable]] = {}
        self._enabled = True
        self._event_enabled: Dict[str, bool] = {}
        self._history: List[CallbackRecord] = []
        self._max_history = max_history
        
        # Logger específico del user_id para multi-tenant
        self.logger = logging.getLogger(f"thea_ia.callbacks.{fsm.user_id}")
    
    def register_callback(
        self,
        event_type: str,
        callback: Callable,
        name: Optional[str] = None
    ) -> 'CallbacksManager':
        """Registrar un callback para un tipo de evento.
        
        Args:
            event_type: Tipo de evento (ej: 'before_transition')
            callback: Función callable a ejecutar
            name: Nombre descriptivo del callback (default: callback.__name__)
        
        Returns:
            Self para encadenación fluida
        
        Raises:
            TypeError: Si callback no es callable
            ValueError: Si event_type está vacío
        
        Example:
            manager.register_callback(
                'before_transition',
                my_callback,
                name='validate_agent_available'
            )
        """
        if not event_type or not isinstance(event_type, str):
            raise ValueError("event_type must be non-empty string")
        
        if not callable(callback):
            raise TypeError(f"callback must be callable, got {type(callback)}")
        
        if event_type not in self._registry:
            self._registry[event_type] = []
        
        self._registry[event_type].append(callback)
        
        cb_name = name or getattr(callback, '__name__', 'anonymous')
        self.logger.debug(f"Registered callback: {event_type} -> {cb_name}")
        
        return self
    
    def unregister_callback(
        self,
        event_type: str,
        callback: Callable
    ) -> bool:
        """Desregistrar un callback.
        
        Args:
            event_type: Tipo de evento
            callback: Callback a remover
        
        Returns:
            True si fue removido, False si no existía
        """
        if event_type not in self._registry:
            return False
        
        try:
            self._registry[event_type].remove(callback)
            self.logger.debug(f"Unregistered callback: {event_type}")
            return True
        except ValueError:
            return False
    
    def execute_callbacks(
        self,
        event_type: str,
        **kwargs
    ) -> Tuple[int, int]:
        """Ejecutar todos los callbacks registrados para un evento.
        
        Args:
            event_type: Tipo de evento a disparar
            **kwargs: Argumentos a pasar a los callbacks
        
        Returns:
            Tupla (total_callbacks, successfully_executed)
        
        Raises:
            CallbackExecutionError: Si callbacks_enabled es False o hay errores críticos
        
        Example:
            success_count, total = fsm.callbacks.execute_callbacks(
                'before_transition',
                from_state='initial',
                to_state='processing',
                trigger='start'
            )
        
        Notes:
            - Si callbacks están deshabilitados globalmente, retorna (0, 0)
            - Errores en callbacks individuales son capturados y loguedos
            - Se registra en auditoría cada ejecución
            - Callbacks se ejecutan secuencialmente
        """
        if not self._enabled or not self._event_enabled.get(event_type, True):
            return (0, 0)
        
        callbacks = self._registry.get(event_type, [])
        if not callbacks:
            return (0, 0)
        
        successful = 0
        
        for callback in callbacks:
            try:
                start_time = datetime.now()
                
                # Ejecutar callback
                callback(self.fsm, **kwargs)
                
                duration_ms = (datetime.now() - start_time).total_seconds() * 1000
                successful += 1
                
                # Registrar éxito
                self._record_execution(
                    event_type=event_type,
                    callback_name=getattr(callback, '__name__', 'anonymous'),
                    success=True,
                    duration_ms=duration_ms
                )
                
            except Exception as e:
                duration_ms = (datetime.now() - start_time).total_seconds() * 1000
                
                # Registrar error
                self._record_execution(
                    event_type=event_type,
                    callback_name=getattr(callback, '__name__', 'anonymous'),
                    success=False,
                    duration_ms=duration_ms,
                    error=e
                )
                
                # Disparar callback de error (si existe)
                try:
                    self._trigger_error_callback(event_type, e, kwargs)
                except Exception:
                    pass  # No propagar errores de error callbacks
                
                self.logger.error(
                    f"Callback error in {event_type}: {callback.__name__}",
                    exc_info=True
                )
        
        return (len(callbacks), successful)
    
    def enable(self, event_type: Optional[str] = None) -> 'CallbacksManager':
        """Habilitar callbacks.
        
        Args:
            event_type: Si se especifica, habilita solo ese tipo de evento.
                       Si es None, habilita todos globalmente.
        
        Returns:
            Self para encadenación
        
        Example:
            manager.disable('before_transition')
            # ... hacer algo sin callbacks de transición ...
            manager.enable('before_transition')
        """
        if event_type is None:
            self._enabled = True
            self.logger.debug("Callbacks globally enabled")
        else:
            self._event_enabled[event_type] = True
            self.logger.debug(f"Callbacks enabled for: {event_type}")
        
        return self
    
    def disable(self, event_type: Optional[str] = None) -> 'CallbacksManager':
        """Deshabilitar callbacks.
        
        Args:
            event_type: Si se especifica, deshabilita solo ese tipo de evento.
                       Si es None, deshabilita todos globalmente.
        
        Returns:
            Self para encadenación
        """
        if event_type is None:
            self._enabled = False
            self.logger.debug("Callbacks globally disabled")
        else:
            self._event_enabled[event_type] = False
            self.logger.debug(f"Callbacks disabled for: {event_type}")
        
        return self
    
    def is_enabled(self, event_type: Optional[str] = None) -> bool:
        """Verificar si callbacks están habilitados.
        
        Args:
            event_type: Si se especifica, verifica estado de ese evento.
                       Si es None, verifica estado global.
        
        Returns:
            True si están habilitados
        """
        if event_type is None:
            return self._enabled
        
        return self._enabled and self._event_enabled.get(event_type, True)
    
    def get_history(
        self,
        event_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Obtener historial de ejecuciones de callbacks (auditoría).
        
        Args:
            event_type: Filtrar por tipo de evento (None = todos)
            limit: Número máximo de registros a retornar (None = todos)
        
        Returns:
            Lista de diccionarios con información de ejecuciones
        
        Example:
            history = manager.get_history(event_type='before_transition', limit=10)
            for record in history:
                print(f"{record['callback_name']}: {record['duration_ms']}ms")
        """
        history = self._history
        
        if event_type:
            history = [r for r in history if r.event_type == event_type]
        
        if limit:
            history = history[-limit:]
        
        return [r.to_dict() for r in history]
    
    def clear_history(self) -> 'CallbacksManager':
        """Limpiar historial de auditoría.
        
        Returns:
            Self para encadenación
        """
        self._history.clear()
        self.logger.debug("Callback history cleared")
        return self
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de ejecuciones de callbacks.
        
        Returns:
            Diccionario con estadísticas:
                - total_callbacks: Número total registrado
                - total_executions: Número total de ejecuciones
                - successful_executions: Ejecuciones exitosas
                - failed_executions: Ejecuciones fallidas
                - average_duration_ms: Duración promedio
                - enabled: Estado global
                - events_with_callbacks: Tipos de eventos con callbacks
        
        Example:
            stats = manager.get_statistics()
            print(f"Success rate: {stats['success_rate']:.2%}")
        """
        total_callbacks = sum(len(cbs) for cbs in self._registry.values())
        
        successful = sum(1 for r in self._history if r.success)
        failed = len(self._history) - successful
        
        avg_duration = 0
        if self._history:
            avg_duration = sum(r.duration_ms for r in self._history) / len(self._history)
        
        return {
            'total_callbacks_registered': total_callbacks,
            'total_executions': len(self._history),
            'successful_executions': successful,
            'failed_executions': failed,
            'success_rate': successful / len(self._history) if self._history else 0,
            'average_duration_ms': avg_duration,
            'max_history_size': self._max_history,
            'current_history_size': len(self._history),
            'globally_enabled': self._enabled,
            'events_with_callbacks': list(self._registry.keys())
        }
    
    def _record_execution(
        self,
        event_type: str,
        callback_name: str,
        success: bool,
        duration_ms: float,
        error: Optional[Exception] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Registrar ejecución de callback en historial (auditoría).
        
        Args:
            event_type: Tipo de evento
            callback_name: Nombre del callback
            success: Si fue exitoso
            duration_ms: Duración en ms
            error: Excepción si ocurrió
            metadata: Datos adicionales
        """
        record = CallbackRecord(
            event_type=event_type,
            callback_name=callback_name,
            timestamp=datetime.now(),
            success=success,
            duration_ms=duration_ms,
            error=error,
            metadata=metadata
        )
        
        self._history.append(record)
        
        # Mantener FIFO: si excedemos max_history, remover el más antiguo
        if len(self._history) > self._max_history:
            self._history.pop(0)
    
    def _trigger_error_callback(
        self,
        event_type: str,
        error: Exception,
        context: Dict[str, Any]
    ) -> None:
        """Disparar callbacks de error cuando algo falla.
        
        Args:
            event_type: Tipo de evento que falló
            error: Excepción que ocurrió
            context: Contexto del evento
        """
        error_callbacks = self._registry.get('on_callback_error', [])
        
        for callback in error_callbacks:
            try:
                callback(
                    self.fsm,
                    event_type=event_type,
                    error=error,
                    context=context
                )
            except Exception:
                self.logger.debug("Error in error callback (silently ignored)")
    
    def __repr__(self) -> str:
        """Representación string de CallbacksManager."""
        total = sum(len(cbs) for cbs in self._registry.values())
        return (
            f"CallbacksManager("
            f"user_id={self.fsm.user_id}, "
            f"callbacks={total}, "
            f"enabled={self._enabled})"
        )