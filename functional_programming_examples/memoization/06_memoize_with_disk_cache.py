"""
6. Memoization with Disk-based Caching

This example demonstrates how to implement memoization with disk-based caching
using Python's pickle module, allowing cached results to persist between program runs.
"""
import hashlib
import os
import pickle
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeVar

T = TypeVar('T', bound=Callable[..., Any])

def get_cache_key(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    """Generate a unique cache key for the function call."""
    # Create a string representation of the function name and arguments
    key_parts = [
        func.__module__ or '',
        func.__qualname__,
        str(args),
        str(sorted(kwargs.items()))
    ]
    key_string = '|'.join(key_parts).encode('utf-8')
    
    # Create a hash of the key string
    return hashlib.md5(key_string).hexdigest()

def memoize_to_disk(cache_dir: str = '.cache') -> Callable[[T], T]:
    """
    Memoization decorator that caches results to disk.
    
    Args:
        cache_dir: Directory to store cache files
    """
    def decorator(func: T) -> T:
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key
            cache_key = get_cache_key(func, *args, **kwargs)
            cache_file = Path(cache_dir) / f"{cache_key}.pkl"
            
            # Try to load from cache
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        timestamp, result = pickle.load(f)
                    
                    # Check if cache entry is still valid (1 hour TTL)
                    if time.time() - timestamp < 3600:  # 1 hour TTL
                        print(f"Cache hit for {func.__name__}{args}")
                        return result
                    else:
                        print(f"Cache expired for {func.__name__}{args}")
                except (pickle.PickleError, EOFError, AttributeError) as e:
                    print(f"Cache error for {func.__name__}{args}: {e}")
                    # If there's an error reading the cache, we'll just recompute
            
            # Compute result if not in cache or cache is invalid
            print(f"Computing {func.__name__}{args}")
            result = func(*args, **kwargs)
            
            # Save to cache
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump((time.time(), result), f)
            except (IOError, pickle.PickleError) as e:
                print(f"Warning: Failed to cache result for {func.__name__}: {e}")
            
            return result
        
        # Add method to clear cache for this function
        def clear_cache() -> None:
            """Clear all cache entries for this function."""
            pattern = f"{func.__module__ or ''}|{func.__qualname__}|"
            pattern_hash = hashlib.md5(pattern.encode('utf-8')).hexdigest()
            
            cache_dir_path = Path(cache_dir)
            for cache_file in cache_dir_path.glob("*.pkl"):
                if cache_file.stem.startswith(pattern_hash):
                    try:
                        cache_file.unlink()
                    except OSError as e:
                        print(f"Error deleting cache file {cache_file}: {e}")
        
        wrapper.clear_cache = clear_cache  # type: ignore
        return wrapper  # type: ignore
    
    return decorator

# Example usage
@memoize_to_disk(cache_dir='.memoize_cache')
def expensive_operation(x: int, y: int) -> int:
    """Simulate an expensive computation."""
    print(f"  Performing expensive calculation: {x} * {y}")
    time.sleep(1)  # Simulate work
    return x * y

@memoize_to_disk(cache_dir='.memoize_cache')
def fetch_data(url: str) -> str:
    """Simulate fetching data from a URL."""
    print(f"  Fetching data from {url}...")
    time.sleep(2)  # Simulate network delay
    return f"Data from {url} (fetched at {time.ctftime(time.time())})"

def demonstrate() -> None:
    """Demonstrate disk-based memoization."""
    print("=== Disk-based Memoization ===\n")
    
    # First run - will compute and cache
    print("First call (will compute and cache):")
    result1 = expensive_operation(5, 7)
    print(f"Result: {result1}\n")
    
    # Second run - should use cached result
    print("Second call (should use cache):")
    result2 = expensive_operation(5, 7)
    print(f"Result: {result2}\n")
    
    # Different arguments - will compute and cache
    print("Different arguments (will compute and cache):")
    result3 = expensive_operation(3, 4)
    print(f"Result: {result3}\n")
    
    # Test with a different function
    print("Testing with a different function (URL fetching):")
    url = "https://api.example.com/data"
    print(fetch_data(url))
    print(fetch_data(url))  # Should use cache
    
    # Clear cache for expensive_operation
    print("\nClearing cache for expensive_operation...")
    expensive_operation.clear_cache()  # type: ignore
    
    # This will recompute
    print("\nAfter clearing cache:")
    print(expensive_operation(5, 7))  # Will recompute
    
    # Show cache files
    cache_dir = Path('.memoize_cache')
    if cache_dir.exists():
        print("\nCache files:")
        for i, file in enumerate(cache_dir.glob('*.pkl'), 1):
            print(f"  {i}. {file.name}")
    else:
        print("\nNo cache directory found.")

if __name__ == "__main__":
    demonstrate()
