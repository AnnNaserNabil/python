"""
5. Memoization for Instance Methods

This example demonstrates how to implement memoization for instance methods,
ensuring that the cache is properly scoped to each instance.
"""
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, cast

T = TypeVar('T', bound=Callable[..., Any])

def memoize_method(method: T) -> T:
    """
    Memoization decorator for instance methods.
    The cache is stored on the instance itself.
    """
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        # Create a cache on the instance if it doesn't exist
        if not hasattr(self, '_memoize_cache'):
            self._memoize_cache: Dict[tuple, Any] = {}
        
        # Create a key from method name and arguments
        key = (method.__name__, args, frozenset(kwargs.items()))
        
        # Return cached result if available
        if key in self._memoize_cache:
            print(f"Cache hit for {self.__class__.__name__}.{method.__name__}{args}")
            return self._memoize_cache[key]
        
        # Compute and cache the result
        print(f"Computing {self.__class__.__name__}.{method.__name__}{args}")
        result = method(self, *args, **kwargs)
        self._memoize_cache[key] = result
        return result
    
    return cast(T, wrapper)

# Example usage
class DataProcessor:
    """A class that performs expensive data processing."""
    
    def __init__(self, name: str):
        self.name = name
    
    @memoize_method
    def process(self, data: str) -> str:
        """Process data (simulated expensive operation)."""
        print(f"  {self.name} is processing: {data}")
        # Simulate expensive computation
        result = f"PROCESSED-{data.upper()}"
        return result
    
    @memoize_method
    def calculate(self, x: int, y: int) -> int:
        """Calculate something (simulated expensive calculation)."""
        print(f"  {self.name} is calculating: {x} + {y}")
        # Simulate expensive calculation
        result = x + y
        return result
    
    def clear_cache(self) -> None:
        """Clear the memoization cache for this instance."""
        if hasattr(self, '_memoize_cache'):
            self._memoize_cache.clear()
            print(f"Cache cleared for {self.name}")

def demonstrate() -> None:
    """Demonstrate memoization for instance methods."""
    print("=== Memoization for Instance Methods ===\n")
    
    # Create two instances
    processor1 = DataProcessor("Processor 1")
    processor2 = DataProcessor("Processor 2")
    
    # Test with first processor
    print("\n--- Testing Processor 1 ---")
    print(processor1.process("test"))  # Compute
    print(processor1.process("test"))  # Cache hit
    print(processor1.calculate(3, 4))  # Compute
    print(processor1.calculate(3, 4))  # Cache hit
    
    # Test with second processor (separate cache)
    print("\n--- Testing Processor 2 ---")
    print(processor2.process("test"))  # Compute (separate instance)
    print(processor2.process("test"))  # Cache hit for this instance
    
    # Test with different arguments
    print("\n--- Testing Different Arguments ---")
    print(processor1.process("hello"))  # Compute (new argument)
    print(processor1.process("test"))   # Cache hit (from earlier)
    print(processor1.calculate(5, 6))   # Compute (new arguments)
    print(processor1.calculate(5, 6))   # Cache hit
    
    # Clear cache for processor1
    print("\n--- Clearing Cache for Processor 1 ---")
    processor1.clear_cache()
    
    # These will be recomputed
    print("\n--- After Cache Clear ---")
    print(processor1.process("test"))  # Compute (cache was cleared)
    print(processor2.process("test"))  # Cache hit (other instance's cache is intact)
    
    # Verify caches are independent
    print("\n--- Verifying Cache Independence ---")
    print(f"Processor 1 cache size: {len(processor1._memoize_cache) if hasattr(processor1, '_memoize_cache') else 0}")
    print(f"Processor 2 cache size: {len(processor2._memoize_cache) if hasattr(processor2, '_memoize_cache') else 0}")

if __name__ == "__main__":
    demonstrate()
