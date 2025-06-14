"""
10. Advanced Higher-Order Function Patterns

Explores advanced patterns and techniques using higher-order functions,
including trampolining, memoization of recursive functions, continuation-passing style,
and other functional programming concepts.
"""
from __future__ import annotations
from typing import (
    TypeVar, Callable, Any, Dict, List, Tuple, Optional, Union, cast,
    Generic, TypeAlias, Protocol
)
from functools import partial, wraps, lru_cache
import time
import sys
import math
from collections.abc import Iterable, Iterator

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# 1. Trampolining for Tail Recursion

class TailCall(Generic[T]):
    """Base class for tail call optimization."""
    pass

class Done(TailCall[T]):
    """Represents the final result of a tail-recursive computation."""
    def __init__(self, result: T):
        self.result = result

class Call(TailCall[T]):
    """Represents a tail call to another function."""
    def __init__(self, thunk: Callable[[], TailCall[T]]):
        self.thunk = thunk

def trampoline[T](func: Callable[..., TailCall[T]]) -> Callable[..., T]:
    """
    Decorator that converts a tail-recursive function into an iterative one.
    
    The decorated function should return either:
    - Done(result) for the final result
    - Call(lambda: func(*args)) for a tail call
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        result = func(*args, **kwargs)
        while isinstance(result, Call):
            result = result.thunk()
        return cast(Done[T], result).result
    return wrapper

# Example: Tail-recursive factorial using trampoline
@trampoline
def factorial_tail(n: int, acc: int = 1) -> TailCall[int]:
    if n <= 1:
        return Done(acc)
    return Call(lambda: factorial_tail(n - 1, n * acc))

# 2. Memoization of Recursive Functions

def memoize_recursive(func: Callable[..., T]) -> Callable[..., T]:
    """
    A memoization decorator that works with recursive functions.
    
    This is more efficient than functools.lru_cache for deeply recursive functions
    because it populates the cache during the recursive calls.
    """
    cache: Dict[tuple, T] = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            # Use a proxy to update the cache during recursion
            def proxy(*args: Any, **kwargs: Any) -> T:
                return func(*args, **kwargs)
            
            # Replace the function with a memoized version
            wrapper._proxy = proxy  # type: ignore
            cache[key] = func(*args, **kwargs)
            del wrapper._proxy  # type: ignore
        
        return cache[key]
    
    return wrapper

# Example: Memoized Fibonacci
@memoize_recursive
def fib_memo(n: int) -> int:
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

# 3. Continuation-Passing Style (CPS)

# A continuation is a function that represents "the rest of the computation"
Continuation: TypeAlias = Callable[[T], None]

def cps_factorial(n: int, cont: Continuation[int]) -> None:
    """Factorial in continuation-passing style."""
    if n == 0:
        cont(1)
    else:
        cps_factorial(n - 1, lambda x: cont(n * x))

def run_cps_factorial(n: int) -> int:
    """Run a CPS function and return its result."""
    result: list[int] = []
    cps_factorial(n, result.append)
    return result[0]

# 4. Function Composition with Multiple Arguments

def compose(*funcs: Callable) -> Callable:
    """
    Compose functions from right to left.
    The first function can take any number of arguments.
    Subsequent functions must take a single argument.
    """
    def composed(*args: Any, **kwargs: Any) -> Any:
        result = funcs[-1](*args, **kwargs)
        for f in reversed(funcs[:-1]):
            result = f(result)
        return result
    return composed

# 5. Function Memoization with Custom Cache Key

def memoize_with_key(
    key_func: Optional[Callable[..., Any]] = None,
    maxsize: Optional[int] = 128
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Memoization decorator with custom cache key function.
    
    Args:
        key_func: Function to generate cache keys from function arguments.
                 If None, uses the arguments directly.
        maxsize: Maximum cache size (passed to lru_cache)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if key_func is None:
            # Use lru_cache directly if no key function is provided
            return lru_cache(maxsize=maxsize)(func)
        
        cache: Dict[Any, T] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = key_func(*args, **kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        
        return wrapper
    
    return decorator

# 6. Function Memoization with Time-based Expiration

def memoize_with_expiry(expiry_seconds: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Memoization decorator with time-based cache expiration.
    
    Args:
        expiry_seconds: Number of seconds after which cache entries expire
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[tuple, tuple[float, T]] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (args, frozenset(kwargs.items()))
            current_time = time.time()
            
            if key in cache:
                timestamp, result = cache[key]
                if current_time - timestamp < expiry_seconds:
                    return result
            
            # Cache miss or expired
            result = func(*args, **kwargs)
            cache[key] = (current_time, result)
            return result
        
        return wrapper
    
    return decorator

# 7. Function Composition with Error Handling

def safe_compose(*funcs: Callable) -> Callable[..., tuple[bool, Any]]:
    """
    Compose functions with error handling.
    
    Returns:
        A tuple (success, result) where success is a boolean indicating
        whether all functions executed successfully.
    """
    def composed(*args: Any, **kwargs: Any) -> tuple[bool, Any]:
        try:
            result = funcs[-1](*args, **kwargs)
            for f in reversed(funcs[:-1]):
                result = f(result)
            return True, result
        except Exception as e:
            return False, e
    return composed

# 8. Memoization with Dependencies

def memoize_with_deps(
    dep_funcs: dict[str, Callable[..., Any]]
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Memoization that depends on other functions.
    
    The cache is invalidated when any of the dependency functions return
    a different value than they did on the previous call.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: dict[tuple, tuple[dict[str, Any], T]] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (args, frozenset(kwargs.items()))
            
            # Get current dependency values
            current_deps = {name: dep() for name, dep in dep_funcs.items()}
            
            # Check cache
            if key in cache:
                cached_deps, result = cache[key]
                if cached_deps == current_deps:
                    return result
            
            # Cache miss or invalidated
            result = func(*args, **kwargs)
            cache[key] = (current_deps, result)
            return result
        
        return wrapper
    
    return decorator

# 9. Function Composition with Type Checking

def type_checked_compose(
    *funcs: Callable,
    input_type: Optional[type] = None,
    output_type: Optional[type] = None
) -> Callable:
    """
    Compose functions with runtime type checking.
    
    Args:
        *funcs: Functions to compose
        input_type: Expected type of the input to the first function
        output_type: Expected type of the output from the last function
    """
    def composed(*args: Any, **kwargs: Any) -> Any:
        # Check input type if specified
        if input_type is not None and args and not isinstance(args[0], input_type):
            raise TypeError(f"Expected input of type {input_type}, got {type(args[0])}")
        
        # Apply functions
        result = funcs[-1](*args, **kwargs)
        for f in reversed(funcs[:-1]):
            result = f(result)
        
        # Check output type if specified
        if output_type is not None and not isinstance(result, output_type):
            raise TypeError(f"Expected output of type {output_type}, got {type(result)}")
        
        return result
    
    return composed

# 10. Function Memoization with Custom Cache Backend

class CacheBackend(Protocol):
    """Protocol for cache backends."""
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def contains(self, key: str) -> bool: ...

class DictCache:
    """Simple in-memory cache using a dictionary."""
    def __init__(self):
        self._cache: dict[str, Any] = {}
    
    def get(self, key: str) -> Any:
        return self._cache[key]
    
    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
    
    def contains(self, key: str) -> bool:
        return key in self._cache

def memoize_with_backend(
    cache: CacheBackend,
    key_func: Optional[Callable[..., str]] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Memoization decorator with a custom cache backend.
    
    Args:
        cache: Cache backend implementing the CacheBackend protocol
        key_func: Function to generate cache keys from function arguments
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if key_func is None:
            def default_key(*args: Any, **kwargs: Any) -> str:
                return f"{func.__name__}:{args}:{frozenset(kwargs.items())}"
            key_func_ = default_key
        else:
            key_func_ = key_func
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = key_func_(*args, **kwargs)
            if cache.contains(key):
                return cache.get(key)
            
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        
        return wrapper
    
    return decorator

def demonstrate_advanced_patterns() -> None:
    print("=== Advanced Higher-Order Function Patterns ===\n")
    
    # 1. Trampolining
    print("1. Trampolining for Tail Recursion:")
    print(f"Factorial of 5: {factorial_tail(5)}")
    print(f"Factorial of 10: {factorial_tail(10)}")
    
    # 2. Memoized Fibonacci
    print("\n2. Memoized Fibonacci:")
    print(f"fib(10) = {fib_memo(10)}")
    print(f"fib(20) = {fib_memo(20)}")
    
    # 3. Continuation-Passing Style
    print("\n3. Continuation-Passing Style (CPS):")
    print(f"5! = {run_cps_factorial(5)}")
    
    # 4. Function Composition
    print("\n4. Function Composition:")
    add_one = lambda x: x + 1
    square = lambda x: x * x
    composed = compose(print, square, add_one)
    print("compose(print, square, add_one)(3) ->")
    composed(3)  # Should print 16
    
    # 5. Memoization with Custom Key
    print("\n5. Memoization with Custom Key:")
    
    def user_key(username: str, _age: int) -> str:
        return f"user:{username}"
    
    @memoize_with_key(key_func=user_key)
    def get_user(username: str, age: int) -> dict:
        print(f"Fetching user {username}...")
        return {"username": username, "age": age, "timestamp": time.time()}
    
    # First call - fetches user
    user1 = get_user("alice", 30)
    # Second call with same username but different age - uses cache
    user2 = get_user("alice", 31)
    print(f"Same user (should be True): {user1 is user2}")
    
    # 6. Memoization with Expiry
    print("\n6. Memoization with Expiry:")
    
    @memoize_with_expiry(expiry_seconds=2)
    def get_current_time() -> float:
        return time.time()
    
    t1 = get_current_time()
    t2 = get_current_time()
    print(f"Times should be equal: {t1 == t2}")
    
    time.sleep(2.1)  # Wait for cache to expire
    t3 = get_current_time()
    print(f"After expiry, times should differ: {t1 != t3}")
    
    # 7. Safe Composition
    print("\n7. Safe Function Composition:")
    safe_ops = safe_compose(
        lambda x: x + 1,
        lambda x: x / 0,  # This will raise an error
        lambda x: x * 2
    )
    
    success, result = safe_ops(5)
    print(f"Operation {'succeeded' if success else 'failed'}: {result}")
    
    # 8. Memoization with Dependencies
    print("\n8. Memoization with Dependencies:")
    
    # Simulate configuration that might change
    config = {"debug": False}
    
    def get_config_debug() -> bool:
        return config["debug"]
    
    @memoize_with_deps({"debug": get_config_debug})
    def expensive_operation(x: int) -> int:
        print(f"Computing with x={x} and debug={get_config_debug()}")
        return x * x
    
    # First call - computes
    print(expensive_operation(5))
    # Second call - uses cache
    print(expensive_operation(5))
    # Change dependency
    config["debug"] = True
    # Cache is invalidated, recomputes
    print(expensive_operation(5))
    
    # 9. Type-Checked Composition
    print("\n9. Type-Checked Composition:")
    
    def to_upper(s: str) -> str:
        return s.upper()
    
    def repeat(s: str) -> str:
        return s * 2
    
    process = type_checked_compose(
        repeat,
        to_upper,
        input_type=str,
        output_type=str
    )
    
    print(process("hello"))  # Should print "HELLOHELLO"
    
    # This would raise a TypeError:
    # process(123)  # Uncomment to see the error
    
    # 10. Custom Cache Backend
    print("\n10. Custom Cache Backend:")
    
    class PrintCache:
        def get(self, key: str) -> Any:
            print(f"Cache get: {key}")
            return None
        
        def set(self, key: str, value: Any) -> None:
            print(f"Cache set: {key} = {value}")
        
        def contains(self, key: str) -> bool:
            print(f"Cache contains: {key}")
            return False
    
    @memoize_with_backend(PrintCache())
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    print(greet("Alice"))
    print(greet("Alice"))  # Should hit the cache

if __name__ == "__main__":
    demonstrate_advanced_patterns()
    
    print("\n=== Key Takeaways ===")
    print("1. Trampolining enables efficient tail recursion in Python")
    print("2. Memoization can be customized with cache keys and expiration")
    print("3. Continuation-passing style enables advanced control flow")
    print("4. Function composition can be enhanced with type checking and error handling")
    print("5. Custom cache backends allow integration with distributed caches")
    print("6. Dependency tracking enables smart cache invalidation")
