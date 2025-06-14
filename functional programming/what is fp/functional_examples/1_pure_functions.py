"""
1. Pure Functions

A pure function is a function that:
1. Always produces the same output for the same input
2. Has no side effects (doesn't modify external state)
3. Only depends on its input parameters
"""

# Example 1: A pure function
def add(a, b):
    """
    A pure function that adds two numbers.
    - Same input always produces same output
    - No side effects
    - Only depends on its input parameters
    """
    return a + b

# Example 2: Impure function (has side effect)
total = 0
def impure_add(a, b):
    """
    An impure function that modifies external state.
    - Modifies the global variable 'total'
    - Has side effects
    - Not referentially transparent
    """
    global total
    total += a + b
    return total

# Example 3: Pure function with immutable data
def capitalize_names(names):
    """
    A pure function that processes a list of names.
    - Returns a new list instead of modifying the input
    - No side effects
    - Original list remains unchanged
    """
    return [name.title() for name in names]

# Testing the functions
if __name__ == "__main__":
    # Test pure add function
    print("Pure add function:")
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"add(2, 3) = {add(2, 3)}")  # Same input, same output
    
    # Test impure add function
    print("\nImpure add function:")
    print(f"impure_add(2, 3) = {impure_add(2, 3)}")
    print(f"impure_add(2, 3) = {impure_add(2, 3)}")  # Same input, different output!
    
    # Test pure function with immutable data
    print("\nPure function with immutable data:")
    names = ["alice", "bob", "charlie"]
    capitalized = capitalize_names(names)
    print(f"Original names: {names}")
    print(f"Capitalized: {capitalized}")
