"""
7. Memoization with Dynamic Programming

This example demonstrates how to use memoization with dynamic programming
to solve complex problems efficiently, such as the knapsack problem.
"""
from functools import lru_cache
from typing import List, Tuple, Dict, Any, TypeVar, Callable
import time

# Type variables for better type hints
T = TypeVar('T')
U = TypeVar('U')

# 1. Basic Fibonacci with and without memoization

def fib_naive(n: int) -> int:
    """Naive recursive Fibonacci without memoization (exponential time)."""
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)


@lru_cache(maxsize=None)
def fib_memoized(n: int) -> int:
    """Recursive Fibonacci with memoization (linear time)."""
    if n <= 1:
        return n
    return fib_memoized(n-1) + fib_memoized(n-2)

def fib_iterative(n: int) -> int:
    """Iterative Fibonacci (constant space, linear time)."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# 2. 0/1 Knapsack Problem

class Item:
    """Represents an item in the knapsack problem."""
    def __init__(self, name: str, weight: int, value: int):
        self.name = name
        self.weight = weight
        self.value = value
    
    def __repr__(self) -> str:
        return f"{self.name}(w={self.weight}, v={self.value})"

def knapsack_naive(items: List[Item], capacity: int) -> Tuple[int, List[Item]]:
    """
    Solve the 0/1 knapsack problem using naive recursion.
    Returns the maximum value and the list of selected items.
    """
    def helper(i: int, remaining_capacity: int) -> Tuple[int, List[Item]]:
        if i < 0 or remaining_capacity <= 0:
            return 0, []
        
        # Option 1: Don't take the current item
        val1, items1 = helper(i - 1, remaining_capacity)
        
        # Option 2: Take the current item (if it fits)
        val2, items2 = 0, []
        if items[i].weight <= remaining_capacity:
            val2, items2 = helper(i - 1, remaining_capacity - items[i].weight)
            val2 += items[i].value
            items2 = items2 + [items[i]]
        
        # Return the better option
        if val1 > val2:
            return val1, items1
        else:
            return val2, items2
    
    return helper(len(items) - 1, capacity)

def knapsack_memoized(items: List[Item], capacity: int) -> Tuple[int, List[Item]]:
    """
    Solve the 0/1 knapsack problem using memoization.
    Returns the maximum value and the list of selected items.
    """
    # Use a dictionary to store computed results
    memo: Dict[Tuple[int, int], Tuple[int, List[Item]]] = {}
    
    def helper(i: int, remaining_capacity: int) -> Tuple[int, List[Item]]:
        # Base cases
        if i < 0 or remaining_capacity <= 0:
            return 0, []
        
        # Check if we've already computed this subproblem
        key = (i, remaining_capacity)
        if key in memo:
            return memo[key]
        
        # Option 1: Don't take the current item
        val1, items1 = helper(i - 1, remaining_capacity)
        
        # Option 2: Take the current item (if it fits)
        val2, items2 = 0, []
        if items[i].weight <= remaining_capacity:
            val2, items2 = helper(i - 1, remaining_capacity - items[i].weight)
            val2 += items[i].value
            items2 = items2 + [items[i]]
        
        # Store and return the better option
        if val1 > val2:
            memo[key] = (val1, items1)
            return val1, items1
        else:
            memo[key] = (val2, items2)
            return val2, items2
    
    return helper(len(items) - 1, capacity)

# 3. Longest Common Subsequence (LCS)

def lcs_naive(s1: str, s2: str) -> int:
    """Naive recursive LCS without memoization."""
    def helper(i: int, j: int) -> int:
        if i < 0 or j < 0:
            return 0
        if s1[i] == s2[j]:
            return 1 + helper(i-1, j-1)
        return max(helper(i-1, j), helper(i, j-1))
    
    return helper(len(s1)-1, len(s2)-1)

def lcs_memoized(s1: str, s2: str) -> int:
    """LCS with memoization."""
    memo: Dict[Tuple[int, int], int] = {}
    
    def helper(i: int, j: int) -> int:
        if (i, j) in memo:
            return memo[(i, j)]
            
        if i < 0 or j < 0:
            result = 0
        elif s1[i] == s2[j]:
            result = 1 + helper(i-1, j-1)
        else:
            result = max(helper(i-1, j), helper(i, j-1))
            
        memo[(i, j)] = result
        return result
    
    return helper(len(s1)-1, len(s2)-1)

# 4. Matrix Chain Multiplication

def matrix_chain_multiplication(dims: List[int]) -> Tuple[int, str]:
    """
    Solve the matrix chain multiplication problem using memoization.
    Returns the minimum number of multiplications and the optimal parenthesization.
    """
    n = len(dims) - 1  # Number of matrices
    
    # memo[i][j] = minimum number of multiplications needed to compute A_i...A_j
    memo: List[List[int]] = [[0] * n for _ in range(n)]
    
    # To store the optimal split points
    split: List[List[int]] = [[0] * n for _ in range(n)]
    
    # Fill the table in a bottom-up manner
    for length in range(2, n + 1):  # length of the chain
        for i in range(n - length + 1):
            j = i + length - 1
            memo[i][j] = float('inf')
            
            for k in range(i, j):
                # Cost of multiplying A_i...A_k and A_{k+1}...A_j
                cost = memo[i][k] + memo[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
                if cost < memo[i][j]:
                    memo[i][j] = cost
                    split[i][j] = k
    
    # Reconstruct the optimal parenthesization
    def get_parenthesization(i: int, j: int) -> str:
        if i == j:
            return f"A{i+1}"
        else:
            k = split[i][j]
            left = get_parenthesization(i, k)
            right = get_parenthesization(k+1, j)
            return f"({left} × {right})"
    
    return memo[0][n-1], get_parenthesization(0, n-1)

def demonstrate() -> None:
    """Demonstrate dynamic programming with memoization."""
    print("=== Dynamic Programming with Memoization ===\n")
    
    # 1. Fibonacci comparison
    print("1. Fibonacci Sequence (n=35):")
    
    start = time.time()
    # Note: Uncomment to run the naive version (very slow for n=35)
    # result_naive = fib_naive(35)
    # naive_time = time.time() - start
    # print(f"Naive recursive: {result_naive} (took {naive_time:.2f} seconds)")
    
    start_memo = time.time()
    result_memo = fib_memoized(35)
    memo_time = time.time() - start_memo
    print(f"With memoization: {result_memo} (took {memo_time:.6f} seconds)")
    
    start_iter = time.time()
    result_iter = fib_iterative(35)
    iter_time = time.time() - start_iter
    print(f"Iterative: {result_iter} (took {iter_time:.6f} seconds)")
    
    # 2. Knapsack problem
    print("\n2. 0/1 Knapsack Problem:")
    
    items = [
        Item("Laptop", 3, 2000),
        Item("Camera", 1, 1500),
        Item("Headphones", 1, 500),
        Item("Smartphone", 1, 1000),
        Item("Tablet", 2, 800),
    ]
    capacity = 5
    
    print(f"Items: {items}")
    print(f"Knapsack capacity: {capacity}")
    
    # Note: The naive version is too slow for more than ~20 items
    # Uncomment to try with very small inputs
    # print("\nNaive solution:")
    # start = time.time()
    # max_val, selected = knapsack_naive(items, capacity)
    # print(f"Max value: {max_val}")
    # print(f"Selected items: {selected}")
    # print(f"Time: {time.time() - start:.6f} seconds")
    
    print("\nMemoized solution:")
    start = time.time()
    max_val, selected = knapsack_memoized(items, capacity)
    print(f"Max value: ${max_val}")
    print(f"Selected items: {selected}")
    print(f"Time: {time.time() - start:.6f} seconds")
    
    # 3. Longest Common Subsequence
    print("\n3. Longest Common Subsequence (LCS):")
    s1 = "ABCBDAB"
    s2 = "BDCAB"
    
    print(f"String 1: {s1}")
    print(f"String 2: {s2}")
    
    # Note: The naive version is too slow for strings longer than ~15 characters
    # print("\nNaive LCS:")
    # start = time.time()
    # lcs_len = lcs_naive(s1, s2)
    # print(f"LCS length: {lcs_len}")
    # print(f"Time: {time.time() - start:.6f} seconds")
    
    print("\nMemoized LCS:")
    start = time.time()
    lcs_len = lcs_memoized(s1, s2)
    print(f"LCS length: {lcs_len}")
    print(f"Time: {time.time() - start:.6f} seconds")
    
    # 4. Matrix Chain Multiplication
    print("\n4. Matrix Chain Multiplication:")
    # Dimensions for matrices A1, A2, A3 where:
    # A1 is 10x30, A2 is 30x5, A3 is 5x60
    dims = [10, 30, 5, 60]
    
    print(f"Matrix dimensions: {dims}")
    min_mults, parenthesization = matrix_chain_multiplication(dims)
    print(f"Minimum multiplications: {min_mults}")
    print(f"Optimal parenthesization: {parenthesization}")

if __name__ == "__main__":
    demonstrate()
