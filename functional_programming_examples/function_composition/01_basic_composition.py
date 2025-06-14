"""
1. Basic Function Composition in Python

This module introduces the fundamental concept of function composition, a core principle
in functional programming. Function composition is the process of combining two or more
functions to create a new function where the output of one function becomes the input
of the next.

Key Concepts:
------------
1. Function Composition (f ∘ g)(x) = f(g(x)): Apply one function to the result of another
2. Piping: Similar to composition but reads left-to-right
3. Type Safety: Using type variables to ensure type consistency in composed functions

Why Use Function Composition?
---------------------------
- Readability: Express complex operations as a pipeline of simple functions
- Reusability: Combine existing functions in new ways
- Maintainability: Small, focused functions are easier to test and debug
- Declarative Style: Focus on what to compute, not how to compute it

Real-world Applications:
----------------------
- Data processing pipelines
- API request/response transformations
- Input validation and sanitization
- Mathematical computations

Example:
-------
>>> def add_one(x): return x + 1
>>> def square(x): return x * x
>>> composed = compose(square, add_one)  # square(add_one(x))
>>> composed(2)  # (2 + 1)² = 9
9
>>> piped = pipe(add_one, square)  # square(add_one(x))
>>> piped(2)  # (2 + 1)² = 9
9
"""
from __future__ import annotations
from typing import Callable, TypeVar, Any

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose_two(f: Callable[[U], V], g: Callable[[T], U]) -> Callable[[T], V]:
    """
    Compose two functions: f ∘ g = f(g(x))
    
    This is the mathematical function composition where the output of g becomes
    the input of f. The resulting function applies g first, then applies f to
    the result of g.
    
    Args:
        f: A function that takes a value of type U and returns a value of type V
        g: A function that takes a value of type T and returns a value of type U
        
    Returns:
        Callable[[T], V]: A new function that takes a value of type T and returns 
                        a value of type V
                        
    Example:
        >>> def add_one(x: int) -> int: return x + 1
        >>> def square(x: int) -> int: return x * x
        >>> add_then_square = compose_two(square, add_one)
        >>> add_then_square(2)  # square(add_one(2)) = (2 + 1)² = 9
        9
        
    Note:
        - The order of arguments follows mathematical function composition
        - Type variables ensure type safety between composed functions
    """
    return lambda x: f(g(x))

def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Compose multiple functions from right to left.
    
    This is a generalized version of compose_two that can handle any number of
    functions. The functions are applied from right to left, meaning the rightmost
    function is applied first and the leftmost function is applied last.
    
    Args:
        *funcs: Variable number of functions to compose
        
    Returns:
        Callable[..., Any]: A new function that applies all input functions
                          from right to left
                          
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> def double(x): return x * 2
        >>> 
        >>> # Compose multiple functions: square(double(add_one(x)))
        >>> composed = compose(square, double, add_one)
        >>> composed(2)  # square(double(add_one(2))) = ((2 + 1) * 2)² = 36
        36
        
    Note:
        - Returns the identity function if no functions are provided
        - Uses functools.reduce for efficient composition
        - Type safety is not strictly enforced for more than two functions
    """
    def _compose(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    
    if not funcs:
        return lambda x: x
    
    return functools.reduce(_compose, funcs)

def pipe(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Pipe functions from left to right.
    
    Similar to compose, but applies functions from left to right, which can be
    more intuitive to read as it matches the order of execution. This is often
    called 'piping' in functional programming.
    
    Args:
        *funcs: Variable number of functions to pipe
        
    Returns:
        Callable[..., Any]: A new function that applies all input functions
                          from left to right
                          
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> def double(x): return x * 2
        >>> 
        >>> # Pipe functions: double(square(add_one(x)))
        >>> piped = pipe(add_one, square, double)
        >>> piped(2)  # double(square(add_one(2))) = ((2 + 1)²) * 2 = 18
        18
        
    Note:
        - Returns the identity function if no functions are provided
        - The first function can take multiple arguments, but subsequent functions
          must take a single argument (the result of the previous function)
    """
    def _pipe(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: g(f(*args, **kwargs))
    
    if not funcs:
        return lambda x: x
    
    return functools.reduce(_pipe, funcs)

def demonstrate_basic_composition() -> None:
    """
    Demonstrate basic function composition and piping with practical examples.
    
    This function shows how to use compose and pipe with various types of functions,
    including mathematical operations, string manipulations, and more complex
    transformations. It also demonstrates the difference between compose (right-to-left)
    and pipe (left-to-right) operations.
    
    Examples include:
    - Mathematical function composition
    - String processing pipelines
    - Multiple function composition
    - Comparison between compose and pipe
    """
    # Basic functions
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x ** 2
    
    # Compose two functions
    add_one_then_double = compose_two(double, add_one)
    print(f"add_one_then_double(3) = {add_one_then_double(3)}")  # (3 + 1) * 2 = 8
    
    # Compose multiple functions right to left
    composed = compose(square, double, add_one)
    print(f"compose(square, double, add_one)(3) = {composed(3)}")  # square(double(add_one(3))) = 64
    
    # Pipe functions left to right
    piped = pipe(add_one, double, square)
    print(f"pipe(add_one, double, square)(3) = {piped(3)}")  # square(double(add_one(3))) = 64
    
    # More complex example with string operations
    to_uppercase = lambda s: s.upper()
    exclaim = lambda s: s + "!"
    repeat = lambda s: s * 3
    
    # Compose string operations
    process_string = compose(exclaim, to_uppercase, repeat)
    print(f"process_string('hello') = {process_string('hello')}")  # 'HELLOHELLOHELLO!'
    
    # Pipe string operations
    process_string_pipe = pipe(repeat, to_uppercase, exclaim)
    print(f"process_string_pipe('hello') = {process_string_pipe('hello')}")  # 'HELLOHELLOHELLO!'

if __name__ == "__main__":
    import functools  # For reduce
    
    print("=== Basic Function Composition ===")
    demonstrate_basic_composition()
    
    print("\n=== Key Takeaways ===")
    print("1. Function composition combines functions to create new functions")
    print("2. compose(f, g)(x) = f(g(x)) - functions are applied right to left")
    print("3. pipe(f, g)(x) = g(f(x)) - functions are applied left to right")
    print("4. Composition allows creating complex behavior from simple functions")
    print("5. The identity function is the neutral element of composition")
