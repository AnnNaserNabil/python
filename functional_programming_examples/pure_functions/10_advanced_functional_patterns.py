"""
10. Advanced Functional Patterns

This module demonstrates advanced functional programming patterns using pure functions in Python.
It provides implementations of common functional programming abstractions that help write more
expressive, maintainable, and bug-resistant code.

Key Concepts:
1. Monads (Maybe, Either): Handle computations that might fail or have side effects in a pure way.
2. Function Currying: Transform multi-argument functions into chains of single-argument functions.
3. Immutable Data Structures: Persistent data structures that enable efficient updates by sharing structure.
4. Lenses: Functional references for updating nested immutable data structures.

Examples:
    >>> # Maybe monad for safe computations
    >>> safe_divide(10, 2).map(lambda x: x * 3)  # Just(15.0)
    >>> safe_divide(10, 0).map(lambda x: x * 3)  # Nothing
    
    # Either monad for error handling
    >>> result = (safe_divide_either(10, 2)
    ...           .map(lambda x: x + 3)
    ...           .bind(lambda x: safe_divide_either(x, 2)))
    >>> print(result)  # Right(4.0)
    
    # Function currying
    >>> add = lambda x, y, z: x + y + z
    >>> curried_add = curry(add)
    >>> add_five = curried_add(2)(3)
    >>> add_five(10)  # 15
    
    # Immutable list
    >>> lst = ImList([1, 2, 3]).cons(0)
    >>> print(lst)  # ImList([0, 1, 2, 3])
    
    # Lenses for nested updates
    >>> person = Person("Alice", 30)
    >>> name_upper = lens(
    ...     lambda p: p.name,
    ...     lambda p, name: Person(name, p.age)
    ... )(lambda n: n.upper())(person)
    >>> print(name_upper)  # Person(name='ALICE', age=30)
"""
from typing import TypeVar, Generic, Callable, Any, Optional, Union, Tuple, List
from dataclasses import dataclass
from functools import partial

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')

# 1. Maybe Monad (Option type)
class Maybe(Generic[T]):
    """
    The Maybe monad represents an optional value that can be either Just(value) or Nothing.
    
    This is used to handle computations that might fail or return None in a pure functional way.
    Instead of returning None or raising exceptions, we return a Maybe that can be chained.
    
    Example:
        >>> def safe_divide(x: float, y: float) -> Maybe[float]:
        ...     return Just(x / y) if y != 0 else Nothing()
        >>> 
        >>> # Safe computations that can't fail
        >>> result = (safe_divide(10, 2)  # Just(5.0)
        ...           .map(lambda x: x * 3)  # Just(15.0)
        ...           .get_or_else(0))       # 15.0
        >>>
        >>> # Safe computations that might fail
        >>> result = (safe_divide(10, 0)  # Nothing
        ...           .map(lambda x: x * 3)  # Still Nothing
        ...           .get_or_else(0))      # 0 (default value)
    """
    
    def bind(self, func: Callable[[T], 'Maybe[U]']) -> 'Maybe[U]':
        """
        Bind a function that returns a Maybe (also known as flatMap).
        
        Args:
            func: A function that takes a value and returns a Maybe
            
        Returns:
            If this is Just(x), returns func(x). If this is Nothing, returns Nothing.
        """
        raise NotImplementedError
    
    def map(self, func: Callable[[T], U]) -> 'Maybe[U]':
        """
        Apply a function to the contained value if it exists.
        
        Args:
            func: Function to apply to the contained value
            
        Returns:
            A new Maybe containing the result of applying func, or Nothing if this is Nothing.
        """
        return self.bind(lambda x: Just(func(x)))
    
    def get_or_else(self, default: T) -> T:
        """
        Get the contained value or return a default if it's Nothing.
        
        Args:
            default: Value to return if this is Nothing
            
        Returns:
            The contained value if Just, otherwise the default value.
        """
        raise NotImplementedError
    
    def is_just(self) -> bool:
        """Return True if this is a Just value."""
        return isinstance(self, Just)
    
    def is_nothing(self) -> bool:
        """Return True if this is Nothing."""
        return isinstance(self, Nothing)
    
    def __or__(self, func):
        """
        Override | operator for chaining operations.
        
        This allows using the | operator for chaining operations:
            result = maybe_value | (lambda x: Just(x + 1)) | (lambda x: Just(x * 2))
        """
        return self.bind(func)


