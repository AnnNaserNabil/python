"""
7. Tree Algorithms with Recursion

Implementing and working with tree data structures using recursion.
- Binary tree traversals
- Binary search tree operations
- Trie (prefix tree)
- AVL tree (self-balancing BST)
- Segment tree
"""
from __future__ import annotations
from typing import TypeVar, Generic, Optional, List, Dict, Any, Callable, Tuple
from dataclasses import dataclass
import math

T = TypeVar('T', int, float, str)
K = TypeVar('K', int, float, str)

# 1. Binary Tree Node and Basic Operations
@dataclass
class TreeNode(Generic[T]):
    """Node in a binary tree."""
    value: T
    left: Optional[TreeNode[T]] = None
    right: Optional[TreeNode[T]] = None
    
    def is_leaf(self) -> bool:
        """Check if the node is a leaf (no children)."""
        return self.left is None and self.right is None
    
    def height(self) -> int:
        """Calculate the height of the tree rooted at this node."""
        if self.is_leaf():
            return 0
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0
        return 1 + max(left_height, right_height)
    
    def size(self) -> int:
        """Calculate the number of nodes in the tree."""
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return 1 + left_size + right_size

# 2. Tree Traversals
def preorder_traversal(root: Optional[TreeNode[T]]) -> List[T]:
    """Pre-order traversal: root -> left -> right."""
    if not root:
        return []
    return [root.value] + preorder_traversal(root.left) + preorder_traversal(root.right)

def inorder_traversal(root: Optional[TreeNode[T]]) -> List[T]:
    """In-order traversal: left -> root -> right."""
    if not root:
        return []
    return inorder_traversal(root.left) + [root.value] + inorder_traversal(root.right)

def postorder_traversal(root: Optional[TreeNode[T]]) -> List[T]:
    """Post-order traversal: left -> right -> root."""
    if not root:
        return []
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.value]

def level_order_traversal(root: Optional[TreeNode[T]]]) -> List[List[T]]:
    """Level-order traversal (breadth-first)."""
    if not root:
        return []
    
    result: List[List[T]] = []
    queue: List[Tuple[TreeNode[T], int]] = [(root, 0)]
    
    while queue:
        node, level = queue.pop(0)
        
        # Add a new level if needed
        if level == len(result):
            result.append([])
        result[level].append(node.value)
        
        # Enqueue children
        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))
    
    return result

