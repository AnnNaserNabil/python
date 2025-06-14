"""
1. Basic Memoization with Function Decorator

This example demonstrates a simple memoization decorator that caches function results.
"""
from functools import wraps
from typing import Any, Callable, Dict, TypeVar, cast

T = TypeVar('T', bound=Callable[..., Any])

def memoize(func: T) -> T:
    """A simple memoization decorator that caches function results."""
    cache: Dict[tuple, Any] = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Create a key from function arguments
        key = (args, frozenset(kwargs.items()))
        
        # Return cached result if available
        if key in cache:
            print(f"Cache hit for {func.__name__}{args}")
            return cache[key]
            
        # Compute and cache result
        print(f"Computing {func.__name__}{args}")
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    return cast(T, wrapper)

# Example usage
@memoize
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def demonstrate() -> None:
    """Demonstrate basic memoization with Fibonacci sequence."""
    print("=== Basic Memoization ===\n")
    
    # First call computes values
    print("First call to fibonacci(5):")
    result1 = fibonacci(5)
    print(f"Result: {result1}\n")
    
    # Second call uses cached values
    print("Second call to fibonacci(5):")
    result2 = fibonacci(5)
    print(f"Result: {result2}\n")
    
    # Compute a larger value (reuses cached results)
    print("Calling fibonacci(10):")
    result3 = fibonacci(10)
    print(f"Result: {result3}")

if __name__ == "__main__":
    demonstrate()
