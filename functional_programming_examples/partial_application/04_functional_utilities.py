"""
4. Functional Utilities with Partial Application

This module demonstrates how to build functional utilities using partial application,
including function composition, currying, and point-free programming.
"""
from functools import partial, reduce
from typing import Any, Callable, TypeVar, List, Dict, Tuple, Sequence, cast
from operator import add, mul, attrgetter, itemgetter, methodcaller

# Type variables for better type hints
T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')
W = TypeVar('W')

# Helper functions
def identity(x: T) -> T:
    """The identity function: returns its argument unchanged."""
    return x

def constant(x: T) -> Callable[..., T]:
    """Return a function that always returns the same value."""
    return lambda *_, **__: x

def flip(f: Callable[..., T]) -> Callable[..., T]:
    """Flip the order of the first two arguments of a function."""
    def flipped(a: Any, b: Any, *args: Any, **kwargs: Any) -> T:
        return f(b, a, *args, **kwargs)
    return flipped

def compose(*funcs: Callable) -> Callable:
    """Compose functions from right to left."""
    def composed(*args: Any, **kwargs: Any) -> Any:
        result = funcs[-1](*args, **kwargs)
        for f in reversed(funcs[:-1]):
            result = f(result)
        return result
    return composed

def pipe(value: Any, *funcs: Callable) -> Any:
    """Pipe a value through a series of functions."""
    return compose(*funcs)(value)

# Partial application utilities
def curry(f: Callable[..., T]) -> Callable[..., Any]:
    """Convert a function to a curried function."""
    def curried(*args: Any, **kwargs: Any) -> Any:
        if len(args) + len(kwargs) >= f.__code__.co_argcount:
            return f(*args, **kwargs)
        return lambda *more_args, **more_kwargs: curried(
            *args, *more_args, **{**kwargs, **more_kwargs}
        )
    return curried

def uncurry(f: Callable) -> Callable[..., Any]:
    """Convert a curried function to take multiple arguments."""
    def uncurried(*args: Any, **kwargs: Any) -> Any:
        result = f
        for arg in args:
            result = result(arg)
        return result
    return uncurried

