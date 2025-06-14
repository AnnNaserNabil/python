"""
3. Memoization with Time-to-Live (TTL)

This example demonstrates a memoization decorator with TTL (Time To Live) support,
which automatically expires cached results after a specified time.
"""
from functools import wraps
import time
from typing import Any, Callable, Dict, Tuple, TypeVar, cast

T = TypeVar('T', bound=Callable[..., Any])

def memoize_ttl(ttl_seconds: int = 60) -> Callable[[T], T]:
    """
    Memoization decorator with TTL (Time To Live).
    
    Args:
        ttl_seconds: Time in seconds to keep results in cache
    """
    def decorator(func: T) -> T:
        cache: Dict[Tuple[Any, ...], Tuple[float, Any]] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create a key from function arguments
            key = (args, frozenset(kwargs.items()))
            
            # Check if we have a cached result that hasn't expired
            current_time = time.time()
            if key in cache:
                timestamp, result = cache[key]
                if current_time - timestamp < ttl_seconds:
                    print(f"Cache hit for {func.__name__}{args} (expires in {ttl_seconds - (current_time - timestamp):.1f}s)")
                    return result
                else:
                    print(f"Cache expired for {func.__name__}{args}")
            else:
                print(f"Cache miss for {func.__name__}{args}")
            
            # Compute and cache the result with current timestamp
            result = func(*args, **kwargs)
            cache[key] = (current_time, result)
            return result
        
        return cast(T, wrapper)
    return decorator

# Example usage
@memoize_ttl(ttl_seconds=3)  # Cache results for 3 seconds
def get_weather(city: str) -> str:
    """Simulate an API call to get weather data."""
    print(f"  Calling weather API for {city}...")
    time.sleep(0.5)  # Simulate network delay
    return f"Weather in {city}: {70 + hash(city) % 20}°F"

def demonstrate() -> None:
    """Demonstrate TTL-based memoization."""
    print("=== Memoization with TTL ===\n")
    
    # First call - caches the result
    print("First call (will cache):")
    print(get_weather("New York"))
    
    # Immediate second call - uses cached result
    print("\nSecond call (immediate, should use cache):")
    print(get_weather("New York"))
    
    # Wait for cache to expire
    print("\nWaiting 4 seconds for cache to expire...")
    time.sleep(4)
    
    # Third call after TTL - recalculates
    print("\nThird call (after TTL, should recalculate):")
    print(get_weather("New York"))
    
    # Different argument - calculates new result
    print("\nDifferent argument (should calculate):")
    print(get_weather("London"))
    
    # Original argument still in cache
    print("\nOriginal argument again (should use cache):")
    print(get_weather("New York"))

if __name__ == "__main__":
    demonstrate()
