"""
4. Memoization with Cache Invalidation

This example demonstrates a memoization decorator with support for explicit
cache invalidation based on specific arguments or complete cache clearing.
"""
from functools import wraps
from typing import Any, Callable, Dict, Optional, Set, Tuple, Type, TypeVar, Union, cast

T = TypeVar('T', bound=Callable[..., Any])

class Memoized:
    """A class to hold memoization state and provide invalidation methods."""
    
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.cache: Dict[Tuple[Any, ...], Any] = {}
        self.arg_indices: Dict[Any, Set[Tuple[Any, ...]]] = {}
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Create a key from function arguments
        key = self._make_key(args, kwargs)
        
        # Return cached result if available
        if key in self.cache:
            print(f"Cache hit for {self.func.__name__}{args}")
            return self.cache[key]
        
        # Compute and cache the result
        print(f"Computing {self.func.__name__}{args}")
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        
        # Track which keys are associated with each argument value
        for i, arg in enumerate(args):
            self.arg_indices.setdefault((i, arg), set()).add(key)
        
        for k, v in kwargs.items():
            self.arg_indices.setdefault((k, v), set()).add(key)
        
        return result
    
    def _make_key(self, args: tuple, kwargs: dict) -> tuple:
        """Create a cache key from function arguments."""
        return (args, frozenset(kwargs.items()))
    
    def invalidate(self, *args: Any, **kwargs: Any) -> None:
        """Invalidate cache entries matching the given arguments."""
        if not args and not kwargs:
            # Clear entire cache if no arguments provided
            self.cache.clear()
            self.arg_indices.clear()
            print("Cache completely cleared")
            return
        
        # Find all keys that match the invalidation pattern
        keys_to_remove = set()
        
        # Check positional arguments
        for i, arg in enumerate(args):
            keys_to_remove.update(self.arg_indices.get((i, arg), set()))
        
        # Check keyword arguments
        for k, v in kwargs.items():
            keys_to_remove.update(self.arg_indices.get((k, v), set()))
        
        # Remove matching keys from cache
        for key in keys_to_remove:
            self.cache.pop(key, None)
        
        print(f"Invalidated {len(keys_to_remove)} cache entries")

def memoize_with_invalidation(func: T) -> T:
    """Memoization decorator with cache invalidation support."""
    memoized = Memoized(func)
    
    # Attach invalidation method to the function
    func.invalidate = memoized.invalidate  # type: ignore
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return memoized(*args, **kwargs)
    
    return cast(T, wrapper)

# Example usage
@memoize_with_invalidation
def get_user_data(user_id: int, data_type: str = 'profile') -> str:
    """Simulate fetching user data from a database."""
    print(f"  Fetching {data_type} data for user {user_id}...")
    return f"{data_type.capitalize()} data for user {user_id}"

def demonstrate() -> None:
    """Demonstrate cache invalidation."""
    print("=== Memoization with Cache Invalidation ===\n")
    
    # First calls - populate cache
    print("First calls (will cache results):")
    print(get_user_data(1, 'profile'))
    print(get_user_data(1, 'settings'))
    print(get_user_data(2, 'profile'))
    
    # These should hit cache
    print("\nCached calls:")
    print(get_user_data(1, 'profile'))
    print(get_user_data(1, 'settings'))
    
    # Invalidate all entries for user_id=1
    print("\nInvalidating cache for user_id=1:")
    get_user_data.invalidate(1)  # type: ignore
    
    # These will be recomputed
    print("\nAfter invalidation:")
    print(get_user_data(1, 'profile'))
    print(get_user_data(2, 'profile'))  # Still in cache
    
    # Invalidate all entries with data_type='profile'
    print("\nInvalidating cache for data_type='profile':")
    get_user_data.invalidate(data_type='profile')  # type: ignore
    
    # These will be recomputed
    print("\nAfter second invalidation:")
    print(get_user_data(1, 'profile'))
    print(get_user_data(2, 'profile'))
    
    # Clear entire cache
    print("\nClearing entire cache:")
    get_user_data.invalidate()  # type: ignore
    
    # These will be recomputed
    print("\nAfter clearing cache:")
    print(get_user_data(1, 'profile'))
    print(get_user_data(2, 'settings'))

if __name__ == "__main__":
    demonstrate()
