"""
2. Using functools.lru_cache

This example demonstrates Python's built-in LRU (Least Recently Used) cache decorator.
"""
from functools import lru_cache
from typing import Any, Callable, TypeVar
import time

T = TypeVar('T', bound=Callable[..., Any])

def demonstrate() -> None:
    """Demonstrate lru_cache with different configurations."""
    print("=== Using lru_cache ===\n")
    
    # 1. Basic usage with default maxsize=128
    @lru_cache
    def fib(n: int) -> int:
        """Calculate nth Fibonacci number (recursive)."""
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)
    
    # First call computes values
    print("First call to fib(30):")
    start = time.perf_counter()
    result = fib(30)
    elapsed = time.perf_counter() - start
    print(f"Result: {result} (took {elapsed:.6f} seconds)\n")
    
    # Second call uses cached values
    print("Second call to fib(30):")
    start = time.perf_counter()
    result = fib(30)
    elapsed = time.perf_counter() - start
    print(f"Result: {result} (took {elapsed:.6f} seconds)\n")
    
    # 2. Using maxsize to limit cache size
    @lru_cache(maxsize=5)
    def expensive_operation(x: int) -> int:
        """Simulate an expensive operation."""
        print(f"  Computing expensive_operation({x})")
        time.sleep(0.5)
        return x * x
    
    print("Testing LRU eviction (maxsize=5):")
    # Fill the cache
    for i in range(5):
        expensive_operation(i)
    
    # Access in order (should all be cached)
    print("\nAccessing cached items:")
    for i in range(5):
        expensive_operation(i)
    
    # Add one more item, which will evict the least recently used (0)
    print("\nAdding one more item (will evict 0):")
    expensive_operation(5)
    
    # Access 0 again (will be recomputed)
    print("\nAccessing evicted item (0):")
    expensive_operation(0)
    
    # 3. Cache info
    print("\nCache info:")
    print(f"fib cache info: {fib.cache_info()}")
    print(f"expensive_operation cache info: {expensive_operation.cache_info()}")
    
    # 4. Clearing the cache
    print("\nClearing caches...")
    fib.cache_clear()
    expensive_operation.cache_clear()
    
    print(f"After clear - fib cache info: {fib.cache_info()}")
    print(f"After clear - expensive_operation cache info: {expensive_operation.cache_info()}")

if __name__ == "__main__":
    demonstrate()
