"""
Functional Programming Examples - From Basic to Advanced

This file contains 10 progressively complex examples demonstrating functional programming concepts.
Each example builds upon the previous ones and includes detailed comments.
"""

# ============================================
# Example 1: Pure Functions (Basic)
# A function that always returns the same output for the same input
# and has no side effects.
# ============================================
def add(a, b):
    """
    A pure function that adds two numbers.
    - Same input always produces same output
    - No side effects
    - Doesn't modify any external state
    """
    return a + b

# ============================================
# Example 2: Immutability
# Working with immutable data structures
# ============================================
def add_to_list(items, new_item):
    """
    Returns a new list with the new item added.
    - Doesn't modify the original list (immutability)
    - Returns a new list instead
    """
    return items + [new_item]  # Creates and returns a new list

# ============================================
# Example 3: Higher-Order Functions
# Functions that take other functions as arguments or return them
# ============================================
def apply_operation(x, y, operation):
    """
    Applies the given operation to x and y.
    - Takes a function as an argument (higher-order function)
    - Returns the result of applying the operation
    """
    return operation(x, y)

def multiply(a, b):
    return a * b

# ============================================
# Example 4: Function Composition
# Combining multiple functions to create more complex behavior
# ============================================
def compose(f, g):
    """
    Returns a new function that applies g and then f.
    - Combines two functions into a new function
    - f(g(x)) is equivalent to compose(f, g)(x)
    """
    return lambda x: f(g(x))

# Example functions to compose
double = lambda x: x * 2
square = lambda x: x ** 2

# Compose the functions
double_then_square = compose(square, double)

# ============================================
# Example 5: Recursion
# Solving problems by having functions call themselves
# ============================================
def factorial(n):
    """
    Calculate factorial using recursion.
    - Base case: factorial(0) = 1
    - Recursive case: n * factorial(n-1)
    """
    return 1 if n == 0 else n * factorial(n - 1)

# ============================================
# Example 6: Closures
# Functions that remember values in their enclosing scope
# ============================================
def make_multiplier(factor):
    """
    Returns a function that multiplies by the given factor.
    - The inner function 'multiplier' remembers the 'factor' value
    - This is a closure
    """
    def multiplier(x):
        return x * factor
    return multiplier

# Create specialized multiplier functions
double = make_multiplier(2)
triple = make_multiplier(3)

# ============================================
# Example 7: Map, Filter, Reduce
# Common higher-order functions for working with collections
# ============================================
from functools import reduce

def process_numbers(numbers):
    """
    Process numbers using map, filter, and reduce.
    - map: transforms each element
    - filter: keeps only elements that match a condition
    - reduce: combines all elements into a single value
    """
    # Double each number
    doubled = list(map(lambda x: x * 2, numbers))
    
    # Keep only even numbers
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    
    # Calculate product of all numbers
    product = reduce(lambda x, y: x * y, numbers, 1)
    
    return doubled, evens, product

# ============================================
# Example 8: Partial Application and Currying
# Creating specialized functions from general ones
# ============================================
from functools import partial

def power(base, exponent):
    return base ** exponent

# Create specialized versions using partial application
square_root = partial(power, exponent=0.5)
cube = partial(power, exponent=3)

def curry(f):
    """
    Converts a function that takes multiple arguments into
    a sequence of functions that each take a single argument.
    """
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= f.__code__.co_argcount:
            return f(*args, **kwargs)
        return (lambda *more_args, **more_kwargs: 
                curried(*args + more_args, **{**kwargs, **more_kwargs}))
    return curried

# Curried version of the power function
@curry
def curried_power(base, exponent):
    return base ** exponent

# ============================================
# Example 9: Memoization
# Caching function results to avoid repeated calculations
# ============================================
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    """
    Calculate the nth Fibonacci number with memoization.
    - Uses lru_cache to cache results
    - Avoids recalculating the same values multiple times
    """
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# ============================================
# Example 10: Monads (Maybe/Optional)
# Handling computations that might fail
# ============================================
from typing import TypeVar, Generic, Callable, Any, Optional

T = TypeVar('T')
U = TypeVar('U')

class Maybe(Generic[T]):
    """
    A simple Maybe monad implementation.
    Represents an optional value that might be present (Just) or not (Nothing).
    """
    def __init__(self, value: Optional[T] = None):
        self._value = value
    
    def bind(self, f: Callable[[T], 'Maybe[U]']) -> 'Maybe[U]':
        if self._value is None:
            return Maybe.nothing()
        return f(self._value)
    
    def map(self, f: Callable[[T], U]) -> 'Maybe[U]':
        if self._value is None:
            return Maybe.nothing()
        return Maybe.just(f(self._value))
    
    @classmethod
    def just(cls, value: T) -> 'Maybe[T]':
        return cls(value)
    
    @classmethod
    def nothing(cls) -> 'Maybe[Any]':
        return cls()
    
    def get_or_else(self, default: T) -> T:
        return self._value if self._value is not None else default

def safe_divide(x: float, y: float) -> Maybe[float]:
    """
    Safely divide two numbers, returning a Maybe monad.
    Returns Nothing if division by zero would occur.
    """
    if y == 0:
        return Maybe.nothing()
    return Maybe.just(x / y)

def safe_sqrt(x: float) -> Maybe[float]:
    """
    Safely calculate square root, returning a Maybe monad.
    Returns Nothing for negative numbers.
    """
    if x < 0:
        return Maybe.nothing()
    return Maybe.just(x ** 0.5)

# Example usage of the Maybe monad
result = (Maybe.just(16)
          .bind(lambda x: safe_sqrt(x))  # sqrt(16) = 4
          .bind(lambda x: safe_divide(8, x))  # 8 / 4 = 2
          .get_or_else("Error in calculation"))

# ============================================
# Running the examples
# ============================================
if __name__ == "__main__":
    print("Example 1: Pure Functions")
    print(f"add(3, 4) = {add(3, 4)}")
    
    print("\nExample 2: Immutability")
    original = [1, 2, 3]
    new_list = add_to_list(original, 4)
    print(f"Original: {original}")
    print(f"New list: {new_list}")
    
    print("\nExample 3: Higher-Order Functions")
    print(f"apply_operation(3, 4, multiply) = {apply_operation(3, 4, multiply)}")
    
    print("\nExample 4: Function Composition")
    print(f"double_then_square(3) = {double_then_square(3)}")
    
    print("\nExample 5: Recursion")
    print(f"factorial(5) = {factorial(5)}")
    
    print("\nExample 6: Closures")
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")
    
    print("\nExample 7: Map, Filter, Reduce")
    numbers = [1, 2, 3, 4, 5]
    doubled, evens, product = process_numbers(numbers)
    print(f"Original: {numbers}")
    print(f"Doubled: {doubled}")
    print(f"Evens: {evens}")
    print(f"Product: {product}")
    
    print("\nExample 8: Partial Application and Currying")
    print(f"square_root(16) = {square_root(16)}")
    print(f"cube(3) = {cube(3)}")
    print(f"curried_power(2)(3) = {curried_power(2)(3)}")
    
    print("\nExample 9: Memoization")
    print(f"fibonacci(10) = {fibonacci(10)}")
    
    print("\nExample 10: Monads (Maybe/Optional)")
    print(f"Result of safe operations: {result}")
    
    # Example of a failed computation
    failed_result = (Maybe.just(-16)
                    .bind(lambda x: safe_sqrt(x))  # Fails for negative numbers
                    .bind(lambda x: safe_divide(8, x))
                    .get_or_else("Error in calculation"))
    print(f"Failed computation result: {failed_result}")
