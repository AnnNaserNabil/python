"""
8. Functional Programming Patterns with Closures

This module demonstrates how to implement common functional programming patterns
using Python closures. These patterns help write more declarative, reusable,
and maintainable code.

Key Concepts:
------------
1. Function Composition: Combining simple functions to build complex operations
2. Currying: Transforming multi-argument functions into chains of single-argument functions
3. Memoization: Caching function results to avoid redundant calculations
4. Partial Application: Fixing some arguments of a function to create new functions
5. Pipelines: Creating data processing flows with function chains

Why Use These Patterns?
---------------------
- Write more declarative and readable code
- Improve code reusability and modularity
- Implement efficient caching strategies
- Create flexible and configurable function behaviors
- Build complex operations from simple, testable components

Real-world Applications:
----------------------
- Data processing and transformation
- API development
- Configuration management
- Performance optimization
- Building domain-specific languages (DSLs)

Example:
-------
>>> # Function composition
>>> add = lambda x, y: x + y
>>> square = lambda x: x * x
>>> process = compose(square, add)
>>> process(2, 3)  # square(add(2, 3)) = (2 + 3)² = 25
25

>>> # Memoization
>>> @memoize_with_ttl(ttl_seconds=60)
... def expensive_computation(x):
...     time.sleep(1)  # Simulate expensive operation
...     return x * x
>>> expensive_computation(4)  # Takes 1 second
16
>>> expensive_computation(4)  # Returns immediately (cached)
16
"""
from __future__ import annotations
from typing import TypeVar, Callable, Any, List, Dict, Tuple
from functools import reduce, partial
import math
import time

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# 1. Function Composition
def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Compose functions from right to left.
    
    Creates a new function that applies the given functions in right-to-left order.
    The output of each function becomes the input to the next.
    
    Args:
        *funcs: Functions to compose. Can be any number of callables.
        
    Returns:
        A new function that applies all functions in right-to-left order.
        
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> process = compose(square, add_one)
        >>> process(2)  # square(add_one(2)) = (2 + 1)² = 9
        9
        
    Note:
        If no functions are provided, returns the identity function (returns input as-is).
    """
    def _compose(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return reduce(_compose, funcs, lambda x: x)

# 2. Currying
def curry(func: Callable[..., T]) -> Callable[..., Any]:
    """
    Convert a function to a curried function.
    
    Currying transforms a function that takes multiple arguments into a sequence
    of functions that each take a single argument. This allows for partial
    application and more flexible function composition.
    
    Args:
        func: The function to curry. Must be a callable.
        
    Returns:
        A curried version of the input function.
        
    Example:
        >>> def add_three(a, b, c):
        ...     return a + b + c
        >>> curried_add = curry(add_three)
        >>> add_five = curried_add(2)(3)  # Partially apply first two args
        >>> add_five(5)  # Apply final argument
        10
        
    Note:
        The function will keep returning new functions until all required
        arguments are provided.
    """
    def curried(*args: Any, **kwargs: Any) -> Any:
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return lambda *more_args, **more_kwargs: curried(
            *args, *more_args, **{**kwargs, **more_kwargs}
        )
    return curried

# 3. Memoization with Cache Invalidation
def memoize_with_ttl(ttl_seconds: int = 300) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that caches function results with an expiration time.
    
    This decorator remembers the return value of a function call for a specified
    duration. If the function is called again with the same arguments within the
    TTL, the cached result is returned instead of recomputing.
    
    Args:
        ttl_seconds: Number of seconds to cache the function result.
                    Defaults to 5 minutes (300 seconds).
                    
    Returns:
        A decorator that can be applied to functions to add TTL-based caching.
        
    Example:
        >>> @memoize_with_ttl(ttl_seconds=60)  # Cache for 1 minute
        ... def get_weather(city: str) -> dict:
        ...     # Expensive API call here
        ...     return {"city": city, "temp": 22.5}
        
    Note:
        - Uses the function's arguments as the cache key
        - Not thread-safe for concurrent access
        - Cache entries are not automatically cleaned up
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[Tuple[Any, ...], Tuple[float, T]] = {}
        
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (args, frozenset(kwargs.items()))
            current_time = time.time()
            
            # Check cache
            if key in cache:
                timestamp, result = cache[key]
                if current_time - timestamp < ttl_seconds:
                    return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache[key] = (current_time, result)
            return result
        
        return wrapper
    return decorator

# 4. Function Pipelines
def pipeline(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Create a pipeline of functions to process data.
    
    pipeline(f, g, h)(x) -> h(g(f(x)))
    """
    def _pipeline(initial: Any) -> Any:
        return reduce(lambda acc, f: f(acc), funcs, initial)
    return _pipeline

