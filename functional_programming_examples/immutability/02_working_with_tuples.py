"""
2. Working with Tuples

Immutable sequences in Python.
- Creating and accessing tuples
- Tuple operations
- When to use tuples vs lists
"""
from typing import Tuple, List, Any

def tuple_creation() -> None:
    """Demonstrate different ways to create tuples."""
    # Empty tuple
    empty = ()
    print(f"Empty tuple: {empty}")
    
    # Single element tuple (note the trailing comma)
    single = (42,)
    print(f"Single element: {single}")
    
    # Multiple elements
    coordinates = (10, 20)
    print(f"Coordinates: {coordinates}")
    
    # Without parentheses (tuple packing)
    colors = 'red', 'green', 'blue'
    print(f"Colors: {colors}")
    
    # From other sequences
    numbers = tuple([1, 2, 3, 4, 5])
    print(f"From list: {numbers}")

def tuple_operations() -> None:
    """Show common operations with tuples."""
    # Accessing elements
    point = (3, 4, 5)
    print(f"First element: {point[0]}")
    print(f"Last element: {point[-1]}")
    
    # Slicing
    print(f"First two: {point[:2]}")
    
    # Length
    print(f"Length: {len(point)}")
    
    # Concatenation (creates a new tuple)
    new_point = point + (6, 7)
    print(f"After concatenation: {new_point}")
    
    # Repetition
    print(f"Repeated: {point * 2}")
    
    # Membership
    print(f"Contains 4: {4 in point}")
    print(f"Contains 10: {10 in point}")

def tuple_unpacking() -> None:
    """Show tuple unpacking and extended unpacking."""
    # Basic unpacking
    x, y = (10, 20)
    print(f"x: {x}, y: {y}")
    
    # Extended unpacking (Python 3+)
    first, *rest = (1, 2, 3, 4, 5)
    print(f"First: {first}, Rest: {rest}")
    
    # Multiple elements and rest
    a, b, *rest, c = (1, 2, 3, 4, 5, 6)
    print(f"a: {a}, b: {b}, rest: {rest}, c: {c}")
    
    # Swapping variables
    x, y = 5, 10
    print(f"Before swap: x={x}, y={y}")
    x, y = y, x
    print(f"After swap: x={x}, y={y}")

def immutable_but_contains_mutable() -> None:
    """Show that while tuples are immutable, their contents might be mutable."""
    # Tuple with a list inside
    mixed = (1, 2, [3, 4])
    print(f"Original tuple: {mixed}")
    
    # The tuple itself is immutable
    try:
        mixed[0] = 10  # This will raise TypeError
    except TypeError as e:
        print(f"Cannot modify tuple: {e}")
    
    # But the list inside can be modified
    mixed[2].append(5)
    print(f"After modifying inner list: {mixed}")

def use_cases() -> None:
    """Common use cases for tuples."""
    # 1. Return multiple values from a function
    def get_coordinates() -> Tuple[int, int]:
        return (10, 20)
    
    x, y = get_coordinates()
    print(f"Coordinates: ({x}, {y})")
    
    # 2. Dictionary keys (must be immutable)
    locations = {
        (35.6895, 139.6917): "Tokyo",
        (40.7128, 74.0060): "New York"
    }
    print(f"Location: {locations[(35.6895, 139.6917)]}")
    
    # 3. Function arguments (as a lightweight record)
    def process_data(data: Tuple[str, int, List[float]]) -> None:
        name, count, values = data
        print(f"Processing {count} items for {name}: {values}")
    
    data = ("sensor1", 3, [22.5, 23.1, 24.0])
    process_data(data)

# Example usage
if __name__ == "__main__":
    print("=== Tuple Creation ===")
    tuple_creation()
    
    print("\n=== Tuple Operations ===")
    tuple_operations()
    
    print("\n=== Tuple Unpacking ===")
    tuple_unpacking()
    
    print("\n=== Immutable but Contains Mutable ===")
    immutable_but_contains_mutable()
    
    print("\n=== Common Use Cases ===")
    use_cases()
    
    # When to use tuples vs lists
    print("\n=== Tuples vs Lists ===")
    print("Use tuples when:")
    print("- The data shouldn't change (e.g., days of the week)")
    print("- You need to use it as a dictionary key")
    print("- You're returning multiple values from a function")
    print("- You want to ensure the data can't be modified")
    print("\nUse lists when:")
    print("- You need to modify the collection")
    print("- You need to add/remove items")
    print("- The order of items might change")
