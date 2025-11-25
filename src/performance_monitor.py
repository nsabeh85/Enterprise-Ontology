import time
import statistics
from typing import Dict, List, Callable


class PerformanceMonitor:
    """Monitor and track performance metrics for query rewriting pipeline"""
    
    def __init__(self):
        self.measurements = {
            'lexicon_load': [],
            'query_rewrite': [],
            'total': []
        }
    
    def measure(self, operation: str, func: Callable, *args, **kwargs):
        """
        Measure execution time of a function
        
        Args:
            operation: Name of operation being measured
            func: Function to execute and measure
            *args, **kwargs: Arguments to pass to function
            
        Returns:
            Result of function execution
        """
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        
        latency_ms = (end - start) * 1000
        
        if operation in self.measurements:
            self.measurements[operation].append(latency_ms)
        
        return result, latency_ms
    
    def get_statistics(self, operation: str = None) -> Dict:
        """
        Calculate performance statistics
        
        Args:
            operation: Specific operation to get stats for, or None for all
            
        Returns:
            Dictionary with performance metrics
        """
        if operation:
            data = self.measurements.get(operation, [])
            if not data:
                return {}
            
            return {
                'operation': operation,
                'count': len(data),
                'mean': statistics.mean(data),
                'median': statistics.median(data),
                'p95': self._percentile(data, 95),
                'p99': self._percentile(data, 99),
                'min': min(data),
                'max': max(data)
            }
        else:
            # Return stats for all operations
            stats = {}
            for op in self.measurements:
                stats[op] = self.get_statistics(op)
            return stats
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * (percentile / 100))
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def print_report(self):
        """Print formatted performance report"""
        print("\n" + "="*60)
        print("PERFORMANCE REPORT")
        print("="*60)
        
        stats = self.get_statistics()
        
        for operation, metrics in stats.items():
            if not metrics:
                continue
                
            print(f"\n{operation.upper().replace('_', ' ')}:")
            print(f"  Samples:  {metrics['count']}")
            print(f"  Mean:     {metrics['mean']:.2f}ms")
            print(f"  Median:   {metrics['median']:.2f}ms")
            print(f"  p95:      {metrics['p95']:.2f}ms")
            print(f"  p99:      {metrics['p99']:.2f}ms")
            print(f"  Min:      {metrics['min']:.2f}ms")
            print(f"  Max:      {metrics['max']:.2f}ms")
        
        print("\n" + "="*60)


# Test function
if __name__ == "__main__":
    import random
    
    # Simulate some operations
    monitor = PerformanceMonitor()
    
    def mock_operation(delay):
        time.sleep(delay / 1000)  # Convert ms to seconds
        return "result"
    
    print("Running performance test...")
    
    # Simulate 100 operations
    for _ in range(100):
        delay = random.uniform(5, 15)  # Random delay between 5-15ms
        monitor.measure('query_rewrite', mock_operation, delay)
    
    # Print report
    monitor.print_report()