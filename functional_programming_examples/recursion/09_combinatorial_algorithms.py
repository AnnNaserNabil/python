"""
9. Combinatorial Algorithms with Recursion

Implementing combinatorial algorithms using recursion.
- Permutations and combinations
- Subset generation
- Parentheses generation
- N-Queens problem
- Sudoku solver
"""
from __future__ import annotations
from typing import List, Set, Tuple, Optional, TypeVar, Any, Callable, Dict
from copy import deepcopy
import time

T = TypeVar('T')

# 1. Permutations
def permutations_recursive(elements: List[T], prefix: List[T] = None) -> List[List[T]]:
    """Generate all permutations of a list using recursion."""
    if prefix is None:
        prefix = []
    
    if not elements:
        return [prefix]
    
    result = []
    for i in range(len(elements)):
        # Choose element at index i
        new_prefix = prefix + [elements[i]]
        remaining = elements[:i] + elements[i+1:]
        # Recursively generate permutations of remaining elements
        result.extend(permutations_recursive(remaining, new_prefix))
    
    return result

def permutations_iterative(elements: List[T]) -> List[List[T]]:
    """Generate all permutations using an iterative approach."""
    if not elements:
        return []
    
    result = [[]]
    
    for element in elements:
        new_permutations = []
        for perm in result:
            for i in range(len(perm) + 1):
                new_permutations.append(perm[:i] + [element] + perm[i:])
        result = new_permutations
    
    return result

# 2. Combinations
def combinations_recursive(elements: List[T], k: int, start: int = 0, prefix: List[T] = None) -> List[List[T]]:
    """Generate all combinations of k elements from the list."""
    if prefix is None:
        prefix = []
    
    if k == 0:
        return [prefix]
    
    result = []
    for i in range(start, len(elements)):
        # Include elements[i] in the current combination
        new_prefix = prefix + [elements[i]]
        # Recursively generate combinations of remaining elements
        result.extend(combinations_recursive(elements, k-1, i+1, new_prefix))
    
    return result

def combinations_with_replacement(elements: List[T], k: int, start: int = 0, prefix: List[T] = None) -> List[List[T]]:
    """Generate combinations with replacement (elements can be repeated)."""
    if prefix is None:
        prefix = []
    
    if k == 0:
        return [prefix]
    
    result = []
    for i in range(start, len(elements)):
        # Include elements[i] in the current combination
        new_prefix = prefix + [elements[i]]
        # Allow the same element to be used again
        result.extend(combinations_with_replacement(elements, k-1, i, new_prefix))
    
    return result

# 3. Subset Generation
def subsets_recursive(elements: List[T], index: int = 0, current: List[T] = None, result: List[List[T]] = None) -> List[List[T]]:
    """Generate all subsets of a set using recursion."""
    if result is None:
        result = []
    if current is None:
        current = []
    
    if index == len(elements):
        result.append(current.copy())
        return result
    
    # Exclude the current element
    subsets_recursive(elements, index + 1, current, result)
    
    # Include the current element
    current.append(elements[index])
    subsets_recursive(elements, index + 1, current, result)
    current.pop()
    
    return result

def subsets_bitmask(elements: List[T]) -> List[List[T]]:
    """Generate all subsets using bitmasking."""
    n = len(elements)
    result = []
    
    # Each bit in 'i' represents whether an element is included
    for mask in range(1 << n):
        subset = [elements[i] for i in range(n) if (mask & (1 << i))]
        result.append(subset)
    
    return result

# 4. Parentheses Generation
def generate_parentheses(n: int, current: str = '', open_count: int = 0, close_count: int = 0, result: List[str] = None) -> List[str]:
    """Generate all valid combinations of n pairs of parentheses."""
    if result is None:
        result = []
    
    # Base case: we've used all parentheses
    if len(current) == 2 * n:
        result.append(current)
        return result
    
    # Add an opening parenthesis if we haven't used all opening ones
    if open_count < n:
        generate_parentheses(n, current + '(', open_count + 1, close_count, result)
    
    # Add a closing parenthesis if it's valid (more opening than closing)
    if close_count < open_count:
        generate_parentheses(n, current + ')', open_count, close_count + 1, result)
    
    return result

# 5. N-Queens Problem
def solve_n_queens(n: int, row: int = 0, board: List[List[str]] = None, 
                  cols: Set[int] = None, diag1: Set[int] = None, 
                  diag2: Set[int] = None, result: List[List[str]] = None) -> List[List[str]]:
    """Solve the N-Queens problem using backtracking."""
    if result is None:
        result = []
    if board is None:
        board = [['.' for _ in range(n)] for _ in range(n)]
    if cols is None:
        cols = set()
    if diag1 is None:  # Diagonal from top-left to bottom-right (r - c)
        diag1 = set()
    if diag2 is None:  # Diagonal from top-right to bottom-left (r + c)
        diag2 = set()
    
    if row == n:
        result.append([''.join(row) for row in board])
        return result
    
    for col in range(n):
        if col not in cols and (row - col) not in diag1 and (row + col) not in diag2:
            # Place the queen
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            # Recurse to place queens in the next row
            solve_n_queens(n, row + 1, board, cols, diag1, diag2, result)
            
            # Backtrack
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    return result

