"""
3. Immutable Data Structures

Creating and working with immutable data structures in Python.
- Using namedtuple
- Using dataclass with frozen=True
- Creating custom immutable classes
"""
from typing import NamedTuple, List, Tuple, Any
from dataclasses import dataclass, field
from collections import namedtuple

# 1. Using namedtuple for simple immutable records
def demonstrate_namedtuple() -> None:
    """Show how to use namedtuple for simple immutable records."""
    # Basic namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    p1 = Point(10, 20)
    print(f"Point: {p1}")
    print(f"x: {p1.x}, y: {p1.y}")
    
    # Access by index or name
    print(f"x (by index): {p1[0]}")
    print(f"y (by name): {p1.y}")
    
    # Immutable - this would raise an AttributeError
    try:
        p1.x = 30
    except AttributeError as e:
        print(f"Cannot modify namedtuple: {e}")
    
    # _replace creates a new instance
    p2 = p1._replace(x=30)
    print(f"New point with x=30: {p2}")
    print(f"Original point unchanged: {p1}")
    
    # _asdict converts to OrderedDict
    print(f"As dictionary: {p1._asdict()}")

# 2. Using dataclass with frozen=True
@dataclass(frozen=True)
class ImmutablePerson:
    """An immutable person record using dataclass."""
    name: str
    age: int
    email: str
    
    def greet(self) -> str:
        """Return a greeting message."""
        return f"Hello, my name is {self.name} and I'm {self.age} years old."

# 3. Custom immutable class with __slots__
class ImmutablePoint:
    """A custom immutable point class."""
    __slots__ = ['_x', '_y']
    
    def __init__(self, x: float, y: float):
        # Use direct attribute assignment to avoid setattr
        object.__setattr__(self, '_x', x)
        object.__setattr__(self, '_y', y)
    
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"'{self.__class__.__name__}' object is immutable")
    
    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"'{self.__class__.__name__}' object is immutable")
    
    def __repr__(self) -> str:
        return f"ImmutablePoint(x={self.x}, y={self.y})"
    
    def move(self, dx: float, dy: float) -> 'ImmutablePoint':
        """Return a new point moved by (dx, dy)."""
        return ImmutablePoint(self.x + dx, self.y + dy)

# 4. Immutable collections with type hints
@dataclass(frozen=True)
class ImmutableCollection:
    """An immutable collection of items."""
    items: Tuple[Any, ...] = field(default_factory=tuple)
    
    def add(self, item: Any) -> 'ImmutableCollection':
        """Return a new collection with the item added."""
        return ImmutableCollection(self.items + (item,))
    
    def remove(self, item: Any) -> 'ImmutableCollection':
        """Return a new collection with the item removed."""
        if item not in self.items:
            return self
        index = self.items.index(item)
        return ImmutableCollection(self.items[:index] + self.items[index+1:])
    
    def __contains__(self, item: Any) -> bool:
        return item in self.items
    
    def __len__(self) -> int:
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)

def demonstrate_immutable_classes() -> None:
    """Show how to work with immutable classes."""
    # Using frozen dataclass
    person = ImmutablePerson("Alice", 30, "alice@example.com")
    print(f"Person: {person}")
    print(person.greet())
    
    # This would raise FrozenInstanceError
    try:
        person.age = 31
    except Exception as e:
        print(f"Cannot modify frozen dataclass: {e}")
    
    # Using custom immutable class
    point = ImmutablePoint(3, 4)
    print(f"Original point: {point}")
    
    # This would raise AttributeError
    try:
        point.x = 10
    except AttributeError as e:
        print(f"Cannot modify immutable point: {e}")
    
    # Create a new point instead
    new_point = point.move(2, 3)
    print(f"Moved point: {new_point}")
    print(f"Original point unchanged: {point}")
    
    # Using immutable collection
    collection = ImmutableCollection((1, 2, 3))
    print(f"Original collection: {collection.items}")
    
    new_collection = collection.add(4).add(5)
    print(f"After adding items: {new_collection.items}")
    
    newer_collection = new_collection.remove(3)
    print(f"After removing 3: {newer_collection.items}")
    print(f"Original collection unchanged: {collection.items}")

# Example usage
if __name__ == "__main__":
    print("=== Named Tuples ===")
    demonstrate_namedtuple()
    
    print("\n=== Immutable Classes ===")
    demonstrate_immutable_classes()
    
    print("\n=== When to Use Which ===")
    print("1. Use namedtuple for simple data structures with a few fields")
    print("2. Use @dataclass(frozen=True) for more complex immutable classes")
    print("3. Use custom immutable classes when you need full control")
    print("4. Prefer immutability when:")
    print("   - Data shouldn't change after creation")
    print("   - Thread safety is important")
    print("   - You want to use objects as dictionary keys")
    print("   - You want to ensure data consistency")
