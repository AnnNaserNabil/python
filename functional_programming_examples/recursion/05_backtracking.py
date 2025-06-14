"""
5. Backtracking Algorithms

Recursive algorithms that build candidates to the solutions and abandon a candidate 
as soon as it determines that it cannot be extended to a valid solution.
- N-Queens problem
- Sudoku solver
- Maze solving
- Subset sum
- Permutations
"""
from typing import List, Tuple, Optional, Set, Dict, Any, TypeVar, Callable
import time

T = TypeVar('T')

# 1. N-Queens Problem
def solve_n_queens(n: int) -> List[List[Tuple[int, int]]]:
    """
    Solve the N-Queens problem: place N queens on an N×N chessboard
    such that no two queens threaten each other.
    Returns a list of all possible solutions, where each solution is a list of (row, col) tuples.
    """
    def is_safe(board: List[Tuple[int, int]], row: int, col: int) -> bool:
        """Check if it's safe to place a queen at board[row][col]."""
        for r, c in board:
            # Check same column or diagonal
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True
    
    def backtrack(row: int, board: List[Tuple[int, int]], solutions: List[List[Tuple[int, int]]]):
        """Backtrack to find all solutions."""
        if row == n:
            solutions.append(board.copy())
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board.append((row, col))
                backtrack(row + 1, board, solutions)
                board.pop()
    
    solutions: List[List[Tuple[int, int]]] = []
    backtrack(0, [], solutions)
    return solutions

