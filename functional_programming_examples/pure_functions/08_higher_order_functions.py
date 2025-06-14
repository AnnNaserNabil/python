"""
8. Higher-Order Pure Functions in Python

This module demonstrates higher-order functions (HOFs) in Python, which are functions that:
1. Take one or more functions as arguments, and/or
2. Return a function as a result

Key Concepts:
------------
- First-class functions: Functions are treated as first-class citizens
- Function factories: Functions that create and return other functions
- Function decorators: Functions that modify the behavior of other functions
- Function composition: Combining simple functions to build more complex ones
- Closures: Functions that remember values in enclosing scopes
- Pure functions: Functions without side effects that always produce the same output for the same input

Why Use Higher-Order Functions?
-----------------------------
- Enable more abstract and declarative code
- Reduce code duplication through function composition
- Allow for more modular and reusable code
- Enable powerful patterns like decorators and function factories
- Are fundamental to functional programming in Python

Common Use Cases:
---------------
- Callback functions
- Event handling
- Decorators for cross-cutting concerns (logging, timing, auth)
- Function composition for data processing pipelines
- Creating specialized versions of functions (partial application)

Example:
-------
>>> def make_multiplier(n):
...     def multiplier(x):
...         return x * n
...     return multiplier
>>> double = make_multiplier(2)
>>> double(5)
10
"""
from typing import Callable, TypeVar, Any, List
from functools import wraps

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def apply_twice(func: Callable[[T], T]) -> Callable[[T], T]:
    """
    Return a new function that applies the input function twice.
    
    This is a higher-order function that takes a function and returns a new function.
    The returned function applies the original function twice to its input.
    
    Args:
        func: A function that takes one argument and returns a value of the same type
        
    Returns:
        Callable[[T], T]: A new function that applies `func` twice to its input
        
    Examples:
        >>> def add_one(x):
        ...     return x + 1
        >>> add_two = apply_twice(add_one)
        >>> add_two(1)
        3  # ((1 + 1) + 1)
        
    Note:
        - The input function should be pure (no side effects)
        - The function is only called once if the input is already the result of `func`
        - Time complexity: O(2 * f) where f is the time complexity of `func`
    """
    def wrapper(x: T) -> T:
        return func(func(x))
    return wrapper

def make_adder(n: int) -> Callable[[int], int]:
    """
    Create a function that adds a fixed number to its argument.
    
    This is a function factory that returns a new function with the value of `n`
    "remembered" by the inner function (a closure).
    
    Args:
        n: The number to add to future arguments
        
    Returns:
        Callable[[int], int]: A function that takes an integer and returns the sum with `n`
        
    Examples:
        >>> add_five = make_adder(5)
        >>> add_five(3)
        8
        >>> add_neg = make_adder(-1)
        >>> add_neg(10)
        9
        
    Note:
        - The returned function is a closure that captures the value of `n`
        - Pure function: Same input always produces the same output
        - Time complexity: O(1) for the returned function
    """
    def adder(x: int) -> int:
        return x + n
    return adder

def compose(*funcs: Callable) -> Callable:
    """
    Compose functions from right to left.
    
    Function composition is a fundamental concept in functional programming where
    the output of one function is used as the input to the next function.
    
    compose(f, g, h)(x) = f(g(h(x)))
    
    Args:
        *funcs: Variable number of functions to compose. Can be zero or more.
               If no functions are provided, returns the identity function.
        
    Returns:
        Callable: A new function that is the composition of the input functions
        
    Examples:
        >>> def double(x): return x * 2
        >>> def square(x): return x * x
        >>> double_then_square = compose(square, double)
        >>> double_then_square(3)  # square(double(3)) = square(6) = 36
        36
        >>> # Compose with no functions returns the identity function
        >>> id_func = compose()
        >>> id_func(42)
        42
        
    Note:
        - Functions are applied from right to left (mathematical composition)
        - The first function in the composition can take any number of arguments
        - Subsequent functions must accept a single argument
        - Pure function: Output depends only on inputs and composed functions
    """
    def composed(*args, **kwargs):
        # Handle empty case (identity function)
        if not funcs:
            if not args:
                raise TypeError("compose() needs at least one argument")
            return args[0] if len(args) == 1 else args
            
        # Apply functions from right to left
        result = funcs[-1](*args, **kwargs)
        for func in reversed(funcs[:-1]):
            result = func(result)
        return result
    return composed

def memoize_pure(func: Callable[..., T]) -> Callable[..., T]:
    """
    Memoization decorator for pure functions with hashable arguments.
    
    Memoization is an optimization technique that caches the results of expensive
    function calls and returns the cached result when the same inputs occur again.
    
    Args:
        func: The pure function to memoize. Must be deterministic (same input
              always produces same output) and have no side effects.
        
    Returns:
        Callable[..., T]: A memoized version of the input function
        
    Examples:
        >>> @memoize_pure
        ... def fibonacci(n):
        ...     if n < 2:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
        >>> # First call computes the result
        >>> fibonacci(10)
        55
        >>> # Subsequent calls with same arguments return cached result
        >>> fibonacci(10)  # Returns immediately
        55
        
    Note:
        - Only works with hashable argument types
        - Uses memory proportional to the number of unique function calls
        - Not suitable for functions with large or unhashable arguments
        - The cache is stored on the function object itself
        - For production use, consider functools.lru_cache instead
    """
    cache = {}
    
    @wraps(func)  # Preserve original function's metadata
    def wrapper(*args, **kwargs):
        # Create a key from function arguments
        # frozenset is used for kwargs to handle unordered dict items
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper

