"""
4. Divide and Conquer Algorithms

Recursive algorithms that solve problems by breaking them into smaller subproblems.
- Binary search
- Merge sort
- Quick sort
- Closest pair of points
- Strassen's matrix multiplication
"""
from typing import List, Tuple, Optional, TypeVar, Any, Callable
import math
import random
import time

T = TypeVar('T', int, float)

# 1. Binary Search
def binary_search_recursive(arr: List[T], target: T, low: int = 0, high: Optional[int] = None) -> Optional[int]:
    """
    Perform binary search on a sorted array using recursion.
    Returns the index of the target if found, None otherwise.
    """
    if high is None:
        high = len(arr) - 1
    
    # Base case: target not found
    if low > high:
        return None
    
    # Find the middle element
    mid = (low + high) // 2
    
    # Base case: target found
    if arr[mid] == target:
        return mid
    
    # Recursive cases
    if arr[mid] > target:
        return binary_search_recursive(arr, target, low, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, high)

# 2. Merge Sort
def merge_sort(arr: List[T]) -> List[T]:
    """Sort an array using the merge sort algorithm."""
    # Base case: array of length 0 or 1 is already sorted
    if len(arr) <= 1:
        return arr
    
    # Divide: split the array into two halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer: merge the sorted halves
    return merge(left, right)

def merge(left: List[T], right: List[T]) -> List[T]:
    """Merge two sorted arrays into a single sorted array."""
    result = []
    i = j = 0
    
    # Compare elements from both arrays and add the smaller one to the result
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

# 3. Quick Sort
def quick_sort(arr: List[T]) -> List[T]:
    """Sort an array using the quick sort algorithm."""
    # Base case: arrays of length 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose a pivot (here we use the last element)
    pivot = arr[-1]
    
    # Partition the array into elements less than, equal to, and greater than the pivot
    less = [x for x in arr[:-1] if x <= pivot]
    greater = [x for x in arr[:-1] if x > pivot]
    
    # Recursively sort the partitions and combine them with the pivot
    return quick_sort(less) + [pivot] + quick_sort(greater)

# 4. Closest Pair of Points (2D)
class Point:
    """A point in 2D space."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate the Euclidean distance to another point."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

def closest_pair_bruteforce(points: List[Point]) -> Tuple[Point, Point, float]:
    """Find the closest pair of points using a brute-force approach."""
    min_dist = float('inf')
    pair = (None, None)
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = points[i].distance_to(points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])
    
    return (*pair, min_dist)

def closest_pair(points: List[Point]) -> Tuple[Point, Point, float]:
    """Find the closest pair of points using a divide and conquer approach."""
    # Base case: use brute force for small inputs
    if len(points) <= 3:
        return closest_pair_bruteforce(points)
    
    # Sort points by x-coordinate
    points_sorted_x = sorted(points, key=lambda p: p.x)
    
    # Divide: split the points into left and right halves
    mid = len(points_sorted_x) // 2
    left_points = points_sorted_x[:mid]
    right_points = points_sorted_x[mid:]
    
    # Conquer: find the closest pairs in each half
    left_p1, left_p2, left_dist = closest_pair(left_points)
    right_p1, right_p2, right_dist = closest_pair(right_points)
    
    # Find the minimum distance between the two halves
    if left_dist < right_dist:
        min_dist = left_dist
        min_pair = (left_p1, left_p2)
    else:
        min_dist = right_dist
        min_pair = (right_p1, right_p2)
    
    # Check for closer pairs that cross the division
    strip = []
    mid_x = points_sorted_x[mid].x
    
    # Collect points within min_dist of the vertical line
    for point in points_sorted_x:
        if abs(point.x - mid_x) < min_dist:
            strip.append(point)
    
    # Sort strip by y-coordinate
    strip_sorted_y = sorted(strip, key=lambda p: p.y)
    
    # Check for closer pairs in the strip
    for i in range(len(strip_sorted_y)):
        # Only check the next 7 points (proven to be sufficient)
        for j in range(i + 1, min(i + 8, len(strip_sorted_y))):
            dist = strip_sorted_y[i].distance_to(strip_sorted_y[j])
            if dist < min_dist:
                min_dist = dist
                min_pair = (strip_sorted_y[i], strip_sorted_y[j])
    
    return (min_pair[0], min_pair[1], min_dist)

# 5. Strassen's Matrix Multiplication
def matrix_multiply(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """Multiply two square matrices using the standard O(n³) algorithm."""
    n = len(a)
    result = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    
    return result

def add_matrices(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """Add two matrices."""
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def subtract_matrices(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """Subtract matrix b from matrix a."""
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def strassen_multiply(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """
    Multiply two square matrices using Strassen's algorithm (O(n^2.81)).
    For simplicity, this implementation assumes n is a power of 2.
    """
    n = len(a)
    
    # Base case: 1x1 matrix
    if n == 1:
        return [[a[0][0] * b[0][0]]]
    
    # Split matrices into quadrants
    half = n // 2
    
    a11 = [row[:half] for row in a[:half]]
    a12 = [row[half:] for row in a[:half]]
    a21 = [row[:half] for row in a[half:]]
    a22 = [row[half:] for row in a[half:]]
    
    b11 = [row[:half] for row in b[:half]]
    b12 = [row[half:] for row in b[:half]]
    b21 = [row[:half] for row in b[half:]]
    b22 = [row[half:] for row in b[half:]]
    
    # Calculate the 7 products using Strassen's formula
    p1 = strassen_multiply(a11, subtract_matrices(b12, b22))
    p2 = strassen_multiply(add_matrices(a11, a12), b22)
    p3 = strassen_multiply(add_matrices(a21, a22), b11)
    p4 = strassen_multiply(a22, subtract_matrices(b21, b11))
    p5 = strassen_multiply(add_matrices(a11, a22), add_matrices(b11, b22))
    p6 = strassen_multiply(subtract_matrices(a12, a22), add_matrices(b21, b22))
    p7 = strassen_multiply(subtract_matrices(a11, a21), add_matrices(b11, b12))
    
    # Calculate the quadrants of the result
    c11 = add_matrices(subtract_matrices(add_matrices(p5, p4), p2), p6)
    c12 = add_matrices(p1, p2)
    c21 = add_matrices(p3, p4)
    c22 = subtract_matrices(subtract_matrices(add_matrices(p5, p1), p3), p7)
    
    # Combine the quadrants into the result matrix
    result = [[0] * n for _ in range(n)]
    for i in range(half):
        for j in range(half):
            result[i][j] = c11[i][j]
            result[i][j + half] = c12[i][j]
            result[i + half][j] = c21[i][j]
            result[i + half][j + half] = c22[i][j]
    
    return result

def generate_random_points(n: int, min_val: float = 0, max_val: float = 100) -> List[Point]:
    """Generate n random points in 2D space."""
    return [Point(random.uniform(min_val, max_val), random.uniform(min_val, max_val)) 
            for _ in range(n)]

def generate_random_matrix(n: int, min_val: int = 0, max_val: int = 10) -> List[List[int]]:
    """Generate a random n×n matrix with integer values."""
    return [[random.randint(min_val, max_val) for _ in range(n)] for _ in range(n)]

def measure_time(func: Callable[..., T], *args: Any, **kwargs: Any) -> tuple[T, float]:
    """Measure the execution time of a function."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time

