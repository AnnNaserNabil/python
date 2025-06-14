"""
8. Immutable State Management

Managing application state in an immutable way.
- State transitions
- Redux-like state management
- Time-travel debugging
- Undo/redo functionality
"""
from typing import TypeVar, Generic, Callable, Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, replace
from functools import reduce
import json
from datetime import datetime

T = TypeVar('T')
S = TypeVar('S')
Action = Dict[str, Any]
Reducer = Callable[[S, Action], S]
Middleware = Callable[['Store', Callable], Callable[[Callable], Callable]]

# 1. Basic state container
@dataclass(frozen=True)
class State:
    """Immutable application state."""
    counter: int = 0
    todos: Tuple[str, ...] = ()
    last_updated: Optional[datetime] = None

# 2. Action creators
def increment(amount: int = 1) -> Action:
    """Create an increment action."""
    return {"type": "INCREMENT", "payload": amount}

def decrement(amount: int = 1) -> Action:
    """Create a decrement action."""
    return {"type": "DECREMENT", "payload": amount}

def add_todo(text: str) -> Action:
    """Create an add todo action."""
    return {"type": "ADD_TODO", "payload": text}

def undo() -> Action:
    """Create an undo action."""
    return {"type": "UNDO"}

def redo() -> Action:
    """Create a redo action."""
    return {"type": "REDO"}

# 3. Reducer function
def reducer(state: State, action: Action) -> State:
    """Pure function that returns a new state based on the action."""
    if action["type"] == "INCREMENT":
        return replace(
            state,
            counter=state.counter + action["payload"],
            last_updated=datetime.now()
        )
    elif action["type"] == "DECREMENT":
        return replace(
            state,
            counter=state.counter - action["payload"],
            last_updated=datetime.now()
        )
    elif action["type"] == "ADD_TODO":
        return replace(
            state,
            todos=(*state.todos, action["payload"]),
            last_updated=datetime.now()
        )
    return state

# 4. Store class
class Store(Generic[S]):
    """Immutable state container with history for undo/redo."""
    
    def __init__(self, reducer: Reducer, initial_state: S, middlewares: List[Middleware] = None):
        self.reducer = reducer
        self.state = initial_state
        self.history: List[S] = [initial_state]
        self.history_index = 0
        self.middlewares = middlewares or []
        self.dispatch = self._apply_middleware(self._dispatch_impl)
    
    def _apply_middleware(self, dispatch: Callable) -> Callable:
        """Apply middleware to the store's dispatch method."""
        for middleware in reversed(self.middlewares):
            dispatch = middleware(self, dispatch)
        return dispatch
    
    def _dispatch_impl(self, action: Action) -> Action:
        """Dispatch an action to update the state."""
        # If we're not at the end of history, truncate the future
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Reduce the current state with the action
        new_state = self.reducer(self.state, action)
        
        # Only update if the state changed
        if new_state != self.state:
            self.history.append(new_state)
            self.history_index = len(self.history) - 1
            self.state = new_state
        
        return action
    
    def get_state(self) -> S:
        """Get the current state."""
        return self.state
    
    def get_history(self) -> List[S]:
        """Get the entire history of states."""
        return self.history
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self.history_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self.history_index < len(self.history) - 1
    
    def undo(self) -> None:
        """Move back one step in history."""
        if self.can_undo():
            self.history_index -= 1
            self.state = self.history[self.history_index]
    
    def redo(self) -> None:
        """Move forward one step in history."""
        if self.can_redo():
            self.history_index += 1
            self.state = self.history[self.history_index]
    
    def subscribe(self, listener: Callable[[], None]) -> Callable[[], None]:
        """Subscribe to state changes."""
        # In a real implementation, this would manage a list of subscribers
        # For simplicity, we'll just return a no-op unsubscribe function
        return lambda: None

# 5. Middleware
def logger_middleware(store: Store, next_dispatch: Callable) -> Callable:
    """Log all actions and states."""
    def middleware(next_handler: Callable) -> Callable:
        def handler(action: Action) -> Action:
            print(f"\nAction: {action['type']}")
            print(f"State before: {json.dumps(serialize_state(store.state), indent=2)}")
            
            result = next_handler(action)
            
            print(f"State after: {json.dumps(serialize_state(store.state), indent=2)}")
            return result
        return handler
    return middleware

def undo_redo_middleware(store: Store, next_dispatch: Callable) -> Callable:
    """Handle undo/redo actions."""
    def middleware(next_handler: Callable) -> Callable:
        def handler(action: Action) -> Action:
            if action["type"] == "UNDO":
                store.undo()
                return action
            elif action["type"] == "REDO":
                store.redo()
                return action
            return next_handler(action)
        return handler
    return middleware

# Helper function to serialize state
def serialize_state(state: Any) -> Dict[str, Any]:
    """Convert state to a serializable dictionary."""
    if isinstance(state, tuple):
        return list(state)
    elif hasattr(state, '__dataclass_fields__'):
        return {
            field: serialize_state(getattr(state, field))
            for field in state.__dataclass_fields__
        }
    elif isinstance(state, dict):
        return {k: serialize_state(v) for k, v in state.items()}
    elif isinstance(state, (list, tuple)):
        return [serialize_state(item) for item in state]
    elif isinstance(state, datetime):
        return state.isoformat()
    return state

def demonstrate_state_management() -> None:
    """Show how to use the immutable state management system."""
    # Create store with middleware
    store = Store(
        reducer=reducer,
        initial_state=State(),
        middlewares=[logger_middleware, undo_redo_middleware]
    )
    
    # Subscribe to state changes
    def on_state_change():
        state = store.get_state()
        print(f"\n=== State changed ===")
        print(f"Counter: {state.counter}")
        print(f"Todos: {state.todos}")
        print(f"Last updated: {state.last_updated}")
    
    # In a real app, you'd call this when the state changes
    # For now, we'll call it manually
    
    print("=== Initial State ===")
    on_state_change()
    
    # Dispatch some actions
    print("\n=== Dispatching Actions ===")
    
    store.dispatch(increment(5))
    on_state_change()
    
    store.dispatch(decrement(2))
    on_state_change()
    
    store.dispatch(add_todo("Learn immutable state management"))
    on_state_change()
    
    store.dispatch(add_todo("Build something cool"))
    on_state_change()
    
    # Test undo/redo
    print("\n=== Testing Undo/Redo ===")
    
    print("\nUndoing last action...")
    store.dispatch(undo())
    on_state_change()
    
    print("\nUndoing again...")
    store.dispatch(undo())
    on_state_change()
    
    print("\nRedoing...")
    store.dispatch(redo())
    on_state_change()
    
    # Print history
    print("\n=== History ===")
    for i, state in enumerate(store.get_history()):
        marker = " ->" if i == store.history_index else "   "
        print(f"{marker} {i}: {state}")

# Example usage
if __name__ == "__main__":
    demonstrate_state_management()
    
    print("\n=== Key Takeaways ===")
    print("1. State is never modified in place, only replaced")
    print("2. The reducer is a pure function that computes the next state")
    print("3. Actions describe state changes")
    print("4. Middleware can intercept and modify actions")
    print("5. Time-travel debugging is possible by keeping a history of states")
