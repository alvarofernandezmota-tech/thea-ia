# test_performance_monitor.py - H07.7 Tests

import pytest
import asyncio
from unittest.mock import AsyncMock
from theaia.core.multi_agent.performance_monitor import PerformanceMonitor


class TestPerformanceMonitor:
    '''Performance monitor tests'''
    
    def setup_method(self):
        self.monitor = PerformanceMonitor()
    
    @pytest.mark.asyncio
    async def test_track_successful_operation(self):
        async def sample_func():
            await asyncio.sleep(0.01)
            return "result"
        
        result = await self.monitor.track_operation("agent_1", "test_op", sample_func)
        
        assert result == "result"
        assert len(self.monitor.metrics) == 1
        assert self.monitor.metrics[0].status == "success"
    
    @pytest.mark.asyncio
    async def test_track_failed_operation(self):
        async def failing_func():
            raise Exception("error")
        
        with pytest.raises(Exception):
            await self.monitor.track_operation("agent_1", "test_op", failing_func)
        
        assert self.monitor.metrics[0].status == "failure"
    
    @pytest.mark.asyncio
    async def test_operation_statistics(self):
        async def sample_func():
            await asyncio.sleep(0.01)
        
        for _ in range(5):
            await self.monitor.track_operation("agent_1", "test_op", sample_func)
        
        stats = self.monitor.get_operation_stats("test_op")
        assert stats['total_calls'] == 5
    
    @pytest.mark.asyncio
    async def test_system_health(self):
        async def sample_func():
            await asyncio.sleep(0.01)
        
        for i in range(3):
            await self.monitor.track_operation(f"agent_{i}", "op", sample_func)
        
        health = self.monitor.get_system_health()
        assert health['total_operations'] == 3
        assert health['unique_agents'] == 3
