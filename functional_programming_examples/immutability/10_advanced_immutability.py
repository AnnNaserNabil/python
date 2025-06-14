"""
10. Advanced Immutability Techniques

Advanced patterns and techniques for working with immutable data in Python.
- Type-safe immutable data structures
- Immutable collections with type checking
- Performance considerations
- Integration with external libraries
"""
from typing import TypeVar, Generic, Callable, Any, Dict, List, Optional, Tuple, Type, cast
from dataclasses import dataclass, field, fields, asdict
from collections.abc import Mapping, Sequence, Set as AbstractSet
import sys
import time
from functools import wraps
from types import MappingProxyType
import json

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 1. Type-safe immutable dictionary
class FrozenDict(Mapping[K, V]):
    """An immutable, hashable dictionary."""
    
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
        self._hash = None
    
    def __getitem__(self, key: K) -> V:
        return self._dict[key]
    
    def __iter__(self):
        return iter(self._dict)
    
    def __len__(self) -> int:
        return len(self._dict)
    
    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(frozenset(self._dict.items()))
        return self._hash
    
    def __repr__(self) -> str:
        return f"FrozenDict({self._dict})"
    
    def set(self, key: K, value: V) -> 'FrozenDict[K, V]':
        """Return a new FrozenDict with the key set to value."""
        new_dict = self._dict.copy()
        new_dict[key] = value
        return FrozenDict(new_dict)
    
    def remove(self, key: K) -> 'FrozenDict[K, V]':
        """Return a new FrozenDict without the specified key."""
        if key not in self._dict:
            return self
        new_dict = self._dict.copy()
        del new_dict[key]
        return FrozenDict(new_dict)

# 2. Type-safe immutable list
class FrozenList(Sequence[T]):
    """An immutable, hashable list."""
    
    def __init__(self, items: Sequence[T] = ()):
        self._list = list(items)
        self._hash = None
    
    def __getitem__(self, index: int) -> T:
        return self._list[index]
    
    def __iter__(self):
        return iter(self._list)
    
    def __len__(self) -> int:
        return len(self._list)
    
    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(tuple(self._list))
        return self._hash
    
    def __repr__(self) -> str:
        return f"FrozenList({self._list})"
    
    def append(self, item: T) -> 'FrozenList[T]':
        """Return a new FrozenList with the item appended."""
        return FrozenList([*self._list, item])
    
    def extend(self, items: Sequence[T]) -> 'FrozenList[T]':
        """Return a new FrozenList with items extended."""
        return FrozenList([*self._list, *items])
    
    def insert(self, index: int, item: T) -> 'FrozenList[T]':
        """Return a new FrozenList with the item inserted at index."""
        new_list = self._list.copy()
        new_list.insert(index, item)
        return FrozenList(new_list)
    
    def remove(self, item: T) -> 'FrozenList[T]':
        """Return a new FrozenList with the first occurrence of item removed."""
        new_list = self._list.copy()
        try:
            new_list.remove(item)
        except ValueError:
            pass
        return FrozenList(new_list)

