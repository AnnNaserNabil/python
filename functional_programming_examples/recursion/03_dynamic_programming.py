"""
3. Recursion and Dynamic Programming

Optimizing recursive solutions with dynamic programming.
- Memoization
- Tabulation
- Fibonacci with DP
- Grid traveler problem
- Knapsack problem
"""
from typing import TypeVar, Dict, List, Callable, Any
from functools import lru_cache
import time

T = TypeVar('T')

# 1. Basic memoization decorator
def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """Basic memoization decorator."""
    cache: Dict[Any, T] = {}
    
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper

# 2. Fibonacci with different implementations
def fib_naive(n: int) -> int:
    """Naive recursive Fibonacci (exponential time)."""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@memoize
def fib_memo(n: int) -> int:
    """Fibonacci with memoization (O(n) time, O(n) space)."""
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

def fib_tabulation(n: int) -> int:
    """Fibonacci with tabulation (O(n) time, O(n) space, no recursion)."""
    if n <= 1:
        return n
    
    table = [0] * (n + 1)
    table[1] = 1
    
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    
    return table[n]

def fib_optimized(n: int) -> int:
    """Optimized Fibonacci (O(n) time, O(1) space)."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

# 3. Grid traveler problem
def grid_traveler_naive(m: int, n: int) -> int:
    """
    Calculate number of ways to travel from top-left to bottom-right
    in an m×n grid, moving only right or down.
    """
    if m == 1 or n == 1:
        return 1
    return grid_traveler_naive(m - 1, n) + grid_traveler_naive(m, n - 1)

@lru_cache(maxsize=None)
def grid_traveler_memo(m: int, n: int) -> int:
    """Grid traveler with memoization."""
    if m == 1 or n == 1:
        return 1
    return grid_traveler_memo(m - 1, n) + grid_traveler_memo(m, n - 1)

def grid_traveler_tabulation(m: int, n: int) -> int:
    """Grid traveler with tabulation."""
    # Create a 2D table initialized with 0s
    table = [[0] * (n + 1) for _ in range(m + 1)]
    table[1][1] = 1  # Base case: one way to travel a 1×1 grid
    
    for i in range(m + 1):
        for j in range(n + 1):
            current = table[i][j]
            if i + 1 <= m:
                table[i + 1][j] += current
            if j + 1 <= n:
                table[i][j + 1] += current
    
    return table[m][n]

# 4. 0/1 Knapsack problem
def knapsack_naive(weights: List[int], values: List[int], capacity: int, n: int) -> int:
    """
    Solve the 0/1 knapsack problem using naive recursion.
    Returns the maximum value that can be obtained with the given capacity.
    """
    # Base case: no items left or no capacity
    if n == 0 or capacity == 0:
        return 0
    
    # If weight of the nth item is more than capacity, skip it
    if weights[n-1] > capacity:
        return knapsack_naive(weights, values, capacity, n-1)
    
    # Return the maximum of two cases:
    # 1. nth item included
    # 2. nth item not included
    return max(
        values[n-1] + knapsack_naive(weights, values, capacity - weights[n-1], n-1),
        knapsack_naive(weights, values, capacity, n-1)
    )

def knapsack_memo(weights: List[int], values: List[int], capacity: int, n: int, memo: Dict[tuple, int] = None) -> int:
    """Knapsack problem with memoization."""
    if memo is None:
        memo = {}
    
    # Check if we've already computed this subproblem
    if (n, capacity) in memo:
        return memo[(n, capacity)]
    
    # Base case
    if n == 0 or capacity == 0:
        return 0
    
    # If weight of the nth item is more than capacity, skip it
    if weights[n-1] > capacity:
        memo[(n, capacity)] = knapsack_memo(weights, values, capacity, n-1, memo)
    else:
        # Return the maximum of including or excluding the current item
        memo[(n, capacity)] = max(
            values[n-1] + knapsack_memo(weights, values, capacity - weights[n-1], n-1, memo),
            knapsack_memo(weights, values, capacity, n-1, memo)
        )
    
    return memo[(n, capacity)]

def knapsack_tabulation(weights: List[int], values: List[int], capacity: int) -> int:
    """Knapsack problem with tabulation."""
    n = len(weights)
    # Create a 2D array to store the maximum value at each capacity for each item
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Build the DP table
    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]

def measure_time(func: Callable[..., T], *args: Any, **kwargs: Any) -> tuple[T, float]:
    """Measure the execution time of a function."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time

def demonstrate_dynamic_programming() -> None:
    """Demonstrate dynamic programming techniques."""
    print("=== Fibonacci Sequence ===")
    n = 35  # Large enough to show the difference
    
    # Naive (very slow for n > 35)
    if n <= 35:
        result, time_taken = measure_time(fib_naive, n)
        print(f"Naive fib({n}): {result} (took {time_taken:.6f}s)")
    
    # With memoization
    result, time_taken = measure_time(fib_memo, n)
    print(f"Memoized fib({n}): {result} (took {time_taken:.6f}s)")
    
    # With tabulation
    result, time_taken = measure_time(fib_tabulation, n)
    print(f"Tabulation fib({n}): {result} (took {time_taken:.6f}s)")
    
    # Optimized (iterative)
    result, time_taken = measure_time(fib_optimized, n)
    print(f"Optimized fib({n}): {result} (took {time_taken:.6f}s)")
    
    print("\n=== Grid Traveler ===")
    m, n = 10, 10
    
    # With memoization (using lru_cache)
    result, time_taken = measure_time(grid_traveler_memo, m, n)
    print(f"Memoized grid_traveler({m}, {n}): {result} (took {time_taken:.6f}s)")
    
    # With tabulation
    result, time_taken = measure_time(grid_traveler_tabulation, m, n)
    print(f"Tabulation grid_traveler({m}, {n}): {result} (took {time_taken:.6f}s)")
    
    print("\n=== 0/1 Knapsack Problem ===")
    values = [60, 100, 120, 150, 200, 220, 250, 280, 300, 320]
    weights = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    capacity = 200
    
    # With memoization
    result, time_taken = measure_time(knapsack_memo, weights, values, capacity, len(weights))
    print(f"Memoized knapsack (value): {result} (took {time_taken:.6f}s)")
    
    # With tabulation
    result, time_taken = measure_time(knapsack_tabulation, weights, values, capacity)
    print(f"Tabulation knapsack (value): {result} (took {time_taken:.6f}s)")

if __name__ == "__main__":
    demonstrate_dynamic_programming()
    
    print("\n=== Key Takeaways ===")
    print("1. Dynamic programming optimizes recursive solutions by storing results of subproblems")
    print("2. Memoization (top-down) is recursive and caches results as they're computed")
    print("3. Tabulation (bottom-up) builds solutions iteratively using a table")
    print("4. Both approaches have O(n) time complexity for problems like Fibonacci")
    print("5. For problems with multiple constraints (like knapsack), tabulation is often more efficient")
