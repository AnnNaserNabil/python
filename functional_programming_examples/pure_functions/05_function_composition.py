"""
5. Function Composition in Python

This module demonstrates function composition, a fundamental concept in functional programming
where the output of one function is used as the input to another. Function composition allows
building complex operations by combining simple, reusable functions.

Key Concepts:
------------
- Function Composition: Combining functions where the output of one function
  becomes the input of another (f ∘ g)(x) = f(g(x))
- Pure Functions: All functions are pure - they have no side effects and always
  produce the same output for the same input
- Declarative Style: Focus on what to compute rather than how to compute it
- Higher-Order Functions: Functions that take other functions as arguments or return them

Why Use Function Composition?
---------------------------
- Encourages code reuse and modularity
- Makes code more readable and maintainable
- Enables a declarative programming style
- Facilitates function pipelining and data transformation
- Makes it easier to reason about code

Real-world Applications:
----------------------
- Data processing pipelines
- API request/response transformations
- Data validation and cleaning
- Mathematical computations
- Building domain-specific languages (DSLs)

Example:
-------
>>> add_one = lambda x: x + 1
>>> square = lambda x: x * x
>>> add_one_then_square = compose(square, add_one)
>>> add_one_then_square(5)  # (5 + 1)² = 36
36
"""
from typing import Callable, TypeVar, List

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(f: Callable[[U], V], g: Callable[[T], U]) -> Callable[[T], V]:
    """
    Compose two functions: compose(f, g)(x) = f(g(x))
    
    This is a pure higher-order function that takes two functions and returns a new function
    that is the composition of the two input functions. The resulting function applies the
    second function to its argument, then applies the first function to the result.
    
    Args:
        f: The outer function to apply second. Must accept the return type of g.
        g: The inner function to apply first. Must accept the initial input type.
        
    Returns:
        Callable[[T], V]: A new function that applies g then f to its input.
        
    Examples:
        >>> add_one = lambda x: x + 1
        >>> square = lambda x: x * x
        >>> add_one_then_square = compose(square, add_one)
        >>> add_one_then_square(5)  # (5 + 1)² = 36
        36
        
        # Can be used with built-in functions
        >>> len_then_str = compose(str, len)
        >>> len_then_str('hello')
        '5'
        
    Note:
        - The output type of g must match the input type of f
        - Both f and g should be pure functions for predictable results
        - For composing more than two functions, use the pipe() function instead
    """
    return lambda x: f(g(x))

def pipe(*funcs: Callable) -> Callable:
    """
    Create a pipeline of functions to apply in sequence (left-to-right).
    
    This is a pure higher-order function that takes any number of functions and returns
    a new function that applies each function in sequence from left to right.
    
    pipe(f, g, h)(x) = h(g(f(x)))
    
    Args:
        *funcs: Any number of functions to compose. Can be zero or more.
              Each function should accept the return type of the previous function.
              The first function can accept any input type.
              
    Returns:
        Callable: A new function that applies each function in sequence.
        
    Examples:
        >>> add_one = lambda x: x + 1
        >>> square = lambda x: x * x
        >>> double = lambda x: x * 2
        
        # Create a pipeline: x → x+1 → (x+1)² → ((x+1)²)*2
        >>> pipeline = pipe(add_one, square, double)
        >>> pipeline(3)  # ((3 + 1)²) * 2 = 32
        32
        
        # Works with any number of functions
        >>> identity = pipe()  # No functions - returns input as-is
        >>> identity(42)
        42
        
    Note:
        - The output type of each function must match the input type of the next
        - All functions should be pure for predictable results
        - For better type safety with two functions, use compose() instead
    """
    def _pipe(x):
        result = x
        for func in funcs:
            result = func(result)
        return result
    return _pipe

