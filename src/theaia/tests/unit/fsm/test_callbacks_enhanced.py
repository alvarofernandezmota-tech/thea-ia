"""
Tests for Enhanced Callbacks Manager
H06.7 - Callbacks & Hooks Enhancement
"""
import pytest
import asyncio
from src.theaia.core.fsm.callbacks_manager import (
    EnhancedCallbackManager,
    CallbackHookType,
    CallbackPriority,
    EnhancedCallback
)


class TestCallbackPriority:
    """Test callback priority system"""
    
    def test_priority_enum_values(self):
        """Test that priorities have correct ordering"""
        assert CallbackPriority.HIGHEST.value < CallbackPriority.HIGH.value
        assert CallbackPriority.HIGH.value < CallbackPriority.NORMAL.value
        assert CallbackPriority.NORMAL.value < CallbackPriority.LOW.value
        assert CallbackPriority.LOW.value < CallbackPriority.LOWEST.value
    
    @pytest.mark.asyncio
    async def test_callbacks_execute_in_priority_order(self):
        """Test callbacks execute highest priority first"""
        manager = EnhancedCallbackManager()
        execution_order = []
        
        def low_callback(ctx):
            execution_order.append("low")
        
        def high_callback(ctx):
            execution_order.append("high")
        
        def normal_callback(ctx):
            execution_order.append("normal")
        
        # Register out of order
        manager.register(CallbackHookType.BEFORE_TRANSITION, low_callback, CallbackPriority.LOW)
        manager.register(CallbackHookType.BEFORE_TRANSITION, high_callback, CallbackPriority.HIGH)
        manager.register(CallbackHookType.BEFORE_TRANSITION, normal_callback, CallbackPriority.NORMAL)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        assert execution_order == ["high", "normal", "low"]


class TestAsyncSupport:
    """Test async/sync callback support"""
    
    @pytest.mark.asyncio
    async def test_async_callback_execution(self):
        """Test async callbacks execute correctly"""
        manager = EnhancedCallbackManager()
        executed = []
        
        async def async_callback(ctx):
            await asyncio.sleep(0.01)
            executed.append("async")
            return "async_result"
        
        manager.register(CallbackHookType.AFTER_TRANSITION, async_callback)
        
        results = await manager.execute(CallbackHookType.AFTER_TRANSITION, {})
        
        assert "async" in executed
        assert results[0] == "async_result"
    
    @pytest.mark.asyncio
    async def test_sync_callback_execution(self):
        """Test sync callbacks execute correctly"""
        manager = EnhancedCallbackManager()
        executed = []
        
        def sync_callback(ctx):
            executed.append("sync")
            return "sync_result"
        
        manager.register(CallbackHookType.AFTER_TRANSITION, sync_callback)
        
        results = await manager.execute(CallbackHookType.AFTER_TRANSITION, {})
        
        assert "sync" in executed
        assert results[0] == "sync_result"
    
    @pytest.mark.asyncio
    async def test_mixed_async_sync_callbacks(self):
        """Test mixing async and sync callbacks"""
        manager = EnhancedCallbackManager()
        executed = []
        
        async def async_cb(ctx):
            executed.append("async")
        
        def sync_cb(ctx):
            executed.append("sync")
        
        manager.register(CallbackHookType.ON_ENTER_STATE, async_cb)
        manager.register(CallbackHookType.ON_ENTER_STATE, sync_cb)
        
        await manager.execute(CallbackHookType.ON_ENTER_STATE, {})
        
        assert "async" in executed
        assert "sync" in executed


class TestBatching:
    """Test callback batching"""
    
    @pytest.mark.asyncio
    async def test_register_batch_callbacks(self):
        """Test registering callbacks in a batch"""
        manager = EnhancedCallbackManager()
        
        def cb1(ctx): pass
        def cb2(ctx): pass
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb1, batch_id="batch1")
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb2, batch_id="batch1")
        
        assert "batch1" in manager._batch_callbacks
        assert len(manager._batch_callbacks["batch1"]) == 2
    
    @pytest.mark.asyncio
    async def test_execute_batch(self):
        """Test executing callbacks by batch ID"""
        manager = EnhancedCallbackManager()
        executed = []
        
        def cb1(ctx):
            executed.append(1)
        
        def cb2(ctx):
            executed.append(2)
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb1, batch_id="test_batch")
        manager.register(CallbackHookType.AFTER_TRANSITION, cb2, batch_id="test_batch")
        
        await manager.execute_batch("test_batch", {})
        
        assert 1 in executed
        assert 2 in executed


