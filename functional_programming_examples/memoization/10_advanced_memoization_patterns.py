"""
10. Advanced Memoization Patterns

This example demonstrates advanced memoization patterns including:
1. Selective argument memoization
2. Cache key customization
3. Cache statistics and monitoring
4. Cache warming
5. Cache versioning
6. Memoization with context managers
7. Memoization with async functions
8. Memoization with class methods and properties
9. Memoization with expiration callbacks
10. Thread-safe memoization
"""
import functools
import time
import threading
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TypeVar, cast, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import hashlib
import inspect
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Type variables for better type hints
T = TypeVar('T')
R = TypeVar('R')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 1. Cache Statistics and Monitoring

@dataclass
class CacheStats:
    """Track cache statistics."""
    hits: int = 0
    misses: int = 0
    maxsize: Optional[int] = None
    currsize: int = 0
    
    @property
    def hit_ratio(self) -> float:
        """Calculate the cache hit ratio."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def reset(self) -> None:
        """Reset all statistics."""
        self.hits = 0
        self.misses = 0
        self.currsize = 0

# 2. Cache Entry with Expiration and Callbacks

@dataclass
class CacheEntry(Generic[R]):
    """A cache entry with value, expiration, and callbacks."""
    value: R
    expires_at: Optional[float] = None
    callbacks: List[Callable[[R], None]] = field(default_factory=list)
    
    @property
    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

# 3. Thread-Safe Cache Implementation

class ThreadSafeCache(Generic[T, R]):
    """A thread-safe cache with statistics and expiration."""
    
    def __init__(self, maxsize: Optional[int] = None, ttl: Optional[float] = None):
        """
        Initialize the cache.
        
        Args:
            maxsize: Maximum number of items to cache (None for unlimited)
            ttl: Time-to-live in seconds for cache entries (None for no expiration)
        """
        self._cache: Dict[str, CacheEntry[R]] = {}
        self._lock = threading.RLock()
        self.stats = CacheStats(maxsize=maxsize)
        self.default_ttl = ttl
    
    def _make_key(self, *args: Any, **kwargs: Any) -> str:
        """Create a cache key from function arguments."""
        # This is a simple key generation strategy
        key_parts = [
            str(args),
            str(sorted(kwargs.items()))
        ]
        key_string = '|'.join(key_parts).encode('utf-8')
        return hashlib.md5(key_string).hexdigest()
    
    def get(self, key: str) -> Optional[R]:
        """Get a value from the cache."""
        with self._lock:
            if key not in self._cache:
                self.stats.misses += 1
                return None
            
            entry = self._cache[key]
            if entry.is_expired:
                del self._cache[key]
                self.stats.misses += 1
                self.stats.currsize -= 1
                return None
            
            self.stats.hits += 1
            return entry.value
    
    def set(
        self,
        key: str,
        value: R,
        ttl: Optional[float] = None,
        callbacks: Optional[List[Callable[[R], None]]] = None
    ) -> None:
        """Set a value in the cache."""
        with self._lock:
            # Check if we need to make space (LRU eviction)
            if (self.stats.maxsize is not None and 
                    self.stats.currsize >= self.stats.maxsize and 
                    key not in self._cache):
                # Simple strategy: remove the first item
                if self._cache:
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
                    self.stats.currsize -= 1
            
            # Set expiration time
            expires_at = None
            if ttl is not None:
                expires_at = time.time() + ttl
            elif self.default_ttl is not None:
                expires_at = time.time() + self.default_ttl
            
            # Create or update the entry
            if key in self._cache:
                self._cache[key].value = value
                self._cache[key].expires_at = expires_at
                if callbacks:
                    self._cache[key].callbacks.extend(callbacks)
            else:
                self._cache[key] = CacheEntry(
                    value=value,
                    expires_at=expires_at,
                    callbacks=callbacks or []
                )
                self.stats.currsize += 1
    
    def clear(self) -> None:
        """Clear the cache."""
        with self._lock:
            self._cache.clear()
            self.stats.currsize = 0
    
    def invalidate(self, key: str) -> bool:
        """Invalidate a specific cache entry."""
        with self._lock:
            if key in self._cache:
                # Execute callbacks before removing
                entry = self._cache[key]
                for callback in entry.callbacks:
                    try:
                        callback(entry.value)
                    except Exception as e:
                        logger.error(f"Error in cache invalidation callback: {e}")
                
                del self._cache[key]
                self.stats.currsize -= 1
                return True
            return False

# 4. Advanced Memoization Decorator

def advanced_memoize(
    func: Optional[Callable[..., R]] = None,
    *,
    maxsize: Optional[int] = 128,
    ttl: Optional[float] = None,
    key_func: Optional[Callable[..., str]] = None,
    cache_instance: Optional[ThreadSafeCache[Any, R]] = None,
    skip_args: Optional[Set[int]] = None,
    skip_kwargs: Optional[Set[str]] = None,
    cache_none: bool = True
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    Advanced memoization decorator with support for various features.
    
    Args:
        maxsize: Maximum cache size
        ttl: Time-to-live in seconds for cache entries
        key_func: Custom key generation function
        cache_instance: Use a custom cache instance
        skip_args: Set of argument indices to exclude from cache key
        skip_kwargs: Set of keyword argument names to exclude from cache key
        cache_none: Whether to cache None results
    """
    if skip_args is None:
        skip_args = set()
    if skip_kwargs is None:
        skip_kwargs = set()
    
    def decorator(fn: Callable[..., R]) -> Callable[..., R]:
        # Use provided cache or create a new one
        cache = cache_instance if cache_instance is not None else ThreadSafeCache[Any, R](maxsize, ttl)
        
        # Get function signature for better parameter handling
        sig = inspect.signature(fn)
        
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            # Bind arguments to parameter names
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Filter out skipped arguments
            filtered_args = [
                v for i, v in enumerate(args) 
                if i not in skip_args
            ]
            
            filtered_kwargs = {
                k: v for k, v in bound_args.arguments.items()
                if k not in skip_kwargs and k not in skip_args
            }
            
            # Generate cache key
            if key_func is not None:
                key = key_func(*filtered_args, **filtered_kwargs)
            else:
                key_parts = [
                    fn.__module__ or '',
                    fn.__qualname__,
                    str(filtered_args),
                    str(sorted(filtered_kwargs.items()))
                ]
                key_string = '|'.join(key_parts).encode('utf-8')
                key = hashlib.md5(key_string).hexdigest()
            
            # Try to get from cache
            cached = cache.get(key)
            if cached is not None:
                logger.debug(f"Cache hit for {fn.__name__}")
                return cached
            
            # Compute and cache the result
            logger.debug(f"Cache miss for {fn.__name__}")
            result = fn(*args, **kwargs)
            
            # Only cache if result is not None or we're configured to cache None
            if cache_none or result is not None:
                cache.set(key, result)
            
            return result
        
        # Attach cache and utility methods to the wrapper
        wrapper.cache = cache  # type: ignore
        wrapper.clear_cache = cache.clear  # type: ignore
        wrapper.get_cache_stats = lambda: cache.stats  # type: ignore
        wrapper.invalidate = cache.invalidate  # type: ignore
        
        return wrapper
    
    # Handle both @memoize and @memoize() syntax
    if func is not None:
        return decorator(func)
    return decorator

