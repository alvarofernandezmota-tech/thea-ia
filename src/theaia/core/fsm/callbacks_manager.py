"""
CallbacksManager - Sistema de callbacks para ConversationStateMachine

Proporciona un sistema robusto para registrar y ejecutar callbacks en eventos FSM.
"""

from collections import deque
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time
import logging


# ═══════════════════════════════════════════════════════════════════════════
# CALLBACK EVENT TYPE
# ═══════════════════════════════════════════════════════════════════════════

class CallbackEventType:
    """Tipos de eventos de callback."""
    
    BEFORE_TRANSITION = "before_transition"
    AFTER_TRANSITION = "after_transition"
    ON_ENTER_STATE = "on_enter_state"
    ON_EXIT_STATE = "on_exit_state"
    ON_CALLBACK_ERROR = "on_callback_error"
    ON_TRANSITION_ERROR = "on_transition_error"
    ON_CONTEXT_CHANGE = "on_context_change"


# ═══════════════════════════════════════════════════════════════════════════
# CALLBACK RECORD
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CallbackRecord:
    """Registro de ejecución de callback."""
    
    event_type: str
    callback_name: str
    timestamp: datetime
    success: bool
    duration_ms: float
    error: Optional[Exception] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario."""
        return {
            "event_type": self.event_type,
            "callback_name": self.callback_name,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "duration_ms": self.duration_ms,
            "error": str(self.error) if self.error else None,
            "metadata": self.metadata
        }


# ═══════════════════════════════════════════════════════════════════════════
# CALLBACKS MANAGER
# ═══════════════════════════════════════════════════════════════════════════

class CallbacksManager:
    """
    Gestiona callbacks para eventos del FSM.
    
    Proporciona:
    - Registro/desregistro de callbacks
    - Ejecución ordenada con manejo de errores
    - Auditoría y estadísticas
    - Enable/disable por evento o globalmente
    
    Args:
        fsm: Instancia de ConversationStateMachine (DEBE tener user_id)
        max_history: Tamaño máximo del historial de auditoría
    """
    
    def __init__(
        self,
        fsm: Any,
        max_history: int = 1000
    ):
        if fsm is None:
            raise ValueError("fsm no puede ser None")
        if max_history < 1:
            raise ValueError("max_history debe ser >= 1")
        
        self.fsm = fsm
        self._max_history = max_history
        
        # Registro de callbacks por tipo de evento
        self._registry: Dict[str, List[Callable]] = {}
        
        # Historial de ejecuciones (FIFO)
        self._history: deque = deque(maxlen=max_history)
        
        # Enable/disable
        self._enabled = True
        self._event_enabled: Dict[str, bool] = {}
        
        # Logger
        user_id = getattr(fsm, 'user_id', 'unknown')
        self.logger = logging.getLogger(
            f"theaia.fsm.callbacks.{user_id}"
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # REGISTRO
    # ═══════════════════════════════════════════════════════════════════════
    
    def register_callback(
        self,
        event_type: str,
        callback: Callable,
        name: Optional[str] = None
    ) -> 'CallbacksManager':
        """
        Registrar callback para un evento.
        
        Args:
            event_type: Tipo de evento (ej: "before_transition")
            callback: Función callback(fsm, **kwargs)
            name: Nombre personalizado (opcional)
            
        Returns:
            self (para encadenación)
        """
        if not event_type:
            raise ValueError("event_type no puede estar vacío")
        
        if not callable(callback):
            raise TypeError(f"callback debe ser callable, recibido: {type(callback)}")
        
        if event_type not in self._registry:
            self._registry[event_type] = []
        
        self._registry[event_type].append(callback)
        
        callback_name = name or getattr(callback, '__name__', 'anonymous')
        self.logger.debug(
            f"Callback '{callback_name}' registrado para '{event_type}'"
        )
        
        return self
    
    def unregister_callback(
        self,
        event_type: str,
        callback: Callable
    ) -> bool:
        """
        Desregistrar callback.
        
        Returns:
            True si se eliminó, False si no existía
        """
        if event_type not in self._registry:
            return False
        
        if callback in self._registry[event_type]:
            self._registry[event_type].remove(callback)
            return True
        
        return False
    
    # ═══════════════════════════════════════════════════════════════════════
    # EJECUCIÓN
    # ═══════════════════════════════════════════════════════════════════════
    
    def execute_callbacks(
        self,
        event_type: str,
        **kwargs
    ) -> Tuple[int, int]:
        """
        Ejecutar todos los callbacks para un evento.
        
        Args:
            event_type: Tipo de evento
            **kwargs: Argumentos para callbacks
            
        Returns:
            (total_ejecutados, exitosos)
        """
        # Check si está habilitado
        if not self._enabled or not self._event_enabled.get(event_type, True):
            return (0, 0)
        
        if event_type not in self._registry:
            return (0, 0)
        
        callbacks = self._registry[event_type]
        total = len(callbacks)
        successful = 0
        
        for callback in callbacks:
            callback_name = getattr(callback, '__name__', 'anonymous')
            start_time = time.time()
            
            try:
                callback(self.fsm, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                # Registrar éxito
                record = CallbackRecord(
                    event_type=event_type,
                    callback_name=callback_name,
                    timestamp=datetime.now(),
                    success=True,
                    duration_ms=duration_ms
                )
                self._history.append(record)
                successful += 1
                
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                
                # Registrar error
                record = CallbackRecord(
                    event_type=event_type,
                    callback_name=callback_name,
                    timestamp=datetime.now(),
                    success=False,
                    duration_ms=duration_ms,
                    error=e
                )
                self._history.append(record)
                
                self.logger.error(
                    f"Error en callback '{callback_name}' para '{event_type}': {e}"
                )
        
        return (total, successful)
    
    # ═══════════════════════════════════════════════════════════════════════
    # ENABLE/DISABLE
    # ═══════════════════════════════════════════════════════════════════════
    
    def disable(self, event_type: Optional[str] = None) -> 'CallbacksManager':
        """Deshabilitar callbacks (globalmente o por evento)."""
        if event_type is None:
            self._enabled = False
        else:
            self._event_enabled[event_type] = False
        return self
    
    def enable(self, event_type: Optional[str] = None) -> 'CallbacksManager':
        """Habilitar callbacks (globalmente o por evento)."""
        if event_type is None:
            self._enabled = True
        else:
            self._event_enabled[event_type] = True
        return self
    
    def is_enabled(self, event_type: Optional[str] = None) -> bool:
        """Verificar si callbacks están habilitados."""
        if event_type is None:
            return self._enabled
        return self._enabled and self._event_enabled.get(event_type, True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # HISTORIAL Y AUDITORÍA
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_history(
        self,
        event_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtener historial de ejecuciones.
        
        Args:
            event_type: Filtrar por tipo (opcional)
            limit: Limitar resultados (opcional)
        """
        history = list(self._history)
        
        if event_type:
            history = [r for r in history if r.event_type == event_type]
        
        if limit:
            history = history[-limit:]
        
        return [r.to_dict() for r in history]
    
    def clear_history(self) -> 'CallbacksManager':
        """Limpiar historial."""
        self._history.clear()
        return self
    
    # ═══════════════════════════════════════════════════════════════════════
    # ESTADÍSTICAS
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de callbacks."""
        total_registered = sum(
            len(callbacks) for callbacks in self._registry.values()
        )
        
        total_executions = len(self._history)
        successful_executions = sum(1 for r in self._history if r.success)
        failed_executions = total_executions - successful_executions
        
        success_rate = (
            successful_executions / total_executions 
            if total_executions > 0 
            else 0.0
        )
        
        return {
            "total_callbacks_registered": total_registered,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": success_rate,
            "enabled": self._enabled
        }
    
    def __repr__(self) -> str:
        """Representación string."""
        user_id = getattr(self.fsm, 'user_id', 'unknown')
        total_callbacks = sum(
            len(callbacks) for callbacks in self._registry.values()
        )
        return (
            f"<CallbacksManager user={user_id} "
            f"callbacks={total_callbacks} "
            f"enabled={self._enabled}>"
        )
