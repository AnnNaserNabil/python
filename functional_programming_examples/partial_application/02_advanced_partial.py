"""
2. Advanced Partial Application

This module demonstrates more advanced uses of partial function application,
including composition, partial application with methods, and creating decorators.
"""
from functools import partial, wraps
from typing import Any, Callable, TypeVar, cast

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(f: Callable[[T], U], g: Callable[..., T]) -> Callable[..., U]:
    """Compose two functions: f ∘ g = f(g(...))"""
    return lambda *args, **kwargs: f(g(*args, **kwargs))

def pipe(value: T, *funcs: Callable) -> Any:
    """Pipe a value through a series of functions."""
    result = value
    for func in funcs:
        result = func(result)
    return result

def demonstrate() -> None:
    """Demonstrate advanced partial application techniques."""
    print("=== Advanced Partial Application ===\n")
    
    # 1. Function composition with partial
    print("1. Function composition:")
    
    def add(x: int, y: int) -> int:
        return x + y
    
    def square(x: int) -> int:
        return x * x
    
    # Compose square with a partially applied add
    add_then_square = compose(square, partial(add, 3))
    print(f"(3 + 2)² = {add_then_square(2)}")
    
    # Using pipe to chain operations
    result = pipe(2, partial(add, 3), square, str)
    print(f"str(square(3 + 2)) = {result}")
    
    # 2. Partial application with methods
    print("\n2. Partial application with methods:")
    
    class Multiplier:
        def __init__(self, factor: int):
            self.factor = factor
        
        def multiply(self, x: int) -> int:
            return self.factor * x
    
    # Create an instance
    doubler = Multiplier(2)
    
    # Create a partially applied method
    double = partial(Multiplier.multiply, doubler)
    print(f"double(5): {double(5)}  # 2 * 5 = 10")
    
    # 3. Creating decorators with partial
    print("\n3. Creating decorators with partial:")
    
    def repeat(n: int = 1):
        """Decorator that repeats function execution n times."""
        def decorator(func: Callable[..., T]) -> Callable[..., list[T]]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> list[T]:
                return [func(*args, **kwargs) for _ in range(n)]
            return wrapper
        return decorator
    
    # Using the decorator with partial
    repeat_twice = partial(repeat, n=2)
    
    @repeat_twice()
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    print(f"greet('Alice'): {greet('Alice')}")
    
    # 4. Partial application with keyword arguments
    print("\n4. Advanced keyword argument handling:")
    
    def create_person(name: str, age: int, city: str = "Unknown", country: str = "Unknown") -> dict:
        return {"name": name, "age": age, "city": city, "country": country}
    
    # Create specialized constructors
    create_ny_resident = partial(create_person, city="New York", country="USA")
    create_londoner = partial(create_person, city="London", country="UK")
    
    alice = create_ny_resident(name="Alice", age=30)
    bob = create_londoner(name="Bob", age=25)
    
    print(f"Alice: {alice}")
    print(f"Bob: {bob}")
    
    # 5. Partial application with mutable defaults
    print("\n5. Handling mutable defaults:")
    
    def append_to_list(item: Any, lst: list[Any] = None) -> list[Any]:
        if lst is None:
            lst = []
        lst.append(item)
        return lst
    
    # Create a partial that fixes the list
    add_to_my_list = partial(append_to_list, lst=[])
    
    # This would have unexpected behavior with mutable defaults
    print("Using partial with mutable default (problematic):")
    print(f"add_to_my_list(1): {add_to_my_list(1)}")
    print(f"add_to_my_list(2): {add_to_my_list(2)}  # Oops! Contains [1, 2]")
    
    # Better approach: use a factory function
    def create_adder() -> Callable[[Any], list[Any]]:
        lst: list[Any] = []
        return partial(append_to_list, lst=lst)
    
    adder = create_adder()
    print("\nUsing factory function (correct):")
    print(f"adder(1): {adder(1)}")
    print(f"adder(2): {adder(2)}  # Contains [1, 2]")
    
    # 6. Partial application with type hints
    print("\n6. Type hints with partial application:")
    
    from typing import TypeVar, Callable, Any
    
    T = TypeVar('T')
    
    def typed_partial(
        func: Callable[..., T], 
        *args: Any, 
        **kwargs: Any
    ) -> Callable[..., T]:
        """A typed version of functools.partial."""
        return wraps(func)(partial(func, *args, **kwargs))
    
    def power(base: float, exponent: float) -> float:
        return base ** exponent
    
    # Create typed partials
    square: Callable[[float], float] = typed_partial(power, exponent=2)
    cube: Callable[[float], float] = typed_partial(power, exponent=3)
    
    print(f"square(4): {square(4)}  # 4² = 16")
    print(f"cube(3): {cube(3)}  # 3³ = 27")
    
    # 7. Practical example: Data processing pipeline
    print("\n7. Data processing pipeline:")
    
    # Define processing steps
    def load_data(source: str) -> list[dict]:
        print(f"Loading data from {source}")
        return [
            {"name": "Alice", "score": 85, "subject": "Math"},
            {"name": "Bob", "score": 90, "subject": "Math"},
            {"name": "Charlie", "score": 78, "subject": "Science"},
        ]
    
    def filter_subject(data: list[dict], subject: str) -> list[dict]:
        return [item for item in data if item["subject"] == subject]
    
    def calculate_average(scores: list[int]) -> float:
        return sum(scores) / len(scores) if scores else 0.0
    
    # Create specialized filters
    filter_math = partial(filter_subject, subject="Math")
    filter_science = partial(filter_subject, subject="Science")
    
    # Create a processing pipeline
    def process_data(
        source: str, 
        filter_func: Callable[[list[dict]], list[dict]]
    ) -> float:
        data = load_data(source)
        filtered = filter_func(data)
        scores = [item["score"] for item in filtered]
        return calculate_average(scores)
    
    # Calculate averages
    math_avg = process_data("database.csv", filter_math)
    science_avg = process_data("database.csv", filter_science)
    
    print(f"Math average: {math_avg:.2f}")
    print(f"Science average: {science_avg:.2f}")

if __name__ == "__main__":
    demonstrate()