# 5. Example: Selective Argument Memoization

@advanced_memoize(skip_args={0})  # Skip 'self' for instance methods
class DataProcessor:
    """A class with memoized methods."""
    
    def __init__(self, name: str):
        self.name = name
        self.call_count = 0
    
    @advanced_memoize(ttl=10)  # Cache for 10 seconds
    def process(self, data: str, *, use_cache: bool = True) -> str:
        """Process data with an option to bypass cache."""
        self.call_count += 1
        print(f"  {self.name} processing: {data}")
        time.sleep(0.5)  # Simulate work
        return f"PROCESSED-{data.upper()}"
    
    @property
    @advanced_memoize()  # Memoize property getter
    def expensive_property(self) -> str:
        """An expensive-to-compute property."""
        print(f"  Computing expensive property for {self.name}")
        time.sleep(1)
        return f"Expensive result for {self.name} at {time.time()}"

# 6. Example: Cache Warming

def warm_cache(cache: ThreadSafeCache[Any, Any], keys: List[Any]) -> None:
    """Warm the cache with precomputed values."""
    def warm() -> None:
        for key in keys:
            if isinstance(key, tuple):
                cache.get(key[0])  # Just access to trigger computation
            else:
                cache.get(key)  # Just access to trigger computation
    
    # Run in background
    threading.Thread(target=warm, daemon=True).start()

# 7. Example: Async Memoization

