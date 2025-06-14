def hex_to_rgb(hex_color):
    # This is a pure function that converts a hex color string to RGB values
    # It follows functional programming principles:
    # 1. It's deterministic - same input always produces same output
    # 2. No side effects - doesn't modify any external state
    # 3. Input validation - validates input before processing
    
    # Check if input is a string first
    # This is a guard clause - a common pattern in functional programming
    if not isinstance(hex_color, str):
        raise Exception("not a hex color string")
        
    # Check length first for early return (another guard clause)
    if len(hex_color) != 6:
        raise Exception("not a hex color string")
        
    # Validate that the string is actually hexadecimal
    if not is_hexadecimal(hex_color):
        raise Exception("not a hex color string")
    
    # Convert hex pairs to RGB values using base 16 (hexadecimal)
    # Each pair of characters represents one color channel (Red, Green, Blue)
    # We use string slicing to extract each pair
    r = int(hex_color[0:2], 16)  # First two characters for Red
    g = int(hex_color[2:4], 16)  # Next two for Green
    b = int(hex_color[4:6], 16)  # Last two for Blue
    
    # Return a tuple of the RGB values
    # Tuples are immutable, which aligns with functional programming principles
    return r, g, b

# Don't edit below this line
def is_hexadecimal(hex_string):
    # Helper pure function that checks if a string is a valid hexadecimal number
    # This is a predicate function - it returns True or False based on a condition
    # It's used for input validation in the main function
    try:
        # Try to convert the string to an integer using base 16 (hexadecimal)
        # If this succeeds, it's a valid hex string
        int(hex_string, 16)
        return True
    except Exception:
        # If conversion fails, it's not a valid hex string
        return False

# Test the function
# In functional programming, we often separate pure functions from side effects (like printing)
# Here we're keeping the I/O separate from the pure logic
print("Testing hex_to_rgb function:")
print()

# Test the example case
# The function is pure, so we can be confident that calling it with the same input
# will always produce the same output
red_val, green_val, blue_val = hex_to_rgb("A020F0")
print(f"hex_to_rgb('A020F0') -> R: {red_val}, G: {green_val}, B: {blue_val}")
print(f"Expected: R: 160, G: 32, B: 240")
print()

# Test other cases
# Using a list of test cases is a functional approach to testing
# Each test case is a tuple of (input, expected_output)
test_cases = [
    "FF0000",  # Red
    "00FF00",  # Green  
    "0000FF",  # Blue
    "FFFFFF",  # White
    "000000",  # Black
]  # Note: In a more complex scenario, we might use a list of (input, expected_output) tuples

# Process each test case
# In functional programming, we'd typically use map() for this,
# but a for loop is used here for clarity
for hex_code in test_cases:
    # The function is pure, so we can call it with the same input multiple times
    # and always get the same result
    r, g, b = hex_to_rgb(hex_code)
    print(f"hex_to_rgb('{hex_code}') -> R: {r}, G: {g}, B: {b}")

# Test error cases
print("\nTesting error cases:")
try:
    hex_to_rgb("GGGGGG")  # Invalid hex
except Exception as e:
    print(f"hex_to_rgb('GGGGGG') -> Exception: {e}")

try:
    hex_to_rgb("FF00")  # Too short
except Exception as e:
    print(f"hex_to_rgb('FF00') -> Exception: {e}")