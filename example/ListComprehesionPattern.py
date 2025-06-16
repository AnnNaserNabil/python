#!/usr/bin/env python3
"""
🎯 MASTERING THE LIST COMPREHENSION PATTERN: [x for x in data if condition]

This is THE most important pattern in Python list comprehensions!

🔍 ANATOMY OF THE PATTERN:
[x for x in data if condition]
 │   │      │        │
 │   │      │        └── Filter: Only include items that meet this condition
 │   │      └─────────── Source: Where we get our data from
 │   └────────────────── Loop: Go through each item one by one
 └────────────────────── Result: What we want to keep/transform

Think of it like: "Give me X, for each X in my data, but only if condition is true"
"""

# 🌟 BEGINNER EXAMPLES - From Simple to Advanced

print("🌟 BASIC FILTERING EXAMPLES")
print("=" * 50)

# Example 1: Filter numbers - Keep only even numbers
print("1️⃣ FILTERING NUMBERS:")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"   Original numbers: {numbers}")

# Pattern: [x for x in data if condition]
#          [x for x in numbers if x % 2 == 0]
even_numbers = [x for x in numbers if x % 2 == 0]
print(f"   Even numbers only: {even_numbers}")
print("   🔍 How it works: Go through each number, keep only if divisible by 2")
print()

# Example 2: Filter strings - Keep only short words
print("2️⃣ FILTERING WORDS BY LENGTH:")
words = ["cat", "elephant", "dog", "hippopotamus", "ant", "butterfly"]
print(f"   Original words: {words}")

# Keep words with 5 or fewer letters
short_words = [word for word in words if len(word) <= 5]
print(f"   Short words (≤5 letters): {short_words}")
print("   🔍 How it works: Check each word's length, keep if 5 letters or less")
print()

# Example 3: Filter by string content
print("3️⃣ FILTERING BY STRING CONTENT:")
fruits = ["apple", "banana", "orange", "grape", "pineapple", "strawberry"]
print(f"   All fruits: {fruits}")

# Keep fruits that contain the letter 'a'
fruits_with_a = [fruit for fruit in fruits if 'a' in fruit]
print(f"   Fruits containing 'a': {fruits_with_a}")
print("   🔍 How it works: Check if letter 'a' exists in each fruit name")
print()

print("=" * 70)
print("🔥 INTERMEDIATE EXAMPLES")
print("=" * 50)

# Example 4: Filter ages - Find adults
print("4️⃣ FILTERING AGES:")
ages = [12, 25, 17, 30, 16, 45, 19, 8, 22]
print(f"   All ages: {ages}")

# Keep ages 18 and above (adults)
adult_ages = [age for age in ages if age >= 18]
print(f"   Adult ages (18+): {adult_ages}")
print("   🔍 How it works: Check each age, keep if 18 or older")
print()

# Example 5: Filter grades - Find passing grades
print("5️⃣ FILTERING GRADES:")
grades = [85, 92, 67, 45, 78, 95, 88, 52, 73, 89]
print(f"   All grades: {grades}")

# Keep grades 70 and above (passing)
passing_grades = [grade for grade in grades if grade >= 70]
print(f"   Passing grades (70+): {passing_grades}")
print("   🔍 How it works: Check each grade, keep if 70 or above")
print()

# Example 6: Filter with multiple conditions
print("6️⃣ MULTIPLE CONDITIONS (AND):")
scores = [65, 85, 92, 78, 45, 88, 95, 72, 68, 90]
print(f"   All scores: {scores}")

# Keep scores between 70 and 90 (good but not perfect)
good_scores = [score for score in scores if score >= 70 and score <= 90]
print(f"   Good scores (70-90): {good_scores}")
print("   🔍 How it works: Check each score, keep if BOTH conditions are true")
print()

print("=" * 70)
print("🚀 ADVANCED EXAMPLES")
print("=" * 50)

# Example 7: Filter dictionaries - People data
print("7️⃣ FILTERING DICTIONARIES:")
people = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 17, "city": "Los Angeles"},
    {"name": "Charlie", "age": 30, "city": "New York"},
    {"name": "Diana", "age": 22, "city": "Chicago"},
    {"name": "Eve", "age": 16, "city": "New York"}
]
print("   People data:")
for person in people:
    print(f"     {person}")

# Keep only adults living in New York
ny_adults = [person for person in people if person["age"] >= 18 and person["city"] == "New York"]
print(f"\n   Adults in New York:")
for person in ny_adults:
    print(f"     {person}")
print("   🔍 How it works: Check each person, keep if age≥18 AND city='New York'")
print()

# Example 8: Extract specific values from dictionaries
print("8️⃣ EXTRACTING VALUES FROM DICTIONARIES:")
# Let's get just the NAMES of young people (under 25)
young_names = [person["name"] for person in people if person["age"] < 25]
print(f"   Names of people under 25: {young_names}")
print("   🔍 How it works: Check each person's age, keep their NAME if under 25")
print()

