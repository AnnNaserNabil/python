"""
5. Python Decorators Implemented with Closures

This module demonstrates how Python decorators are implemented using closures.
Decorators are a powerful feature that allow modifying or enhancing functions
without changing their source code.

Key Concepts:
------------
1. Decorator Pattern: A function that takes a function and returns a new function
2. Closures: Inner functions that remember variables from their enclosing scope
3. Decorator Factories: Functions that return decorators with custom behavior
4. Function Wrapping: Preserving function metadata with @functools.wraps

Why Use Decorators?
-----------------
- Code Reuse: Apply the same functionality to multiple functions
- Separation of Concerns: Keep cross-cutting concerns separate from business logic
- Readability: Clearly indicate special behavior with @syntax
- Extensibility: Add functionality without modifying the original function

Common Use Cases:
---------------
- Logging and debugging
- Timing and performance measurement
- Access control and authentication
- Input validation
- Caching and memoization
- Retry mechanisms

Example:
-------
>>> @timer
... def calculate():
...     return 2 ** 100
>>> calculate()  # Automatically prints the execution time
1267650600228229401496703205376
"""
from __future__ import annotations
from typing import Callable, TypeVar, Any, cast
import time
import functools
import math

T = TypeVar('T', bound=Callable[..., Any])

def simple_decorator(func: T) -> T:
    """
    A basic decorator that adds print statements around function execution.
    
    This is the simplest form of a decorator that takes a function and returns
    a new function that adds behavior before and after the original function.
    
    Args:
        func (T): The function to be decorated
        
    Returns:
        T: A new function that wraps the original function
        
    Example:
        >>> @simple_decorator
        ... def say_hello():
        ...     print("Hello!")
        >>> say_hello()
        Calling say_hello
        Hello!
        Finished say_hello
        
    Note:
        The cast(T, wrapper) is used to maintain type information. In practice,
        you might want to use @functools.wraps(func) to preserve the original
        function's metadata.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return cast(T, wrapper)

def timer(func: T) -> T:
    """
    A decorator that measures and prints the execution time of a function.
    
    This decorator is useful for performance testing and optimization.
    It works with functions that take any number of arguments and return any value.
    
    Args:
        func (T): The function to be timed
        
    Returns:
        T: A new function that times the execution of the original function
        
    Example:
        >>> @timer
        ... def slow_function():
        ...     return sum(i**2 for i in range(10**6))
        >>> result = slow_function()  # Prints execution time
        
    Note:
        Uses time.perf_counter() for high-precision timing.
        The timing includes the overhead of the decorator itself.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return cast(T, wrapper)

def repeat(num_times: int) -> Callable[[T], T]:
    """
    A decorator factory that creates a decorator to repeat a function call.
    
    This is an example of a decorator that takes arguments. The outer function
    accepts the configuration (number of times to repeat), and returns a
    decorator function that can be applied to other functions.
    
    Args:
        num_times (int): How many times to repeat the function call
        
    Returns:
        Callable[[T], T]: A decorator function
        
    Example:
        >>> @repeat(3)
        ... def greet(name):
        ...     print(f"Hello {name}!")
        >>> greet("Alice")
        Hello Alice!
        Hello Alice!
        Hello Alice!
        
    Note:
        The function's return value will only be from the last call.
        All previous calls' return values are discarded.
    """
    def decorator(func: T) -> T:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for _ in range(num_times - 1):
                func(*args, **kwargs)
            return func(*args, **kwargs)
        return cast(T, wrapper)
    return decorator