def demonstrate_divide_and_conquer() -> None:
    """Demonstrate divide and conquer algorithms."""
    print("=== Binary Search ===")
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 11
    print(f"Searching for {target} in {sorted_array}")
    index = binary_search_recursive(sorted_array, target)
    print(f"Found at index: {index}")
    
    print("\n=== Merge Sort ===")
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array: {arr}")
    sorted_arr = merge_sort(arr)
    print(f"Sorted array: {sorted_arr}")
    
    print("\n=== Quick Sort ===")
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array: {arr}")
    sorted_arr = quick_sort(arr)
    print(f"Sorted array: {sorted_arr}")
    
    print("\n=== Closest Pair of Points ===")
    # Use a fixed seed for reproducibility
    random.seed(42)
    points = generate_random_points(20)
    print(f"Generated {len(points)} random points")
    
    # Brute-force approach (for small n)
    if len(points) <= 10:
        p1, p2, dist = measure_time(closest_pair_bruteforce, points)
        print(f"Brute-force: Closest pair is {p1} and {p2} with distance {dist:.4f}")
    
    # Divide and conquer approach
    p1, p2, dist = measure_time(closest_pair, points)
    print(f"Divide & Conquer: Closest pair is {p1} and {p2} with distance {dist:.4f}")
    
    print("\n=== Matrix Multiplication (Strassen's Algorithm) ===")
    # For simplicity, use small matrices (powers of 2)
    n = 4
    a = generate_random_matrix(n, 0, 5)
    b = generate_random_matrix(n, 0, 5)
    
    print("Matrix A:")
    for row in a:
        print(row)
    
    print("\nMatrix B:")
    for row in b:
        print(row)
    
    # Standard matrix multiplication
    result_std, time_std = measure_time(matrix_multiply, a, b)
    
    # Strassen's algorithm
    result_strassen, time_strassen = measure_time(strassen_multiply, a, b)
    
    print("\nStandard matrix multiplication result:")
    for row in result_std:
        print(row)
    
    print("\nStrassen's algorithm result:")
    for row in result_strassen:
        print(row)
    
    print(f"\nTime taken (standard): {time_std:.6f}s")
    print(f"Time taken (Strassen): {time_strassen:.6f}s")

if __name__ == "__main__":
    demonstrate_divide_and_conquer()
    
    print("\n=== Key Takeaways ===")
    print("1. Divide and conquer breaks problems into smaller subproblems")
    print("2. Binary search is O(log n) time complexity")
    print("3. Merge sort and quick sort are O(n log n) sorting algorithms")
    print("4. Closest pair of points can be solved in O(n log n) time")
    print("5. Strassen's algorithm (O(n^2.81)) is more efficient than the standard O(n³) for large matrices")
