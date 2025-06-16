# ---------------------------------------
# 🎯 MINI PROJECT: Higher-Order Functions
# ---------------------------------------

print("🎉 Welcome to the Higher-Order Functions Playground!")

# ------------------------------
# Part 1: Basic Function Example
# ------------------------------

def square(x):
    return x * x

def my_map(func, items):
    """
    Applies a function to each item in a list and returns the result.
    Equivalent to the built-in map().
    """
    result = []
    for item in items:
        result.append(func(item))
    return result

print("\n🔢 Squaring numbers with my_map:")
print(my_map(square, [1, 2, 3, 4, 5]))  # [1, 4, 9, 16, 25]

# -----------------------------
# Part 2: Custom my_filter()
# -----------------------------

def is_even(x):
    return x % 2 == 0

def my_filter(func, numbers):
    """
    Filters items based on the function passed.
    Equivalent to the built-in filter().
    """
    result = []
    for num in numbers:
        if func(num):
            result.append(num)
    return result

print("\n⚖️ Filtering even numbers:")
print(my_filter(is_even, [1, 2, 3, 4, 5, 6]))  # [2, 4, 6]

# ------------------------------------
# Part 3: Functions that Return Functions
# ------------------------------------

def make_multiplier(n):
    """
    Returns a function that multiplies its input by n.
    """
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print("\n💥 Using function returned by another function:")
print(f"Double of 5: {double(5)}")  # 10
print(f"Triple of 5: {triple(5)}")  # 15

# ------------------------------------
# Part 4: Passing Functions as Arguments
# ------------------------------------

def say_hello(name):
    return f"Hello, {name}!"

def say_goodbye(name):
    return f"Goodbye, {name}!"

def greet(greeting_func, name):
    """
    Uses the function you pass to greet a person.
    """
    return greeting_func(name)

print("\n👋 Greeting using passed-in function:")
print(greet(say_hello, "Ann"))
print(greet(say_goodbye, "Ann"))

# ------------------------------------
# Part 5: Using Lambda Functions
# ------------------------------------

print("\n⚡️ Using lambda (anonymous function) with my_map:")
squared = my_map(lambda x: x * x, [10, 20, 30])
print(f"Squares: {squared}")

# ------------------------------------
# 🧠 Challenge Mode: Try This Yourself
# ------------------------------------
print("\n🎯 Your Turn! Try to complete these challenges:")

print("1. Write a function that returns whether a number is greater than 10.")
print("2. Use `my_filter()` to filter numbers > 10 from a list.")
print("3. Create a `make_power(n)` function that returns a function to raise numbers to the power of `n`.")
print("4. Use `lambda` with `my_filter()` to keep only odd numbers.")
print("5. Make a custom `my_reduce(func, items)` function that reduces a list to a single value.")

# You can uncomment and try things below 👇

# def is_big(x):
#     return x > 10

# print(my_filter(is_big, [3, 12, 7, 18, 1]))

# def make_power(n):
#     def power(x):
#         return x ** n
#     return power

# square_func = make_power(2)
# cube_func = make_power(3)
# print(square_func(4))  # 16
# print(cube_func(2))    # 8