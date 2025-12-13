# test_fallback.py - H07.6 Tests

import pytest
import asyncio
from unittest.mock import AsyncMock
from theaia.core.multi_agent.fallback_manager import (
    FallbackManager, 
    CircuitBreaker, 
    FallbackConfig
)


class TestCircuitBreaker:
    '''Circuit breaker tests'''
    
    def setup_method(self):
        self.breaker = CircuitBreaker(threshold=2, timeout_s=1)
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_closes_after_successes(self):
        func = AsyncMock(return_value="success")
        result = await self.breaker.call(func)
        assert result == "success"
        assert self.breaker.state == "closed"
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_opens_after_threshold(self):
        func = AsyncMock(side_effect=Exception("error"))
        
        for _ in range(2):
            with pytest.raises(Exception):
                await self.breaker.call(func)
        
        assert self.breaker.state == "open"
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_rejects_when_open(self):
        func = AsyncMock(side_effect=Exception("error"))
        
        for _ in range(2):
            with pytest.raises(Exception):
                await self.breaker.call(func)
        
        with pytest.raises(RuntimeError, match="Circuit breaker is open"):
            await self.breaker.call(func)


class TestFallbackManager:
    '''Fallback manager tests'''
    
    def setup_method(self):
        self.config = FallbackConfig(max_retries=3, retry_delay_ms=10)
        self.manager = FallbackManager(self.config)
    
    @pytest.mark.asyncio
    async def test_primary_function_succeeds(self):
        primary = AsyncMock(return_value="primary_result")
        fallback = AsyncMock()
        
        result = await self.manager.execute_with_fallback(
            "agent_1", primary, [fallback]
        )
        
        assert result == "primary_result"
        fallback.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_fallback_called_on_failure(self):
        primary = AsyncMock(side_effect=Exception("failed"))
        fallback = AsyncMock(return_value="fallback_result")
        
        result = await self.manager.execute_with_fallback(
            "agent_1", primary, [fallback]
        )
        
        assert result == "fallback_result"
    
    @pytest.mark.asyncio
    async def test_retry_count_tracking(self):
        primary = AsyncMock(side_effect=Exception("failed"))
        fallback = AsyncMock(return_value="ok")
        
        await self.manager.execute_with_fallback("agent_1", primary, [fallback])
        
        assert self.manager.get_retry_count("agent_1") > 0
    
    @pytest.mark.asyncio
    async def test_agent_reset(self):
        primary = AsyncMock(side_effect=Exception("failed"))
        fallback = AsyncMock(return_value="ok")
        
        await self.manager.execute_with_fallback("agent_1", primary, [fallback])
        self.manager.reset_agent("agent_1")
        
        assert self.manager.get_retry_count("agent_1") == 0
