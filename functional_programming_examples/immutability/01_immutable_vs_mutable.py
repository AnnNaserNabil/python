"""
1. Immutable vs Mutable Types

Understanding the difference between immutable and mutable types in Python.
- Immutable types: int, float, str, tuple, frozenset, bytes
- Mutable types: list, dict, set, bytearray, custom classes
"""

def demonstrate_immutable():
    """
    Show how immutable types work in Python.
    Variables with immutable types cannot be changed in-place.
    """
    # Immutable examples
    x = 10
    print(f"Original x: {x}, id: {id(x)}")
    
    # This creates a new object, doesn't modify the existing one
    x = x + 5
    print(f"After addition: {x}, id: {id(x)} (new object)")
    
    # Strings are also immutable
    s = "hello"
    print(f"\nOriginal s: {s}, id: {id(s)}")
    
    # This creates a new string
    s = s + " world"
    print(f"After concatenation: {s}, id: {id(s)} (new object)")
    
    # Tuples are immutable
    t = (1, 2, 3)
    print(f"\nOriginal tuple: {t}, id: {id(t)}")
    
    # This creates a new tuple
    t = t + (4, 5)
    print(f"After addition: {t}, id: {id(t)} (new object)")

def demonstrate_mutable():
    """
    Show how mutable types work in Python.
    Variables with mutable types can be changed in-place.
    """
    # List is mutable
    lst = [1, 2, 3]
    print(f"\nOriginal list: {lst}, id: {id(lst)}")
    
    # This modifies the list in-place
    lst.append(4)
    print(f"After append: {lst}, id: {id(lst)} (same object)")
    
    # Dictionary is also mutable
    d = {'a': 1, 'b': 2}
    print(f"\nOriginal dict: {d}, id: {id(d)}")
    
    # This modifies the dict in-place
    d['c'] = 3
    print(f"After adding key: {d}, id: {id(d)} (same object)")

def demonstrate_shared_references():
    """
    Show how mutable objects can lead to unexpected behavior when shared.
    """
    # Two variables referencing the same list
    a = [1, 2, 3]
    b = a  # b references the same list as a
    
    print(f"\na: {a}, id: {id(a)}")
    print(f"b: {b}, id: {id(b)}")
    
    # Modifying through one reference affects the other
    a.append(4)
    print("\nAfter modifying a:")
    print(f"a: {a}, id: {id(a)}")
    print(f"b: {b}, id: {id(b)}")
    
    # With immutable types, this doesn't happen
    x = 10
    y = x  # y gets a copy of the value
    x = x + 5
    print(f"\nx: {x}, y: {y}")

# Example usage
if __name__ == "__main__":
    print("=== Immutable Types ===")
    demonstrate_immutable()
    
    print("\n=== Mutable Types ===")
    demonstrate_mutable()
    
    print("\n=== Shared References ===")
    demonstrate_shared_references()
    
    # Key takeaways
    print("\n=== Key Takeaways ===")
    print("1. Immutable types (int, str, tuple) cannot be changed in-place")
    print("2. Operations on immutable types create new objects")
    print("3. Mutable types (list, dict, set) can be changed in-place")
    print("4. Multiple variables can reference the same mutable object")
    print("5. Changes to a mutable object are visible through all references")
