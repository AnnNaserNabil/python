"""
2. Recursive Data Structures

Working with recursive data structures in Python.
- Linked lists
- Binary trees
- Nested lists
- Directory traversal
- JSON processing
"""
from __future__ import annotations
from typing import TypeVar, Generic, List, Any, Optional, Union, Dict
from dataclasses import dataclass
import json
import os

T = TypeVar('T')

# 1. Linked List
@dataclass
class Node(Generic[T]):
    """A node in a linked list."""
    value: T
    next: Optional[Node[T]] = None

def list_to_linked_list(items: List[T]) -> Optional[Node[T]]:
    """Convert a Python list to a linked list."""
    if not items:
        return None
    head = Node(items[0])
    current = head
    for item in items[1:]:
        current.next = Node(item)
        current = current.next
    return head

def print_linked_list(head: Optional[Node[T]]) -> str:
    """Convert a linked list to a string representation."""
    if not head:
        return "None"
    return f"{head.value} -> {print_linked_list(head.next)}"

def sum_linked_list(head: Optional[Node[int]]) -> int:
    """Calculate the sum of all values in a linked list."""
    if not head:
        return 0
    return head.value + sum_linked_list(head.next)

# 2. Binary Tree
@dataclass
class TreeNode(Generic[T]):
    """A node in a binary tree."""
    value: T
    left: Optional[TreeNode[T]] = None
    right: Optional[TreeNode[T]] = None

def tree_size(node: Optional[TreeNode[T]]) -> int:
    """Calculate the number of nodes in a binary tree."""
    if not node:
        return 0
    return 1 + tree_size(node.left) + tree_size(node.right)

def tree_depth(node: Optional[TreeNode[T]]) -> int:
    """Calculate the depth of a binary tree."""
    if not node:
        return 0
    return 1 + max(tree_depth(node.left), tree_depth(node.right))

# 3. Nested Lists
def flatten(nested_list: List[Any]) -> List[Any]:
    """Flatten a nested list structure."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# 4. Directory Traversal
def list_files_recursive(path: str) -> List[str]:
    """List all files in a directory and its subdirectories."""
    result = []
    for entry in os.scandir(path):
        if entry.is_file():
            result.append(entry.path)
        elif entry.is_dir():
            result.extend(list_files_recursive(entry.path))
    return result

# 5. JSON Processing
def find_values_by_key(json_obj: Union[Dict, List, Any], key: str) -> List[Any]:
    """Find all values associated with a given key in a JSON object."""
    results = []
    
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == key:
                results.append(v)
            if isinstance(v, (dict, list)):
                results.extend(find_values_by_key(v, key))
    elif isinstance(json_obj, list):
        for item in json_obj:
            if isinstance(item, (dict, list)):
                results.extend(find_values_by_key(item, key))
    
    return results

def demonstrate_recursive_structures() -> None:
    """Demonstrate recursive data structures."""
    print("=== Linked List ===")
    numbers = [1, 2, 3, 4, 5]
    linked_list = list_to_linked_list(numbers)
    print(f"Linked list: {print_linked_list(linked_list)}")
    print(f"Sum of values: {sum_linked_list(linked_list)}")
    
    print("\n=== Binary Tree ===")
    # Create a binary tree:
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    tree = TreeNode(1,
                   TreeNode(2,
                           TreeNode(4),
                           TreeNode(5)),
                   TreeNode(3))
    
    print(f"Tree size: {tree_size(tree)}")
    print(f"Tree depth: {tree_depth(tree)}")
    
    print("\n=== Nested Lists ===")
    nested = [1, [2, [3, 4], 5], 6, [7, 8]]
    print(f"Original: {nested}")
    print(f"Flattened: {flatten(nested)}")
    
    print("\n=== Directory Traversal ===")
    # List Python files in the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    python_files = [f for f in list_files_recursive(current_dir) 
                   if f.endswith('.py')]
    print(f"Found {len(python_files)} Python files in {current_dir}:")
    for file in python_files[:5]:  # Show first 5 files
        print(f"- {os.path.basename(file)}")
    if len(python_files) > 5:
        print(f"... and {len(python_files) - 5} more")
    
    print("\n=== JSON Processing ===")
    json_data = {
        "name": "John",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown"
        },
        "pets": [
            {"type": "dog", "name": "Fido"},
            {"type": "cat", "name": "Whiskers"}
        ],
        "children": [
            {"name": "Alice", "age": 5},
            {"name": "Bob", "age": 3}
        ]
    }
    
    print("All 'name' values in JSON:")
    for name in find_values_by_key(json_data, "name"):
        print(f"- {name}")

if __name__ == "__main__":
    demonstrate_recursive_structures()
    
    print("\n=== Key Takeaways ===")
    print("1. Recursive data structures contain references to themselves")
    print("2. Linked lists and trees are common recursive data structures")
    print("3. Many real-world structures (file systems, JSON) are recursive")
    print("4. Recursive algorithms naturally operate on recursive structures")
    print("5. Be mindful of recursion depth with large or unbalanced structures")
