"""
Performance measurement utilities
"""

import time
import tracemalloc
from typing import Callable, Any, Tuple, Dict
from functools import wraps


def measure_time(func: Callable) -> Callable:
    """Decorator to measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper


def measure_memory(func: Callable) -> Callable:
    """Decorator to measure memory usage"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return result, peak / 1024 / 1024  # Convert to MB
    return wrapper


def benchmark_algorithm(
    algorithm: Callable,
    *args,
    iterations: int = 1,
    **kwargs
) -> Dict[str, Any]:
    """
    Comprehensive benchmark of an algorithm
    
    Args:
        algorithm: Function to benchmark
        args: Positional arguments for the algorithm
        iterations: Number of times to run the algorithm
        kwargs: Keyword arguments for the algorithm
        
    Returns:
        Dictionary with performance metrics
    """
    times = []
    memories = []
    
    for _ in range(iterations):
        # Measure time
        start_time = time.perf_counter()
        tracemalloc.start()
        
        result = algorithm(*args, **kwargs)
        
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        times.append(end_time - start_time)
        memories.append(peak / 1024 / 1024)  # MB
    
    return {
        'result': result,
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'avg_memory': sum(memories) / len(memories),
        'peak_memory': max(memories),
        'iterations': iterations
    }


class PerformanceTracker:
    """Track performance metrics across multiple algorithm runs"""
    
    def __init__(self):
        self.metrics = {}
    
    def track(self, name: str, time: float, memory: float, **extra):
        """Record performance metrics"""
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append({
            'time': time,
            'memory': memory,
            **extra
        })
    
    def get_summary(self, name: str) -> Dict[str, float]:
        """Get summary statistics for an algorithm"""
        if name not in self.metrics:
            return {}
        
        times = [m['time'] for m in self.metrics[name]]
        memories = [m['memory'] for m in self.metrics[name]]
        
        return {
            'avg_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'avg_memory': sum(memories) / len(memories),
            'runs': len(times)
        }
    
    def compare(self) -> Dict[str, Dict[str, float]]:
        """Compare all tracked algorithms"""
        return {name: self.get_summary(name) for name in self.metrics}
