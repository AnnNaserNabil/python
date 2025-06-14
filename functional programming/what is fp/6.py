def file_to_prompt(file, to_string):
    # This is a higher-order function - it takes another function as an argument (to_string)
    # This is a key concept in functional programming
    
    # Call the passed-in function to convert the file to a string
    # The function doesn't care how to_string works, it just knows it can call it
    content = to_string(file)
    
    # Return the formatted string
    # This function is pure - it has no side effects and always returns the same output
    # for the same input (file and to_string function)
    return f"```\n{content}\n```"

# Test the function
# Here we define a simple function that will be passed to file_to_prompt
# This demonstrates how higher-order functions can work with different implementations
def example_to_string(file_dict):
    # This is a simple implementation that ignores the input and returns a fixed string
    # In a real application, this would extract and format the content from the file_dict
    return "an example string"

# Test case
# Create a sample file dictionary
file_dict = {"name": "example.txt", "content": "some content"}

# Call file_to_prompt, passing both the file and the to_string function
# This shows how functions can be passed as arguments, just like any other value
result = file_to_prompt(file_dict, example_to_string)

# Print the results
print("Result:")
print(result)
print()

# Show the expected format for comparison
print("Expected format:")
print("```")
print("an example string")
print("```")

# This example demonstrates several functional programming concepts:
# 1. Higher-order functions (functions that take other functions as arguments)
# 2. Pure functions (no side effects, same input always produces same output)
# 3. Function composition (building complex behavior by combining simple functions)
# 4. First-class functions (treating functions as values that can be passed around)