class Just(Maybe[T]):
    """
    Represents a value that exists (the successful case of Maybe).
    
    This is used to wrap a value that was successfully computed.
    """
    
    def __init__(self, value: T):
        self.value = value
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Apply the function to the contained value."""
        return func(self.value)
    
    def get_or_else(self, default: T) -> T:
        """Return the contained value, ignoring the default."""
        return self.value
    
    def __str__(self) -> str:
        return f"Just({self.value})"

    def __eq__(self, other):
        """Two Just values are equal if their contained values are equal."""
        return isinstance(other, Just) and self.value == other.value


class Nothing(Maybe[Any]):
    """
    Represents the absence of a value (the failure case of Maybe).
    
    This is used to represent a computation that failed or returned no value.
    """
    
    _instance = None
    
    def __new__(cls):
        # Make Nothing a singleton
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def bind(self, func: Callable[[Any], Maybe[Any]]) -> 'Nothing':
        """Binding on Nothing always returns Nothing (the zero element)."""
        return self
    
    def get_or_else(self, default: T) -> T:
        """Return the default value since we contain nothing."""
        return default
    
    def __str__(self) -> str:
        return "Nothing"
    
    def __eq__(self, other):
        """All Nothing values are equal to each other."""
        return isinstance(other, Nothing)

# 2. Either Monad for error handling
class Either(Generic[E, T]):
    """
    The Either monad represents a value that can be either a success (Right) or failure (Left).
    
    This is used for error handling in a pure functional way, where Left typically contains
    an error value and Right contains a successful result. Unlike Maybe, Either can carry
    detailed error information in the Left case.
    
    Example:
        >>> def safe_divide(x: float, y: float) -> Either[str, float]:
        ...     if y == 0:
        ...         return Left("Division by zero")
        ...     return Right(x / y)
        >>>
        >>> # Successful computation
        >>> result = (safe_divide(10, 2)  # Right(5.0)
        ...           .map(lambda x: x * 3)   # Right(15.0)
        ...           .get_or_else(0))        # 15.0
        >>>
        >>> # Failed computation with error handling
        >>> result = (safe_divide(10, 0)  # Left("Division by zero")
        ...           .map(lambda x: x * 3)   # Still Left("Division by zero")
        ...           .get_or_else(0))        # 0 (default value)
    """
    
    def bind(self, func: Callable[[T], 'Either[E, U]']) -> 'Either[E, U]':
        """
        Bind a function that returns an Either (also known as flatMap).
        
        Args:
            func: A function that takes a value and returns an Either
            
        Returns:
            If this is Right(x), returns func(x). If this is Left, returns the Left unchanged.
        """
        raise NotImplementedError
    
    def map(self, func: Callable[[T], U]) -> 'Either[E, U]':
        """
        Apply a function to the contained value if this is a Right.
        
        Args:
            func: Function to apply to the contained value
            
        Returns:
            A new Either with the function applied to the Right value, or the original Left.
        """
        return self.bind(lambda x: Right(func(x)))
    
    def map_error(self, func: Callable[[E], E]) -> 'Either[E, T]':
        """
        Apply a function to the error value if this is a Left.
        
        Args:
            func: Function to apply to the error value
            
        Returns:
            A new Either with the function applied to the Left value, or the original Right.
        """
        raise NotImplementedError
    
    def get_or_else(self, default: T) -> T:
        """
        Get the contained value or return a default if this is a Left.
        
        Args:
            default: Value to return if this is a Left
            
        Returns:
            The contained value if Right, otherwise the default value.
        """
        raise NotImplementedError
    
    def __or__(self, func):
        """
        Override | operator for chaining operations.
        
        This allows using the | operator for chaining operations:
            result = either_value | (lambda x: Right(x + 1)) | (lambda x: Right(x * 2))
        """
        return self.bind(func)


class Left(Either[E, Any]):
    """
    Represents a failed computation with an error value.
    
    This is the Left case of the Either monad, typically used to represent
    an error or failure case where we want to preserve error information.
    """
    
    def __init__(self, error: E):
        self.error = error
    
    def bind(self, func: Callable[[Any], Either[E, U]]) -> 'Left[E, Any]':
        """Binding on Left always returns the same Left (the error is propagated)."""
        return self
    
    def map(self, func: Callable[[Any], U]) -> 'Left[E, Any]':
        """Mapping over Left returns the same Left (no-op)."""
        return self
    
    def map_error(self, func: Callable[[E], E]) -> 'Left[E, Any]':
        """Apply the function to the error value."""
        return Left(func(self.error))
    
    def get_or_else(self, default: T) -> T:
        """Return the default value since we have an error."""
        return default
    
    def __str__(self) -> str:
        return f"Left({self.error})"
    
    def __eq__(self, other):
        """Two Left values are equal if their errors are equal."""
        return isinstance(other, Left) and self.error == other.error


class Right(Either[Any, T]):
    """
    Represents a successful computation with a result value.
    
    This is the Right case of the Either monad, representing a successful
    computation result. The name comes from being the "right" or correct case.
    """
    
    def __init__(self, value: T):
        self.value = value
    
    def bind(self, func: Callable[[T], Either[E, U]]) -> Either[E, U]:
        """Apply the function to the contained value."""
        return func(self.value)
    
    def map_error(self, func: Callable[[Any], E]) -> 'Right[E, T]':
        """Mapping error over Right is a no-op."""
        return self
    
    def get_or_else(self, default: T) -> T:
        """Return the contained value, ignoring the default."""
        return self.value
    
    def __str__(self) -> str:
        return f"Right({self.value})"
    
    def __eq__(self, other):
        """Two Right values are equal if their contained values are equal."""
        return isinstance(other, Right) and self.value == other.value

# 3. Function currying
def curry(func: Callable[..., T], arity: Optional[int] = None) -> Callable:
    """
    Convert a function to a curried function.
    
    Currying transforms a function that takes multiple arguments into a sequence
    of functions that each take a single argument. This enables partial application
    and function composition.
    
    Args:
        func: The function to curry
        arity: Number of arguments the function expects (None to auto-detect)
        
    Returns:
        A curried version of the function
        
    Example:
        >>> def add_three(a, b, c):
        ...     return a + b + c
        >>> 
        >>> curried_add = curry(add_three)
        >>> add_five = curried_add(2)(3)  # Partial application
        >>> add_five(10)  # 15
        >>> 
        >>> # Can also call with multiple arguments at once
        >>> curried_add(2, 3, 10)  # 15
        >>> curried_add(2)(3, 10)  # 15
    """
    if arity is None:
        arity = func.__code__.co_argcount
    
    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        return lambda *more: curried(*(args + more))
    
    return curried

# 4. Immutable data structure with structural sharing
class ImList(Generic[T]):
    """
    An immutable list implementation with structural sharing.
    
    This is a persistent data structure where operations return new lists that
    share structure with the original list for efficiency. Because the list is
    immutable, it's thread-safe and can be safely shared between different parts
    of a program without defensive copying.
    
    Attributes:
        _items: Internal tuple storing the list items (private)
        
    Example:
        >>> lst = ImList.from_list([1, 2, 3])
        >>> lst2 = lst.cons(0)  # New list with 0 prepended
        >>> print(lst2)         # ImList([0, 1, 2, 3])
        >>> print(lst)          # Original list is unchanged: ImList([1, 2, 3])
        >>> 
        >>> # Structural sharing example
        >>> lst3 = lst2.tail()  # Shares structure with lst2
        >>> print(lst3)         # ImList([1, 2, 3])
    """
    __slots__ = ('_items',)  # Prevents adding new attributes
    
    def __init__(self, items=None):
        """
        Initialize the immutable list.
        
        Args:
            items: An optional iterable of items to initialize the list with
        """
        object.__setattr__(self, '_items', tuple(items) if items is not None else ())
    
    def __setattr__(self, name, value):
        """Prevent modification of attributes to maintain immutability."""
        raise AttributeError(f"'{self.__class__.__name__}' object is immutable")
    
    def __delattr__(self, name):
        """Prevent deletion of attributes to maintain immutability."""
        raise AttributeError(f"'{self.__class__.__name__}' object is immutable")
    
    @classmethod
    def from_list(cls, items: List[T]) -> 'ImList[T]':
        """
        Create an ImList from a regular list.
        
        Args:
            items: A list of items to create the ImList from
            
        Returns:
            A new ImList containing the items
        """
        return cls(tuple(items) if items is not None else ())
    
    def cons(self, item: T) -> 'ImList[T]':
        """
        Add an item to the front of the list.
        
        This operation is O(1) and shares the entire existing list structure
        with the new list.
        
        Args:
            item: The item to add to the front of the list
            
        Returns:
            A new ImList with the item added to the front
        """
        return ImList((item,) + self._items)
    
    def head(self) -> T:
        """
        Get the first item in the list.
        
        Returns:
            The first item in the list
            
        Raises:
            IndexError: If the list is empty
        """
        if not self._items:
            raise IndexError("head of empty list")
        return self._items[0]
    
    def tail(self) -> 'ImList[T]':
        """
        Get the list without the first item.
        
        This operation is O(1) and shares the tail of the list structure.
        
        Returns:
            A new ImList without the first item
            
        Raises:
            IndexError: If the list is empty
        """
        if not self._items:
            raise IndexError("tail of empty list")
        return ImList(self._items[1:])
    
    def is_empty(self) -> bool:
        """
        Check if the list is empty.
        
        Returns:
            True if the list has no items, False otherwise
        """
        return len(self._items) == 0
    
    def __iter__(self):
        """Return an iterator over the list items."""
        return iter(self._items)
    
    def __len__(self) -> int:
        """Return the number of items in the list."""
        return len(self._items)
    
    def __str__(self) -> str:
        """Return a string representation of the list."""
        return f"ImList({list(self._items)})"
    
    def __eq__(self, other) -> bool:
        """Two ImLists are equal if they contain the same items in the same order."""
        if not isinstance(other, ImList):
            return False
        return self._items == other._items

# 5. Lenses for immutable updates
class Lens:
    """
    A lens for getting and setting values in nested immutable data structures.
    
    Lenses provide a way to focus on a specific part of a data structure and
    perform operations (get, set, modify) in a purely functional way. They're
    particularly useful with immutable data structures where you can't modify
    values in place.
    """
    
    __slots__ = ('getter', 'setter')
    
    def __init__(self, getter: Callable[[T], U], setter: Callable[[T, U], T]):
        """
        Initialize a lens with getter and setter functions.
        
        Args:
            getter: Function that extracts the value to focus on from a structure
            setter: Function that returns a new structure with the value updated
        """
        self.getter = getter
        self.setter = setter
    
    def __call__(self, func: Callable[[U], U]) -> Callable[[T], T]:
        """
        Apply a function to the focused value.
        
        Args:
            func: Function to apply to the focused value
            
        Returns:
            A function that takes a structure and returns a new structure
            with the focused value transformed by func
        """
        def wrapper(structure: T) -> T:
            return self.setter(structure, func(self.getter(structure)))
        return wrapper
    
    def __or__(self, other: 'Lens') -> 'Lens':
        """
        Compose this lens with another lens.
        
        The resulting lens will first apply this lens, then the other lens.
        
        Args:
            other: Another lens to compose with
            
        Returns:
            A new lens that is the composition of the two lenses
        """
        return Lens(
            getter=lambda s: other.getter(self.getter(s)),
            setter=lambda s, v: self.setter(s, other.setter(self.getter(s), v))
        )

def lens(getter: Callable[[T], U], setter: Callable[[T, U], T]) -> Lens:
    """
    Create a lens for getting and setting values in nested immutable data structures.
    
    Args:
        getter: Function that extracts the value to focus on from a structure
        setter: Function that returns a new structure with the value updated
        
    Returns:
        A Lens object that can be used to modify the focused value
        
    Example:
        >>> @dataclass(frozen=True)
        ... class Person:
        ...     name: str
        ...     age: int
        >>>
        >>> # Create a lens for the 'name' field
        >>> name_lens = lens(
        ...     getter=lambda p: p.name,
        ...     setter=lambda p, name: Person(name, p.age)
        ... )
        >>>
        >>> # Create a person
        >>> person = Person("Alice", 30)
        >>>
        >>> # Use the lens to modify the name
        >>> upper_name = name_lens(lambda n: n.upper())(person)
        >>> print(upper_name)  # Person(name='ALICE', age=30)
        >>>
        >>> # The original person is unchanged
        >>> print(person)  # Person(name='Alice', age=30)
    """
    return Lens(getter, setter)

if __name__ == "__main__":
    print("=== Advanced Functional Patterns Examples ===\n")
    
    # 1. Maybe Monad examples
    print("1. Maybe Monad: Handling optional values")
    print("-" * 50)
    
    def safe_divide(x: float, y: float) -> Maybe[float]:
        """Safely divide two numbers, returning Nothing on division by zero."""
        return Just(x / y) if y != 0 else Nothing()
    
    # Successful computation
    result = safe_divide(10, 2).map(lambda x: x * 3)
    print(f"10 / 2 * 3 = {result}")
    
    # Division by zero is handled gracefully
    result = safe_divide(10, 0).map(lambda x: x * 3).get_or_else(0)
    print(f"10 / 0 * 3 = {result} (with default 0)")
    
    # Chaining operations with | operator
    result = (Just(10) 
             | (lambda x: safe_divide(x, 2))  # Just(5.0)
             | (lambda x: Just(x * 3)))      # Just(15.0)
    print(f"Chained operations: {result}")
    
    # 2. Either Monad examples
    print("\n2. Either Monad: Error handling")
    print("-" * 50)
    
    def safe_divide_either(x: float, y: float) -> Either[str, float]:
        """Divide two numbers with error handling."""
        if y == 0:
            return Left("Division by zero")
        return Right(x / y)
    
    # Successful computation chain
    result = (
        safe_divide_either(10, 2)  # Right(5.0)
        .map(lambda x: x + 3)      # Right(8.0)
        .bind(lambda x: safe_divide_either(x, 2))  # Right(4.0)
    )
    print(f"(10 / 2 + 3) / 2 = {result}")
    
    # Error case - computation short-circuits on first error
    result = (
        safe_divide_either(10, 0)   # Left("Division by zero")
        .map(lambda x: x + 3)      # Still Left
        .bind(lambda x: safe_divide_either(x, 2))  # Still Left
    )
    print(f"(10 / 0 + 3) / 2 = {result}")
    
    # Error transformation
    result = (
        safe_divide_either(10, 0)
        .map_error(lambda e: f"Error: {e}")
    )
    print(f"Transformed error: {result}")
    
    # 3. Function Currying
    print("\n3. Function Currying")
    print("-" * 50)
    
    def add_three(a: int, b: int, c: int) -> int:
        """Add three numbers together."""
        return a + b + c
    
    # Curried version
    curried_add = curry(add_three)
    
    # Partial application
    add_five = curried_add(2)(3)  # Partially applied
    print(f"add_five(10) = {add_five(10)}")  # 15
    
    # Different ways to call the curried function
    print(f"All args: {curried_add(2, 3, 10)}")  # 15
    print(f"Two then one: {curried_add(2, 3)(10)}")  # 15
    print(f"One, two, one: {curried_add(2)(3, 10)}")  # 15
    
    # 4. Immutable List with structural sharing
    print("\n4. Immutable List with Structural Sharing")
    print("-" * 50)
    
    # Create a list using from_list
    lst = ImList.from_list([1, 2, 3])
    print(f"Original list: {lst}")
    
    # Add to the front (creates new list, shares structure)
    lst2 = lst.cons(0)
    print(f"After cons(0): {lst2}")
    print(f"Head: {lst2.head()}, Tail: {lst2.tail()}")
    
    # Original list is unchanged
    print(f"Original list remains unchanged: {lst}")
    
    # Iteration
    print("Items in list:", end=" ")
    for item in lst2:
        print(item, end=" ")
    print()
    
    # 5. Lenses for immutable updates
    print("\n5. Lenses for Nested Updates")
    print("-" * 50)
    
    @dataclass(frozen=True)
    class Address:
        street: str
        city: str
        
    @dataclass(frozen=True)
    class Person:
        name: str
        age: int
        address: Address
    
    # Create lenses
    name_lens = lens(
        lambda p: p.name,
        lambda p, name: Person(name, p.age, p.address)
    )
    
    age_lens = lens(
        lambda p: p.age,
        lambda p, age: Person(p.name, age, p.address)
    )
    
    address_lens = lens(
        lambda p: p.address,
        lambda p, address: Person(p.name, p.age, address)
    )
    
    street_lens = lens(
        lambda a: a.street,
        lambda a, street: Address(street, a.city)
    )
    
    # Create a lens for the street field of a person's address
    person_address_street_lens = Lens(
        getter=lambda p: p.address.street,
        setter=lambda p, street: Person(
            p.name,
            p.age,
            Address(street, p.address.city)
        )
    )
    
    # Create a person
    person = Person(
        name="Alice",
        age=30,
        address=Address("123 Main St", "Springfield")
    )
    
    print(f"Original: {person}")
    
    # Update name to uppercase
    upper_name = name_lens(lambda n: n.upper())(person)
    print(f"Uppercase name: {upper_name}")
    
    # Increment age
    older = age_lens(lambda a: a + 1)(person)
    print(f"Older: {older}")
    
    # Update nested street address
    new_address = person_address_street_lens(
        lambda s: s.replace("Main", "Oak")
    )(person)
    print(f"New address: {new_address}")
    
    # Apply each lens transformation separately for clarity
    updated = person
    updated = name_lens(lambda n: n.upper())(updated)
    updated = age_lens(lambda a: a + 1)(updated)
    updated = person_address_street_lens(lambda s: s.upper())(updated)
    print(f"Fully updated: {updated}")
    
    # 6. Combining patterns
    print("\n6. Combining Patterns")
    print("-" * 50)
    
    def parse_age(age_str: str) -> Either[str, int]:
        """Parse age string to int with validation."""
        try:
            age = int(age_str)
            return Right(age) if age >= 0 else Left("Age cannot be negative")
        except ValueError:
            return Left("Invalid age format")
    
    def create_person(name: str, age_str: str) -> Either[str, Person]:
        """Create a person with validation using Either monad."""
        if not name.strip():
            return Left("Name cannot be empty")
            
        return (
            parse_age(age_str)
            .map(lambda age: Person(name, age, Address("", "")))
        )
    
    # Test cases
    test_cases = [
        ("Alice", "30"),
        ("", "30"),  # Empty name
        ("Bob", "-5"),  # Negative age
        ("Charlie", "abc"),  # Invalid age format
    ]
    
    for name, age_str in test_cases:
        result = create_person(name, age_str)
        status = "✓" if isinstance(result, Right) else "✗"
        print(f"{status} {name!r}, {age_str!r} -> {result}")
    
    print("\nAll examples completed successfully!")
