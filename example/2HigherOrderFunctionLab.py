# -----------------------------
# 🎉 FUNCTION LAB: Build Your Own Map, Filter, Reduce
# -----------------------------

print("Welcome to the Function Lab 🧪")
print("We'll use higher-order functions to build some powerful tools!")

# -----------------------------
# ✅ Step 1: my_map (Takes a function and applies to each item)
# -----------------------------
def my_map(func, iterable):
    result = []
    for item in iterable:
        result.append(func(item))  # Apply the passed-in function
    return result

# Example usage
def square(x):
    return x * x

print("\n🔢 my_map result (square numbers):")
print(my_map(square, [1, 2, 3, 4]))  # [1, 4, 9, 16]

# Try with lambda
print("my_map with lambda (x + 10):")
print(my_map(lambda x: x + 10, [1, 2, 3]))  # [11, 12, 13]

# -----------------------------
# ✅ Step 2: my_filter (Keep items that match a condition)
# -----------------------------
def my_filter(condition_func, iterable):
    result = []
    for item in iterable:
        if condition_func(item):
            result.append(item)
    return result

# Example usage
def is_even(x):
    return x % 2 == 0

print("\n⚖️ my_filter result (even numbers):")
print(my_filter(is_even, [1, 2, 3, 4, 5, 6]))  # [2, 4, 6]

# Try with lambda
print("my_filter with lambda (x > 3):")
print(my_filter(lambda x: x > 3, [1, 2, 3, 4, 5]))  # [4, 5]

# -----------------------------
# ✅ Step 3: my_reduce (Reduce a list into a single value)
# -----------------------------
def my_reduce(reducer_func, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer

    for item in it:
        value = reducer_func(value, item)
    return value

# Example usage
def add(a, b):
    return a + b

print("\n🔗 my_reduce result (sum):")
print(my_reduce(add, [1, 2, 3, 4]))  # 10

# Try with lambda
print("my_reduce with lambda (multiply):")
print(my_reduce(lambda a, b: a * b, [1, 2, 3, 4]))  # 24

# -----------------------------
# 🧠 Challenge Mode: Make Your Own
# -----------------------------

print("\n🧠 Challenge: Create your own functions and try with map/filter/reduce!")

# For example:
# - A function to capitalize names
# - A filter for names longer than 5 characters
# - A reduce to count total characters in a list of strings

names = ["ann", "jonathan", "mia", "elizabeth", "leo"]

# Capitalize all names
print("\nCapitalized names:")
print(my_map(lambda name: name.capitalize(), names))

# Filter names longer than 5 letters
print("Long names:")
print(my_filter(lambda name: len(name) > 5, names))

# Total number of characters in all names
print("Total characters:")
print(my_reduce(lambda total, name: total + len(name), names, 0))