def apply_all(funcs: List[Callable[[T], U]], x: T) -> List[U]:
    """
    Apply a list of functions to a single value and collect all results.
    
    This is a pure function that applies each function in the input list to the
    given value and returns a list of the results in the same order as the functions.
    
    Args:
        funcs: A list of functions to apply. Can be empty.
             Each function should accept a value of type T as input.
        x: The input value to pass to each function.
        
    Returns:
        List[U]: A list containing the result of applying each function to x.
               The length of the result list matches the length of funcs.
               
    Examples:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> def double(x): return x * 2
        
        >>> results = apply_all([add_one, square, double], 3)
        >>> results  # [3+1, 3*3, 3*2] = [4, 9, 6]
        [4, 9, 6]
        
        # Works with any number of functions
        >>> apply_all([str, float, bool], 0)
        ['0', 0.0, False]
        
        # Empty function list returns empty result
        >>> apply_all([], 'test')
        []
        
    Note:
        - The input value is not modified
        - The order of results matches the order of functions in the input list
        - All functions should be pure for predictable results
        - Type hints ensure type safety between input and output types
    """
    return [f(x) for f in funcs]

# Example usage
if __name__ == "__main__":
    print("=== Function Composition Examples ===\n")
    
    # Define some simple pure functions for demonstration
    def add_one(x: int) -> int:
        """Add 1 to the input number."""
        return x + 1
        
    def square(x: int) -> int:
        """Return the square of the input number."""
        return x * x
        
    def double(x: int) -> int:
        """Double the input number."""
        return x * 2
        
    def to_upper(s: str) -> str:
        """Convert string to uppercase."""
        return s.upper()
    
    # Example 1: Basic function composition
    print("1. Basic Composition (compose function):")
    # Create a new function that first adds one, then squares the result
    add_one_then_square = compose(square, add_one)
    
    # Test with different inputs
    for num in [0, 1, 2, 3, 4]:
        result = add_one_then_square(num)
        print(f"({num} + 1)² = {result}")
    
    # Example 2: Function pipelining
    print("\n2. Function Pipelining (pipe function):")
    # Create a pipeline: x → x+1 → (x+1)² → ((x+1)²)*2
    transform = pipe(add_one, square, double)
    
    # Test the pipeline
    for num in [0, 1, 2, 3, 4]:
        result = transform(num)
        print(f"2 * ({num} + 1)² = {result}")
    
    # Example 3: Applying multiple functions to a single value
    print("\n3. Applying Multiple Functions (apply_all function):")
    # Define a list of transformation functions
    transformations = [
        str,                # Convert to string
        lambda x: x * 2,    # Double the number
        lambda x: x ** 3,   # Cube the number
        lambda x: f"X{x:03d}",  # Format with prefix and padding
        lambda x: x > 10    # Check if greater than 10
    ]
    
    # Apply all transformations to the same input
    for num in [2, 5, 8]:
        results = apply_all(transformations, num)
        print(f"\nApplying all transformations to {num}:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result} ({type(result).__name__})")
    
    # Example 4: String processing pipeline
    print("\n4. String Processing Pipeline:")
    # Define string processing functions
    def add_greeting(name: str) -> str:
        return f"Hello, {name}!"
    
    def add_emphasis(text: str) -> str:
        return f"{text.upper()}!!!"
    
    # Create a string processing pipeline
    process_name = pipe(
        str.strip,          # Remove whitespace
        str.capitalize,     # Capitalize first letter
        add_greeting,       # Add greeting
        add_emphasis        # Add emphasis
    )
    
    # Test the string pipeline
    names = ["  alice", "bob  ", "  CHARLIE  "]
    for name in names:
        result = process_name(name)
        print(f"'{name}' → '{result}'")
    
    # Verify function purity with assertions
    print("\nVerifying function purity...")
    assert add_one_then_square(0) == 1
    assert transform(0) == 2
    test_results = apply_all([add_one, square, double], 3)
    assert test_results == [4, 9, 6]
    
    print("\nAll tests passed! All functions are pure and working as expected.")
    assert add_one_then_square(1) == 4
    assert transform(2) == 18  # 2 * (2 + 1)²
    assert apply_all([], 10) == []
    assert apply_all([str, len], "hello") == ["hello", 5]
