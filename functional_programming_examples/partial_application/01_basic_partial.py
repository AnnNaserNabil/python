"""
1. Basic Partial Application

This module demonstrates the fundamentals of partial function application in Python.
Partial application allows us to fix a certain number of arguments of a function
and generate a new function with reduced arity.
"""
from functools import partial
from typing import Any, Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def demonstrate() -> None:
    """Demonstrate basic partial application."""
    print("=== Basic Partial Application ===\n")
    
    # 1. Basic partial application with functools.partial
    print("1. Using functools.partial:")
    
    def greet(greeting: str, name: str) -> str:
        return f"{greeting}, {name}!"
    
    # Create a new function with the first argument fixed
    say_hello = partial(greet, "Hello")
    print(f"say_hello('Alice'): {say_hello('Alice')}")
    print(f"say_hello('Bob'): {say_hello('Bob')}")
    
    # Fixing a different argument using keyword arguments
    greet_alice = partial(greet, name="Alice")
    print(f"greet_alice('Hi'): {greet_alice('Hi')}")
    print(f"greet_alice('Hey'): {greet_alice('Hey')}")
    
    # 2. Manual partial application
    print("\n2. Manual partial application:")
    
    def add(x: int, y: int) -> int:
        return x + y
    
    def manual_partial(f: Callable[..., T], *args: Any, **kwargs: Any) -> Callable[..., T]:
        """Manually implement partial application."""
        def wrapped(*more_args: Any, **more_kwargs: Any) -> T:
            all_args = args + more_args
            all_kwargs = {**kwargs, **more_kwargs}
            return f(*all_args, **all_kwargs)
        return wrapped
    
    add_five = manual_partial(add, 5)
    print(f"add_five(3): {add_five(3)}  # 5 + 3 = 8")
    print(f"add_five(7): {add_five(7)}  # 5 + 7 = 12")
    
    # 3. Partial application with multiple arguments
    print("\n3. Multiple argument partial application:")
    
    def power(base: float, exponent: float) -> float:
        return base ** exponent
    
    # Create specialized functions
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"square(5): {square(5)}  # 5^2 = 25")
    print(f"cube(3): {cube(3)}  # 3^3 = 27")
    
    # 4. Partial with keyword arguments
    print("\n4. Partial with keyword arguments:")
    
    def format_name(first: str, last: str, title: str = "") -> str:
        if title:
            return f"{title}. {first} {last}"
        return f"{first} {last}"
    
    format_dr = partial(format_name, title="Dr")
    format_mr = partial(format_name, title="Mr")
    
    print(f"format_dr('Alice', 'Smith'): {format_dr('Alice', 'Smith')}")
    print(f"format_mr('John', 'Doe'): {format_mr('John', 'Doe')}")
    
    # 5. Using lambda for partial application
    print("\n5. Using lambda for partial application:")
    
    multiply = lambda x, y: x * y
    double = lambda x: multiply(2, x)
    triple = lambda x: multiply(3, x)
    
    print(f"double(4): {double(4)}  # 2 * 4 = 8")
    print(f"triple(4): {triple(4)}  # 3 * 4 = 12")
    
    # 6. Currying vs partial application
    print("\n6. Currying vs partial application:")
    
    # Curried add function (returns functions until all args are provided)
    def curried_add(x: int) -> Callable[[int], int]:
        def add_y(y: int) -> int:
            return x + y
        return add_y
    
    # Partial application of a regular function
    add_five_partial = partial(add, 5)
    add_five_curried = curried_add(5)
    
    print(f"add_five_partial(3): {add_five_partial(3)}  # 5 + 3 = 8")
    print(f"add_five_curried(3): {add_five_curried(3)}  # 5 + 3 = 8")
    
    # 7. Practical example: Processing data
    print("\n7. Practical example: Processing data:")
    
    def process_data(data: list[float], factor: float, offset: float) -> list[float]:
        return [x * factor + offset for x in data]
    
    # Create specialized processors
    normalize = partial(process_data, factor=1.0/255, offset=0.0)
    denormalize = partial(process_data, factor=255.0, offset=0.0)
    
    data = [0, 64, 128, 192, 255]
    print(f"Original data: {data}")
    normalized = normalize(data)
    print(f"Normalized: {[f'{x:.2f}' for x in normalized]}")
    denormalized = denormalize(normalized)
    print(f"Denormalized: {[round(x) for x in denormalized]}")

if __name__ == "__main__":
    demonstrate()
