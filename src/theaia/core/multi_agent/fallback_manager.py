# fallback_manager.py - H07.6 Core

import asyncio
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FailoverStrategy(Enum):
    '''Failover strategies'''
    IMMEDIATE = "immediate"
    RETRY = "retry"
    CIRCUIT_BREAKER = "circuit"


@dataclass
class FallbackConfig:
    '''Fallback configuration'''
    max_retries: int = 3
    retry_delay_ms: int = 100
    backoff_multiplier: float = 2.0
    max_delay_ms: int = 10000
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout_s: int = 60


class CircuitBreaker:
    '''Circuit breaker implementation'''
    
    def __init__(self, threshold: int = 5, timeout_s: int = 60):
        self.failure_count = 0
        self.success_count = 0
        self.threshold = threshold
        self.timeout = timeout_s
        self.last_failure_time = None
        self.state = "closed"
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        '''Execute function with circuit breaker protection'''
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise RuntimeError("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            self._record_failure()
            raise
    
    def _record_success(self):
        self.success_count += 1
        if self.state == "half-open":
            self.state = "closed"
            self.failure_count = 0
    
    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.threshold:
            self.state = "open"
    
    def _should_attempt_reset(self) -> bool:
        if not self.last_failure_time:
            return False
        return datetime.now() - self.last_failure_time >= timedelta(seconds=self.timeout)


class FallbackManager:
    '''Manage agent fallbacks and failovers'''
    
    def __init__(self, config: FallbackConfig = None):
        self.config = config or FallbackConfig()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.fallback_handlers: Dict[str, List[Callable]] = {}
        self.retry_history: Dict[str, List[datetime]] = {}
    
    async def execute_with_fallback(
        self, 
        agent_id: str, 
        primary_func: Callable, 
        fallback_funcs: List[Callable],
        *args, 
        **kwargs
    ) -> Any:
        '''Execute function with fallback chain'''
        
        if agent_id not in self.circuit_breakers:
            self.circuit_breakers[agent_id] = CircuitBreaker(
                self.config.circuit_breaker_threshold,
                self.config.circuit_breaker_timeout_s
            )
        
        breaker = self.circuit_breakers[agent_id]
        retry_delay = self.config.retry_delay_ms
        
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"Agent {agent_id}: Attempt {attempt + 1}")
                result = await breaker.call(primary_func, *args, **kwargs)
                return result
            except Exception as e:
                logger.warning(f"Agent {agent_id}: Attempt {attempt + 1} failed: {e}")
                self._record_retry(agent_id)
                
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(retry_delay / 1000)
                    retry_delay = min(
                        int(retry_delay * self.config.backoff_multiplier),
                        self.config.max_delay_ms
                    )
        
        for i, fallback_func in enumerate(fallback_funcs):
            try:
                logger.info(f"Agent {agent_id}: Trying fallback {i + 1}")
                result = await fallback_func(*args, **kwargs)
                return result
            except Exception as e:
                logger.warning(f"Agent {agent_id}: Fallback {i + 1} failed: {e}")
                if i == len(fallback_funcs) - 1:
                    raise
        
        raise RuntimeError(f"All attempts failed for agent {agent_id}")
    
    def register_fallback(self, agent_id: str, handler: Callable):
        '''Register a fallback handler'''
        if agent_id not in self.fallback_handlers:
            self.fallback_handlers[agent_id] = []
        self.fallback_handlers[agent_id].append(handler)
    
    def _record_retry(self, agent_id: str):
        '''Record retry attempt'''
        if agent_id not in self.retry_history:
            self.retry_history[agent_id] = []
        self.retry_history[agent_id].append(datetime.now())
    
    def get_retry_count(self, agent_id: str) -> int:
        '''Get retry count'''
        return len(self.retry_history.get(agent_id, []))
    
    def reset_agent(self, agent_id: str):
        '''Reset agent state'''
        if agent_id in self.circuit_breakers:
            del self.circuit_breakers[agent_id]
        if agent_id in self.retry_history:
            del self.retry_history[agent_id]
