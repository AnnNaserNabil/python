"""
8. Memoization and Caching

Memoization is an optimization technique used to speed up function calls by caching 
the results of expensive function calls and returning the cached result when the 
same inputs occur again.
"""

from functools import lru_cache, wraps
from typing import Callable, TypeVar, Any, Dict, Tuple
import time

T = TypeVar('T')
R = TypeVar('R')

def time_it(func: Callable[..., R]) -> Callable[..., R]:
    """Decorator to measure the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds")
        return result
    return wrapper

# Example 1: Basic memoization using a dictionary
def memoize(func: Callable[..., R]) -> Callable[..., R]:
    """A simple memoization decorator."""
    cache: Dict[Tuple[Any, ...], R] = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a key from the function arguments
        key = (args, frozenset(kwargs.items()))
        
        # If result is not in cache, compute and store it
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    return wrapper

# Example 2: Fibonacci with and without memoization
@time_it
def fib(n: int) -> int:
    """Naive recursive Fibonacci implementation (exponential time)."""
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


@time_it
@memoize
def fib_memoized(n: int) -> int:
    """Memoized recursive Fibonacci implementation (linear time)."""
    if n < 2:
        return n
    return fib_memoized(n-1) + fib_memoized(n-2)

# Example 3: Using Python's built-in lru_cache
@time_it
@lru_cache(maxsize=128)
def fib_lru(n: int) -> int:
    """Fibonacci using Python's built-in LRU cache."""
    if n < 2:
        return n
    return fib_lru(n-1) + fib_lru(n-2)

# Example 4: Memoization for expensive computations
@memoize
def expensive_computation(n: int) -> int:
    """Simulate an expensive computation."""
    print(f"Computing for {n}...")
    time.sleep(1)  # Simulate work
    return n * n

# Example 5: Memoization with multiple arguments
@memoize
def combinations(n: int, k: int) -> int:
    """Calculate combinations (n choose k) with memoization."""
    if k == 0 or k == n:
        return 1
    return combinations(n-1, k-1) + combinations(n-1, k)

# Example 6: Memoization with keyword arguments
@memoize
def greet(name: str, greeting: str = "Hello") -> str:
    """A simple greeting function with memoization."""
    print(f"Generating greeting for {name}...")
    return f"{greeting}, {name}!"

# Example 7: Memoization for API calls (simulated)
import random

@memoize
def get_weather(city: str) -> dict:
    """Simulate an API call to get weather data."""
    print(f"Fetching weather for {city}...")
    time.sleep(1)  # Simulate network delay
    return {
        "city": city,
        "temperature": random.uniform(-10, 35),  # Random temperature
        "humidity": random.uniform(0, 100),      # Random humidity
        "timestamp": time.time()
    }

# Testing the functions
if __name__ == "__main__":
    # Test basic memoization
    print("=== Basic Memoization ===")
    print("First call (should compute):", expensive_computation(5))
    print("Second call (should use cache):", expensive_computation(5))
    
    # Test Fibonacci with and without memoization
    print("\n=== Fibonacci Performance ===")
    n = 30  # Small enough to run in reasonable time without memoization
    
    print(f"\nComputing fib({n}) without memoization:")
    result = fib(n)
    print(f"fib({n}) = {result}")
    
    print(f"\nComputing fib({n}) with custom memoization:")
    result = fib_memoized(n)
    print(f"fib_memoized({n}) = {result}")
    
    print(f"\nComputing fib({n}) with lru_cache:")
    result = fib_lru(n)
    print(f"fib_lru({n}) = {result}")
    
    # Test combinations with memoization
    print("\n=== Combinations ===")
    print("Computing combinations(20, 10) with memoization:")
    start_time = time.perf_counter()
    result = combinations(20, 10)
    end_time = time.perf_counter()
    print(f"combinations(20, 10) = {result}")
    print(f"Took {end_time - start_time:.6f} seconds")
    
    # Test with keyword arguments
    print("\n=== Memoization with Keyword Arguments ===")
    print(greet("Alice"))          # First call - computes
    print(greet("Alice"))          # Second call - uses cache
    print(greet("Bob", "Hi"))      # Different arguments - computes
    print(greet("Alice", "Hi"))    # Different greeting - computes
    print(greet("Alice"))          # Original greeting - uses cache
    
    # Test simulated API calls
    print("\n=== Simulated API Calls ===")
    cities = ["London", "Paris", "Tokyo", "New York", "London"]
    
    for city in cities:
        weather = get_weather(city)
        print(f"{city}: {weather['temperature']:.1f}°C")
    
    # Clear the cache for get_weather
    get_weather.cache_clear()
    
    print("\nAfter clearing cache:")
    for city in cities:
        weather = get_weather(city)
        print(f"{city}: {weather['temperature']:.1f}°C")
