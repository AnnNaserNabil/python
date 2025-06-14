"""
8. Memoization with Dependency Injection

This example demonstrates how to implement memoization in a way that's testable
and follows dependency injection principles, making it easier to mock and test.
"""
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, Generic, Type, cast
import time
import random

# Type variables for better type hints
T = TypeVar('T')  # Input type
R = TypeVar('R')  # Return type

class Cache(Generic[T, R]):
    """Abstract base class for cache implementations."""
    def get(self, key: T) -> Optional[R]:
        """Get a value from the cache."""
        raise NotImplementedError
    
    def set(self, key: T, value: R) -> None:
        """Store a value in the cache."""
        raise NotImplementedError
    
    def clear(self) -> None:
        """Clear the cache."""
        raise NotImplementedError

class InMemoryCache(Cache[T, R]):
    """In-memory cache implementation."""
    def __init__(self) -> None:
        self._store: Dict[T, R] = {}
    
    def get(self, key: T) -> Optional[R]:
        return self._store.get(key)
    
    def set(self, key: T, value: R) -> None:
        self._store[key] = value
    
    def clear(self) -> None:
        self._store.clear()

class TimedCache(Cache[T, R]):
    """In-memory cache with TTL (Time To Live) support."""
    def __init__(self, ttl_seconds: float = 60.0) -> None:
        self._store: Dict[T, Tuple[float, R]] = {}
        self._ttl = ttl_seconds
    
    def get(self, key: T) -> Optional[R]:
        if key not in self._store:
            return None
        
        timestamp, value = self._store[key]
        if time.time() - timestamp > self._ttl:
            del self._store[key]
            return None
            
        return value
    
    def set(self, key: T, value: R) -> None:
        self._store[key] = (time.time(), value)
    
    def clear(self) -> None:
        self._store.clear()

def memoize_with_di(cache: Optional[Cache[T, R]] = None) -> Callable[[Callable[[T], R]], Callable[[T], R]]:
    """
    Memoization decorator that accepts a cache implementation via dependency injection.
    
    Args:
        cache: Cache implementation to use. If None, uses a default in-memory cache.
    """
    def decorator(func: Callable[[T], R]) -> Callable[[T], R]:
        # Use the provided cache or create a default one
        _cache = cache if cache is not None else InMemoryCache[T, R]()
        
        @wraps(func)
        def wrapper(arg: T) -> R:
            # Check cache first
            cached_result = _cache.get(arg)
            if cached_result is not None:
                print(f"Cache hit for {func.__name__}({arg})")
                return cached_result
            
            # Compute and cache the result
            print(f"Cache miss for {func.__name__}({arg}), computing...")
            result = func(arg)
            _cache.set(arg, result)
            return result
        
        # Attach cache to the wrapper for testing and management
        wrapper.cache = _cache  # type: ignore
        
        return wrapper
    
    return decorator

# Example usage
class DataService:
    """A service that performs expensive data operations."""
    
    def __init__(self, cache: Optional[Cache[str, str]] = None):
        # Use provided cache or create a default one
        self._cache = cache if cache is not None else InMemoryCache[str, str]()
    
    @memoize_with_di()  # Uses default cache
    def get_user_profile(self, user_id: str) -> str:
        """Get user profile (simulated expensive operation)."""
        print(f"  Fetching profile for user {user_id}...")
        time.sleep(0.5)  # Simulate work
        return f"Profile data for user {user_id}"
    
    # Using the class-level cache
    def get_user_settings(self, user_id: str) -> str:
        """Get user settings with explicit cache usage."""
        # Check cache first
        cached = self._cache.get(user_id)
        if cached is not None:
            print(f"Cache hit for settings of user {user_id}")
            return cached
        
        # Compute and cache the result
        print(f"Cache miss for settings of user {user_id}, computing...")
        time.sleep(0.3)  # Simulate work
        result = f"Settings for user {user_id}"
        self._cache.set(user_id, result)
        return result

# Test double for testing
class MockCache(Cache[str, str]):
    """A mock cache for testing purposes."""
    def __init__(self):
        self.get_calls = 0
        self.set_calls = 0
        self.clear_calls = 0
        self._store: Dict[str, str] = {}
    
    def get(self, key: str) -> Optional[str]:
        self.get_calls += 1
        return self._store.get(key)
    
    def set(self, key: str, value: str) -> None:
        self.set_calls += 1
        self._store[key] = value
    
    def clear(self) -> None:
        self.clear_calls += 1
        self._store.clear()

def test_data_service() -> None:
    """Test the DataService with a mock cache."""
    print("\n=== Testing DataService with Mock Cache ===")
    
    # Create a mock cache
    mock_cache = MockCache()
    
    # Create service with the mock cache
    service = DataService(cache=mock_cache)
    
    # First call - should miss cache
    print("\nFirst call (should miss):")
    result1 = service.get_user_settings("user123")
    print(f"Result: {result1}")
    
    # Second call - should hit cache
    print("\nSecond call (should hit):")
    result2 = service.get_user_settings("user123")
    print(f"Result: {result2}")
    
    # Verify cache was used
    print("\nCache statistics:")
    print(f"  get() calls: {mock_cache.get_calls}")
    print(f"  set() calls: {mock_cache.set_calls}")
    print(f"  clear() calls: {mock_cache.clear_calls}")

def demonstrate() -> None:
    """Demonstrate memoization with dependency injection."""
    print("=== Memoization with Dependency Injection ===\n")
    
    # 1. Using the default cache
    print("1. Using default in-memory cache:")
    service1 = DataService()
    
    print("\nFirst call (will compute):")
    print(service1.get_user_profile("alice"))
    
    print("\nSecond call (will use cache):")
    print(service1.get_user_profile("alice"))
    
    # 2. Using a timed cache
    print("\n2. Using timed cache (TTL=2 seconds):")
    timed_cache = TimedCache[str, str](ttl_seconds=2.0)
    
    @memoize_with_di(cache=timed_cache)
    def get_weather(city: str) -> str:
        """Get weather data (simulated)."""
        print(f"  Fetching weather for {city}...")
        time.sleep(0.3)
        return f"Weather in {city}: {random.randint(50, 90)}°F"
    
    print("\nFirst call (will compute):")
    print(get_weather("New York"))
    
    print("\nImmediate second call (will use cache):")
    print(get_weather("New York"))
    
    print("\nWaiting for cache to expire...")
    time.sleep(2.5)
    
    print("\nAfter TTL (will compute again):")
    print(get_weather("New York"))
    
    # 3. Run tests
    test_data_service()

if __name__ == "__main__":
    demonstrate()
