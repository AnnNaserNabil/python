def format_line(line):
    # This function demonstrates function chaining, a common pattern in functional programming
    # Each method is called on the result of the previous method, creating a pipeline of transformations
    # 1. strip() - Removes whitespace from both ends (pure function)
    # 2. upper() - Converts to uppercase (pure function)
    # 3. replace() - Removes all periods (pure function)
    # 4. Adds '...' at the end
    # 
    # Note: Each operation returns a new string (immutability) and doesn't modify the original
    return f"{line.strip().upper().replace('.', '')}..."

# Test the function with various inputs
# In functional programming, we often use higher-order functions for testing
# Here we're using a list of test cases to verify our pure function
print("Testing the fixed format_line function:")
print()

# Test cases to demonstrate the fixes
# This is a list of input-output pairs that we'll use to test our function
# The function should handle each case correctly according to functional principles
test_lines = [
    "  hello world.  ",  # Tests whitespace and period removal
    "this has periods...",  # Tests multiple periods
    "  mixed case text.  ",  # Tests case conversion
    "no periods here",  # Tests no periods case
    "   multiple   spaces   and   periods...   "  # Tests multiple spaces and periods
]

print("Original buggy version results (for comparison):")
def buggy_format_line(line):
    # This is the original buggy version shown for comparison
    # Demonstrates why immutability is important - the original function had side effects
    # and didn't handle all cases correctly
    return f"{line.rstrip().capitalize().replace(',', '')}...."

for test in test_lines:
    result = buggy_format_line(test)
    print(f"'{test}' -> '{result}'")

print("\nFixed version results (functional approach):")
# Using a simple loop to demonstrate the functional approach
# In a more complex scenario, we might use map() or list comprehensions
for test in test_lines:
    # Each call to format_line is independent and has no side effects
    result = format_line(test)
    print(f"'{test}' -> '{result}'")