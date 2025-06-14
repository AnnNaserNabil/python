"""
4. Operator Composition

Demonstrates how to compose Python's operator module functions
with function composition to create concise and expressive code.
"""
from __future__ import annotations
from typing import Callable, TypeVar, Any, Tuple, List, Dict
from functools import partial, reduce
import operator
from operator import itemgetter, attrgetter, methodcaller

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Compose functions from right to left."""
    def _compose(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return reduce(_compose, funcs, lambda x: x)

def pipe(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Pipe functions from left to right."""
    def _pipe(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: g(f(*args, **kwargs))
    return reduce(_pipe, funcs, lambda x: x)

def demonstrate_basic_operators() -> None:
    """Demonstrate basic operator composition."""
    # Basic arithmetic
    add_five = partial(operator.add, 5)
    multiply_by_three = partial(operator.mul, 3)
    
    # Compose operations
    transform = compose(
        multiply_by_three,
        add_five
    )
    
    print(f"transform(10) = {transform(10)}")  # (10 + 5) * 3 = 45
    
    # Comparison operators
    is_positive = partial(operator.lt, 0)  # 0 < x
    is_even = lambda x: x % 2 == 0
    
    # Combine with logical operators
    from functools import partial
    both = lambda f, g: lambda x: f(x) and g(x)
    
    is_positive_even = both(is_positive, is_even)
    print(f"is_positive_even(4) = {is_positive_even(4)}")
    print(f"is_positive_even(3) = {is_positive_even(3)}")
    print(f"is_positive_even(-2) = {is_positive_even(-2)}")

def demonstrate_itemgetter() -> None:
    """Demonstrate itemgetter in composition."""
    data = [
        {"name": "Alice", "age": 30, "scores": [85, 90, 78]},
        {"name": "Bob", "age": 25, "scores": [70, 65, 80]},
        {"name": "Charlie", "age": 35, "scores": [90, 92, 88]}
    ]
    
    # Get names
    get_name = itemgetter("name")
    names = list(map(get_name, data))
    print(f"Names: {names}")
    
    # Get average score for each person
    get_scores = itemgetter("scores")
    get_average = lambda scores: sum(scores) / len(scores)
    
    # Compose to get average score
    get_avg_score = compose(get_average, get_scores)
    avg_scores = list(map(get_avg_score, data))
    print(f"Average scores: {avg_scores}")
    
    # Sort by age
    get_age = itemgetter("age")
    sorted_by_age = sorted(data, key=get_age)
    print(f"Sorted by age: {[get_name(p) for p in sorted_by_age]}")
    
    # Sort by average score (descending)
    sorted_by_score = sorted(data, key=compose(get_average, get_scores), reverse=True)
    print(f"Sorted by average score: {[get_name(p) for p in sorted_by_score]}")

def demonstrate_attrgetter() -> None:
    """Demonstrate attrgetter in composition."""
    from collections import namedtuple
    
    # Define a simple class
    Person = namedtuple('Person', ['name', 'age', 'address'])
    Address = namedtuple('Address', ['street', 'city', 'zipcode'])
    
    # Create some data
    people = [
        Person("Alice", 30, Address("123 Main St", "Springfield", "12345")),
        Person("Bob", 25, Address("456 Oak Ave", "Shelbyville", "54321")),
        Person("Charlie", 35, Address("789 Pine Rd", "Springfield", "12345"))
    ]
    
    # Get names
    get_name = attrgetter("name")
    names = list(map(get_name, people))
    print(f"Names: {names}")
    
    # Get cities using nested attribute access
    get_city = attrgetter("address.city")
    cities = list(map(get_city, people))
    print(f"Cities: {cities}")
    
    # Group people by city
    from itertools import groupby
    
    # Sort by city first (required for groupby)
    people_sorted = sorted(people, key=get_city)
    
    # Group by city
    for city, group in groupby(people_sorted, key=get_city):
        group_people = list(group)
        print(f"\nPeople in {city}:")
        for person in group_people:
            print(f"  - {person.name} ({person.age})")

def demonstrate_methodcaller() -> None:
    """Demonstrate methodcaller in composition."""
    # Sample data
    strings = ["hello", "world", "functional", "programming", "in", "python"]
    
    # Create method callers
    upper = methodcaller("upper")
    count_l = methodcaller("count", "l")
    
    # Count 'l's in each string (case insensitive)
    l_counts = list(map(compose(count_l, upper), strings))
    print(f"'l' counts: {l_counts}")
    
    # More complex: filter strings with more than one 'l' (case insensitive)
    has_multiple_ls = compose(
        partial(operator.lt, 1),  # count > 1
        count_l,
        upper
    )
    
    filtered = list(filter(has_multiple_ls, strings))
    print(f"Strings with multiple 'l's: {filtered}")

def demonstrate_operator_chaining() -> None:
    """Demonstrate operator chaining with function composition."""
    # Define some operations
    add = operator.add
    mul = operator.mul
    sub = operator.sub
    
    # Compose mathematical operations
    # f(x) = (x + 5) * 3 - 2
    f = compose(
        partial(sub, 2),     # subtract 2
        partial(mul, 3),     # multiply by 3
        partial(add, 5)      # add 5
    )
    
    print("\nMathematical function composition:")
    for x in range(1, 6):
        print(f"f({x}) = {f(x)}")
    
    # Boolean operations
    is_positive = partial(operator.lt, 0)  # 0 < x
    is_even = lambda x: x % 2 == 0
    
    # Combine with logical operators
    from functools import partial
    
    # Create logical operators as functions
    AND = lambda f, g: lambda x: f(x) and g(x)
    OR = lambda f, g: lambda x: f(x) or g(x)
    NOT = lambda f: lambda x: not f(x)
    
    # Combine predicates
    is_positive_even = AND(is_positive, is_even)
    is_odd_or_negative = OR(NOT(is_even), NOT(is_positive))
    
    print("\nLogical function composition:")
    for x in [-3, -2, -1, 0, 1, 2, 3, 4]:
        print(f"{x}: pos_even={is_positive_even(x)}, odd_or_neg={is_odd_or_negative(x)}")

if __name__ == "__main__":
    print("=== Operator Composition ===")
    
    print("\n--- Basic Operators ---")
    demonstrate_basic_operators()
    
    print("\n--- Itemgetter ---")
    demonstrate_itemgetter()
    
    print("\n--- Attrgetter ---")
    demonstrate_attrgetter()
    
    print("\n--- Methodcaller ---")
    demonstrate_methodcaller()
    
    print("\n--- Operator Chaining ---")
    demonstrate_operator_chaining()
    
    print("\n=== Key Takeaways ===")
    print("1. Python's operator module provides function versions of operators")
    print("2. itemgetter, attrgetter, and methodcaller are powerful tools for data access")
    print("3. Operators can be composed to create complex transformations")
    print("4. Function composition makes operator chaining more readable")
    print("5. These techniques are particularly useful for data processing pipelines")