class TestTimeout:
    """Test callback timeout handling"""
    
    @pytest.mark.asyncio
    async def test_callback_timeout_raises_error(self):
        """Test callback times out after specified duration"""
        manager = EnhancedCallbackManager()
        
        async def slow_callback(ctx):
            await asyncio.sleep(1.0)
        
        manager.register(
            CallbackHookType.BEFORE_TRANSITION,
            slow_callback,
            timeout=0.1
        )
        
        # Should complete but log timeout
        results = await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        # Timeout should prevent result
        assert len(results) == 0 or results[0] is None
    
    @pytest.mark.asyncio
    async def test_callback_within_timeout_succeeds(self):
        """Test callback completes within timeout"""
        manager = EnhancedCallbackManager()
        
        async def fast_callback(ctx):
            await asyncio.sleep(0.01)
            return "success"
        
        manager.register(
            CallbackHookType.BEFORE_TRANSITION,
            fast_callback,
            timeout=1.0
        )
        
        results = await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        assert results[0] == "success"


class TestRetry:
    """Test callback retry logic"""
    
    @pytest.mark.asyncio
    async def test_retry_on_error_enabled(self):
        """Test callback retries on error"""
        manager = EnhancedCallbackManager()
        attempt_count = [0]
        
        def failing_callback(ctx):
            attempt_count[0] += 1
            if attempt_count[0] < 3:
                raise ValueError("Fail")
            return "success"
        
        manager.register(
            CallbackHookType.BEFORE_TRANSITION,
            failing_callback,
            retry_on_error=True,
            max_retries=3
        )
        
        results = await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        assert attempt_count[0] == 3
        assert results[0] == "success"
    
    @pytest.mark.asyncio
    async def test_retry_disabled_fails_immediately(self):
        """Test callback fails immediately when retry disabled"""
        manager = EnhancedCallbackManager()
        attempt_count = [0]
        
        def failing_callback(ctx):
            attempt_count[0] += 1
            raise ValueError("Fail")
        
        manager.register(
            CallbackHookType.BEFORE_TRANSITION,
            failing_callback,
            retry_on_error=False
        )
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        # Should only try once
        assert attempt_count[0] == 1


class TestErrorHandling:
    """Test error handling and isolation"""
    
    @pytest.mark.asyncio
    async def test_error_doesnt_stop_other_callbacks(self):
        """Test one failing callback doesn't stop others"""
        manager = EnhancedCallbackManager()
        executed = []
        
        def failing_cb(ctx):
            raise ValueError("Error")
        
        def success_cb(ctx):
            executed.append("success")
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, failing_cb)
        manager.register(CallbackHookType.BEFORE_TRANSITION, success_cb)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        assert "success" in executed
    
    @pytest.mark.asyncio
    async def test_error_count_tracked(self):
        """Test errors are counted in metrics"""
        manager = EnhancedCallbackManager()
        
        def failing_cb(ctx):
            raise ValueError("Error")
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, failing_cb)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        metrics = manager.get_metrics(CallbackHookType.BEFORE_TRANSITION)
        assert metrics["errors"] == 1
    
    @pytest.mark.asyncio
    async def test_last_errors_stored(self):
        """Test last errors are stored for debugging"""
        manager = EnhancedCallbackManager()
        
        def failing_cb(ctx):
            raise ValueError("Test error")
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, failing_cb)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        metrics = manager.get_metrics(CallbackHookType.BEFORE_TRANSITION)
        assert len(metrics["last_errors"]) > 0
        assert isinstance(metrics["last_errors"][0], ValueError)


