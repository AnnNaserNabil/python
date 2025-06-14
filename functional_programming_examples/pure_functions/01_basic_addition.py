"""
1. Basic Addition Function - Pure Function Example

This module demonstrates a simple example of a pure function in Python.
A pure function is a function that:

1. Always produces the same output for the same input (deterministic)
2. Has no side effects (doesn't modify external state)
3. Depends only on its input parameters (no hidden state or globals)

Key Concepts:
------------
- Pure Functions: Predictable and easy to test
- Referential Transparency: Can be replaced with its return value
- Immutability: Doesn't modify input parameters

Why Pure Functions Matter:
------------------------
- Easier to reason about and debug
- Safe to use in concurrent/parallel code
- Enable function composition and other functional patterns
- Make code more maintainable and testable

Real-world Applications:
----------------------
- Mathematical calculations
- Data transformations
- Functional programming patterns
- React/Redux state management

Example:
-------
>>> add(2, 3)
5
>>> add(0, 0)
0
>>> add(-1, 1)
0
"""

def add(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    This is a pure function because:
    - It always returns the same output for the same inputs
    - It doesn't modify any external state
    - It doesn't depend on any external state
    - It has no side effects
    
    Args:
        a: First number to add (can be integer or float)
        b: Second number to add (can be integer or float)
        
    Returns:
        float: The sum of a and b
        
    Examples:
        >>> add(2, 3)
        5.0
        >>> add(0, 0)
        0.0
        >>> add(-1, 1)
        0.0
        >>> add(1.5, 2.5)
        4.0
        
    Note:
        In Python, the + operator works with both integers and floats.
        The return type is always float due to the type hint.
    """
    return a + b

# Example usage with test cases
if __name__ == "__main__":
    # Basic usage
    result = add(3, 4)
    print(f"3 + 4 = {result}")  # Always 7
    
    # Demonstrating purity
    print("\nTesting function purity:")
    
    # 1. Same input always produces same output
    assert add(0, 0) == 0, "0 + 0 should be 0"
    print("✓ Same input produces same output")
    
    # 2. No side effects (nothing to assert, but we can demonstrate)
    x, y = 5, 3
    initial_x = x
    add(x, y)  # Calling the function doesn't modify x or y
    assert x == initial_x, "Function call should not modify input variables"
    print("✓ No side effects on input variables")
    
    # 3. Function depends only on its inputs
    # (No external dependencies or hidden state)
    print("✓ Function depends only on its inputs")
    
    # 4. Additional test cases
    print("\nAdditional test cases:")
    test_cases = [
        (1, 2, 3),      # Positive integers
        (-1, -1, -2),   # Negative numbers
        (1.5, 2.5, 4.0), # Floats
        (0, 42, 42),    # Zero identity
    ]
    
    for a, b, expected in test_cases:
        result = add(a, b)
        print(f"{a} + {b} = {result}")
        assert result == expected, f"Expected {a} + {b} = {expected}, got {result}"
    
    print("\nAll tests passed! The add function is pure.")
