"""
4. Immutable Updates

Techniques for working with immutable data structures in Python.
- Updating nested immutable structures
- Using helper functions for common operations
- Structural sharing for efficiency
"""
from typing import List, Dict, Any, Tuple, TypeVar, Callable, Optional
from dataclasses import dataclass, field, replace
from copy import deepcopy

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 1. Updating nested tuples
def update_in_tuple(t: Tuple[Any, ...], index: int, value: Any) -> Tuple[Any, ...]:
    """
    Return a new tuple with the element at index replaced by value.
    
    Args:
        t: Input tuple
        index: Index to update
        value: New value
        
    Returns:
        New tuple with the updated value
    """
    return t[:index] + (value,) + t[index+1:]

def update_nested_tuple(t: Any, path: List[Any], value: Any) -> Any:
    """
    Update a value in a nested tuple structure.
    
    Args:
        t: Input tuple or value
        path: List of indices to navigate to the value to update
        value: New value
        
    Returns:
        New tuple with the updated value
    """
    if not path:
        return value
    
    if not isinstance(t, tuple):
        raise ValueError("Path doesn't match tuple structure")
    
    index = path[0]
    if index >= len(t):
        raise IndexError("Index out of range")
    
    return t[:index] + (update_nested_tuple(t[index], path[1:], value),) + t[index+1:]

# 2. Immutable dictionary updates
def dict_set(d: Dict[K, V], key: K, value: V) -> Dict[K, V]:
    """Return a new dict with key set to value."""
    new_dict = d.copy()
    new_dict[key] = value
    return new_dict

def dict_update(d: Dict[K, V], updates: Dict[K, V]) -> Dict[K, V]:
    """Return a new dict with multiple updates."""
    return {**d, **updates}

def dict_dissoc(d: Dict[K, V], key: K) -> Dict[K, V]:
    """Return a new dict without the specified key."""
    new_dict = d.copy()
    new_dict.pop(key, None)
    return new_dict

# 3. Immutable list operations
def list_append(lst: List[T], item: T) -> List[T]:
    """Return a new list with item appended."""
    return lst + [item]

def list_remove(lst: List[T], item: T) -> List[T]:
    """Return a new list with the first occurrence of item removed."""
    new_list = lst.copy()
    try:
        new_list.remove(item)
    except ValueError:
        pass
    return new_list

# 4. Nested immutable updates with paths
def get_in(d: Dict, keys: List[K], default: Any = None) -> Any:
    """Get a value from a nested dict using a list of keys."""
    current = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current

def assoc_in(d: Dict, keys: List[K], value: Any) -> Dict:
    """Return a new dict with the value at path set to value."""
    if not keys:
        return value
    
    key = keys[0]
    if len(keys) == 1:
        return dict_set(d, key, value)
    
    current = d.get(key, {})
    if not isinstance(current, dict):
        current = {}
        
    return dict_set(d, key, assoc_in(current, keys[1:], value))

# 5. Working with dataclasses
@dataclass(frozen=True)
class Address:
    street: str
    city: str
    zip_code: str

@dataclass(frozen=True)
class Person:
    name: str
    age: int
    address: Address
    
    def with_age(self, new_age: int) -> 'Person':
        """Return a new Person with the updated age."""
        return replace(self, age=new_age)
    
    def with_address(self, **updates: Any) -> 'Person':
        """Return a new Person with the updated address."""
        new_address = replace(self.address, **updates)
        return replace(self, address=new_address)

def demonstrate_updates() -> None:
    """Demonstrate various immutable update techniques."""
    # 1. Updating tuples
    point = (1, 2, 3)
    new_point = update_in_tuple(point, 1, 20)
    print(f"Original point: {point}")
    print(f"Updated point: {new_point}")
    
    # 2. Nested tuple updates
    nested = ((1, 2), (3, 4, (5, 6)))
    updated = update_nested_tuple(nested, [1, 2, 0], 50)
    print(f"\nOriginal nested: {nested}")
    print(f"Updated nested: {updated}")
    
    # 3. Dictionary updates
    person = {"name": "Alice", "age": 30, "address": {"city": "New York"}}
    updated_person = assoc_in(person, ["address", "zip"], "10001")
    print(f"\nOriginal person: {person}")
    print(f"Updated person: {updated_person}")
    
    # 4. Working with dataclasses
    address = Address("123 Main St", "Anytown", "12345")
    alice = Person("Alice", 30, address)
    
    # Update age
    alice_older = alice.with_age(31)
    print(f"\nOriginal age: {alice.age}")
    print(f"Updated age: {alice_older.age}")
    
    # Update address
    alice_moved = alice.with_address(city="Newtown")
    print(f"\nOriginal city: {alice.address.city}")
    print(f"Updated city: {alice_moved.address.city}")
    
    # Original objects are unchanged
    print(f"\nOriginal objects unchanged:")
    print(f"Original point: {point}")
    print(f"Original person: {person}")
    print(f"Original Alice: {alice.name}, {alice.age}, {alice.address.city}")

# Example usage
if __name__ == "__main__":
    demonstrate_updates()
    
    print("\n=== Key Takeaways ===")
    print("1. Always return new objects instead of modifying in-place")
    print("2. Use helper functions for common update patterns")
    print("3. For complex nested updates, use path-based functions")
    print("4. Take advantage of Python's built-in copy mechanisms")
    print("5. Consider using dataclasses with frozen=True for complex structures")
