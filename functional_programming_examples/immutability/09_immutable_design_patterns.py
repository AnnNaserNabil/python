"""
9. Immutable Design Patterns

Common patterns for working with immutable data in Python.
- The builder pattern for complex objects
- The lens pattern for nested updates
- The flyweight pattern for memory efficiency
- The prototype pattern for object creation
"""
from typing import TypeVar, Generic, Callable, Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from copy import deepcopy
import json

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 1. Builder Pattern for Complex Immutable Objects
@dataclass(frozen=True)
class Address:
    street: str
    city: str
    zip_code: str
    country: str = "USA"

@dataclass(frozen=True)
class ContactInfo:
    email: str
    phone: str

@dataclass(frozen=True)
class Person:
    name: str
    age: int
    address: Address
    contacts: Tuple[ContactInfo, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)

class PersonBuilder:
    """Builder for creating immutable Person objects."""
    
    def __init__(self):
        self._name = None
        self._age = None
        self._address = None
        self._contacts = []
        self._metadata = {}
    
    def with_name(self, name: str) -> 'PersonBuilder':
        self._name = name
        return self
    
    def with_age(self, age: int) -> 'PersonBuilder':
        self._age = age
        return self
    
    def with_address(self, street: str, city: str, zip_code: str, country: str = "USA") -> 'PersonBuilder':
        self._address = Address(street, city, zip_code, country)
        return self
    
    def add_contact(self, email: str, phone: str) -> 'PersonBuilder':
        self._contacts.append(ContactInfo(email, phone))
        return self
    
    def with_metadata(self, key: str, value: Any) -> 'PersonBuilder':
        self._metadata[key] = value
        return self
    
    def build(self) -> Person:
        if None in (self._name, self._age, self._address):
            raise ValueError("Name, age, and address are required")
        return Person(
            name=self._name,
            age=self._age,
            address=self._address,
            contacts=tuple(self._contacts),
            metadata=self._metadata.copy()
        )

# 2. Lens Pattern for Nested Updates
def lens(getter: Callable[[T], V], setter: Callable[[T, V], T]) -> Callable[[Callable[[V], V]], Callable[[T], T]]:
    """Create a lens for getting and setting values in nested structures."""
    def _lens(func: Callable[[V], V]) -> Callable[[T], T]:
        def wrapper(structure: T) -> T:
            return setter(structure, func(getter(structure)))
        return wrapper
    return _lens

# 3. Flyweight Pattern for Memory Efficiency
class FlyweightFactory(Generic[T]):
    """Flyweight factory for immutable objects."""
    
    def __init__(self):
        self._pool: Dict[Any, T] = {}
    
    def get_flyweight(self, key: Any, constructor: Callable[..., T], *args, **kwargs) -> T:
        """Get or create a flyweight object."""
        if key not in self._pool:
            self._pool[key] = constructor(*args, **kwargs)
        return self._pool[key]

# 4. Prototype Pattern for Object Creation
class Prototype(Generic[T]):
    """Prototype for creating immutable objects with modifications."""
    
    def __init__(self, prototype: T):
        self._prototype = prototype
    
    def clone(self, **changes: Any) -> T:
        """Create a new object with the given changes."""
        if not hasattr(self._prototype, '__dataclass_fields__'):
            raise ValueError("Prototype must be a dataclass instance")
        
        # Create a deep copy of the prototype's __dict__
        data = asdict(self._prototype)
        
        # Apply changes
        for key, value in changes.items():
            if key in data:
                data[key] = value
        
        # Create a new instance of the same class
        return self._prototype.__class__(**data)

# Example usage of all patterns
def demonstrate_design_patterns() -> None:
    """Show how to use the immutable design patterns."""
    # 1. Builder Pattern
    print("=== Builder Pattern ===")
    person_builder = PersonBuilder()
    person = (
        person_builder
        .with_name("Alice")
        .with_age(30)
        .with_address("123 Main St", "Anytown", "12345")
        .add_contact("alice@example.com", "555-1234")
        .with_metadata("employee_id", "E12345")
        .build()
    )
    print(f"Built person: {person}")
    
    # 2. Lens Pattern
    print("\n=== Lens Pattern ===")
    # Create a lens for the street address
    street_lens = lens(
        lambda p: p.address.street,
        lambda p, street: Person(
            name=p.name,
            age=p.age,
            address=Address(
                street=street,
                city=p.address.city,
                zip_code=p.address.zip_code,
                country=p.address.country
            ),
            contacts=p.contacts,
            metadata=p.metadata
        )
    )
    
    # Function to update the street
    def to_upper(street: str) -> str:
        return street.upper()
    
    # Apply the lens
    updated_person = street_lens(to_upper)(person)
    print(f"Original street: {person.address.street}")
    print(f"Updated street: {updated_person.address.street}")
    
    # 3. Flyweight Pattern
    print("\n=== Flyweight Pattern ===")
    factory = FlyweightFactory[Address]()
    
    # These should return the same instance
    addr1 = factory.get_flyweight("home", Address, "123 Main St", "Anytown", "12345")
    addr2 = factory.get_flyweight("home", Address, "123 Main St", "Anytown", "12345")
    
    print(f"addr1 is addr2: {addr1 is addr2}")
    print(f"addr1: {addr1}")
    
    # This will create a new instance
    addr3 = factory.get_flyweight("work", Address, "456 Work St", "Business", "67890")
    print(f"addr3: {addr3}")
    
    # 4. Prototype Pattern
    print("\n=== Prototype Pattern ===")
    prototype = Prototype(person)
    
    # Create a modified clone
    cloned_person = prototype.clone(age=31, metadata={"employee_id": "E12345", "department": "Engineering"})
    
    print(f"Original age: {person.age}")
    print(f"Cloned age: {cloned_person.age}")
    print(f"Original metadata: {person.metadata}")
    print(f"Cloned metadata: {cloned_person.metadata}")
    
    # The original is unchanged
    print(f"Original person is cloned person: {person is cloned_person}")
    print(f"But they have the same name: {person.name == cloned_person.name}")

# Example usage
if __name__ == "__main__":
    demonstrate_design_patterns()
    
    print("\n=== Key Takeaways ===")
    print("1. Builder Pattern: Use for creating complex immutable objects step by step")
    print("2. Lens Pattern: Use for updating nested immutable data structures")
    print("3. Flyweight Pattern: Use to share common immutable objects for memory efficiency")
    print("4. Prototype Pattern: Use to create new objects by copying and modifying existing ones")
    print("5. Combine these patterns as needed for your specific use case")
