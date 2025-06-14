"""
9. Distributed Memoization with Redis

This example demonstrates how to implement a distributed memoization system
using Redis as a shared cache, allowing multiple processes or machines to share
cached function results.
"""
import json
import pickle
import time
import hashlib
import functools
from typing import Any, Callable, Dict, Optional, TypeVar, cast, Union, List, Tuple
import logging

# Try to import Redis, but make it optional
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logging.warning("Redis not available. Install with: pip install redis")

# Type variables for better type hints
T = TypeVar('T')
R = TypeVar('R')

class RedisCache:
    """A Redis-based cache implementation."""
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        ttl: int = 3600,  # Default TTL: 1 hour
        prefix: str = "memoize:",
        serializer: str = 'pickle'  # 'pickle' or 'json'
    ) -> None:
        """Initialize the Redis cache.
        
        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number
            password: Redis password if required
            ttl: Time-to-live in seconds for cached items
            prefix: Prefix for all cache keys
            serializer: Serialization method ('pickle' or 'json')
        """
        if not REDIS_AVAILABLE:
            raise RuntimeError("Redis is not available. Install with: pip install redis")
        
        self._redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=False  # We'll handle serialization ourselves
        )
        self.ttl = ttl
        self.prefix = prefix
        self.serializer = serializer
    
    def _serialize(self, value: Any) -> bytes:
        """Serialize a value for storage in Redis."""
        if self.serializer == 'json':
            return json.dumps(value).encode('utf-8')
        else:  # pickle
            return pickle.dumps(value)
    
    def _deserialize(self, data: bytes) -> Any:
        """Deserialize a value from Redis."""
        if not data:
            return None
            
        if self.serializer == 'json':
            return json.loads(data.decode('utf-8'))
        else:  # pickle
            return pickle.loads(data)
    
    def _make_key(self, key: str) -> str:
        """Create a prefixed cache key."""
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Any:
        """Get a value from the cache."""
        try:
            data = self._redis.get(self._make_key(key))
            return self._deserialize(data) if data is not None else None
        except (redis.RedisError, pickle.PickleError, json.JSONDecodeError) as e:
            logging.error(f"Error getting from Redis cache: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in the cache."""
        try:
            serialized = self._serialize(value)
            ttl = ttl if ttl is not None else self.ttl
            return self._redis.set(
                name=self._make_key(key),
                value=serialized,
                ex=ttl
            )
        except (redis.RedisError, TypeError, OverflowError) as e:
            logging.error(f"Error setting Redis cache: {e}")
            return False
    
    def delete(self, *keys: str) -> int:
        """Delete one or more keys from the cache."""
        try:
            prefixed_keys = [self._make_key(k) for k in keys]
            return self._redis.delete(*prefixed_keys)
        except redis.RedisError as e:
            logging.error(f"Error deleting from Redis cache: {e}")
            return 0
    
    def clear(self) -> bool:
        """Clear all keys with the prefix."""
        try:
            # Note: This is not atomic in Redis < 6.2.0
            keys = self._redis.keys(f"{self.prefix}*")
            if keys:
                self._redis.delete(*keys)
            return True
        except redis.RedisError as e:
            logging.error(f"Error clearing Redis cache: {e}")
            return False

def memoize_redis(
    redis_cache: Optional[RedisCache] = None,
    key_func: Optional[Callable[..., str]] = None,
    ttl: Optional[int] = None
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    Memoization decorator that uses Redis as a distributed cache.
    
    Args:
        redis_cache: RedisCache instance. If None, tries to use a default local Redis.
        key_func: Function to generate cache keys. Defaults to a hash of function name and arguments.
        ttl: Time-to-live in seconds for cached items. Overrides RedisCache's default.
    """
    if redis_cache is None and REDIS_AVAILABLE:
        redis_cache = RedisCache()  # Default local Redis
    elif redis_cache is None:
        raise ValueError("Redis is not available and no cache was provided")
    
    if key_func is None:
        def default_key_func(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
            """Default key function using function name and argument hashes."""
            # Create a unique key based on function name and arguments
            key_parts = [
                func.__module__ or '',
                func.__qualname__,
                str(args),
                str(sorted(kwargs.items()))
            ]
            key_string = '|'.join(key_parts).encode('utf-8')
            return hashlib.md5(key_string).hexdigest()
        
        key_func = default_key_func
    
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            # Generate cache key
            cache_key = key_func(func, *args, **kwargs)  # type: ignore
            
            # Try to get from cache
            cached = redis_cache.get(cache_key)
            if cached is not None:
                logging.debug(f"Cache hit for {func.__name__}")
                return cast(R, cached)
            
            # Compute and cache the result
            logging.debug(f"Cache miss for {func.__name__}, computing...")
            result = func(*args, **kwargs)
            redis_cache.set(cache_key, result, ttl=ttl)
            return result
        
        # Add cache management methods to the wrapper
        wrapper.cache = redis_cache  # type: ignore
        
        def clear_cache() -> bool:
            """Clear all cache entries for this function."""
            # This is a simplified version that would need pattern matching in Redis
            # A more complete implementation would track keys to delete them
            return redis_cache.clear()
        
        wrapper.clear_cache = clear_cache  # type: ignore
        
        return wrapper
    
    return decorator

# Example usage
if __name__ == "__main__":
    import os
    import sys
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    
    # Check if Redis is available
    if not REDIS_AVAILABLE:
        print("Redis is not available. Install with: pip install redis")
        sys.exit(1)
    
    try:
        # Try to connect to Redis
        redis_cache = RedisCache(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', '6379')),
            db=int(os.getenv('REDIS_DB', '0')),
            password=os.getenv('REDIS_PASSWORD'),
            ttl=300,  # 5 minutes
            serializer='json'  # Use JSON for better interoperability
        )
        
        # Simple test to verify connection
        redis_cache.set("test", "Redis is working")
        print("Connected to Redis successfully!")
        
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        print("Using in-memory fallback (not distributed)")
        redis_cache = None
    
    # Example 1: Basic function with Redis memoization
    @memoize_redis(redis_cache, ttl=60)  # Cache for 1 minute
    def get_weather(city: str) -> Dict[str, Any]:
        """Get weather data (simulated)."""
        print(f"  Fetching weather for {city}...")
        time.sleep(1)  # Simulate API call
        return {
            "city": city,
            "temperature": 72 + (hash(city) % 20) - 10,  # Random-ish temp
            "conditions": random.choice(["sunny", "cloudy", "rainy", "partly cloudy"]),
            "timestamp": time.time()
        }
    
    # Example 2: Function with complex arguments
    @memoize_redis(redis_cache, ttl=300)  # Cache for 5 minutes
    def search_products(
        query: str,
        filters: Dict[str, Any],
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Search for products (simulated)."""
        print(f"  Searching products with query: {query}")
        time.sleep(1.5)  # Simulate database query
        
        # Generate some dummy results
        results = [
            {
                "id": i,
                "name": f"{query.capitalize()} Product {i}",
                "price": round(10 + (hash(f"{query}{i}") % 1000) / 10, 2),
                "in_stock": (hash(f"{query}{i}") % 2) == 0
            }
            for i in range(1, page_size + 1)
        ]
        
        return {
            "query": query,
            "filters": filters,
            "page": page,
            "page_size": page_size,
            "total": 100,  # Simulated total
            "results": results
        }
    
    def demonstrate() -> None:
        """Demonstrate Redis-based memoization."""
        print("\n=== Redis-based Memoization ===\n")
        
        # Test weather function
        print("1. Testing weather function:")
        
        print("\nFirst call (will compute):")
        weather1 = get_weather("New York")
        print(f"Result: {weather1}")
        
        print("\nSecond call (should use cache):")
        weather2 = get_weather("New York")
        print(f"Result: {weather2}")
        
        print("\nDifferent city (will compute):")
        weather3 = get_weather("London")
        print(f"Result: {weather3}")
        
        # Test product search
        print("\n2. Testing product search:")
        
        filters = {"category": "electronics", "min_price": 50, "in_stock": True}
        
        print("\nFirst search (will compute):")
        results1 = search_products("laptop", filters, page=1)
        print(f"Found {len(results1['results'])} results")
        
        print("\nSame search (should use cache):")
        results2 = search_products("laptop", filters, page=1)
        print(f"Found {len(results2['results'])} results")
        
        # Different page - should be a separate cache entry
        print("\nDifferent page (will compute):")
        results3 = search_products("laptop", filters, page=2)
        print(f"Found {len(results3['results'])} results")
        
        # Clear cache for the search_products function
        print("\nClearing cache for search_products...")
        search_products.clear_cache()  # type: ignore
        
        print("\nAfter cache clear (will compute):")
        results4 = search_products("laptop", filters, page=1)
        print(f"Found {len(results4['results'])} results")
    
    demonstrate()