# 3. Binary Search Tree
class BinarySearchTree(Generic[T]):
    """Binary Search Tree implementation."""
    
    def __init__(self):
        self.root: Optional[TreeNode[T]] = None
    
    def insert(self, value: T) -> None:
        """Insert a value into the BST."""
        self.root = self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: Optional[TreeNode[T]], value: T) -> TreeNode[T]:
        """Helper method for recursive insertion."""
        if node is None:
            return TreeNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        
        return node
    
    def search(self, value: T) -> bool:
        """Search for a value in the BST."""
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[TreeNode[T]], value: T) -> bool:
        """Helper method for recursive search."""
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def delete(self, value: T) -> None:
        """Delete a value from the BST."""
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node: Optional[TreeNode[T]], value: T) -> Optional[TreeNode[T]]:
        """Helper method for recursive deletion."""
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children: get the inorder successor (smallest
            # in the right subtree)
            node.value = self._min_value(node.right)
            
            # Delete the inorder successor
            node.right = self._delete_recursive(node.right, node.value)
        
        return node
    
    def _min_value(self, node: TreeNode[T]) -> T:
        """Find the minimum value in a subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current.value
    
    def is_valid(self) -> bool:
        """Check if the tree is a valid BST."""
        return self._is_valid_recursive(self.root, None, None)
    
    def _is_valid_recursive(self, node: Optional[TreeNode[T]], min_val: Optional[T], max_val: Optional[T]) -> bool:
        """Helper method for BST validation."""
        if node is None:
            return True
        
        if (min_val is not None and node.value <= min_val) or \
           (max_val is not None and node.value >= max_val):
            return False
        
        return (self._is_valid_recursive(node.left, min_val, node.value) and
                self._is_valid_recursive(node.right, node.value, max_val))

# 4. Trie (Prefix Tree)
class TrieNode:
    """Node in a trie."""
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word = False

class Trie:
    """Trie (prefix tree) implementation."""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search for an exact word in the trie."""
        node = self._search_prefix(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the trie starts with the given prefix."""
        return self._search_prefix(prefix) is not None
    
    def _search_prefix(self, prefix: str) -> Optional[TrieNode]:
        """Helper method to search for a prefix in the trie."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def get_all_words(self) -> List[str]:
        """Get all words in the trie."""
        words: List[str] = []
        self._collect_words(self.root, "", words)
        return words
    
    def _collect_words(self, node: TrieNode, prefix: str, words: List[str]) -> None:
        """Helper method to collect all words in the trie."""
        if node.is_end_of_word:
            words.append(prefix)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, words)

# 5. AVL Tree (Self-balancing BST)
class AVLNode(Generic[T]):
    """Node in an AVL tree."""
    def __init__(self, value: T):
        self.value = value
        self.left: Optional[AVLNode[T]] = None
        self.right: Optional[AVLNode[T]] = None
        self.height = 1

class AVLTree(Generic[T]):
    """AVL Tree (self-balancing BST) implementation."""
    
    def __init__(self):
        self.root: Optional[AVLNode[T]] = None
    
    def insert(self, value: T) -> None:
        """Insert a value into the AVL tree."""
        self.root = self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: Optional[AVLNode[T]], value: T) -> AVLNode[T]:
        """Helper method for recursive insertion."""
        # Perform standard BST insertion
        if node is None:
            return AVLNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)
        
        # Update height of the ancestor node
        node.height = 1 + max(self._get_height(node.left), 
                             self._get_height(node.right))
        
        # Get the balance factor
        balance = self._get_balance(node)
        
        # Perform rotations if needed to balance the tree
        # Left Left Case
        if balance > 1 and value < node.left.value:  # type: ignore
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and value > node.right.value:  # type: ignore
            return self._rotate_left(node)
        
        # Left Right Case
        if balance > 1 and value > node.left.value:  # type: ignore
            node.left = self._rotate_left(node.left)  # type: ignore
            return self._rotate_right(node)
        
        # Right Left Case
        if balance < -1 and value < node.right.value:  # type: ignore
            node.right = self._rotate_right(node.right)  # type: ignore
            return self._rotate_left(node)
        
        return node
    
    def _get_height(self, node: Optional[AVLNode[T]]) -> int:
        """Get the height of a node."""
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node: Optional[AVLNode[T]]) -> int:
        """Get the balance factor of a node."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rotate_right(self, z: AVLNode[T]) -> AVLNode[T]:
        """Right rotation for balancing the tree."""
        y = z.left
        T3 = y.right
        
        # Perform rotation
        y.right = z
        z.left = T3
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left), 
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        
        # Return the new root
        return y
    
    def _rotate_left(self, z: AVLNode[T]) -> AVLNode[T]:
        """Left rotation for balancing the tree."""
        y = z.right
        T2 = y.left
        
        # Perform rotation
        y.left = z
        z.right = T2
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left), 
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        
        # Return the new root
        return y

# 6. Segment Tree
class SegmentTree:
    """Segment Tree for range queries."""
    
    def __init__(self, data: List[int]):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        
        # Initialize the segment tree with zeros
        self.tree = [0] * (2 * self.size)
        
        # Fill the leaves with the input data
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        
        # Build the tree
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, index: int, value: int) -> None:
        """Update the value at the given index."""
        # Update the leaf node
        pos = self.size + index
        self.tree[pos] = value
        
        # Update all the ancestors
        pos //= 2
        while pos >= 1:
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]
            pos //= 2
    
    def query_range(self, left: int, right: int) -> int:
        """Query the sum of elements in the range [left, right]."""
        # Convert to 0-based indexing
        left += self.size
        right += self.size
        
        result = 0
        
        while left <= right:
            # If left is a right child, add it to the result
            if left % 2 == 1:
                result += self.tree[left]
                left += 1
            
            # If right is a left child, add it to the result
            if right % 2 == 0:
                result += self.tree[right]
                right -= 1
            
            # Move to the parent nodes
            left //= 2
            right //= 2
        
        return result

def demonstrate_tree_algorithms() -> None:
    """Demonstrate tree algorithms."""
    print("=== Binary Tree Traversals ===")
    # Create a binary tree:
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print(f"Pre-order: {preorder_traversal(root)}")
    print(f"In-order: {inorder_traversal(root)}")
    print(f"Post-order: {postorder_traversal(root)}")
    print(f"Level-order: {level_order_traversal(root)}")
    print(f"Tree height: {root.height()}")
    print(f"Tree size: {root.size()}")
    
    print("\n=== Binary Search Tree ===")
    bst = BinarySearchTree()
    for num in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(num)
    
    print(f"In-order traversal: {inorder_traversal(bst.root)}")
    print(f"Is 40 in BST? {bst.search(40)}")
    print(f"Is 100 in BST? {bst.search(100)}")
    print(f"Is valid BST? {bst.is_valid()}")
    
    print("\n=== Trie (Prefix Tree) ===")
    trie = Trie()
    words = ["apple", "app", "apricot", "banana", "bat"]
    for word in words:
        trie.insert(word)
    
    print(f"All words in trie: {trie.get_all_words()}")
    print(f"Search 'app': {trie.search('app')}")
    print(f"Search 'appl': {trie.search('appl')}")
    print(f"Starts with 'ba': {trie.starts_with('ba')}")
    
    print("\n=== AVL Tree ===")
    avl = AVLTree()
    for num in [10, 20, 30, 40, 50, 25]:
        avl.insert(num)
    
    print(f"In-order traversal: {inorder_traversal(avl.root)}")
    
    print("\n=== Segment Tree ===")
    data = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(data)
    print(f"Original array: {data}")
    print(f"Sum of range [1, 3]: {st.query_range(1, 3)}")
    print("Updating index 2 to 10")
    st.update(2, 10)
    print(f"New sum of range [1, 3]: {st.query_range(1, 3)}")

if __name__ == "__main__":
    demonstrate_tree_algorithms()
    
    print("\n=== Key Takeaways ===")
    print("1. Tree traversals (pre-order, in-order, post-order, level-order) are fundamental operations")
    print("2. Binary Search Trees provide O(log n) search, insert, and delete operations")
    print("3. Tries are efficient for string operations and prefix searches")
    print("4. AVL trees are self-balancing BSTs that maintain O(log n) height")
    print("5. Segment trees allow efficient range queries and point updates in O(log n) time")
