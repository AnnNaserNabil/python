"""
7. Immutable Data Structures in Python

This module demonstrates how to work with immutable data structures in a pure functional style.
Immutable objects are fundamental to functional programming as they prevent unintended
side effects and make code more predictable and easier to reason about.

Key Concepts:
------------
- Immutability: Once created, an immutable object cannot be changed
- Pure Functions: Functions that don't modify their inputs and have no side effects
- Value Semantics: Objects are compared by their values, not identities
- Defensive Copies: Creating new objects instead of modifying existing ones

Why Use Immutable Data Structures?
--------------------------------
- Thread Safety: No need for locks in concurrent code
- Predictability: Values can't change unexpectedly
- Debugging: Easier to track changes in program state
- Caching: Safe to cache results of pure functions
- Functional Programming: Enables referential transparency

Python's Built-in Immutable Types:
--------------------------------
- Basic: int, float, bool, str, tuple, frozenset, bytes
- Standard Library: datetime, time, namedtuple, frozendict (from types module)
- Third-party: pyrsistent, immutables, frozenlist, etc.

When to Use:
-----------
- When you need to ensure data integrity
- For function parameters and return values
- In concurrent/parallel programming
- When implementing functional data structures
- For configuration and constant data

Example:
-------
>>> p = (3, 4)
>>> p2 = move_point(p, 1, 2)
>>> p  # Original unchanged
(3, 4)
>>> p2  # New point created
(4, 6)
"""
from typing import NamedTuple, List, Tuple, Dict, Any
from dataclasses import dataclass, replace
from copy import deepcopy

# 1. Using tuples for immutable data
Point2D = Tuple[float, float]

def move_point(p: Point2D, dx: float, dy: float) -> Point2D:
    """
    Move a 2D point by (dx, dy) and return a new point.
    
    This is a pure function that demonstrates immutability by creating a new
    tuple instead of modifying the input point. The original point remains unchanged.
    
    Args:
        p: Original point as a tuple (x, y)
        dx: Distance to move along the x-axis (can be negative)
        dy: Distance to move along the y-axis (can be negative)
        
    Returns:
        Point2D: A new tuple representing the moved point (x + dx, y + dy)
        
    Examples:
        >>> move_point((0, 0), 5, 3)
        (5, 3)
        >>> move_point((1, 1), -1, -1)
        (0, 0)
        >>> p = (10, 20)
        >>> p_moved = move_point(p, 2, 3)
        >>> p  # Original unchanged
        (10, 20)
        >>> p_moved
        (12, 23)
        
    Note:
        - Time complexity: O(1)
        - Space complexity: O(1) (creates a new tuple)
        - Pure function: No side effects, deterministic
    """
    x, y = p
    return (x + dx, y + dy)

# 2. Using NamedTuple for more readable code
class Person(NamedTuple):
    """
    An immutable record representing a person.
    
    This class demonstrates the use of typing.NamedTuple to create
    simple, immutable data structures with type hints and a clean syntax.
    
    Attributes:
        name: Full name of the person (e.g., "John Doe")
        age: Age in years (must be non-negative)
        email: Email address (should be valid but not enforced here)
        
    Examples:
        >>> alice = Person("Alice", 30, "alice@example.com")
        >>> alice.name
        'Alice'
        >>> alice.age
        30
        >>> alice.email
        'alice@example.com'
        
    Note:
        - Instances are immutable (cannot be modified after creation)
        - Supports equality comparison by value
        - Provides a nice string representation
        - Memory efficient (uses __slots__)
        - Can be used as dictionary keys (hashable)
    """
    name: str
    age: int
    email: str

def celebrate_birthday(person: Person) -> Person:
    """
    Create a new Person with age incremented by 1.
    
    This function demonstrates the principle of immutability by returning
    a new Person instance rather than modifying the existing one.
    
    Args:
        person: The person whose birthday we're celebrating
        
    Returns:
        Person: A new Person instance with age incremented by 1
        
    Examples:
        >>> alice = Person("Alice", 30, "alice@example.com")
        >>> older_alice = celebrate_birthday(alice)
        >>> alice.age  # Original unchanged
        30
        >>> older_alice.age
        31
        >>> alice is older_alice  # Different objects
        False
        
    Note:
        - Pure function: No side effects, deterministic
        - Returns a new Person instance
        - Original person remains unchanged
        - Time complexity: O(1)
        - Space complexity: O(1) (creates a new Person)
    """
    return Person(
        name=person.name,
        age=person.age + 1,
        email=person.email
    )

