# performance_monitor.py - H07.7 Core

import time
import asyncio
from typing import Dict, List
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import statistics
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    '''Performance metrics'''
    agent_id: str
    operation: str
    execution_time_ms: float
    memory_used_mb: float = 0
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "success"


class PerformanceMonitor:
    '''Monitor agent performance'''
    
    def __init__(self, max_history: int = 1000):
        self.metrics: List[PerformanceMetrics] = []
        self.max_history = max_history
        self.operation_stats: Dict[str, Dict] = defaultdict(lambda: {
            'count': 0, 'total_time': 0, 'min_time': float('inf'),
            'max_time': 0, 'errors': 0
        })
    
    async def track_operation(self, agent_id: str, operation: str, func, *args, **kwargs):
        '''Track operation performance'''
        start_time = time.time()
        status = "success"
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
        except asyncio.TimeoutError:
            status = "timeout"
            raise
        except Exception:
            status = "failure"
            raise
        finally:
            execution_time = (time.time() - start_time) * 1000
            
            metric = PerformanceMetrics(
                agent_id=agent_id,
                operation=operation,
                execution_time_ms=execution_time,
                status=status
            )
            self._record_metric(metric)
        
        return result
    
    def _record_metric(self, metric: PerformanceMetrics):
        self.metrics.append(metric)
        
        if len(self.metrics) > self.max_history:
            self.metrics = self.metrics[-self.max_history:]
        
        key = metric.operation
        stats = self.operation_stats[key]
        stats['count'] += 1
        stats['total_time'] += metric.execution_time_ms
        stats['min_time'] = min(stats['min_time'], metric.execution_time_ms)
        stats['max_time'] = max(stats['max_time'], metric.execution_time_ms)
        
        if metric.status != "success":
            stats['errors'] += 1
    
    def get_operation_stats(self, operation: str) -> Dict:
        '''Get operation statistics'''
        stats = self.operation_stats.get(operation, {})
        
        if stats.get('count', 0) > 0:
            return {
                'operation': operation,
                'total_calls': stats['count'],
                'avg_time_ms': stats['total_time'] / stats['count'],
                'min_time_ms': stats['min_time'],
                'max_time_ms': stats['max_time'],
                'error_rate': stats['errors'] / stats['count']
            }
        return {}
    
    def get_agent_stats(self, agent_id: str) -> Dict:
        '''Get agent statistics'''
        agent_metrics = [m for m in self.metrics if m.agent_id == agent_id]
        
        if not agent_metrics:
            return {}
        
        times = [m.execution_time_ms for m in agent_metrics]
        
        return {
            'agent_id': agent_id,
            'total_operations': len(agent_metrics),
            'avg_execution_time_ms': statistics.mean(times),
            'median_execution_time_ms': statistics.median(times),
            'error_rate': sum(1 for m in agent_metrics if m.status != "success") / len(agent_metrics)
        }
    
    def get_system_health(self) -> Dict:
        '''Get system health'''
        if not self.metrics:
            return {}
        
        times = [m.execution_time_ms for m in self.metrics]
        success = sum(1 for m in self.metrics if m.status == "success")
        
        return {
            'total_operations': len(self.metrics),
            'success_rate': success / len(self.metrics),
            'avg_operation_time_ms': statistics.mean(times),
            'unique_agents': len(set(m.agent_id for m in self.metrics))
        }
    
    def get_slow_operations(self, threshold_ms: float = 1000) -> List[PerformanceMetrics]:
        '''Get slow operations'''
        return [m for m in self.metrics if m.execution_time_ms > threshold_ms]
    
    def get_failed_operations(self) -> List[PerformanceMetrics]:
        '''Get failed operations'''
        return [m for m in self.metrics if m.status != "success"]