def partial_application_demo() -> None:
    """Demonstrate partial application with functional utilities."""
    print("=== Functional Utilities with Partial Application ===\n")
    
    # 1. Basic function composition
    print("1. Function composition:")
    
    # Define some simple functions
    add_one = partial(add, 1)
    double = partial(mul, 2)
    square = lambda x: x * x
    
    # Compose functions
    add_one_then_double = compose(double, add_one)
    add_one_then_double_then_square = compose(square, add_one_then_double)
    
    print(f"add_one_then_double(3): {add_one_then_double(3)}")
    print(f"add_one_then_double_then_square(3): {add_one_then_double_then_square(3)}")
    
    # 2. Using pipe for readable function chaining
    print("\n2. Using pipe for readable chaining:")
    
    result = pipe(
        3,
        lambda x: x + 1,  # 4
        lambda x: x * 2,  # 8
        lambda x: x ** 2, # 64
        str,              # "64"
        lambda s: f"Result: {s}"
    )
    print(f"pipe result: {result}")
    
    # 3. Currying and partial application
    print("\n3. Currying and partial application:")
    
    # A simple function that takes three arguments
    def greet(greeting: str, name: str, punctuation: str) -> str:
        return f"{greeting}, {name}{punctuation}"
    
    # Curry the function
    curried_greet = curry(greet)
    
    # Create specialized versions
    say_hello = curried_greet("Hello")
    say_hi = curried_greet("Hi")
    
    print(f"say_hello('Alice')('!'): {say_hello('Alice')('!')}")
    print(f"say_hi('Bob')('!!!'): {say_hi('Bob')('!!!')}")
    
    # 4. Point-free programming
    print("\n4. Point-free programming:")
    
    # Define data
    people = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "New York"},
    ]
    
    # Point-free style with operator module
    get_name = itemgetter("name")
    get_age = itemgetter("age")
    get_city = itemgetter("city")
    
    # Create point-free functions
    is_from_ny = compose(partial(eq, "New York"), get_city)
    get_adult_age = compose(str, get_age)
    format_person = lambda p: f"{get_name(p)} ({get_age(p)})"
    
    # Process data in a point-free style
    new_yorkers = filter(is_from_ny, people)
    formatted = map(format_person, new_yorkers)
    
    print("New York residents:", list(formatted))
    
    # 5. Function composition with multiple arguments
    print("\n5. Function composition with multiple arguments:")
    
    def add(a: int, b: int) -> int:
        return a + b
    
    def multiply(a: int, b: int) -> int:
        return a * b
    
    # Create a function that adds 1 to its argument and then multiplies by 2
    add1_times2 = compose(
        partial(multiply, 2),  # Takes one argument, multiplies by 2
        partial(add, 1)        # Takes one argument, adds 1
    )
    
    print(f"add1_times2(3): {add1_times2(3)}  # (3 + 1) * 2 = 8")
    
    # 6. Function composition with keyword arguments
    print("\n6. Function composition with keyword arguments:")
    
    def greet2(name: str, *, greeting: str = "Hello", punctuation: str = "!") -> str:
        return f"{greeting}, {name}{punctuation}"
    
    # Create a specialized greeter
    greet_formally = partial(greet2, greeting="Good day", punctuation=".")
    greet_excitedly = partial(greet2, punctuation="!!!")
    
    print(f"greet_formally('Alice'): {greet_formally('Alice')}")
    print(f"greet_excitedly('Bob'): {greet_excitedly('Bob')}")
    
    # 7. Practical example: Data processing pipeline
    print("\n7. Practical example: Data processing pipeline")
    
    # Sample data
    orders = [
        {"id": 1, "customer": "Alice", "amount": 100, "status": "completed"},
        {"id": 2, "customer": "Bob", "amount": 200, "status": "pending"},
        {"id": 3, "customer": "Alice", "amount": 150, "status": "completed"},
        {"id": 4, "customer": "Charlie", "amount": 300, "status": "shipped"},
        {"id": 5, "customer": "Bob", "amount": 50, "status": "completed"},
    ]
    
    # Helper functions
    get_amount = itemgetter("amount")
    get_status = itemgetter("status")
    get_customer = itemgetter("customer")
    
    # Predicates
    is_completed = compose(partial(eq, "completed"), get_status)
    is_customer = lambda name: compose(partial(eq, name), get_customer)
    
    # Transformations
    format_order = lambda order: f"{get_customer(order)}: ${get_amount(order)}"
    
    # Pipeline
    def process_orders(orders: List[Dict], customer: str) -> List[str]:
        return pipe(
            orders,
            partial(filter, is_completed),
            partial(filter, is_customer(customer)),
            partial(sorted, key=get_amount, reverse=True),
            partial(map, format_order)
        )
    
    # Process orders
    alice_orders = process_orders(orders, "Alice")
    bob_orders = process_orders(orders, "Bob")
    
    print("\nAlice's completed orders (highest first):")
    for order in alice_orders:
        print(f"- {order}")
    
    print("\nBob's completed orders (highest first):")
    for order in bob_orders:
        print(f"- {order}")
    
    # 8. Advanced: Function composition with multiple return values
    print("\n8. Function composition with multiple return values:")
    
    def split_name(full_name: str) -> Tuple[str, str]:
        first, *rest = full_name.split()
        last = rest[-1] if rest else ""
        return first, last
    
    def format_greeting(first: str, last: str) -> str:
        return f"Hello, {' '.join([first, last]).strip()}!"
    
    # Compose functions that return tuples
    def compose_with_unpack(f: Callable, g: Callable) -> Callable:
        def composed(*args: Any, **kwargs: Any) -> Any:
            return g(*f(*args, **kwargs))
        return composed
    
    greet_by_full_name = compose_with_unpack(split_name, format_greeting)
    
    print(f"greet_by_full_name('John Doe'): {greet_by_full_name('John Doe')}")
    print(f"greet_by_full_name('Alice'): {greet_by_full_name('Alice')}")

if __name__ == "__main__":
    partial_application_demo()
