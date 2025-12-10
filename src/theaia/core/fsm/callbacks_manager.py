from enum import Enum
from typing import Callable, Any, Optional, List, Dict
from dataclasses import dataclass, field
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CallbackPriority(Enum):
    """Prioridades de ejecución de callbacks"""
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    LOWEST = 4

class CallbackHookType(Enum):
    """Tipos de hooks FSM"""
    BEFORE_TRANSITION = "before_transition"
    AFTER_TRANSITION = "after_transition"
    ON_ENTER_STATE = "on_enter_state"
    ON_EXIT_STATE = "on_exit_state"
    ON_ERROR = "on_error"
    ON_STATE_TIMEOUT = "on_state_timeout"

@dataclass
class EnhancedCallback:
    """Callback con prioridad y metadata"""
    func: Callable
    priority: CallbackPriority = CallbackPriority.NORMAL
    is_async: bool = False
    batch_id: Optional[str] = None
    timeout: Optional[float] = None  # segundos
    retry_on_error: bool = False
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)

class EnhancedCallbackManager:
    """
    Gestor avanzado de callbacks con:
    - Prioridades
    - Soporte async/sync
    - Batching
    - Timeouts
    - Retry logic
    - Métricas avanzadas
    """
    
    def __init__(self):
        self._callbacks: Dict[CallbackHookType, List[EnhancedCallback]] = {
            hook: [] for hook in CallbackHookType
        }
        self._batch_callbacks: Dict[str, List[EnhancedCallback]] = {}
        self._enabled = True
        self._hook_enabled: Dict[CallbackHookType, bool] = {
            hook: True for hook in CallbackHookType
        }
        
        # Métricas
        self._execution_count: Dict[CallbackHookType, int] = {
            hook: 0 for hook in CallbackHookType
        }
        self._total_execution_time: Dict[CallbackHookType, float] = {
            hook: 0.0 for hook in CallbackHookType
        }
        self._error_count: Dict[CallbackHookType, int] = {
            hook: 0 for hook in CallbackHookType
        }
        self._last_errors: Dict[CallbackHookType, List[Exception]] = {
            hook: [] for hook in CallbackHookType
        }
    
    def register(
        self,
        hook_type: CallbackHookType,
        callback: Callable,
        priority: CallbackPriority = CallbackPriority.NORMAL,
        batch_id: Optional[str] = None,
        timeout: Optional[float] = None,
        retry_on_error: bool = False,
        **metadata
    ) -> None:
        """Registra callback con configuración avanzada"""
        is_async = asyncio.iscoroutinefunction(callback)
        
        enhanced_cb = EnhancedCallback(
            func=callback,
            priority=priority,
            is_async=is_async,
            batch_id=batch_id,
            timeout=timeout,
            retry_on_error=retry_on_error,
            metadata=metadata
        )
        
        self._callbacks[hook_type].append(enhanced_cb)
        
        # Ordenar por prioridad
        self._callbacks[hook_type].sort(key=lambda x: x.priority.value)
        
        # Registrar en batch si aplica
        if batch_id:
            if batch_id not in self._batch_callbacks:
                self._batch_callbacks[batch_id] = []
            self._batch_callbacks[batch_id].append(enhanced_cb)
        
        logger.debug(
            f"Registered {hook_type.value} callback with priority {priority.name}"
        )
    
    async def execute(
        self,
        hook_type: CallbackHookType,
        context: Dict[str, Any],
        **kwargs
    ) -> List[Any]:
        """Ejecuta todos los callbacks de un hook con manejo avanzado"""
        if not self._enabled or not self._hook_enabled.get(hook_type, True):
            return []
        
        results = []
        callbacks = self._callbacks.get(hook_type, [])
        
        start_time = datetime.now()
        
        for cb in callbacks:
            try:
                result = await self._execute_single(cb, context, **kwargs)
                results.append(result)
                
            except Exception as e:
                self._error_count[hook_type] += 1
                self._last_errors[hook_type].append(e)
                
                # Mantener solo últimos 10 errores
                if len(self._last_errors[hook_type]) > 10:
                    self._last_errors[hook_type].pop(0)
                
                logger.error(
                    f"Callback {hook_type.value} failed: {e}",
                    exc_info=True
                )
                
                # No romper ejecución de otros callbacks
                if not cb.retry_on_error:
                    continue
        
        # Actualizar métricas
        execution_time = (datetime.now() - start_time).total_seconds()
        self._execution_count[hook_type] += 1
        self._total_execution_time[hook_type] += execution_time
        
        return results
    
    async def _execute_single(
        self,
        callback: EnhancedCallback,
        context: Dict[str, Any],
        **kwargs
    ) -> Any:
        """Ejecuta un callback individual con timeout y retry"""
        retries = 0
        last_error = None
        
        while retries <= callback.max_retries:
            try:
                if callback.is_async:
                    if callback.timeout:
                        return await asyncio.wait_for(
                            callback.func(context, **kwargs),
                            timeout=callback.timeout
                        )
                    return await callback.func(context, **kwargs)
                else:
                    # Ejecutar sync en thread pool para no bloquear
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(
                        None,
                        callback.func,
                        context,
                        **kwargs
                    )
                    
            except asyncio.TimeoutError:
                logger.warning(
                    f"Callback timeout after {callback.timeout}s"
                )
                raise
                
            except Exception as e:
                last_error = e
                if callback.retry_on_error and retries < callback.max_retries:
                    retries += 1
                    await asyncio.sleep(0.1 * retries)  # Backoff
                    continue
                raise
        
        if last_error:
            raise last_error
    
    async def execute_batch(
        self,
        batch_id: str,
        context: Dict[str, Any],
        **kwargs
    ) -> List[Any]:
        """Ejecuta todos los callbacks de un batch"""
        if batch_id not in self._batch_callbacks:
            return []
        
        results = []
        for cb in self._batch_callbacks[batch_id]:
            try:
                result = await self._execute_single(cb, context, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch {batch_id} callback failed: {e}")
        
        return results
    
    def enable_hook(self, hook_type: CallbackHookType, enabled: bool = True):
        """Habilita/deshabilita un tipo de hook específico"""
        self._hook_enabled[hook_type] = enabled
    
    def get_metrics(self, hook_type: Optional[CallbackHookType] = None) -> Dict:
        """Obtiene métricas de ejecución"""
        if hook_type:
            avg_time = (
                self._total_execution_time[hook_type] / 
                self._execution_count[hook_type]
                if self._execution_count[hook_type] > 0 else 0
            )
            return {
                "executions": self._execution_count[hook_type],
                "total_time": self._total_execution_time[hook_type],
                "average_time": avg_time,
                "errors": self._error_count[hook_type],
                "last_errors": self._last_errors[hook_type][-3:]
            }
        
        # Métricas globales
        total_executions = sum(self._execution_count.values())
        total_errors = sum(self._error_count.values())
        
        return {
            "total_executions": total_executions,
            "total_errors": total_errors,
            "error_rate": total_errors / total_executions if total_executions > 0 else 0,
            "by_hook": {
                hook.value: self.get_metrics(hook)
                for hook in CallbackHookType
            }
        }
    
    def clear_callbacks(self, hook_type: Optional[CallbackHookType] = None):
        """Limpia callbacks registrados"""
        if hook_type:
            self._callbacks[hook_type] = []
        else:
            for hook in CallbackHookType:
                self._callbacks[hook] = []
            self._batch_callbacks.clear()
    
    def get_registered_count(self, hook_type: CallbackHookType) -> int:
        """Obtiene número de callbacks registrados para un hook"""
        return len(self._callbacks.get(hook_type, []))