def memoize(func: T) -> T:
    """
    A memoization decorator that caches function results.
    
    Memoization is an optimization technique that stores the results of expensive
    function calls and returns the cached result when the same inputs occur again.
    
    Args:
        func (T): The function to be memoized
        
    Returns:
        T: A new function with memoization capability
        
    Example:
        >>> @memoize
        ... def fibonacci(n):
        ...     if n < 2:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
        >>> fibonacci(30)  # Fast due to memoization
        
    Note:
        - Uses a dictionary to cache results
        - Converts keyword arguments to a frozenset for hashability
        - Not suitable for functions with unhashable arguments
        - For production use, consider `functools.lru_cache` instead
    """
    cache: dict[tuple[Any, ...], Any] = {}
    
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Create a key from function arguments
        key = (args, frozenset(kwargs.items()))
        
        # Return cached result if available
        if key in cache:
            return cache[key]
        
        # Call the function and cache the result
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    # Copy function attributes for better introspection
    functools.update_wrapper(wrapper, func)
    return cast(T, wrapper)

def validate_input(validator: Callable[[Any], bool], error_msg: str = "Invalid input") -> Callable[[T], T]:
    """A decorator factory that validates function input."""
    def decorator(func: T) -> T:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for arg in args:
                if not validator(arg):
                    raise ValueError(f"{error_msg}: {arg}")
            for arg in kwargs.values():
                if not validator(arg):
                    raise ValueError(f"{error_msg}: {arg}")
            return func(*args, **kwargs)
        return cast(T, wrapper)
    return decorator

# Example usage of the decorators
@simple_decorator
def greet(name: str) -> None:
    """Greet someone."""
    print(f"Hello, {name}!")

@timer
def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

@repeat(3)
def say_hello(name: str) -> None:
    """Say hello multiple times."""
    print(f"Hello, {name}!")

@memoize
def factorial(n: int) -> int:
    """Calculate factorial with memoization."""
    print(f"Calculating factorial({n})")
    if n == 0:
        return 1
    return n * factorial(n - 1)

@validate_input(lambda x: x > 0, "Number must be positive")
def square_root(x: float) -> float:
    """Calculate the square root of a positive number."""
    return math.sqrt(x)

def demonstrate_decorators() -> None:
    """
    Demonstrate various decorator patterns and their use cases.
    
    This function shows how different decorators can be applied to functions
    to add functionality like logging, timing, validation, and memoization.
    
    The examples include:
    1. Simple function decoration
    2. Function timing with the @timer decorator
    3. Function repetition with @repeat
    4. Memoization of recursive functions
    5. Input validation with a decorator factory
    
    Each example demonstrates a different aspect of how decorators can be
    used to separate concerns and add reusable functionality to functions.
    """
    print("=== Simple Decorator ===")
    greet("Alice")
    
    print("\n=== Timer Decorator ===")
    # Note: This will be slow due to the recursive implementation
    # For better performance, we'll use a small number
    print(f"Fibonacci(10) = {calculate_fibonacci(10)}")
    
    print("\n=== Repeat Decorator ===")
    say_hello("Bob")
    
    print("\n=== Memoization Decorator ===")
    print(f"factorial(5) = {factorial(5)}")
    print(f"factorial(5) = {factorial(5)} (cached)")
    print(f"factorial(6) = {factorial(6)} (uses cached result for 5!)")
    
    print("\n=== Validation Decorator ===")
    try:
        print(f"sqrt(16) = {square_root(16)}")
        print("Trying sqrt(-1)...")
        print(f"sqrt(-1) = {square_root(-1)}")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Show that decorators preserve function metadata
    print("\n=== Function Metadata ===")
    print(f"factorial.__name__ = {factorial.__name__}")
    print(f"factorial.__doc__ = {factorial.__doc__.strip()}")

if __name__ == "__main__":
    print("=== Decorators as Closures ===")
    demonstrate_decorators()
    
    print("\n=== Key Takeaways ===")
    print("1. Decorators are functions that modify the behavior of other functions")
    print("2. Decorators are implemented using closures to maintain state")
    print("3. Decorators can accept arguments using decorator factories")
    print("4. The @ syntax is just syntactic sugar for function application")
    print("5. functools.wraps helps preserve function metadata")
    print("6. Decorators are powerful tools for cross-cutting concerns")