# 5. Partial Application with Placeholders
class _Placeholder:
    def __init__(self, pos: int):
        self.pos = pos

def _(pos: int = 0) -> _Placeholder:
    """Create a placeholder for partial application."""
    return _Placeholder(pos)

def partial_apply(func: Callable[..., T], *args: Any, **kwargs: Any) -> Callable[..., T]:
    """Partially apply arguments to a function with placeholders."""
    placeholders: List[Tuple[int, int]] = [
        (i, arg.pos) for i, arg in enumerate(args) if isinstance(arg, _Placeholder)
    ]
    
    def wrapper(*more_args: Any, **more_kwargs: Any) -> T:
        # Fill placeholders with more_args
        new_args = list(args)
        for i, pos in placeholders:
            if pos < len(more_args):
                new_args[i] = more_args[pos]
        
        # Add any remaining args
        remaining_args = more_args[len(placeholders):]
        all_args = [arg for arg in new_args if not isinstance(arg, _Placeholder)]
        all_args.extend(remaining_args)
        
        return func(*all_args, **{**kwargs, **more_kwargs})
    
    return wrapper

# 6. Function Memoization with Custom Key Function
def memoize_with_key(key_func: Callable[..., Any]) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Memoize function results with a custom key function."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[Any, T] = {}
        
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = key_func(*args, **kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        
        return wrapper
    return decorator

# Example usage of the functional patterns
def demonstrate_functional_patterns() -> None:
    """
    Showcase various functional programming patterns using closures.
    
    This function demonstrates:
    1. Function composition to build complex operations
    2. Currying for partial function application
    3. Memoization with TTL for performance optimization
    4. Function pipelines for data processing
    5. Advanced partial application with placeholders
    
    Each example is designed to be self-contained and shows both the
    implementation and usage of these patterns.
    
    The examples progress from basic to more advanced patterns, building
    on concepts introduced earlier in the module.
    """
    print("=== Function Composition ===")
    add = lambda x, y: x + y
    square = lambda x: x * x
    double = lambda x: x * 2
    
    composed = compose(double, square, add)
    print(f"compose(double, square, add)(3, 4) = {composed(3, 4)}")  # double(square(add(3,4)))
    
    print("\n=== Currying ===")
    @curry
    def add_three(a: int, b: int, c: int) -> int:
        return a + b + c
    
    add_five = add_three(2)(3)  # Partial application
    print(f"add_three(2)(3)(5) = {add_three(2)(3)(5)}")
    print(f"add_five(10) = {add_five(10)}")
    
    print("\n=== Memoization with TTL ===")
    @memoize_with_ttl(ttl_seconds=2)
    def expensive_operation(x: int) -> int:
        print(f"Computing expensive_operation({x})...")
        time.sleep(1)
        return x * x
    
    print("First call (computes):", expensive_operation(5))
    print("Second call (cached):", expensive_operation(5))
    print("Waiting for cache to expire...")
    time.sleep(3)
    print("After TTL (computes again):", expensive_operation(5))
    
    print("\n=== Function Pipelines ===")
    process = pipeline(
        lambda x: x * 2,         # Double
        lambda x: x + 10,         # Add 10
        lambda x: f"Result: {x}"  # Format
    )
    print(f"Pipeline result: {process(5)}")
    
    print("\n=== Partial Application with Placeholders ===")
    def greet(greeting: str, name: str, punctuation: str = "!") -> str:
        return f"{greeting}, {name}{punctuation}"
    
    # Create a new function with placeholders
    hello = partial_apply(greet, _(), "World")
    print(hello("Hello"))  # Fills the first placeholder
    
    # Another example with multiple placeholders
    format_name = partial_apply("{1}, {0} {2}".format, _(), _(), _())
    print(format_name("John", "Doe", "Mr."))
    
    print("\n=== Memoization with Custom Key Function ===")
    @memoize_with_key(lambda x, y: (x, y % 2))  # Only cache based on x and y's parity
    def special_add(x: int, y: int) -> int:
        print(f"Computing special_add({x}, {y})...")
        return x + y
    
    print("special_add(2, 3) =", special_add(2, 3))  # Computes
    print("special_add(2, 5) =", special_add(2, 5))  # Uses cache (same x and y%2)
    print("special_add(3, 3) =", special_add(3, 3))  # Computes (different x)

if __name__ == "__main__":
    print("=== Functional Programming Patterns with Closures ===")
    demonstrate_functional_patterns()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures enable powerful functional programming patterns")
    print("2. Function composition allows creating new functions from existing ones")
    print("3. Currying and partial application provide flexible function interfaces")
    print("4. Memoization can be customized with TTL and key functions")
    print("5. Pipelines create readable data processing flows")
    print("6. These patterns promote code reuse and maintainability")