# 6. Sudoku Solver
def find_empty_cell(grid: List[List[Optional[int]]]) -> Optional[Tuple[int, int]]:
    """Find an empty cell in the Sudoku grid."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] is None:
                return (i, j)
    return None

def is_valid(grid: List[List[Optional[int]]], row: int, col: int, num: int) -> bool:
    """Check if placing 'num' at (row, col) is valid."""
    # Check row
    if num in grid[row]:
        return False
    
    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[box_row + i][box_col + j] == num:
                return False
    
    return True

def solve_sudoku(grid: List[List[Optional[int]]]) -> bool:
    """Solve the Sudoku puzzle using backtracking."""
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True  # Puzzle solved
    
    row, col = empty_cell
    
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            
            if solve_sudoku(grid):
                return True
            
            # Backtrack
            grid[row][col] = None
    
    return False

def print_sudoku(grid: List[List[Optional[int]]]) -> None:
    """Print the Sudoku grid."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j] if grid[i][j] is not None else '.', end=" ")
        print()

def demonstrate_combinatorial_algorithms() -> None:
    """Demonstrate combinatorial algorithms."""
    print("=== Permutations ===")
    elements = [1, 2, 3]
    print(f"All permutations of {elements} (recursive):")
    perms_rec = permutations_recursive(elements)
    for i, perm in enumerate(perms_rec, 1):
        print(f"{i}. {perm}")
    
    print(f"\nAll permutations of {elements} (iterative):")
    perms_iter = permutations_iterative(elements)
    for i, perm in enumerate(perms_iter, 1):
        print(f"{i}. {perm}")
    
    print("\n=== Combinations ===")
    elements = [1, 2, 3, 4]
    k = 2
    print(f"All combinations of {k} elements from {elements}:")
    combs = combinations_recursive(elements, k)
    for i, comb in enumerate(combs, 1):
        print(f"{i}. {comb}")
    
    print(f"\nCombinations with replacement (k={k}):")
    combs_rep = combinations_with_replacement(elements, k)
    for i, comb in enumerate(combs_rep, 1):
        print(f"{i}. {comb}")
    
    print("\n=== Subsets ===")
    elements = [1, 2, 3]
    print(f"All subsets of {elements} (recursive):")
    subs_rec = subsets_recursive(elements)
    for i, subset in enumerate(subs_rec, 1):
        print(f"{i}. {subset}")
    
    print(f"\nAll subsets of {elements} (bitmask):")
    subs_bit = subsets_bitmask(elements)
    for i, subset in enumerate(subs_bit, 1):
        print(f"{i}. {subset}")
    
    print("\n=== Generate Parentheses ===")
    n = 3
    print(f"All valid combinations of {n} pairs of parentheses:")
    parens = generate_parentheses(n)
    for i, p in enumerate(parens, 1):
        print(f"{i}. {p}")
    
    print("\n=== N-Queens Problem ===")
    n = 4
    print(f"Solutions to the {n}-Queens problem:")
    solutions = solve_n_queens(n)
    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i}:")
        for row in solution:
            print(' '.join(row))
        print()
    
    print("\n=== Sudoku Solver ===")
    # 0 represents empty cells
    sudoku_grid = [
        [5, 3, None, None, 7, None, None, None, None],
        [6, None, None, 1, 9, 5, None, None, None],
        [None, 9, 8, None, None, None, None, 6, None],
        [8, None, None, None, 6, None, None, None, 3],
        [4, None, None, 8, None, 3, None, None, 1],
        [7, None, None, None, 2, None, None, None, 6],
        [None, 6, None, None, None, None, 2, 8, None],
        [None, None, None, 4, 1, 9, None, None, 5],
        [None, None, None, None, 8, None, None, 7, 9]
    ]
    
    print("Original Sudoku:")
    print_sudoku(sudoku_grid)
    
    if solve_sudoku(sudoku_grid):
        print("\nSolved Sudoku:")
        print_sudoku(sudoku_grid)
    else:
        print("No solution exists")

if __name__ == "__main__":
    demonstrate_combinatorial_algorithms()
    
    print("\n=== Key Takeaways ===")
    print("1. Permutations are all possible orderings of a set")
    print("2. Combinations are selections of items where order doesn't matter")
    print("3. Subsets are all possible combinations of any length")
    print("4. Backtracking is powerful for constraint satisfaction problems")
    print("5. Pruning invalid paths early improves efficiency")
    print("6. Bitmasking can be used for efficient subset generation")
