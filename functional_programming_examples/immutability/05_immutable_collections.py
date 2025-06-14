"""
5. Immutable Collections

Working with immutable collections in Python.
- Using frozenset
- Immutable dictionaries with MappingProxyType
- Creating custom immutable collection classes
"""
from typing import Any, Set, Dict, List, TypeVar, Generic, Iterable, Iterator, Mapping
from collections.abc import MutableMapping, MutableSet, MutableSequence
from types import MappingProxyType
from functools import reduce

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 1. frozenset - immutable set
def demonstrate_frozenset() -> None:
    """Show how to use frozenset for immutable sets."""
    # Create frozensets
    fs1 = frozenset([1, 2, 3, 4, 5])
    fs2 = frozenset([4, 5, 6, 7, 8])
    
    print(f"fs1: {fs1}")
    print(f"fs2: {fs2}")
    
    # Set operations return new frozensets
    union = fs1.union(fs2)
    intersection = fs1.intersection(fs2)
    difference = fs1.difference(fs2)
    
    print(f"\nUnion: {union}")
    print(f"Intersection: {intersection}")
    print(f"Difference (fs1 - fs2): {difference}")
    
    # frozenset is hashable and can be used as dictionary keys
    sets_dict = {
        frozenset([1, 2, 3]): "first three",
        frozenset([4, 5, 6]): "next three"
    }
    print(f"\nDictionary with frozenset keys: {sets_dict}")

# 2. MappingProxyType - read-only view of a dictionary
def demonstrate_mapping_proxy() -> None:
    """Show how to use MappingProxyType for immutable dict views."""
    # Create a regular dictionary
    data = {"name": "Alice", "age": 30, "city": "New York"}
    
    # Create a read-only view
    read_only = MappingProxyType(data)
    
    print(f"Read-only view: {read_only}")
    print(f"Accessing values: name={read_only['name']}, age={read_only['age']}")
    
    # Attempting to modify raises TypeError
    try:
        read_only["age"] = 31
    except TypeError as e:
        print(f"\nCannot modify read-only view: {e}")
    
    # Changes to original are reflected in the view
    data["age"] = 31
    print(f"\nAfter modifying original: {read_only}")

# 3. Immutable List-like class
class ImmutableList(Generic[T]):
    """An immutable list-like collection."""
    
    def __init__(self, items: Iterable[T] = ()):
        self._items = tuple(items)
    
    def __getitem__(self, index: int) -> T:
        return self._items[index]
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._items)
    
    def __contains__(self, item: T) -> bool:
        return item in self._items
    
    def __repr__(self) -> str:
        return f"ImmutableList({list(self._items)})"
    
    def append(self, item: T) -> 'ImmutableList[T]':
        """Return a new list with the item appended."""
        return ImmutableList((*self._items, item))
    
    def extend(self, items: Iterable[T]) -> 'ImmutableList[T]':
        """Return a new list with items extended."""
        return ImmutableList((*self._items, *items))
    
    def filter(self, predicate: Callable[[T], bool]) -> 'ImmutableList[T]':
        """Return a new list with items that satisfy the predicate."""
        return ImmutableList(item for item in self if predicate(item))
    
    def map(self, func: Callable[[T], V]) -> 'ImmutableList[V]':
        """Apply a function to each item and return a new list."""
        return ImmutableList(func(item) for item in self)
    
    def reduce(self, func: Callable[[T, T], T], initial: T = None) -> T:
        """Reduce the list to a single value using the function."""
        if initial is None:
            return reduce(func, self._items)
        return reduce(func, self._items, initial)

# 4. Immutable Dictionary class
class ImmutableDict(Mapping[K, V]):
    """An immutable dictionary implementation."""
    
    def __init__(self, items: Mapping[K, V] = None, **kwargs):
        self._dict = dict(items or {}, **kwargs)
    
    def __getitem__(self, key: K) -> V:
        return self._dict[key]
    
    def __iter__(self) -> Iterator[K]:
        return iter(self._dict)
    
    def __len__(self) -> int:
        return len(self._dict)
    
    def __repr__(self) -> str:
        return f"ImmutableDict({self._dict})"
    
    def set(self, key: K, value: V) -> 'ImmutableDict[K, V]':
        """Return a new dict with the key set to value."""
        new_dict = self._dict.copy()
        new_dict[key] = value
        return ImmutableDict(new_dict)
    
    def update(self, other: Mapping[K, V] = None, **kwargs) -> 'ImmutableDict[K, V]':
        """Return a new dict with items from other and kwargs."""
        new_dict = self._dict.copy()
        if other:
            new_dict.update(other)
        new_dict.update(kwargs)
        return ImmutableDict(new_dict)
    
    def remove(self, key: K) -> 'ImmutableDict[K, V]':
        """Return a new dict without the specified key."""
        if key not in self._dict:
            return self
        new_dict = self._dict.copy()
        del new_dict[key]
        return ImmutableDict(new_dict)

def demonstrate_immutable_collections() -> None:
    """Show how to use the custom immutable collections."""
    # ImmutableList
    print("=== ImmutableList ===")
    lst = ImmutableList([1, 2, 3, 4, 5])
    print(f"Original: {lst}")
    
    # Operations return new instances
    lst2 = lst.append(6).append(7)
    print(f"After append: {lst2}")
    
    # Original is unchanged
    print(f"Original unchanged: {lst}")
    
    # Map and filter
    lst3 = lst.map(lambda x: x * 2).filter(lambda x: x > 5)
    print(f"Mapped and filtered: {lst3}")
    
    # Reduce
    total = lst.reduce(lambda x, y: x + y)
    print(f"Sum of {lst}: {total}")
    
    # ImmutableDict
    print("\n=== ImmutableDict ===")
    d = ImmutableDict({"a": 1, "b": 2, "c": 3})
    print(f"Original: {d}")
    
    # Update operations return new instances
    d2 = d.set("d", 4).set("e", 5)
    print(f"After set: {d2}")
    
    # Remove a key
    d3 = d2.remove("b")
    print(f"After remove 'b': {d3}")
    
    # Original is unchanged
    print(f"Original unchanged: {d}")

# Example usage
if __name__ == "__main__":
    print("=== frozenset ===")
    demonstrate_frozenset()
    
    print("\n=== MappingProxyType ===")
    demonstrate_mapping_proxy()
    
    print("\n=== Custom Immutable Collections ===")
    demonstrate_immutable_collections()
    
    print("\n=== When to Use Which ===")
    print("1. Use frozenset when you need an immutable set")
    print("2. Use MappingProxyType for read-only views of dictionaries")
    print("3. Use custom immutable collections when you need more control")
    print("4. Consider using third-party libraries like 'immutables' or 'pyrsistent' for production use")
