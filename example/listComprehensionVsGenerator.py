#!/usr/bin/env python3
"""
📚 List Comprehensions vs Generator Expressions - BEGINNER FRIENDLY
10 Examples Each - With Detailed Comments for New Programmers

🎯 WHAT ARE THESE?
- List Comprehension: A shortcut to create lists (uses square brackets [])
- Generator Expression: A memory-efficient way to create data one piece at a time (uses parentheses ())

Think of it like:
- List = Making a complete shopping list on paper (takes space, but you can see everything)
- Generator = Remembering items one by one as you shop (saves memory, but you get items as needed)
"""

import sys  # This helps us check memory usage
import time  # This helps us measure how fast our code runs
from functools import reduce  # This helps with mathematical operations

# 🔥 LIST COMPREHENSIONS - Creates complete lists RIGHT NOW
print("🔥 LIST COMPREHENSIONS (Makes complete lists immediately)")
print("=" * 50)

# 1. BASIC MATH - Make a list of squared numbers
# Old way: squares_list = []
#          for x in range(10):
#              squares_list.append(x**2)
# New way (list comprehension):
squares_list = [x**2 for x in range(10)]  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
print("1. Squares of 0-9:", squares_list)
# This creates ALL squares at once and stores them in memory

# 2. FILTERING - Keep only even numbers
# This means: "Give me x, but only if x divided by 2 has no remainder"
evens_list = [x for x in range(20) if x % 2 == 0]
print("2. Even numbers 0-19:", evens_list)
# The "if x % 2 == 0" part is like a filter - it only keeps even numbers

# 3. TEXT PROCESSING - Convert words to uppercase
words = ["python", "java", "javascript", "go"]  # Our original list
# This says: "Take each word and make it UPPERCASE"
uppercase_list = [word.upper() for word in words]
print("3. Uppercase words:", uppercase_list)

# 4. NESTED LOOPS - Make pairs of numbers (like coordinates)
# This is like: for x in range(3):
#                   for y in range(3):
#                       make pair (x,y)
cartesian_list = [(x, y) for x in range(3) for y in range(3)]
print("4. All number pairs (0-2):", cartesian_list)
# Creates pairs like (0,0), (0,1), (0,2), (1,0), etc.

# 5. WORKING WITH DICTIONARIES - Extract high scores
scores = {"Alice": 95, "Bob": 87, "Charlie": 92, "Diana": 98}
# This says: "Give me the score, but only if it's 90 or higher"
high_scores_list = [score for score in scores.values() if score >= 90]
print("5. Scores 90 and above:", high_scores_list)
# scores.values() gets just the numbers: [95, 87, 92, 98]

# 6. FINDING POSITIONS - Where are the vowels in this sentence?
sentence = "The quick brown fox jumps over the lazy dog"
# enumerate() gives us both position (i) and character (char)
# We only want positions where the character is a vowel
vowel_positions_list = [i for i, char in enumerate(sentence) if char.lower() in 'aeiou']
print("6. Vowel positions in sentence:", vowel_positions_list)

# 7. ADVANCED MATH - Calculate factorials (1!, 2!, 3!, etc.)
numbers = [1, 2, 3, 4, 5]
# Factorial of 5 = 5 × 4 × 3 × 2 × 1 = 120
# reduce() multiplies all numbers in a range together
factorial_approximation_list = [reduce(lambda a, b: a * b, range(1, n + 1)) for n in numbers]
print("7. Factorials (1! to 5!):", factorial_approximation_list)

# 8. COMPLEX FILTERING - Find people who meet multiple conditions
data = [{"name": "Alice", "age": 25, "city": "NYC"}, 
        {"name": "Bob", "age": 30, "city": "LA"}, 
        {"name": "Charlie", "age": 35, "city": "NYC"}]
# This says: "Give me names of people who are 25+ years old AND live in NYC"
nyc_adults_list = [person["name"] for person in data if person["age"] >= 25 and person["city"] == "NYC"]
print("8. Adults living in NYC:", nyc_adults_list)

# 9. FLATTENING LISTS - Turn a 2D list into a 1D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Like a tic-tac-toe board
# This takes each row, then each item in that row, and puts them all in one list
flattened_list = [item for row in matrix for item in row]
print("9. Flattened matrix:", flattened_list)
# Turns [[1,2,3], [4,5,6], [7,8,9]] into [1,2,3,4,5,6,7,8,9]

# 10. FILE PROCESSING - Find specific file types
files = ["document.pdf", "image.jpg", "script.py", "data.csv", "photo.png"]
# Find Python files (ending with .py or .pyw)
python_files_list = [f for f in files if f.endswith(('.py', '.pyw'))]
# Get file extensions for non-Python files
other_extensions_list = [f.split('.')[-1] for f in files if not f.endswith(('.py', '.pyw'))]
print("10. Python files:", python_files_list)
print("    Other file extensions:", other_extensions_list)