# 3. Immutable data class with runtime type checking
@dataclass(frozen=True)
class ImmutableData:
    """Base class for immutable data classes with runtime type checking."""
    
    def __post_init__(self):
        """Validate types after initialization."""
        for field_name, field_type in self.__annotations__.items():
            value = getattr(self, field_name)
            self._validate_type(field_name, value, field_type)
    
    def _validate_type(self, name: str, value: Any, type_hint: Type) -> None:
        """Validate that value matches the type hint."""
        # Handle Optional[T]
        if hasattr(type_hint, '__origin__') and type_hint.__origin__ is type(Optional):
            if value is None:
                return
            type_hint = type_hint.__args__[0]
        
        # Handle List[T], Dict[K, V], etc.
        if hasattr(type_hint, '__origin__') and type_hint.__origin__ in (list, List):
            if not isinstance(value, (list, FrozenList)):
                raise TypeError(f"{name} must be a list, got {type(value).__name__}")
            item_type = type_hint.__args__[0]
            for i, item in enumerate(value):
                self._validate_type(f"{name}[{i}]", item, item_type)
            return
        
        if hasattr(type_hint, '__origin__') and type_hint.__origin__ in (dict, Dict):
            if not isinstance(value, (dict, FrozenDict)):
                raise TypeError(f"{name} must be a dict, got {type(value).__name__}")
            key_type, value_type = type_hint.__args__
            for k, v in value.items():
                self._validate_type(f"{name} key '{k}'", k, key_type)
                self._validate_type(f"{name}['{k}']", v, value_type)
            return
        
        # Handle nested ImmutableData
        if (isinstance(type_hint, type) and 
            hasattr(type_hint, '__annotations__') and 
            issubclass(type_hint, ImmutableData)):
            if not isinstance(value, type_hint):
                raise TypeError(f"{name} must be of type {type_hint.__name__}, got {type(value).__name__}")
            return
        
        # Handle built-in types
        if type_hint is Any:
            return
            
        if not isinstance(value, type_hint):
            raise TypeError(f"{name} must be of type {type_hint.__name__}, got {type(value).__name__}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary, handling nested ImmutableData objects."""
        def _to_dict(obj):
            if isinstance(obj, ImmutableData):
                return {k: _to_dict(v) for k, v in asdict(obj).items()}
            elif isinstance(obj, (list, tuple, FrozenList)):
                return [_to_dict(item) for item in obj]
            elif isinstance(obj, (dict, FrozenDict)):
                return {k: _to_dict(v) for k, v in obj.items()}
            else:
                return obj
        
        return {k: _to_dict(v) for k, v in asdict(self).items()}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImmutableData':
        """Create an instance from a dictionary."""
        return cls(**data)

# 4. Performance measurement
def measure_performance() -> None:
    """Compare performance of different immutable collection implementations."""
    import timeit
    
    # Test data
    size = 10_000
    data = list(range(size))
    
    # Test list vs FrozenList
    print(f"\n=== Performance Comparison (size={size}) ===")
    
    # List creation
    list_time = timeit.timeit(lambda: list(data), number=100)
    frozen_list_time = timeit.timeit(lambda: FrozenList(data), number=100)
    print(f"List creation (list vs FrozenList): {list_time:.6f}s vs {frozen_list_time:.6f}s")
    
    # List append
    lst = list(data)
    flst = FrozenList(data)
    list_append_time = timeit.timeit(lambda: lst.append(1), number=1000)
    frozen_list_append_time = timeit.timeit(lambda: flst.append(1), number=1000)
    print(f"List append (list vs FrozenList): {list_append_time:.6f}s vs {frozen_list_append_time:.6f}s")
    
    # Dictionary creation
    dict_data = {str(i): i for i in range(size)}
    dict_time = timeit.timeit(lambda: dict(dict_data), number=100)
    frozen_dict_time = timeit.timeit(lambda: FrozenDict(dict_data), number=100)
    print(f"Dict creation (dict vs FrozenDict): {dict_time:.6f}s vs {frozen_dict_time:.6f}s")
    
    # Dictionary get
    d = dict(dict_data)
    fd = FrozenDict(dict_data)
    key = str(size // 2)
    dict_get_time = timeit.timeit(lambda: d[key], number=10000)
    frozen_dict_get_time = timeit.timeit(lambda: fd[key], number=10000)
    print(f"Dict get (dict vs FrozenDict): {dict_get_time:.6f}s vs {frozen_dict_get_time:.6f}s")

# 5. Example usage with type checking
@dataclass(frozen=True)
class Address(ImmutableData):
    street: str
    city: str
    zip_code: str
    country: str = "USA"

@dataclass(frozen=True)
class Person(ImmutableData):
    name: str
    age: int
    address: Address
    phone_numbers: FrozenList[str] = field(default_factory=FrozenList)
    metadata: FrozenDict[str, Any] = field(default_factory=FrozenDict)

def demonstrate_advanced_immutability() -> None:
    """Show advanced immutability techniques."""
    # Create an address
    address = Address("123 Main St", "Anytown", "12345")
    
    # Create a person with phone numbers and metadata
    person = Person(
        name="Alice",
        age=30,
        address=address,
        phone_numbers=FrozenList(["555-1234", "555-5678"]),
        metadata=FrozenDict({"employee_id": "E12345", "department": "Engineering"})
    )
    
    print("=== Person ===")
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    print(f"Address: {person.address.street}, {person.address.city}")
    print(f"Phone numbers: {list(person.phone_numbers)}")
    print(f"Metadata: {dict(person.metadata)}")
    
    # Try to modify the person (will raise AttributeError)
    try:
        person.name = "Bob"  # type: ignore
    except AttributeError as e:
        print(f"\nCannot modify person: {e}")
    
    # Create a modified copy
    new_person = Person(
        name=person.name,
        age=person.age + 1,
        address=person.address,
        phone_numbers=person.phone_numbers.append("555-9012"),
        metadata=person.metadata.set("promotion", "Senior Engineer")
    )
    
    print("\n=== Modified Person ===")
    print(f"Name: {new_person.name}")
    print(f"Age: {new_person.age}")
    print(f"Phone numbers: {list(new_person.phone_numbers)}")
    print(f"Metadata: {dict(new_person.metadata)}")
    
    # Type checking
    print("\n=== Type Checking ===")
    try:
        # This will raise TypeError due to wrong type for age
        bad_person = Person(
            name="Bob",
            age="thirty",  # Should be int
            address=address
        )
    except TypeError as e:
        print(f"Type check failed: {e}")
    
    # Convert to dict and back
    print("\n=== Serialization ===")
    person_dict = person.to_dict()
    print(f"As dict: {json.dumps(person_dict, indent=2)}")
    
    # Measure performance
    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        measure_performance()

# Example usage
if __name__ == "__main__":
    demonstrate_advanced_immutability()
    
    print("\n=== Key Takeaways ===")
    print("1. Use FrozenDict and FrozenList for type-safe immutable collections")
    print("2. Create base classes with runtime type checking for complex data structures")
    print("3. Be aware of the performance implications of immutability")
    print("4. Consider using libraries like 'pyrsistent' or 'immutables' for production use")
    print("5. Always measure performance when working with large immutable data structures")
