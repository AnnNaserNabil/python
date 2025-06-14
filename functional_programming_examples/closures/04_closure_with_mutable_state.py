"""
4. Managing Mutable State with Closures in Python

This module demonstrates how closures can work with mutable objects like lists and
dictionaries to create encapsulated stateful objects without using classes.

Key Concepts:
------------
1. Mutable State: Using lists and dictionaries within closures to maintain state
2. Encapsulation: Hiding implementation details while exposing a clean interface
3. Data Integrity: Controlling access to mutable state through well-defined functions
4. Object-oriented Patterns: Implementing patterns similar to objects but with closures

Why Use Closures for State Management?
----------------------------------
- Simplicity: Lighter weight than classes for simple stateful operations
- Encapsulation: Internal state is not directly accessible from outside
- Flexibility: Can create multiple independent instances of the same stateful function
- Functional Style: Maintains immutability of the function interface

Real-world Applications:
-----------------------
- Simple stateful services or managers
- Implementing the Module Pattern in Python
- Creating lightweight alternatives to classes
- Managing configuration or application state

Example:
-------
>>> todo = create_todo_list()
>>> todo['add']('Buy milk', priority=2, tags=['shopping', 'home'])
>>> todo['add']('Write docs', priority=1, tags=['work'])
>>> todo['complete'](1)
True
>>> todo['get_todos'](completed=False)
[{'id': 2, 'name': 'Write docs', 'priority': 1, 'tags': ['work'], 'completed': False}]
"""
from __future__ import annotations
from typing import Callable, List, Dict, Any, Optional

def create_todo_list() -> Dict[str, Any]:
    """
    Create a todo list manager using closures to maintain state.
    
    This function demonstrates how to create an encapsulated todo list manager
    without using classes. The internal state (the list of todos) is hidden
    within the closure and can only be modified through the returned functions.
    
    Returns:
        Dict[str, Any]: A dictionary containing methods to interact with the todo list:
            - 'add': Function to add a new todo
            - 'complete': Function to mark a todo as completed
            - 'get_todos': Function to retrieve todos (optionally filtered)
            - 'get_by_tag': Function to get todos with a specific tag
            - 'get_stats': Function to get statistics about the todos
            
    Example:
        >>> todo = create_todo_list()
        >>> todo['add']('Learn Python', priority=1, tags=['education'])
        >>> todo['add']('Go shopping', tags=['shopping', 'home'])
        >>> todo['complete'](1)
        True
        >>> stats = todo['get_stats']()
        
    Implementation Notes:
    - Uses a list to store todos internally
    - Each todo is a dictionary with id, name, priority, tags, and completed status
    - The internal state is not directly accessible from outside
    - All modifications happen through the returned interface
    """
    todos: List[Dict[str, Any]] = []
    
    def add_todo(name: str, priority: int = 1, tags: Optional[List[str]] = None) -> None:
        """Add a new todo item."""
        if tags is None:
            tags = []
        todos.append({
            'id': len(todos) + 1,
            'name': name,
            'priority': priority,
            'tags': tags,
            'completed': False
        })
    
    def complete_todo(todo_id: int) -> bool:
        """Mark a todo as completed."""
        for todo in todos:
            if todo['id'] == todo_id:
                todo['completed'] = True
                return True
        return False
    
    def get_todos(completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get todos, optionally filtered by completion status."""
        if completed is None:
            return todos.copy()
        return [todo for todo in todos if todo['completed'] == completed]
    
    def get_todos_by_tag(tag: str) -> List[Dict[str, Any]]:
        """Get todos that have the specified tag."""
        return [todo for todo in todos if tag in todo['tags']]
    
    def get_stats() -> Dict[str, int]:
        """Get statistics about the todo list."""
        completed = sum(1 for todo in todos if todo['completed'])
        return {
            'total': len(todos),
            'completed': completed,
            'pending': len(todos) - completed,
            'high_priority': sum(1 for todo in todos if todo['priority'] > 7 and not todo['completed'])
        }
    
    # Return a dictionary with the todo list and its methods
    return {
        'add': add_todo,
        'complete': complete_todo,
        'get_all': lambda: get_todos(),
        'get_active': lambda: get_todos(False),
        'get_completed': lambda: get_todos(True),
        'get_by_tag': get_todos_by_tag,
        'stats': get_stats,
        '_todos': todos  # Exposing for demonstration (not recommended in production)
    }

def demonstrate_mutable_state() -> None:
    """
    Demonstrate how closures can maintain and modify mutable state.
    
    This function shows various operations on a todo list implemented
    using closures with mutable state. It demonstrates:
    - Adding todos with different priorities and tags
    - Marking todos as completed
    - Filtering and retrieving todos based on different criteria
    - Getting statistics about the todo list
    
    The example highlights how the internal state is maintained between
    function calls and how different instances of the todo list maintain
    their own independent state.
    
    Note how the internal list of todos is not directly accessible from
    outside the closure, ensuring data integrity and encapsulation.
    """
    # Create a new todo list
    todo_list = create_todo_list()
    
    # Add some todos
    todo_list['add']("Learn Python closures", 8, ["programming", "python"])
    todo_list['add']("Buy groceries", 5, ["shopping"])
    todo_list['add']("Write tests", 9, ["programming", "testing"])
    
    # Display all todos
    print("All todos:")
    for todo in todo_list['get_all']():
        print(f"- {todo['name']} (Priority: {todo['priority']}, Completed: {todo['completed']})")
    
    # Complete a todo
    todo_list['complete'](1)
    
    # Display active todos
    print("\nActive todos:")
    for todo in todo_list['get_active']():
        print(f"- {todo['name']}")
    
    # Get todos by tag
    print("\nProgramming todos:")
    for todo in todo_list['get_by_tag']("programming"):
        print(f"- {todo['name']}")
    
    # Get statistics
    stats = todo_list['stats']()
    print("\nTodo List Statistics:")
    print(f"Total: {stats['total']}")
    print(f"Completed: {stats['completed']}")
    print(f"Pending: {stats['pending']}")
    print(f"High Priority Pending: {stats['high_priority']}")
    
    # Show that the state is maintained between calls
    todo_list['add']("Document code", 7, ["programming", "documentation"])
    print(f"\nTotal todos after adding one more: {len(todo_list['get_all']())}")
    
    # Show that we can access the internal state (not recommended in practice)
    print("\nDirect access to todos (for demonstration):")
    for todo in todo_list['_todos']:
        print(f"- {todo}")

if __name__ == "__main__":
    print("=== Closure with Mutable State ===")
    demonstrate_mutable_state()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures can maintain and modify mutable state")
    print("2. The state is preserved between function calls")
    print("3. Multiple functions can share and modify the same state")
    print("4. This pattern is similar to objects with private state")
    print("5. Be cautious with mutable state in closures as it can lead to unexpected behavior")