# Check how much memory our list uses
print(f"\n💾 Memory used by squares_list: {sys.getsizeof(squares_list)} bytes")
print("(This list is stored completely in your computer's memory)")

print("\n" + "="*70 + "\n")

# ⚡ GENERATOR EXPRESSIONS - Creates items ONE AT A TIME when needed
print("⚡ GENERATOR EXPRESSIONS (Makes items one-by-one when needed)")
print("=" * 50)

# 1. BASIC SQUARES - But this time, we don't make the whole list at once
squares_gen = (x**2 for x in range(10))  # Notice: () instead of []
print("1. Squares generator object:", squares_gen)
print("   This doesn't show the numbers yet! It's like a recipe, not the actual food.")
# To get the actual numbers, we need to ask for them:
print("   First 5 squares:", [next(squares_gen) for _ in range(5)])
print("   (Each time we call next(), it calculates ONE square)")

# 2. FILTERING EVENS - Same logic, but with ()
evens_gen = (x for x in range(20) if x % 2 == 0)
print("2. Even numbers generator:", list(evens_gen))
print("   (We used list() to convert the generator to a list so we can see all items)")

# 3. TEXT PROCESSING - Same as before, but memory efficient
uppercase_gen = (word.upper() for word in words)
print("3. Uppercase generator:", list(uppercase_gen))

# 4. NESTED LOOPS - Same pairs, but calculated when needed
cartesian_gen = ((x, y) for x in range(3) for y in range(3))
print("4. Cartesian generator:", list(cartesian_gen))

# 5. DICTIONARY PROCESSING - Same filtering, but one score at a time
high_scores_gen = (score for score in scores.values() if score >= 90)
print("5. High scores generator:", list(high_scores_gen))

# 6. STRING PROCESSING - Same vowel finding, but lazily
vowel_positions_gen = (i for i, char in enumerate(sentence) if char.lower() in 'aeiou')
print("6. Vowel positions generator:", list(vowel_positions_gen))

# 7. MATHEMATICAL OPERATIONS - Same factorials, but calculated on demand
factorial_gen = (reduce(lambda a, b: a * b, range(1, n + 1)) for n in numbers)
print("7. Factorials generator:", list(factorial_gen))

# 8. COMPLEX FILTERING - Same logic, but memory efficient
nyc_adults_gen = (person["name"] for person in data if person["age"] >= 25 and person["city"] == "NYC")
print("8. NYC adults generator:", list(nyc_adults_gen))

# 9. MATRIX FLATTENING - Same flattening, but item by item
flattened_gen = (item for row in matrix for item in row)
print("9. Flattened generator:", list(flattened_gen))

# 10. LARGE NUMBERS - This is where generators really shine!
# Imagine we want to work with squares of numbers from 0 to 999,999
large_squares_gen = (x**2 for x in range(1000000))  # 1 million numbers!
print("10. Large squares generator:", large_squares_gen)
print("    This generator can handle 1 MILLION squares without using much memory!")
print("    First 5 large squares:", [next(large_squares_gen) for _ in range(5)])
print("    (It only calculates squares when we ask for them)")

# Check memory usage - this will be MUCH smaller than a list!
print(f"\n💾 Memory used by squares_gen: {sys.getsizeof(squares_gen)} bytes")
print("(This is just the 'recipe' - the actual numbers aren't stored in memory yet)")

print("\n" + "="*70 + "\n")

# 🚀 PERFORMANCE COMPARISON - Let's see the difference!
print("🚀 PERFORMANCE AND MEMORY COMPARISON")
print("=" * 50)

def time_comparison():
    """Compare how fast and memory-efficient each approach is"""
    n = 100000  # Let's test with 100,000 numbers
    
    # LIST COMPREHENSION - Make the whole list RIGHT NOW
    print(f"🧪 Creating {n:,} squared numbers...")
    
    start_time = time.time()  # Start the timer
    squares_list = [x**2 for x in range(n)]  # Create ALL squares immediately
    list_creation_time = time.time() - start_time  # Stop the timer
    list_memory = sys.getsizeof(squares_list)  # Check memory usage
    
    # GENERATOR EXPRESSION - Just create the "recipe"
    start_time = time.time()  # Start the timer
    squares_gen = (x**2 for x in range(n))  # Create just the generator
    gen_creation_time = time.time() - start_time  # Stop the timer
    gen_memory = sys.getsizeof(squares_gen)  # Check memory usage
    
    print(f"📊 CREATION RESULTS:")
    print(f"List (makes everything now): {list_creation_time:.6f} seconds, {list_memory:,} bytes")
    print(f"Generator (makes recipe): {gen_creation_time:.6f} seconds, {gen_memory:,} bytes")
    print(f"💡 Memory saved by generator: {list_memory - gen_memory:,} bytes!")
    
    # Now let's time how long it takes to ADD UP all the numbers
    squares_gen = (x**2 for x in range(n))  # Create a fresh generator
    
    print(f"\n🧮 Adding up all {n:,} squares...")
    
    start_time = time.time()
    list_sum = sum(squares_list)  # Add up the list (already exists)
    list_sum_time = time.time() - start_time
    
    start_time = time.time()
    gen_sum = sum(squares_gen)  # Add up the generator (calculates as it goes)
    gen_sum_time = time.time() - start_time
    
    print(f"📊 SUMMING RESULTS:")
    print(f"List sum: {list_sum_time:.6f} seconds")
    print(f"Generator sum: {gen_sum_time:.6f} seconds")
    print(f"✅ Both got the same answer: {list_sum:,}")

