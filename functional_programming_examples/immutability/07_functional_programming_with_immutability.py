"""
7. Functional Programming with Immutability

How to write functional code using immutable data structures.
- Map, filter, reduce with immutability
- Function composition
- Recursive algorithms
- Lazy evaluation
"""
from typing import TypeVar, Callable, List, Iterator, Any, Sequence, Tuple, Dict
from functools import reduce
from dataclasses import dataclass, replace
from collections.abc import Iterable

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')
V = TypeVar('V')

# 1. Basic functional operations with immutability
def map_immutable(func: Callable[[T], U], items: Sequence[T]) -> Tuple[U, ...]:
    """Apply a function to each item in the sequence immutably."""
    return tuple(func(item) for item in items)

def filter_immutable(predicate: Callable[[T], bool], items: Sequence[T]) -> Tuple[T, ...]:
    """Filter items in the sequence immutably."""
    return tuple(item for item in items if predicate(item))

def reduce_immutable(func: Callable[[U, T], U], items: Sequence[T], initial: U) -> U:
    """Reduce a sequence immutably."""
    return reduce(func, items, initial)

# 2. Function composition with immutability
def compose(*funcs: Callable) -> Callable:
    """Compose functions from right to left."""
    def _compose(f, g):
        return lambda x: f(g(x))
    return reduce(_compose, funcs, lambda x: x)

def pipe(value: T, *funcs: Callable) -> Any:
    """Pipe a value through a series of functions."""
    return reduce(lambda x, f: f(x), funcs, value)

# 3. Immutable data transformations
@dataclass(frozen=True)
class Person:
    name: str
    age: int
    email: str

def process_people(people: Sequence[Person]) -> Tuple[Dict[str, int], ...]:
    """
    Process a list of people immutably.
    Returns a tuple of dicts with name and age category.
    """
    def get_age_category(age: int) -> str:
        if age < 18:
            return "minor"
        elif age < 65:
            return "adult"
        else:
            return "senior"
    
    return tuple(
        {"name": person.name, "age_category": get_age_category(person.age)}
        for person in people
    )

# 4. Recursive algorithms with immutability
def quicksort(items: Sequence[T]) -> Tuple[T, ...]:
    """Sort a sequence immutably using quicksort."""
    if len(items) <= 1:
        return tuple(items)
    
    pivot = items[0]
    less = tuple(x for x in items[1:] if x <= pivot)
    greater = tuple(x for x in items[1:] if x > pivot)
    
    return quicksort(less) + (pivot,) + quicksort(greater)

# 5. Lazy evaluation with generators
def fibonacci() -> Iterator[int]:
    """Generate an infinite sequence of Fibonacci numbers."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def take(n: int, iterable: Iterable[T]) -> Tuple[T, ...]:
    """Take the first n items from an iterable."""
    return tuple(x for _, x in zip(range(n), iterable))

# 6. Immutable data transformations with function chaining
class ImmutableStream(Sequence[T]):
    """A sequence that supports functional-style operations with immutability."""
    
    def __init__(self, items: Sequence[T] = ()):
        self._items = tuple(items)
    
    def __getitem__(self, index: int) -> T:
        return self._items[index]
    
    def __len__(self) -> int:
        return len(self._items)
    
    def map(self, func: Callable[[T], U]) -> 'ImmutableStream[U]':
        """Apply a function to each element."""
        return ImmutableStream(func(x) for x in self._items)
    
    def filter(self, predicate: Callable[[T], bool]) -> 'ImmutableStream[T]':
        """Filter elements based on a predicate."""
        return ImmutableStream(x for x in self._items if predicate(x))
    
    def reduce(self, func: Callable[[U, T], U], initial: U) -> U:
        """Reduce the sequence to a single value."""
        return reduce(func, self._items, initial)
    
    def flat_map(self, func: Callable[[T], Iterable[U]]) -> 'ImmutableStream[U]':
        """Apply a function that returns iterables and flatten the result."""
        return ImmutableStream(
            item
            for sublist in (func(x) for x in self._items)
            for item in sublist
        )
    
    def to_list(self) -> Tuple[T, ...]:
        """Convert to an immutable tuple."""
        return self._items
    
    def __repr__(self) -> str:
        return f"ImmutableStream({list(self._items)})"

def demonstrate_functional_immutability() -> None:
    """Show examples of functional programming with immutability."""
    # 1. Basic operations
    numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    
    # Map and filter
    squares = map_immutable(lambda x: x * x, numbers)
    evens = filter_immutable(lambda x: x % 2 == 0, numbers)
    sum_squares = reduce_immutable(lambda x, y: x + y, squares, 0)
    
    print(f"Numbers: {numbers}")
    print(f"Squares: {squares}")
    print(f"Evens: {evens}")
    print(f"Sum of squares: {sum_squares}")
    
    # 2. Function composition
    add_five = lambda x: x + 5
    square = lambda x: x * x
    
    composed = compose(str, add_five, square)
    result = composed(3)  # (3^2) + 5 = 14
    print(f"\nComposed function (square then add_five then str): {result}")
    
    # 3. Processing people
    people = (
        Person("Alice", 25, "alice@example.com"),
        Person("Bob", 17, "bob@example.com"),
        Person("Charlie", 70, "charlie@example.com"),
    )
    
    processed = process_people(people)
    print("\nProcessed people:")
    for person in processed:
        print(f"  - {person['name']}: {person['age_category']}")
    
    # 4. Quicksort
    unsorted = (3, 6, 8, 10, 1, 2, 1)
    sorted_nums = quicksort(unsorted)
    print(f"\nQuicksort: {unsorted} -> {sorted_nums}")
    
    # 5. Lazy evaluation
    fibs = take(10, fibonacci())
    print(f"\nFirst 10 Fibonacci numbers: {fibs}")
    
    # 6. ImmutableStream
    stream = ImmutableStream(range(1, 6))  # 1, 2, 3, 4, 5
    result = (
        stream
        .map(lambda x: x * 2)      # 2, 4, 6, 8, 10
        .filter(lambda x: x > 5)    # 6, 8, 10
        .reduce(lambda x, y: x + y, 0)  # 24
    )
    print(f"\nImmutableStream result: {result}")

# Example usage
if __name__ == "__main__":
    demonstrate_functional_immutability()
    
    print("\n=== Key Takeaways ===")
    print("1. Use tuples and frozen dataclasses for immutable data")
    print("2. Prefer map/filter/reduce over loops for transformations")
    print("3. Compose small, pure functions to build complex behavior")
    print("4. Use generators for lazy evaluation of sequences")
    print("5. Consider using libraries like 'toolz' or 'fn.py' for more functional utilities")
