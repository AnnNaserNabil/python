"""
7. Partial Application and Currying

Partial Application:
Creating a new function by fixing some number of arguments to a function.

Currying:
Transforming a function that takes multiple arguments into a sequence of functions
that each take a single argument.
"""

from functools import partial
from typing import Callable, TypeVar, Any

T = TypeVar('T')
R = TypeVar('R')

def curry(func: Callable[..., R]) -> Callable[..., R]:
    """
    A decorator that transforms a function into a curried function.
    The curried function can take arguments one at a time.
    """
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return (lambda *more_args, **more_kwargs: 
                curried(*args + more_args, **{**kwargs, **more_kwargs}))
    return curried

# Example 1: Partial application with functools.partial
def power(base: float, exponent: float) -> float:
    return base ** exponent

# Create new functions using partial application
square = partial(power, exponent=2)
cube = partial(power, exponent=3)
square_root = partial(power, exponent=0.5)

# Example 2: Curried function using our decorator
@curry
def add(a: int, b: int) -> int:
    return a + b

# Example 3: Curried function with multiple arguments
@curry
def greet(greeting: str, name: str, punctuation: str = '!') -> str:
    return f"{greeting}, {name}{punctuation}"

# Example 4: Using currying with map
@curry
def map_curried(func: Callable[[T], R], items: list[T]) -> list[R]:
    return [func(item) for item in items]

# Example 5: Function composition with currying
@curry
def compose(f: Callable[[R], Any], g: Callable[[T], R], x: T) -> Any:
    return f(g(x))

def double(x: int) -> int:
    return x * 2

def increment(x: int) -> int:
    return x + 1

# Testing the functions
if __name__ == "__main__":
    print("Partial Application Examples:")
    print(f"square(5) = {square(5)}")
    print(f"cube(3) = {cube(3)}")
    print(f"square_root(16) = {square_root(16)}")
    
    # Using partial with different arguments
    power_of_2 = partial(power, 2)  # Fix base=2
    print(f"power_of_2(3) = {power_of_2(3)} (2^3)")
    print(f"power_of_2(4) = {power_of_2(4)} (2^4)")
    
    print("\nCurrying Examples:")
    # Using the curried add function
    add_five = add(5)  # Returns a new function that adds 5 to its argument
    print(f"add_five(3) = {add_five(3)}")
    print(f"add(5)(3) = {add(5)(3)}")
    
    # Using the curried greet function
    hello = greet("Hello")  # Fix greeting="Hello"
    hello_john = hello("John")  # Fix name="John"
    print(hello_john)  # Hello, John!
    
    # Change punctuation
    print(hello("John")("?"))  # Hello, John?
    
    # All at once
    print(greet("Hi")("Alice")("."))  # Hi, Alice.
    
    print("\nCurrying with map:")
    # Using the curried map function
    numbers = [1, 2, 3, 4, 5]
    double_all = map_curried(double)
    print(f"double_all({numbers}) = {double_all(numbers)}")
    
    # Using composition with currying
    print("\nFunction Composition with Currying:")
    # Compose increment and double: increment(double(x))
    increment_after_double = compose(increment)(double)
    print(f"increment_after_double(5) = {increment_after_double(5)}")
    
    # Create a function that adds 1, then doubles, then adds 1 again
    complex_operation = compose(double, compose(increment, double))
    print(f"complex_operation(5) = {complex_operation(5)}")
    
    # Practical example: Processing a list of numbers
    print("\nProcessing a list with curried functions:")
    process = compose(list, map_curried(compose(increment, double)))
    print(f"process({numbers}) = {process(numbers)}")
    
    # Another example: Formatting numbers
    @curry
    def format_number(fmt: str, number: float) -> str:
        return fmt.format(number)
    
    format_currency = format_number("${:,.2f}")
    format_percent = format_number("{:.1%}")
    
    print(f"format_currency(1234.567) = {format_currency(1234.567)}")
    print(f"format_percent(0.123) = {format_percent(0.123)}")
    
    # Currying with keyword arguments
    @curry
    def create_person(name: str, age: int, city: str) -> dict:
        return {"name": name, "age": age, "city": city}
    
    create_from_london = create_person(city="London")
    alice = create_from_london("Alice")(30)
    print(f"\nCreated person: {alice}")
    
    # You can also fix arguments in any order
    thirty_years_old = create_person(age=30)
    bob = thirty_years_old("Bob")("Paris")
    print(f"Another person: {bob}")