time_comparison()

print("\n" + "="*70 + "\n")

# 💡 WHEN TO USE EACH - A beginner's guide
print("💡 WHEN TO USE EACH - BEGINNER'S GUIDE")
print("=" * 50)

print("📋 USE LIST COMPREHENSIONS [ ] WHEN:")
print("• 🎯 You need ALL the data right now")
print("• 🔄 You'll look at the data multiple times")
print("• 📏 You need to know how many items there are (len())")
print("• 🎲 You need to access items by position (my_list[5])")
print("• 📊 You're working with small amounts of data")
print("• Example: Making a list of your friends' names")

print("\n⚡ USE GENERATOR EXPRESSIONS ( ) WHEN:")
print("• 💾 You're working with LOTS of data")
print("• 🔄 You only need to go through the data once")
print("• 💰 You want to save memory")
print("• ⏰ You want to start working with data before it's all ready")
print("• 🔗 You're passing data to functions like sum(), max(), min()")
print("• Example: Processing a huge file line by line")

print("\n🎯 REAL-WORLD EXAMPLES:")

# Example 1: Small data - use list comprehension
print("\n1️⃣ SMALL DATA EXAMPLE - List Comprehension:")
favorite_numbers = [7, 13, 21, 42]
doubled_numbers = [num * 2 for num in favorite_numbers]  # Creates: [14, 26, 42, 84]
print(f"   My favorite numbers: {favorite_numbers}")
print(f"   Doubled: {doubled_numbers}")
print(f"   I can access any number: doubled_numbers[0] = {doubled_numbers[0]}")
print("   ✅ Good choice! Small data, need to access multiple times")

# Example 2: Large data - use generator expression
print("\n2️⃣ LARGE DATA EXAMPLE - Generator Expression:")
def process_large_dataset():
    # Imagine processing millions of sensor readings
    sensor_readings = (reading * 1.8 + 32 for reading in range(1000000))  # Convert Celsius to Fahrenheit
    
    # We only want readings above 100°F
    hot_readings = (temp for temp in sensor_readings if temp > 100)
    
    # Find the average of the first 1000 hot readings
    first_thousand_hot = [next(hot_readings) for _ in range(1000)]
    average_temp = sum(first_thousand_hot) / len(first_thousand_hot)
    
    return average_temp

average = process_large_dataset()
print(f"   Average of first 1000 hot readings: {average:.2f}°F")
print("   ✅ Good choice! Large data, only needed once, memory efficient")

# Example 3: Chain multiple operations
print("\n3️⃣ CHAINING OPERATIONS - Generator Pipeline:")
def create_data_pipeline():
    """Show how generators can work together like an assembly line"""
    # Step 1: Generate numbers
    numbers = (x for x in range(1000))
    print("   Step 1: Created number generator (0 to 999)")
    
    # Step 2: Square them
    squares = (x**2 for x in numbers)
    print("   Step 2: Created squares generator")
    
    # Step 3: Keep only even squares
    even_squares = (x for x in squares if x % 2 == 0)
    print("   Step 3: Created even squares filter")
    
    # Step 4: Keep only large ones
    large_even_squares = (x for x in even_squares if x > 10000)
    print("   Step 4: Created large even squares filter")
    
    # Step 5: Take just the first 10
    result = []
    for i, value in enumerate(large_even_squares):
        if i >= 10:  # Stop after 10 items
            break
        result.append(value)
    
    return result

pipeline_result = create_data_pipeline()
print(f"   Final result (first 10): {pipeline_result}")
print("   ✅ Each step only calculates what's needed for the next step!")

print("\n🎓 SUMMARY FOR BEGINNERS:")
print("List Comprehension []: Like making a complete grocery list on paper")
print("Generator Expression (): Like remembering grocery items as you shop")
print("Both do the same job, but generators save memory for big tasks!")
print("\n🚀 Start with lists for learning, use generators when you need efficiency!")