def time_it(func: Callable) -> Callable:
    """
    Decorator that prints the time a function takes to execute.
    
    This is a higher-order function that adds timing functionality to any
    input function. Note that this decorator is not purely functional
    as it has the side effect of printing to stdout.
    
    Args:
        func: The function to be timed
        
    Returns:
        Callable: A wrapped version of the input function that prints timing information
        
    Examples:
        >>> @time_it
        ... def slow_function(n):
        ...     return sum(range(n))
        >>> result = slow_function(1_000_000)  # Prints timing info
        slow_function took 0.012345 seconds
        
    Note:
        - Not a pure function (has side effect of printing)
        - Uses time.perf_counter() for high-resolution timing
        - Preserves the original function's metadata with @wraps
        - Can be used as a decorator or called directly
    """
    @wraps(func)  # Preserve original function's metadata
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

# Example usage
if __name__ == "__main__":
    print("=== Higher-Order Functions Examples ===\n")
    
    # 1. Demonstrate apply_twice
    print("1. Applying a function twice:")
    
    def add_five(x: int) -> int:
        """Add 5 to the input."""
        return x + 5
    
    # apply_twice(add_five) creates a function that adds 10 (5 + 5)
    add_ten = apply_twice(add_five)
    result = add_ten(5)  # add_five(add_five(5)) = add_five(10) = 15
    print(f"add_ten(5) = {result}")
    
    # Demonstrate with a different function
    def square(x: int) -> int:
        """Square the input."""
        return x * x
    
    # apply_twice(square) creates a function that raises to the 4th power
    fourth_power = apply_twice(square)
    print(f"fourth_power(2) = {fourth_power(2)}")  # ((2²)²) = 16
    
    # 2. Demonstrate make_adder (function factory)
    print("\n2. Creating functions with make_adder:")
    
    add_three = make_adder(3)
    add_neg_one = make_adder(-1)
    
    print(f"add_three(7) = {add_three(7)}")
    print(f"add_neg_one(10) = {add_neg_one(10)}")
    
    # 3. Demonstrate function composition
    print("\n3. Function composition:")
    
    def double(x: int) -> int:
        """Double the input."""
        return x * 2
    
    def square(x: int) -> int:
        """Square the input."""
        return x * x
    
    # Compose functions: first double, then square
    double_then_square = compose(square, double)
    
    # Compose functions: first square, then double
    square_then_double = compose(double, square)
    
    x = 3
    print(f"double_then_square({x}) = square(double({x})) = {double_then_square(x)}")
    print(f"square_then_double({x}) = double(square({x})) = {square_then_double(x)}")
    
    # 4. Demonstrate memoization with Fibonacci
    print("\n4. Memoization with Fibonacci sequence:")
    
    @memoize_pure
    def fib(n: int) -> int:
        """Calculate nth Fibonacci number using recursion with memoization."""
        if n < 2:
            return n
        return fib(n-1) + fib(n-2)
    
    # This would be very slow without memoization
    print("First 15 Fibonacci numbers (with memoization):")
    for i in range(15):
        print(f"fib({i}) = {fib(i)}")
    
    # 5. Demonstrate timing with a slow function
    print("\n5. Timing function execution:")
    
    @time_it
    def slow_function(n: int) -> int:
        """A deliberately slow function to demonstrate timing."""
        total = 0
        for i in range(n):
            total += i
        return total
    
    # First call (will be slower)
    print("First call (computing result):")
    result1 = slow_function(10_000_000)
    
    # Second call with same input (will be faster if result was cached)
    print("\nSecond call (with same input):")
    result2 = slow_function(10_000_000)
    
    print(f"\nResults: {result1} (should equal {result2})")
    
    # 6. Verify function purity and correctness with assertions
    print("\n6. Verifying function purity and correctness...")
    
    # Test apply_twice
    assert add_ten(0) == 10  # 0 + 5 + 5 = 10
    assert fourth_power(3) == 81  # (3²)² = 81
    
    # Test make_adder
    assert add_three(5) == 8
    assert add_neg_one(10) == 9
    
    # Test compose
    assert double_then_square(4) == 64  # (4*2)² = 64
    assert square_then_double(4) == 32  # (4²)*2 = 32
    
    # Test memoize_pure
    assert fib(10) == 55
    
    # Test compose with no functions (should return identity function)
    identity = compose()
    assert identity(42) == 42
    
    print("\nAll tests passed! All higher-order functions are working as expected.")
