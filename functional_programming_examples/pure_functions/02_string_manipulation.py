"""
2. String Manipulation with Pure Functions

This module demonstrates pure functions for string manipulation in Python.
Pure functions are functions that:
1. Always produce the same output for the same input
2. Have no side effects (don't modify external state)
3. Depend only on their input parameters

Key Concepts:
------------
- Immutability: Strings in Python are immutable, making them naturally
  compatible with pure functional programming.
- Function Purity: These functions don't modify their inputs and have no side effects.
- Composability: Pure functions can be easily composed together.

Why Use Pure Functions for String Manipulation?
--------------------------------------------
- Predictable behavior
- Easier to test and debug
- Thread-safe by design
- Enable function composition
- Make code more maintainable

Real-world Applications:
----------------------
- Text processing and analysis
- Data cleaning and transformation
- Input validation and sanitization
- Template rendering
- Natural language processing

Example:
-------
>>> reverse_string("hello")
'olleh'
>>> count_vowels("Python")
1
>>> is_palindrome("radar")
True
"""

def reverse_string(s: str) -> str:
    """
    Reverse the characters in a string.
    
    This is a pure function because:
    - It always returns the same output for the same input
    - It doesn't modify the input string (strings are immutable in Python)
    - It has no side effects
    - It depends only on its input parameter
    
    Args:
        s: The string to be reversed. Can be any valid string including empty string.
        
    Returns:
        str: A new string with characters in reverse order
        
    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("Python")
        'nohtyP'
        >>> reverse_string("")
        ''
        >>> reverse_string("a")
        'a'
        
    Note:
        - Uses Python's string slicing with step -1 to reverse the string
        - Original string remains unchanged (strings are immutable in Python)
    """
    return s[::-1]

def count_vowels(s: str) -> int:
    """
    Count the number of vowels in a string (case-insensitive).
    
    This is a pure function because:
    - It always returns the same output for the same input
    - It doesn't modify the input string
    - It has no side effects
    - It depends only on its input parameter
    
    Args:
        s: The string in which to count vowels. Can be any valid string.
        
    Returns:
        int: The count of vowels (a, e, i, o, u) in the string, case-insensitive
        
    Examples:
        >>> count_vowels("hello")
        2
        >>> count_vowels("Python")
        1
        >>> count_vowels("Rhythm")
        0
        >>> count_vowels("AEIOU")
        5
        
    Note:
        - Converts the string to lowercase for case-insensitive comparison
        - Only counts English vowels (a, e, i, o, u)
        - Returns 0 for empty string or strings with no vowels
    """
    vowels = {'a', 'e', 'i', 'o', 'u'}
    return sum(1 for char in s.lower() if char in vowels)

def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome (reads the same forwards and backwards).
    
    This is a pure function that:
    - Is case-insensitive
    - Considers only alphanumeric characters
    - Returns True for empty string or single character strings
    
    Args:
        s: The string to check
        
    Returns:
        bool: True if the string is a palindrome, False otherwise
        
    Examples:
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("race a car")
        False
        >>> is_palindrome("")
        True
        >>> is_palindrome("a")
        True
    """
    # Convert to lowercase and filter non-alphanumeric characters
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

# Example usage and tests
if __name__ == "__main__":
    print("=== String Manipulation with Pure Functions ===\n")
    
    # Test reverse_string
    test_strings = ["hello", "Python", "", "a", "racecar"]
    for s in test_strings:
        print(f"Original: {s!r}")
        print(f"Reversed: {reverse_string(s)!r}")
    
    # Test count_vowels
    print("\n=== Vowel Count ===")
    test_cases = [
        ("hello", 2),
        ("Python", 1),
        ("AEIOU", 5),
        ("xyz", 0),
        ("", 0)
    ]
    
    for s, expected in test_cases:
        result = count_vowels(s)
        print(f"'{s}': {result} vowels")
        assert result == expected, f"Expected {expected} vowels in '{s}', got {result}"
    
    # Test is_palindrome
    print("\n=== Palindrome Check ===")
    palindrome_tests = [
        ("A man a plan a canal Panama", True),
        ("race a car", False),
        ("", True),
        ("a", True),
        ("No 'x' in Nixon", True),
        ("Python", False)
    ]
    
    for s, expected in palindrome_tests:
        result = is_palindrome(s)
        print(f"'{s}': {'Is' if result else 'Is not'} a palindrome")
        assert result == expected, f"Expected {expected} for '{s}'"
    
    print("\nAll tests passed! All functions are pure.")
