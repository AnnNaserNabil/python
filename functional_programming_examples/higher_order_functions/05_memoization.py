"""
5. Memoization and Caching

Techniques for optimizing function calls with memoization.
- Basic memoization
- Memoization with function decorators
- Memoization with LRU cache
- Custom cache implementations
- Memoization for recursive functions
"""
from typing import TypeVar, Callable, Any, Dict, Tuple, Optional, Hashable
from functools import lru_cache, wraps
import time
import math
import hashlib
import pickle

T = TypeVar('T')
U = TypeVar('U')

# 1. Basic memoization with a dictionary
def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """Basic memoization decorator using a dictionary."""
    cache: Dict[Tuple[Any, ...], T] = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # Create a key from args and kwargs
        key = (args, frozenset(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper

# 2. Memoization with LRU (Least Recently Used) cache
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number (naive recursive implementation)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@memoize
def fibonacci_memoized(n: int) -> int:
    """Calculate the nth Fibonacci number with memoization."""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)

# 3. Using functools.lru_cache
@lru_cache(maxsize=128)
def factorial(n: int) -> int:
    """Calculate factorial with LRU cache."""
    print(f"Calculating factorial({n})")
    if n == 0:
        return 1
    return n * factorial(n - 1)

# 4. Memoization with custom cache key function
def memoize_with_key(key_func: Callable[..., Hashable]) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Memoization decorator with custom key function.
    
    Args:
        key_func: Function that takes the same arguments as the decorated function
                 and returns a hashable key.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[Hashable, T] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = key_func(*args, **kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        
        return wrapper
    return decorator

def hash_args(*args: Any, **kwargs: Any) -> str:
    """Create a hash from function arguments."""
    # Convert args and kwargs to bytes and hash them
    args_bytes = pickle.dumps((args, sorted(kwargs.items())))
    return hashlib.sha256(args_bytes).hexdigest()

# 5. Memoization with time-based expiration
def memoize_with_expiry(expiry_seconds: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Memoization decorator with time-based expiration.
    
    Args:
        expiry_seconds: Number of seconds before a cache entry expires.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[Tuple[Any, ...], Tuple[float, T]] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (args, frozenset(kwargs.items()))
            current_time = time.time()
            
            if key in cache:
                timestamp, result = cache[key]
                if current_time - timestamp < expiry_seconds:
                    return result
            
            # Either not in cache or expired
            result = func(*args, **kwargs)
            cache[key] = (current_time, result)
            return result
        
        return wrapper
    return decorator

# 6. Memoization for instance methods
def memoize_method(func: Callable[..., T]) -> Callable[..., T]:
    """Memoization decorator for instance methods."""
    cache_attr = f"_memoize_cache_{func.__name__}"
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, {})
        
        cache = getattr(self, cache_attr)
        key = (args, frozenset(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
        return cache[key]
    
    return wrapper

# 7. Memoization with cache statistics
def memoize_with_stats(func: Callable[..., T]) -> Callable[..., T]:
    """Memoization decorator that tracks cache statistics."""
    cache: Dict[Tuple[Any, ...], T] = {}
    hits = 0
    misses = 0
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        nonlocal hits, misses
        key = (args, frozenset(kwargs.items()))
        
        if key in cache:
            hits += 1
            return cache[key]
        
        misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    def stats() -> Dict[str, int]:
        return {
            'hits': hits,
            'misses': misses,
            'size': len(cache),
            'hit_ratio': hits / (hits + misses) if (hits + misses) > 0 else 0.0
        }
    
    wrapper.cache_info = stats  # type: ignore
    wrapper.cache_clear = cache.clear  # type: ignore
    
    return wrapper

# Example classes and functions for demonstration
class ExpensiveCalculator:
    """A class with expensive calculations that can benefit from memoization."""
    
    @memoize_method
    def calculate(self, x: float, y: float) -> float:
        print(f"Calculating for {x}, {y}")
        time.sleep(0.5)  # Simulate expensive calculation
        return x ** 2 + y ** 2
    
    @memoize_with_expiry(expiry_seconds=2)
    def time_sensitive_calculation(self, x: float) -> float:
        print(f"Performing time-sensitive calculation for {x}")
        return math.sin(x) * math.cos(x)

@memoize_with_key(key_func=hash_args)
def expensive_operation(x: int, y: int, name: str = "default") -> Dict[str, Any]:
    """An expensive operation that benefits from memoization."""
    print(f"Running expensive operation with x={x}, y={y}, name={name}")
    time.sleep(1)  # Simulate expensive operation
    return {
        'result': x * y,
        'sum': x + y,
        'name': name,
        'timestamp': time.time()
    }

def demonstrate_memoization() -> None:
    """Show examples of different memoization techniques."""
    print("=== Basic Memoization ===")
    
    # Without memoization
    start = time.time()
    result = fibonacci(35)
    elapsed = time.time() - start
    print(f"Fibonacci(35) without memoization: {result} (took {elapsed:.2f}s)")
    
    # With memoization
    start = time.time()
    result = fibonacci_memoized(35)
    elapsed = time.time() - start
    print(f"Fibonacci(35) with memoization: {result} (took {elapsed:.2f}s)")
    
    print("\n=== LRU Cache ===")
    # First call - calculations will be performed
    print("First call to factorial(5):")
    print(f"Result: {factorial(5)}")
    
    # Second call - results come from cache
    print("\nSecond call to factorial(5):")
    print(f"Result: {factorial(5)}")
    
    print("\n=== Custom Cache Key ===")
    # First call - performs the calculation
    result1 = expensive_operation(10, 20, name="test")
    print(f"Result 1: {result1['result']}")
    
    # Second call with same arguments - uses cache
    result2 = expensive_operation(10, 20, name="test")
    print(f"Result 2 (cached): {result2['result']}")
    
    print("\n=== Time-based Expiration ===")
    calculator = ExpensiveCalculator()
    
    # First call - performs the calculation
    print("First call:")
    result1 = calculator.time_sensitive_calculation(1.0)
    print(f"Result: {result1:.4f}")
    
    # Second call within expiry - uses cache
    print("\nSecond call (immediate, uses cache):")
    result2 = calculator.time_sensitive_calculation(1.0)
    print(f"Result: {result2:.4f}")
    
    # Wait for expiry and call again
    print("\nWaiting for cache to expire...")
    time.sleep(3)
    print("Third call (after expiry, recalculates):")
    result3 = calculator.time_sensitive_calculation(1.0)
    print(f"Result: {result3:.4f}")
    
    print("\n=== Method Memoization ===")
    calc = ExpensiveCalculator()
    
    # First call - performs the calculation
    print("First calculation:")
    result1 = calc.calculate(3, 4)
    print(f"Result: {result1}")
    
    # Second call with same arguments - uses cache
    print("\nSecond calculation (same args, uses cache):")
    result2 = calc.calculate(3, 4)
    print(f"Result: {result2}")
    
    # Different arguments - performs calculation
    print("\nThird calculation (different args, calculates):")
    result3 = calc.calculate(5, 6)
    print(f"Result: {result3}")
    
    print("\n=== Cache Statistics ===")
    @memoize_with_stats
    def square(x: int) -> int:
        return x * x
    
    # Make some calls
    for i in [1, 2, 3, 4, 5, 1, 2, 3]:
        _ = square(i)
    
    # Print cache statistics
    stats = square.cache_info()  # type: ignore
    print(f"Cache stats: {stats}")
    
    # Clear the cache
    square.cache_clear()  # type: ignore
    stats = square.cache_info()  # type: ignore
    print(f"After clear - Cache stats: {stats}")

def main() -> None:
    """Demonstrate memoization techniques."""
    demonstrate_memoization()
    
    print("\n=== Key Takeaways ===")
    print("1. Memoization caches function results to avoid redundant calculations")
    print("2. Use @functools.lru_cache for a simple, thread-safe LRU cache")
    print("3. Custom memoization allows for more control over caching behavior")
    print("4. Consider cache invalidation strategies (size limits, time-based expiry)")
    print("5. Be cautious with mutable arguments and ensure proper key generation")
    print("6. Monitor cache hit/miss ratios to tune cache size and eviction policies")

if __name__ == "__main__":
    main()