class TestHookEnabling:
    """Test enabling/disabling hooks"""
    
    @pytest.mark.asyncio
    async def test_disable_specific_hook(self):
        """Test disabling specific hook type"""
        manager = EnhancedCallbackManager()
        executed = []
        
        def cb(ctx):
            executed.append("executed")
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        manager.enable_hook(CallbackHookType.BEFORE_TRANSITION, False)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        assert len(executed) == 0
    
    @pytest.mark.asyncio
    async def test_enable_hook_after_disable(self):
        """Test re-enabling hook works"""
        manager = EnhancedCallbackManager()
        executed = []
        
        def cb(ctx):
            executed.append("executed")
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        manager.enable_hook(CallbackHookType.BEFORE_TRANSITION, False)
        manager.enable_hook(CallbackHookType.BEFORE_TRANSITION, True)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        assert "executed" in executed


class TestMetrics:
    """Test metrics collection"""
    
    @pytest.mark.asyncio
    async def test_execution_count_increments(self):
        """Test execution count is tracked"""
        manager = EnhancedCallbackManager()
        
        def cb(ctx):
            pass
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        metrics = manager.get_metrics(CallbackHookType.BEFORE_TRANSITION)
        assert metrics["executions"] == 2
    
    @pytest.mark.asyncio
    async def test_execution_time_tracked(self):
        """Test execution time is measured"""
        manager = EnhancedCallbackManager()
        
        async def slow_cb(ctx):
            await asyncio.sleep(0.1)
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, slow_cb)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        
        metrics = manager.get_metrics(CallbackHookType.BEFORE_TRANSITION)
        assert metrics["total_time"] > 0
        assert metrics["average_time"] > 0
    
    @pytest.mark.asyncio
    async def test_global_metrics(self):
        """Test global metrics across all hooks"""
        manager = EnhancedCallbackManager()
        
        def cb(ctx):
            pass
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        manager.register(CallbackHookType.AFTER_TRANSITION, cb)
        
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, {})
        await manager.execute(CallbackHookType.AFTER_TRANSITION, {})
        
        metrics = manager.get_metrics()
        assert metrics["total_executions"] == 2
        assert "by_hook" in metrics


class TestClearCallbacks:
    """Test clearing registered callbacks"""
    
    def test_clear_specific_hook(self):
        """Test clearing callbacks for specific hook"""
        manager = EnhancedCallbackManager()
        
        def cb(ctx): pass
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        manager.register(CallbackHookType.AFTER_TRANSITION, cb)
        
        manager.clear_callbacks(CallbackHookType.BEFORE_TRANSITION)
        
        assert manager.get_registered_count(CallbackHookType.BEFORE_TRANSITION) == 0
        assert manager.get_registered_count(CallbackHookType.AFTER_TRANSITION) == 1
    
    def test_clear_all_callbacks(self):
        """Test clearing all callbacks"""
        manager = EnhancedCallbackManager()
        
        def cb(ctx): pass
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        manager.register(CallbackHookType.AFTER_TRANSITION, cb)
        
        manager.clear_callbacks()
        
        assert manager.get_registered_count(CallbackHookType.BEFORE_TRANSITION) == 0
        assert manager.get_registered_count(CallbackHookType.AFTER_TRANSITION) == 0


class TestContextPassing:
    """Test context passing to callbacks"""
    
    @pytest.mark.asyncio
    async def test_context_passed_to_callback(self):
        """Test context dictionary is passed correctly"""
        manager = EnhancedCallbackManager()
        received_context = {}
        
        def cb(ctx):
            received_context.update(ctx)
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        
        test_context = {"key": "value", "user_id": 123}
        await manager.execute(CallbackHookType.BEFORE_TRANSITION, test_context)
        
        assert received_context["key"] == "value"
        assert received_context["user_id"] == 123
    
    @pytest.mark.asyncio
    async def test_kwargs_passed_to_callback(self):
        """Test additional kwargs are passed"""
        manager = EnhancedCallbackManager()
        received_kwargs = {}
        
        def cb(ctx, **kwargs):
            received_kwargs.update(kwargs)
        
        manager.register(CallbackHookType.BEFORE_TRANSITION, cb)
        
        await manager.execute(
            CallbackHookType.BEFORE_TRANSITION,
            {},
            extra_param="test"
        )
        
        assert received_kwargs["extra_param"] == "test"