# 3. Using dataclass with frozen=True for complex immutable structures
@dataclass(frozen=True)
class ShoppingCart:
    """
    An immutable shopping cart implemented using @dataclass(frozen=True).
    
    This class demonstrates how to create more complex immutable data structures
    with methods that return new instances rather than modifying the current one.
    
    Attributes:
        items: List of item names in the cart
        total: Total price of all items in the cart
        
    Examples:
        >>> cart = ShoppingCart([], 0.0)
        >>> cart = cart.add_item("Apple", 1.50)
        >>> cart = cart.add_item("Banana", 0.99)
        >>> cart.items
        ['Apple', 'Banana']
        >>> cart.total
        2.49
        >>> cart = cart.remove_item("Apple", 1.50)
        >>> cart.items
        ['Banana']
        >>> cart.total
        0.99
        
    Note:
        - frozen=True makes instances immutable
        - Methods return new instances instead of modifying self
        - Supports equality comparison by value
        - Provides a nice string representation
        - More flexible than NamedTuple for complex cases
    """
    items: List[str]
    total: float
    
    def add_item(self, item: str, price: float) -> 'ShoppingCart':
        """
        Add an item to the cart and return a new cart.
        
        This method demonstrates immutability by creating a new ShoppingCart
        instance with the updated items and total, rather than modifying
        the current instance.
        
        Args:
            item: Name of the item to add (must be non-empty string)
            price: Price of the item (must be non-negative)
            
        Returns:
            ShoppingCart: A new cart with the item added
            
        Raises:
            ValueError: If item is empty or price is negative
            
        Examples:
            >>> cart = ShoppingCart([], 0.0)
            >>> cart = cart.add_item("Apple", 1.50)
            >>> len(cart.items)
            1
            >>> cart.total
            1.5
            >>> cart = cart.add_item("Banana", 0.99)
            >>> len(cart.items)
            2
            >>> cart.total
            2.49
            
        Note:
            - Pure function: No side effects, deterministic
            - Returns a new ShoppingCart instance
            - Original cart remains unchanged
            - Time complexity: O(n) where n is number of items (due to list concatenation)
            - Space complexity: O(n) (creates a new list)
        """
        if not item:
            raise ValueError("Item name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
            
        new_items = self.items + [item]
        return ShoppingCart(new_items, self.total + price)
    
    def remove_item(self, item: str, price: float) -> 'ShoppingCart':
        """
        Remove an item from the cart and return a new cart.
        
        This method demonstrates how to handle removal from an immutable
        collection by creating a new list without the specified item.
        
        Args:
            item: Name of the item to remove (must exist in cart)
            price: Price of the item (must match the original price)
            
        Returns:
            ShoppingCart: A new cart with the item removed
            
        Raises:
            ValueError: If item is not in the cart or price doesn't match
            
        Examples:
            >>> cart = ShoppingCart(["Apple", "Banana"], 2.49)
            >>> cart = cart.remove_item("Apple", 1.50)
            >>> cart.items
            ['Banana']
            >>> cart.total
            0.99
            
        Note:
            - Pure function: No side effects, deterministic
            - Returns a new ShoppingCart instance
            - Original cart remains unchanged
            - Time complexity: O(n) where n is number of items
            - Space complexity: O(n) (creates a new list)
        """
        if item not in self.items:
            raise ValueError(f"Item '{item}' not in cart")
            
        # In a real application, you might want to track item prices separately
        # to handle cases where the same item has different prices
        expected_total = self.total - price
        if expected_total < 0:
            raise ValueError("Price would result in negative total")
            
        new_items = self.items.copy()
        new_items.remove(item)
        return ShoppingCart(new_items, expected_total)

if __name__ == "__main__":
    print("=== Immutable Data Structures Examples ===\n")
    
    # 1. Demonstrating basic immutability with tuples
    print("1. Working with tuples (immutable sequences):")
    original_point = (3, 4)
    moved_point = move_point(original_point, 1, 2)
    
    print(f"Original point: {original_point}")
    print(f"After moving by (1, 2): {moved_point}")
    print(f"Same object? {original_point is moved_point}")
    print(f"Original unchanged? {original_point == (3, 4)}")
    
    # 2. Using NamedTuple for structured data
    print("\n2. Using NamedTuple for immutable records:")
    alice = Person("Alice", 30, "alice@example.com")
    alice_older = celebrate_birthday(alice)
    
    print(f"Original: {alice.name}, age {alice.age}")
    print(f"After birthday: {alice_older.name}, age {alice_older.age}")
    print(f"Same object? {alice is alice_older}")
    print(f"Original unchanged? {alice.age == 30}")
    
    # 3. Using frozen dataclass for complex structures
    print("\n3. Using @dataclass(frozen=True) for complex immutable objects:")
    
    # Create a new cart and add items
    print("\nCreating a shopping cart...")
    cart = ShoppingCart([], 0.0)
    print(f"Initial cart: {len(cart.items)} items, total: ${cart.total:.2f}")
    
    # Add some items
    cart = cart.add_item("Apple", 1.50)
    cart = cart.add_item("Banana", 0.99)
    cart = cart.add_item("Orange", 1.25)
    print(f"Cart items: {cart.items}, Total: ${cart.total:.2f}")
    
    # 4. Demonstrating immutability
    print("\n4. Demonstrating immutability:")
    
    # Original point is unchanged
    print(f"Original point still (3, 4)? {original_point == (3, 4)}")
    
    # Original person is unchanged
    print(f"Alice's age still 30? {alice.age == 30}")
    
    # Original cart is unchanged
    empty_cart = ShoppingCart([], 0.0)
    print(f"Empty cart still empty? {len(empty_cart.items) == 0}")
    
    # 5. Error handling examples
    print("\n5. Error handling examples:")
    
    try:
        # Try to add item with negative price
        cart.add_item("Invalid", -1.00)
    except ValueError as e:
        print(f"Error adding item: {e}")
    
    try:
        # Try to remove non-existent item
        cart.remove_item("Nonexistent", 0.00)
    except ValueError as e:
        print(f"Error removing item: {e}")
    
    # 6. Performance considerations
    print("\n6. Performance considerations:")
    print("- Creating many new objects has memory overhead")
    print("- But enables better caching and optimization opportunities")
    print("- Often the benefits of immutability outweigh the costs")
    
    # 7. Verifying immutability with assertions
    print("\n7. Verifying immutability with assertions...")
    
    # Original cart remains unchanged after operations
    cart_after_operations = cart.add_item("Test", 1.0)
    assert "Test" in cart_after_operations.items
    assert "Test" not in cart.items  # Original unchanged
    assert len(cart_after_operations.items) == len(cart.items) + 1
    
    # Verify function purity
    p1 = (1, 2)
    p2 = move_point(p1, 0, 0)
    assert p1 == p2  # Same value
    assert p1 is not p2  # But different objects
    
    print("\nAll tests passed! All data structures are immutable as expected.")
