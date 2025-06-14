"""
6. Structural Sharing in Immutable Data Structures

How immutable data structures can share structure for efficiency.
- Persistent data structures
- Path copying
- Implementation of a persistent vector
"""
from typing import TypeVar, Generic, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass
import math

T = TypeVar('T')

# 1. Simple example of structural sharing
def demonstrate_structural_sharing() -> None:
    """Show how immutable data structures can share structure."""
    # Original list
    original = [1, 2, 3, 4, 5]
    
    # "Modify" by creating new lists that share structure
    with_first = [0, *original]  # Prepend 0
    with_last = [*original, 6]   # Append 6
    
    # In a real persistent data structure, the tails would be shared
    print("Original list:", original)
    print("With first:", with_first)
    print("With last:", with_last)
    
    # In a real implementation, the memory would look like:
    # original:  [1, 2, 3, 4, 5]
    # with_first: [0] → points to original's memory
    # with_last: points to original's memory → [6]

# 2. Implementation of a persistent vector with structural sharing
class Vector(Generic[T]):
    """
    A persistent vector implementation with structural sharing.
    This is a simplified version for demonstration.
    """
    
    # Branching factor (number of children per node)
    BRANCHING = 32
    # Number of bits needed to represent indices within a node
    BITS = 5  # since 2^5 = 32
    # Mask to extract the last BITS bits
    MASK = (1 << BITS) - 1
    
    class Node:
        """Internal node structure."""
        __slots__ = ['children']
        
        def __init__(self):
            self.children = [None] * Vector.BRANCHING
    
    def __init__(self, root: Optional['Vector.Node'] = None, count: int = 0, shift: int = 0):
        self.root = root or Vector.Node()
        self.count = count
        self.shift = shift
    
    def __len__(self) -> int:
        return self.count
    
    def __getitem__(self, index: int) -> T:
        if index < 0 or index >= self.count:
            raise IndexError("Index out of range")
        
        node = self.root
        shift = self.shift
        
        # Traverse the tree to find the value
        while shift > 0:
            node = node.children[(index >> shift) & self.MASK]
            if node is None:
                raise IndexError("Invalid index")
            shift -= self.BITS
        
        return node.children[index & self.MASK]
    
    def append(self, value: T) -> 'Vector[T]':
        """Return a new vector with the value appended."""
        if self.count < (1 << (self.shift + self.BITS)):
            # There's room in the current root
            new_root = self._clone_node(self.root)
            self._append_to_node(new_root, self.count, self.shift, value)
            return Vector(new_root, self.count + 1, self.shift)
        else:
            # Need to create a new level
            new_root = Vector.Node()
            new_root.children[0] = self.root
            new_shift = self.shift + self.BITS
            
            # If the tree is too deep, we need to add more levels
            if (self.count >> new_shift) > 0:
                new_root = self._expand_root(new_root, self.shift)
                new_shift += self.BITS
            
            new_vector = Vector(new_root, self.count, new_shift)
            return new_vector.append(value)
    
    def _clone_node(self, node: 'Vector.Node') -> 'Vector.Node':
        """Create a shallow copy of a node."""
        new_node = Vector.Node()
        new_node.children = list(node.children)
        return new_node
    
    def _append_to_node(self, node: 'Vector.Node', index: int, shift: int, value: T) -> None:
        """Recursively append a value to the appropriate position in the tree."""
        if shift == 0:
            node.children[index & self.MASK] = value
        else:
            child_idx = (index >> shift) & self.MASK
            if node.children[child_idx] is None:
                node.children[child_idx] = Vector.Node()
            else:
                node.children[child_idx] = self._clone_node(node.children[child_idx])
            self._append_to_node(node.children[child_idx], index, shift - self.BITS, value)
    
    def _expand_root(self, root: 'Vector.Node', shift: int) -> 'Vector.Node':
        """Expand the root when the tree becomes too deep."""
        new_root = Vector.Node()
        new_root.children[0] = root
        
        # Keep adding levels until we have enough space
        while (self.count >> (shift + 2 * self.BITS)) > 0:
            shift += self.BITS
            newer_root = Vector.Node()
            newer_root.children[0] = new_root
            new_root = newer_root
        
        return new_root
    
    def __repr__(self) -> str:
        items = []
        for i in range(self.count):
            items.append(str(self[i]))
        return f"Vector([{', '.join(items)}])"

# 3. Persistent hash map with structural sharing
class HashMap(Generic[K, V]):
    """
    A simplified persistent hash map with structural sharing.
    This is a demonstration and not for production use.
    """
    
    def __init__(self, data: Optional[dict] = None):
        self._data = dict(data or {})
    
    def __getitem__(self, key: K) -> V:
        return self._data[key]
    
    def __contains__(self, key: K) -> bool:
        return key in self._data
    
    def set(self, key: K, value: V) -> 'HashMap[K, V]':
        """Return a new HashMap with the key set to value."""
        new_data = self._data.copy()
        new_data[key] = value
        return HashMap(new_data)
    
    def remove(self, key: K) -> 'HashMap[K, V]':
        """Return a new HashMap without the specified key."""
        if key not in self._data:
            return self
        new_data = self._data.copy()
        del new_data[key]
        return HashMap(new_data)
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __repr__(self) -> str:
        return f"HashMap({self._data})"

def demonstrate_persistent_structures() -> None:
    """Show how persistent data structures work with structural sharing."""
    # 1. Using our Vector
    print("=== Persistent Vector ===")
    v = Vector()
    for i in range(10):
        v = v.append(i * 10)
    
    print(f"Vector with 10 elements: {v}")
    print(f"Element at index 5: {v[5]}")
    
    # 2. Using our HashMap
    print("\n=== Persistent HashMap ===")
    m = HashMap()
    m = m.set("a", 1).set("b", 2).set("c", 3)
    print(f"Original map: {m}")
    
    m2 = m.set("b", 20).set("d", 4)
    print(f"Modified map: {m2}")
    print(f"Original unchanged: {m}")
    
    # In a real implementation, the internal structure would be shared
    # between m and m2 where possible

# Example usage
if __name__ == "__main__":
    print("=== Structural Sharing ===")
    demonstrate_structural_sharing()
    
    print("\n=== Persistent Data Structures ===")
    demonstrate_persistent_structures()
    
    print("\n=== Key Takeaways ===")
    print("1. Structural sharing allows immutable data structures to be efficient")
    print("2. Only modified parts of the structure need to be copied")
    print("3. Unmodified parts can be safely shared between versions")
    print("4. This is how languages like Clojure and Scala implement immutability efficiently")
    print("5. For production use, consider libraries like 'pyrsistent' or 'immutables'")