# Example 9: Filter file names
print("9️⃣ FILTERING FILE NAMES:")
files = [
    "document.pdf", "photo.jpg", "script.py", "data.csv", 
    "image.png", "code.py", "report.pdf", "music.mp3"
]
print(f"   All files: {files}")

# Keep only Python files (.py extension)
python_files = [file for file in files if file.endswith(".py")]
print(f"   Python files only: {python_files}")
print("   🔍 How it works: Check each filename, keep if it ends with '.py'")

# Keep only image files
image_extensions = [".jpg", ".png", ".gif", ".bmp"]
image_files = [file for file in files if any(file.endswith(ext) for ext in image_extensions)]
print(f"   Image files only: {image_files}")
print("   🔍 How it works: Check if filename ends with any image extension")
print()

# Example 10: Filter with mathematical conditions
print("🔟 MATHEMATICAL FILTERING:")
numbers = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
print(f"   All numbers: {numbers}")

# Keep perfect squares greater than 20
import math
large_squares = [num for num in numbers if num > 20 and math.sqrt(num) == int(math.sqrt(num))]
print(f"   Perfect squares > 20: {large_squares}")
print("   🔍 How it works: Check if number > 20 AND its square root is a whole number")
print()

print("=" * 70)
print("🎓 PATTERN VARIATIONS")
print("=" * 50)

# Show different ways to use the same pattern
sample_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("📝 BASIC PATTERN VARIATIONS:")
print(f"   Original data: {sample_data}")
print()

# 1. Simple filtering (keep as-is)
print("1. Keep the number as-is:")
evens = [x for x in sample_data if x % 2 == 0]
print(f"   [x for x in data if x % 2 == 0] = {evens}")
print()

# 2. Transform while filtering
print("2. Transform the number while filtering:")
even_squares = [x**2 for x in sample_data if x % 2 == 0]
print(f"   [x**2 for x in data if x % 2 == 0] = {even_squares}")
print("   (Square the number, but only even numbers)")
print()

# 3. Multiple transformations
print("3. Complex transformation:")
processed = [f"Number: {x*2}" for x in sample_data if x > 5]
print(f"   [f'Number: {{x*2}}' for x in data if x > 5] = {processed}")
print("   (Double the number, format as string, but only if > 5)")
print()

print("=" * 70)
print("🤔 COMMON BEGINNER MISTAKES & FIXES")
print("=" * 50)

print("❌ MISTAKE 1: Forgetting the condition")
# Wrong: all_numbers = [x for x in sample_data]  # This just copies the list
# Right: Use regular assignment for copying
print("   Wrong: [x for x in data]  # Just copies, no point!")
print("   Right: Use data.copy() or list(data) to copy")
print()

print("❌ MISTAKE 2: Complex conditions without parentheses")
# Can be confusing: [x for x in data if x > 5 and x < 10 or x == 1]
# Better: [x for x in data if (x > 5 and x < 10) or x == 1]
confusing = [x for x in sample_data if x > 5 and x < 10 or x == 1]
clear = [x for x in sample_data if (x > 5 and x < 10) or x == 1]
print(f"   Confusing: {confusing}")
print(f"   Clear with parentheses: {clear}")
print()

print("❌ MISTAKE 3: Trying to modify the original list")
print("   Wrong: [x for x in data if x != 5]  # Doesn't change original")
print("   Right: data = [x for x in data if x != 5]  # Assigns new list")
print()

print("=" * 70)
print("🏆 PRACTICE CHALLENGES")
print("=" * 50)

print("Try these on your own! (Answers below)")
practice_data = ["hello", "world", "python", "programming", "code", "fun"]
practice_numbers = [10, 15, 20, 25, 30, 35, 40, 45, 50]

print("Challenge 1: Keep words longer than 4 letters")
print("Challenge 2: Keep numbers divisible by 5 and greater than 20")
print("Challenge 3: Keep words that start with 'p'")
print()

print("💡 ANSWERS:")
challenge1 = [word for word in practice_data if len(word) > 4]
challenge2 = [num for num in practice_numbers if num % 5 == 0 and num > 20]
challenge3 = [word for word in practice_data if word.startswith('p')]

print(f"Answer 1: {challenge1}")
print(f"Answer 2: {challenge2}")
print(f"Answer 3: {challenge3}")

print("\n" + "=" * 70)
print("🎯 SUMMARY FOR BEGINNERS")
print("=" * 70)

print("""
🔥 THE GOLDEN PATTERN: [x for x in data if condition]

1️⃣ Start with your data (list, string, etc.)
2️⃣ Go through each item one by one (for x in data)
3️⃣ Check if item meets your condition (if condition)
4️⃣ Keep items that pass the test (x or transform x)

💡 REMEMBER:
- The 'if' part is optional (you can filter or not filter)
- You can transform 'x' before keeping it (like x*2 or x.upper())
- Conditions can be simple (x > 5) or complex (x > 5 and x < 10)
- You can work with any type of data (numbers, strings, dictionaries, etc.)

🚀 Practice makes perfect! Start simple and build up to complex examples.
""")