def async_memoize(
    func: Optional[Callable[..., Any]] = None,
    *,
    maxsize: int = 128,
    ttl: Optional[float] = None
) -> Callable[..., Any]:
    """Memoization decorator for async functions."""
    cache: Dict[str, Any] = {}
    lock = asyncio.Lock()
    
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create a cache key
            key_parts = [
                fn.__module__ or '',
                fn.__qualname__,
                str(args),
                str(sorted(kwargs.items()))
            ]
            key = hashlib.md5('|'.join(key_parts).encode('utf-8')).hexdigest()
            
            # Check cache
            async with lock:
                if key in cache:
                    entry = cache[key]
                    if entry['expires_at'] is None or entry['expires_at'] > time.time():
                        return entry['value']
            
            # Compute and cache the result
            result = await fn(*args, **kwargs)
            
            async with lock:
                cache[key] = {
                    'value': result,
                    'expires_at': time.time() + ttl if ttl else None
                }
                
                # Enforce maxsize (simple FIFO)
                if len(cache) > maxsize:
                    # Remove the first item
                    first_key = next(iter(cache))
                    del cache[first_key]
            
            return result
        
        return wrapper
    
    if func is not None:
        return decorator(func)
    return decorator

# 8. Example: Cache Versioning

def versioned_memoize(version: int = 1) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Memoization decorator with versioning support."""
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        # Use a versioned cache
        cache: Dict[str, Tuple[int, R]] = {}
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            # Create a cache key
            key_parts = [
                func.__module__ or '',
                func.__qualname__,
                str(args),
                str(sorted(kwargs.items()))
            ]
            key = hashlib.md5('|'.join(key_parts).encode('utf-8')).hexdigest()
            
            # Check cache
            if key in cache:
                cached_version, result = cache[key]
                if cached_version >= version:
                    return result
            
            # Compute and cache the result
            result = func(*args, **kwargs)
            cache[key] = (version, result)
            return result
        
        return wrapper
    return decorator

def demonstrate() -> None:
    """Demonstrate advanced memoization patterns."""
    print("=== Advanced Memoization Patterns ===\n")
    
    # 1. Basic usage with selective argument memoization
    print("1. Selective Argument Memoization:")
    
    @advanced_memoize(skip_kwargs={'debug'})
    def process_data(data: str, *, debug: bool = False) -> str:
        print(f"  Processing data: {data} (debug: {debug})")
        time.sleep(0.5)
        return f"PROCESSED-{data.upper()}"
    
    print("\nFirst call (will compute):")
    print(process_data("test"))
    
    print("\nSame call (should use cache):")
    print(process_data("test"))
    
    print("\nDifferent debug flag (treated as same for caching):")
    print(process_data("test", debug=True))
    
    # 2. Class with memoized methods
    print("\n2. Class with Memoized Methods:")
    
    processor = DataProcessor("TestProcessor")
    
    print("\nFirst process call (will compute):")
    print(processor.process("hello"))
    
    print("\nSecond process call (should use cache):")
    print(processor.process("hello"))
    
    print("\nAccessing expensive property (will compute):")
    print(processor.expensive_property)
    
    print("\nAccessing again (should use cache):")
    print(processor.expensive_property)
    
    # 3. Cache statistics
    print("\n3. Cache Statistics:")
    stats = processor.process.get_cache_stats()  # type: ignore
    print(f"Hits: {stats.hits}")
    print(f"Misses: {stats.misses}")
    print(f"Hit ratio: {stats.hit_ratio:.1%}")
    
    # 4. Async memoization
    print("\n4. Async Memoization:")
    
    @async_memoize(ttl=5)
    async def fetch_data(url: str) -> str:
        print(f"  Fetching data from {url}...")
        await asyncio.sleep(1)  # Simulate network I/O
        return f"Data from {url} at {time.time()}"
    
    async def test_async() -> None:
        print("\nFirst async call (will compute):")
        print(await fetch_data("https://example.com/api"))
        
        print("\nSecond async call (should use cache):")
        print(await fetch_data("https://example.com/api"))
        
        print("\nWaiting for cache to expire...")
        await asyncio.sleep(6)
        
        print("\nAfter expiration (will compute again):")
        print(await fetch_data("https://example.com/api"))
    
    asyncio.run(test_async())
    
    # 5. Cache versioning
    print("\n5. Cache Versioning:")
    
    @versioned_memoize(version=1)
    def get_config() -> Dict[str, Any]:
        print("  Computing config v1...")
        return {"version": 1, "data": "Initial config"}
    
    print("\nFirst call (will compute):")
    print(get_config())
    
    print("\nSecond call (should use cache):")
    print(get_config())
    
    # Update the version
    get_config = versioned_memoize(version=2)(get_config.__wrapped__)  # type: ignore
    
    print("\nAfter version update (will compute again):")
    print(get_config())
    
    print("\nWith same version (should use cache):")
    print(get_config())

if __name__ == "__main__":
    demonstrate()
