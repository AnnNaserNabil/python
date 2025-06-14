"""
2. Function Composition with Partials in Python

This module demonstrates how to combine `functools.partial` with function composition
to create powerful and flexible function pipelines. Partial application allows us to
fix a certain number of arguments of a function, generating a new function with
fewer parameters.

Key Concepts:
------------
1. Partial Application: Fixing some arguments of a function to produce a new function
2. Function Composition: Combining functions to create more complex operations
3. Currying: Transforming a multi-argument function into a sequence of single-argument functions

Why Use Partials with Composition?
--------------------------------
- Specialization: Create specific functions from general ones
- Readability: Make code more declarative and intention-revealing
- Reusability: Reuse existing functions in new contexts
- Flexibility: Build complex behaviors by combining simple functions

Real-world Applications:
----------------------
- Data transformation pipelines
- Configuration of reusable components
- Mathematical and scientific computing
- API wrappers and adapters

Example:
-------
>>> from functools import partial
>>> add = lambda x, y: x + y
>>> add_five = partial(add, 5)
>>> double = partial(lambda x, y: x * y, 2)
>>> process = compose(double, add_five)
>>> process(3)  # double(add_five(3)) = (3 + 5) * 2 = 16
16
"""
from __future__ import annotations
from typing import Callable, TypeVar, Any
from functools import partial, reduce
import math

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Compose functions from right to left.
    
    Composes functions such that the output of each function is passed as input
    to the next function in the sequence (right to left).
    
    Args:
        *funcs: Variable number of functions to compose
        
    Returns:
        Callable[..., Any]: A new function that applies all input functions
                          from right to left
                          
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> composed = compose(square, add_one)
        >>> composed(2)  # square(add_one(2)) = (2 + 1)² = 9
        9
    """
    def _compose(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return reduce(_compose, funcs, lambda x: x)

def pipe(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Pipe functions from left to right.
    
    Applies functions in sequence from left to right, where the output of each
    function becomes the input to the next function.
    
    Args:
        *funcs: Variable number of functions to pipe
        
    Returns:
        Callable[..., Any]: A new function that applies all input functions
                          from left to right
                          
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> piped = pipe(add_one, square)
        >>> piped(2)  # square(add_one(2)) = (2 + 1)² = 9
        9
    """
    def _pipe(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: g(f(*args, **kwargs))
    return reduce(_pipe, funcs, lambda x: x)

def demonstrate_partials() -> None:
    """
    Demonstrate function composition with partial application.
    
    This function shows how to use `functools.partial` to create specialized
    functions from general ones, and then compose them to create more complex
    operations. It includes examples of:
    
    1. Creating simple partial functions
    2. Composing partial functions
    3. Building complex transformations through composition
    4. Using both positional and keyword arguments with partials
    
    The examples progress from basic to more advanced usage patterns.
    """
    # Basic math functions
    add = lambda x, y: x + y
    multiply = lambda x, y: x * y
    power = lambda x, y: x ** y
    
    # Create specialized functions using partial
    add_five = partial(add, 5)
    double = partial(multiply, 2)
    square = partial(power, y=2)
    cube = partial(power, y=3)
    
    # Compose with partials
    add_five_then_double = compose(double, add_five)
    print(f"add_five_then_double(3) = {add_five_then_double(3)}")  # (3 + 5) * 2 = 16
    
    # More complex composition
    process_number = compose(
        lambda x: x + 1,        # Increment
        partial(power, y=2),     # Square
        partial(add, 3),         # Add 3
        lambda x: x * 2          # Double
    )
    print(f"process_number(2) = {process_number(2)}")  # ((2 * 2) + 3) ^ 2 + 1 = 50
    
    # String processing example
    greet = lambda name: f"Hello, {name}!"
    exclaim = lambda s: s.upper() + "!!!"
    add_smile = lambda s: s + " 😊"
    
    enthusiastic_greeting = compose(add_smile, exclaim, greet)
    print(f"enthusiastic_greeting('Alice') = {enthusiastic_greeting('Alice')}")
    
    # Data processing pipeline
    data = [1, 2, 3, 4, 5]
    
    # Create processing steps
    filter_even = partial(filter, lambda x: x % 2 == 0)
    multiply_by = lambda factor: partial(map, lambda x: x * factor)
    sum_all = partial(sum)
    
    # Compose the pipeline
    pipeline = compose(
        sum_all,                # Sum all numbers
        multiply_by(3),         # Multiply each by 3
        filter_even,            # Keep even numbers
        lambda x: map(str, x)   # Convert to strings for demonstration
    )
    
    # Need to convert map/filter to list for printing
    result = list(pipeline(data))
    print(f"Pipeline result: {result}")  # ['6', '12']
    
    # Alternative with list comprehensions
    pipeline2 = compose(
        sum,
        partial(map, lambda x: x * 3),
        partial(filter, lambda x: x % 2 == 0)
    )
    
    result2 = pipeline2(data)
    print(f"Pipeline2 result: {result2}")  # 18 (6 + 12)

def demonstrate_currying() -> None:
    """
    Demonstrate currying and its relationship with partial application.
    
    Currying is the technique of transforming a function that takes multiple
    arguments into a sequence of functions that each take a single argument.
    This function shows:
    
    1. Manual currying of functions
    2. Using partial application to simulate currying
    3. Composing curried functions
    4. Practical examples of currying in function pipelines
    
    Note the difference between currying (transforming functions) and
    partial application (fixing arguments).
    """
    # A curried add function
    def add(x: int) -> Callable[[int], int]:
        def inner(y: int) -> int:
            return x + y
        return inner
    
    # Curried multiply
    def multiply(x: int) -> Callable[[int], int]:
        return lambda y: x * y
    
    # Compose curried functions
    add_then_multiply = compose(
        multiply(3),  # Triple the result
        add(5)        # Add 5
    )
    
    print(f"add_then_multiply(10) = {add_then_multiply(10)}")  # (10 + 5) * 3 = 45
    
    # More complex example with multiple arguments
    def power(exponent: float) -> Callable[[float], float]:
        return lambda base: base ** exponent
    
    def root(n: float) -> Callable[[float], float]:
        return lambda x: x ** (1/n)
    
    # Compose mathematical operations
    transform = compose(
        power(2),       # Square the result
        root(2),        # Square root
        power(3),       # Cube the number
        lambda x: x + 1  # Add 1
    )
    
    # ((1 + 1)^3)^(1/2))^2 = (1 + 1)^3 = 8
    print(f"transform(1) = {transform(1):.1f}")

def demonstrate_real_world() -> None:
    """
    Demonstrate practical, real-world applications of composition with partials.
    
    This function shows how these concepts can be applied to solve common
    programming problems, including:
    
    1. Data processing and transformation
    2. Configuration of reusable components
    3. Building domain-specific languages (DSLs)
    4. Creating flexible APIs
    
    Each example is designed to show how partial application and composition
    can lead to more maintainable and expressive code.
    """
    # Data validation pipeline
    def validate_non_empty(s: str) -> str:
        if not s.strip():
            raise ValueError("String cannot be empty")
        return s
    
    def validate_length(max_length: int) -> Callable[[str], str]:
        def validator(s: str) -> str:
            if len(s) > max_length:
                raise ValueError(f"String exceeds maximum length of {max_length}")
            return s
        return validator
    
    def normalize_whitespace(s: str) -> str:
        return ' '.join(s.split())
    
    def to_title_case(s: str) -> str:
        return s.title()
    
    # Create a validation and normalization pipeline
    process_name = pipe(
        str,                    # Convert to string
        validate_non_empty,     # Check not empty
        validate_length(50),    # Check length
        normalize_whitespace,   # Normalize spaces
        to_title_case           # Format name
    )
    
    test_names = ["  john   doe  ", "", "a" * 60, 12345]
    
    print("\nName Processing:")
    for name in test_names:
        try:
            result = process_name(name)
            print(f"'{name}' -> '{result}'")
        except ValueError as e:
            print(f"Error processing '{name}': {e}")

if __name__ == "__main__":
    print("=== Composition with Partials ===")
    demonstrate_partials()
    
    print("\n=== Currying and Composition ===")
    demonstrate_currying()
    
    print("\n=== Real-world Example ===")
    demonstrate_real_world()
    
    print("\n=== Key Takeaways ===")
    print("1. functools.partial creates specialized functions from general ones")
    print("2. Partials work well with composition to create pipelines")
    print("3. Currying transforms multi-argument functions into chains of single-argument functions")
    print("4. Real-world uses include data validation, transformation pipelines")
    print("5. Composition with partials enables clean, readable data processing")