def print_n_queens_solution(solution: List[Tuple[int, int]], n: int) -> None:
    """Print a single N-Queens solution."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for row, col in solution:
        board[row][col] = 'Q'
    
    for row in board:
        print(' '.join(row))
    print()

# 2. Sudoku Solver
def solve_sudoku(grid: List[List[int]]) -> Optional[List[List[int]]]:
    """
    Solve a Sudoku puzzle using backtracking.
    Empty cells are represented by 0.
    Returns the solved grid, or None if no solution exists.
    """
    def is_valid(grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if it's valid to place num at grid[row][col]."""
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
    
    def find_empty_cell(grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Find an empty cell (0) in the grid."""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None
    
    def backtrack(grid: List[List[int]]) -> bool:
        """Backtrack to solve the Sudoku."""
        empty_cell = find_empty_cell(grid)
        if not empty_cell:
            return True  # Puzzle solved
        
        row, col = empty_cell
        
        for num in range(1, 10):  # Try numbers 1-9
            if is_valid(grid, row, col, num):
                grid[row][col] = num
                
                if backtrack(grid):
                    return True
                
                grid[row][col] = 0  # Backtrack
        
        return False  # Trigger backtracking
    
    # Create a copy of the grid to avoid modifying the original
    grid_copy = [row.copy() for row in grid]
    return grid_copy if backtrack(grid_copy) else None

def print_sudoku(grid: List[List[int]]) -> None:
    """Print a Sudoku grid."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j] if grid[i][j] != 0 else '.', end=" ")
        print()

# 3. Maze Solving
def solve_maze(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
    """
    Solve a maze using backtracking.
    The maze is a 2D list where 0 represents a wall and 1 represents a path.
    Returns a list of (row, col) tuples representing the path from start to end,
    or None if no path exists.
    """
    rows, cols = len(maze), len(maze[0]) if maze else 0
    
    def is_valid(row: int, col: int) -> bool:
        """Check if the cell is a valid move."""
        return 0 <= row < rows and 0 <= col < cols and maze[row][col] == 1
    
    def backtrack(row: int, col: int, path: List[Tuple[int, int]], visited: Set[Tuple[int, int]]]) -> bool:
        """Backtrack to find a path from (row, col) to end."""
        # Check if we've reached the end
        if (row, col) == end:
            path.append((row, col))
            return True
        
        # Mark the current cell as visited
        visited.add((row, col))
        path.append((row, col))
        
        # Try all 4 possible directions (right, down, left, up)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if is_valid(new_row, new_col) and (new_row, new_col) not in visited:
                if backtrack(new_row, new_col, path, visited):
                    return True
        
        # If no direction worked, backtrack
        path.pop()
        return False
    
    # Check if start and end are valid
    if not (is_valid(*start) and is_valid(*end)):
        return None
    
    path: List[Tuple[int, int]] = []
    visited: Set[Tuple[int, int]] = set()
    
    if backtrack(start[0], start[1], path, visited):
        return path
    return None

def print_maze(maze: List[List[int]], path: Optional[List[Tuple[int, int]]] = None) -> None:
    """Print the maze with the solution path."""
    if path is None:
        path = []
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in path:
                print('*', end=' ')
            else:
                print('█' if maze[i][j] == 0 else ' ', end=' ')
        print()

# 4. Subset Sum
def subset_sum(numbers: List[int], target: int) -> Optional[List[int]]:
    """
    Find a subset of numbers that sums to the target using backtracking.
    Returns the first subset found, or None if no such subset exists.
    """
    def backtrack(start: int, path: List[int], current_sum: int) -> bool:
        """Backtrack to find a subset with the target sum."""
        if current_sum == target:
            return True
        
        for i in range(start, len(numbers)):
            # Skip duplicates to avoid duplicate subsets
            if i > start and numbers[i] == numbers[i-1]:
                continue
                
            if current_sum + numbers[i] > target:
                continue
                
            path.append(numbers[i])
            if backtrack(i + 1, path, current_sum + numbers[i]):
                return True
            path.pop()
        
        return False
    
    # Sort to handle duplicates and optimize pruning
    numbers.sort()
    result: List[int] = []
    
    if backtrack(0, result, 0):
        return result
    return None

# 5. Permutations
def permutations(elements: List[T]) -> List[List[T]]:
    """Generate all permutations of a list using backtracking."""
    def backtrack(path: List[T], used: List[bool]) -> None:
        """Backtrack to generate all permutations."""
        if len(path) == len(elements):
            result.append(path.copy())
            return
        
        for i in range(len(elements)):
            if not used[i]:
                # Skip duplicates
                if i > 0 and elements[i] == elements[i-1] and not used[i-1]:
                    continue
                    
                used[i] = True
                path.append(elements[i])
                backtrack(path, used)
                path.pop()
                used[i] = False
    
    elements.sort()  # Sort to handle duplicates
    result: List[List[T]] = []
    used = [False] * len(elements)
    backtrack([], used)
    return result

def demonstrate_backtracking() -> None:
    """Demonstrate backtracking algorithms."""
    print("=== N-Queens Problem ===")
    n = 4  # Try with larger n (e.g., 8) for more interesting results
    solutions = solve_n_queens(n)
    print(f"Number of solutions for {n}-Queens: {len(solutions)}")
    if solutions:
        print("\nOne possible solution:")
        print_n_queens_solution(solutions[0], n)
    
    print("\n=== Sudoku Solver ===")
    # 0 represents empty cells
    sudoku_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    print("Original Sudoku:")
    print_sudoku(sudoku_grid)
    
    solution = solve_sudoku(sudoku_grid)
    if solution:
        print("\nSolved Sudoku:")
        print_sudoku(solution)
    else:
        print("No solution exists")
    
    print("\n=== Maze Solver ===")
    maze = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 1]
    ]
    
    start = (0, 0)
    end = (8, 9)
    
    print("Maze (█ = wall,   = path, * = solution):")
    path = solve_maze(maze, start, end)
    
    if path:
        print(f"Path found with {len(path)} steps:")
        print_maze(maze, path)
    else:
        print("No path exists")
    
    print("\n=== Subset Sum ===")
    numbers = [10, 7, 5, 18, 12, 20, 15]
    target = 35
    print(f"Numbers: {numbers}")
    print(f"Target sum: {target}")
    
    subset = subset_sum(numbers, target)
    if subset:
        print(f"Subset that sums to {target}: {subset}")
    else:
        print(f"No subset sums to {target}")
    
    print("\n=== Permutations ===")
    items = [1, 2, 2]  # Try with duplicate elements
    print(f"All unique permutations of {items}:")
    perms = permutations(items)
    for i, perm in enumerate(perms, 1):
        print(f"{i}. {perm}")

if __name__ == "__main__":
    demonstrate_backtracking()
    
    print("\n=== Key Takeaways ===")
    print("1. Backtracking is a systematic way to try different sequences of decisions")
    print("2. It's often used for constraint satisfaction problems")
    print("3. Pruning invalid paths early improves efficiency")
    print("4. Time complexity is often O(k^m) where k is branching factor and m is max depth")
    print("5. Memoization can sometimes optimize backtracking solutions")
