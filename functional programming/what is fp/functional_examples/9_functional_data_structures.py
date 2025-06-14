"""
9. Functional Data Structures

Functional programming often uses immutable data structures to maintain referential transparency.
This module demonstrates how to work with immutable data structures in Python.
"""
from dataclasses import dataclass, replace
from typing import Generic, TypeVar, List, Optional, Tuple, Dict, Any
from collections import namedtuple
from copy import deepcopy

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# 1. Immutable Point using namedtuple
Point = namedtuple('Point', ['x', 'y'])

# 2. Immutable linked list node
@dataclass(frozen=True)
class ListNode(Generic[T]):
    value: T
    next: Optional['ListNode[T]'] = None
    
    def __str__(self) -> str:
        return f"{self.value} -> {self.next if self.next else 'None'}"

# 3. Immutable binary tree node
@dataclass(frozen=True)
class TreeNode(Generic[T]):
    value: T
    left: Optional['TreeNode[T]'] = None
    right: Optional['TreeNode[T]'] = None
    
    def __str__(self, level: int = 0) -> str:
        ret = "\t" * level + f"{self.value}\n"
        if self.left:
            ret += self.left.__str__(level + 1)
        if self.right:
            ret += self.right.__str__(level + 1)
        return ret

# 4. Immutable dictionary with update operations
class ImmutableDict(Dict[K, V]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the dictionary immutable after initialization
        self._frozen = True
    
    def __setitem__(self, key, value):
        if hasattr(self, '_frozen') and self._frozen:
            raise TypeError("ImmutableDict does not support item assignment")
        super().__setitem__(key, value)
    
    def update(self, *args, **kwargs):
        if hasattr(self, '_frozen') and self._frozen:
            raise TypeError("ImmutableDict does not support update()")
        super().update(*args, **kwargs)
    
    def set(self, key: K, value: V) -> 'ImmutableDict[K, V]':
        """Return a new ImmutableDict with the key-value pair added/updated."""
        new_dict = ImmutableDict(self)
        new_dict._frozen = False  # Temporarily unfreeze to update
        super(ImmutableDict, new_dict).__setitem__(key, value)
        new_dict._frozen = True
        return new_dict
    
    def remove(self, key: K) -> 'ImmutableDict[K, V]':
        """Return a new ImmutableDict with the key removed."""
        if key not in self:
            return self
        new_dict = ImmutableDict(self)
        new_dict._frozen = False  # Temporarily unfreeze to update
        super(ImmutableDict, new_dict).pop(key)
        new_dict._frozen = True
        return new_dict

# 5. Immutable list with functional operations
class ImmutableList(List[T]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frozen = True
    
    def __setitem__(self, index, value):
        if self._frozen:
            raise TypeError("ImmutableList does not support item assignment")
        super().__setitem__(index, value)
    
    def append(self, value):
        if self._frozen:
            raise TypeError("ImmutableList does not support append()")
        super().append(value)
    
    def extend(self, iterable):
        if self._frozen:
            raise TypeError("ImmutableList does not support extend()")
        super().extend(iterable)
    
    def insert(self, index, value):
        if self._frozen:
            raise TypeError("ImmutableList does not support insert()")
        super().insert(index, value)
    
    def pop(self, index=-1):
        if self._frozen:
            raise TypeError("ImmutableList does not support pop()")
        return super().pop(index)
    
    def remove(self, value):
        if self._frozen:
            raise TypeError("ImmutableList does not support remove()")
        super().remove(value)
    
    def clear(self):
        if self._frozen:
            raise TypeError("ImmutableList does not support clear()")
        super().clear()
    
    # Functional operations that return new instances
    def cons(self, value: T) -> 'ImmutableList[T]':
        """Add an element to the front of the list (like :: in Scala/Haskell)."""
        new_list = ImmutableList([value])
        new_list._frozen = False
        new_list.extend(self)
        new_list._frozen = True
        return new_list
    
    def tail(self) -> 'ImmutableList[T]':
        """Return a new list without the first element."""
        if not self:
            return self
        return ImmutableList(self[1:])
    
    def map(self, func: callable) -> 'ImmutableList[Any]':
        """Apply a function to each element and return a new ImmutableList."""
        return ImmutableList([func(x) for x in self])
    
    def filter(self, predicate: callable) -> 'ImmutableList[T]':
        """Filter elements based on a predicate and return a new ImmutableList."""
        return ImmutableList([x for x in self if predicate(x)])
    
    def fold_left(self, initial: Any, func: callable) -> Any:
        """Fold left operation (like reduce but with an initial value)."""
        result = initial
        for item in self:
            result = func(result, item)
        return result
    
    def zip_with(self, other: 'ImmutableList[Any]') -> 'ImmutableList[Tuple[T, Any]]':
        """Zip this list with another list and return a new ImmutableList of tuples."""
        return ImmutableList(list(zip(self, other)))

# Example usage
if __name__ == "__main__":
    print("=== Immutable Point ===")
    p1 = Point(1, 2)
    print(f"Original point: {p1}")
    # p1.x = 3  # This would raise an AttributeError
    p2 = p1._replace(x=3)  # Create a new point with x updated
    print(f"Updated point: {p2}")
    
    print("\n=== Immutable Linked List ===")
    lst = ListNode(1, ListNode(2, ListNode(3, None)))
    print(f"Original list: {lst}")
    # Create a new list with 0 prepended
    new_lst = ListNode(0, lst)
    print(f"New list with 0 prepended: {new_lst}")
    
    print("\n=== Immutable Binary Tree ===")
    tree = TreeNode(1, 
                   TreeNode(2, 
                           TreeNode(4),
                           TreeNode(5)),
                   TreeNode(3))
    print("Binary tree:")
    print(tree)
    
    print("\n=== Immutable Dictionary ===")
    d1 = ImmutableDict(a=1, b=2, c=3)
    print(f"Original dict: {d1}")
    # d1['d'] = 4  # This would raise a TypeError
    d2 = d1.set('d', 4)  # Create a new dict with 'd' added
    print(f"After adding 'd': {d2}")
    d3 = d2.remove('b')  # Create a new dict with 'b' removed
    print(f"After removing 'b': {d3}")
    
    print("\n=== Immutable List ===")
    l1 = ImmutableList([1, 2, 3, 4, 5])
    print(f"Original list: {l1}")
    # l1.append(6)  # This would raise a TypeError
    l2 = l1.cons(0)  # Add 0 to the front
    print(f"After cons(0): {l2}")
    l3 = l2.map(lambda x: x * 2)  # Double each element
    print(f"After mapping *2: {l3}")
    l4 = l3.filter(lambda x: x > 5)  # Keep elements > 5
    print(f"After filtering >5: {l4}")
    sum_l4 = l4.fold_left(0, lambda acc, x: acc + x)  # Sum all elements
    print(f"Sum of elements: {sum_l4}")
    
    print("\n=== Zipping Lists ===")
    nums = ImmutableList([1, 2, 3])
    letters = ImmutableList(['a', 'b', 'c'])
    zipped = nums.zip_with(letters)
    print(f"Zipped: {zipped}")
