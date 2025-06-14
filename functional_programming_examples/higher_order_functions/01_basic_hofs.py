"""
1. Basic Higher-Order Functions (HOFs)

This module introduces the fundamental concept of higher-order functions in Python.
A higher-order function is a function that either:
1. Takes one or more functions as arguments, or
2. Returns a function as its result

Key concepts covered:
- Functions as first-class objects
- Passing functions as arguments to other functions
- Returning functions from functions (function factories)
- Built-in higher-order functions (map, filter, reduce)
- Function composition

Why use HOFs?
- Enables more abstract and declarative programming
- Promotes code reuse and modularity
- Makes code more concise and readable
- Facilitates function composition and chaining
"""
from typing import TypeVar, Callable, List, Any, Tuple, Dict, Iterator
from functools import reduce
import operator

T = TypeVar('T')
U = TypeVar('U')

# 1. Functions as first-class objects
def greet(name: str) -> str:
    """A simple greeting function."""
    return f"Hello, {name}!"

def demonstrate_first_class() -> None:
    """
    Demonstrate that functions are first-class objects in Python.
    
    In Python, functions are first-class objects, which means they can be:
    - Assigned to variables
    - Stored in data structures (lists, dictionaries, etc.)
    - Passed as arguments to other functions
    - Returned from other functions
    
    This function shows practical examples of these capabilities.
    """
    # Assign function to a variable
    say_hello = greet
    print(say_hello("Alice"))  # Output: Hello, Alice!
    
    # Store functions in a list
    functions = [greet, str.upper, str.lower]
    for func in functions:
        print(func("Functional Programming"))
    
    # Functions can be dictionary values
    func_dict = {
        'greet': greet,
        'length': len,
        'type': type
    }
    print(func_dict['greet']("Bob"))  # Output: Hello, Bob!
    print(func_dict['length']("Python"))  # Output: 6

# 2. Passing functions as arguments
def apply_twice(func: Callable[[T], T], value: T) -> T:
    """
    Apply a function to a value twice.
    
    This is a simple example of a higher-order function that takes another
    function as an argument and applies it twice to the input value.
    
    Args:
        func: A function that takes one argument and returns a value of the same type
        value: The initial value to apply the function to
        
    Returns:
        The result of applying the function twice to the input value
        
    Example:
        >>> apply_twice(lambda x: x * 2, 2)  # Returns 8 (2 * 2 * 2)
    """
    return func(func(value))

def square(x: int) -> int:
    """Return the square of a number."""
    return x * x

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]

# 3. Returning functions from functions
def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a function that multiplies by the given factor."""
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier

def create_greeting(greeting: str) -> Callable[[str], str]:
    """Return a greeting function with the specified greeting."""
    def greet_name(name: str) -> str:
        return f"{greeting}, {name}!"
    return greet_name

# 4. Built-in higher-order functions
def demonstrate_builtin_hofs() -> None:
    """Show examples of built-in higher-order functions."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    
    # map: apply a function to each item in an iterable
    squares = list(map(square, numbers))
    print(f"Squares: {squares}")
    
    # filter: keep items where the function returns True
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Even numbers: {evens}")
    
    # reduce: apply a function of two arguments cumulatively
    product = reduce(operator.mul, numbers, 1)
    print(f"Product of numbers: {product}")
    
    # sorted with a key function
    sorted_names = sorted(names, key=len)
    print(f"Names sorted by length: {sorted_names}")
    
    # any and all with a predicate
    has_long_name = any(len(name) > 5 for name in names)
    print(f"Has name longer than 5 chars: {has_long_name}")

# 5. Function composition
def compose(*funcs: Callable) -> Callable:
    """Compose functions from right to left."""
    def _compose(f, g):
        return lambda x: f(g(x))
    return reduce(_compose, funcs, lambda x: x)

def add_one(x: int) -> int:
    """Add one to a number."""
    return x + 1

def double(x: int) -> int:
    """Double a number."""
    return x * 2

def demonstrate_composition() -> None:
    """Show function composition in action."""
    # Compose add_one and double (double then add_one)
    add_one_then_double = compose(double, add_one)
    print(f"add_one_then_double(5) = {add_one_then_double(5)}")  # (5 + 1) * 2 = 12
    
    # Compose multiple functions
    func = compose(str, add_one, double, add_one)
    print(f"Composed function(3) = {func(3)}")  # str(add_one(double(add_one(3))))

def main() -> None:
    """Demonstrate basic higher-order functions."""
    print("=== Functions as First-Class Objects ===")
    demonstrate_first_class()
    
    print("\n=== Passing Functions as Arguments ===")
    print(f"Square of 5: {apply_twice(square, 5)}")  # (5^2)^2 = 625
    print(f"Reverse twice: {apply_twice(reverse_string, 'hello')}")  # olleh -> hello
    
    print("\n=== Returning Functions ===")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"Double of 7: {double(7)}")
    print(f"Triple of 7: {triple(7)}")
    
    say_hi = create_greeting("Hi")
    say_hola = create_greeting("Hola")
    print(say_hi("Alice"))
    print(say_hola("Bob"))
    
    print("\n=== Built-in Higher-Order Functions ===")
    demonstrate_builtin_hofs()
    
    print("\n=== Function Composition ===")
    demonstrate_composition()
    
    print("\n=== Key Takeaways ===")
    print("1. Functions are first-class objects in Python")
    print("2. Higher-order functions take functions as arguments or return them")
    print("3. Built-in functions like map, filter, and reduce are powerful tools")
    print("4. Function composition allows creating complex behavior from simple functions")
    print("5. Use lambda for simple anonymous functions, but prefer named functions for clarity")

if __name__ == "__main__":
    main()
