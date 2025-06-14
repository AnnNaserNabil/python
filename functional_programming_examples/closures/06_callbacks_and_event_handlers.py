"""
6. Callbacks and Event Handlers with Closures

This module demonstrates how closures can be used to implement callbacks and event
handlers in Python. It shows how to create an event system where functions can
subscribe to events and be notified when those events occur.

Key Concepts:
------------
1. Event-Driven Programming: Writing code that responds to events (like button clicks)
2. Callback Functions: Functions passed as arguments to be executed later
3. Event Emitters: Objects that emit events and notify registered handlers
4. Closures in Callbacks: How closures maintain access to their lexical scope

Why Use Closures for Event Handling?
---------------------------------
- Decoupling: Event emitters don't need to know about the handlers
- Stateful Handlers: Handlers can maintain state between calls
- Multiple Handlers: Multiple functions can respond to the same event
- Clean Architecture: Separates event generation from event handling

Real-world Applications:
----------------------
- GUI programming (button clicks, key presses)
- Network programming (request/response handling)
- Game development (collision detection, game events)
- Asynchronous programming (callbacks for completed operations)

Example:
-------
>>> emitter = EventEmitter()
>>> @emitter.on('click')
... def handle_click(event, data):
...     print(f"Button clicked: {data}")
>>> emitter.emit('click', 'User clicked the button!')
"""
from __future__ import annotations
from typing import Callable, Dict, List, Any, Optional, Protocol, runtime_checkable
from dataclasses import dataclass, field
from datetime import datetime
import time
import random

# Protocol for event handlers
@runtime_checkable
class EventHandler(Protocol):
    def __call__(self, event: str, data: Any) -> None:
        ...

# Event data structure
@dataclass
class Event:
    """Represents an event with a name, data, and timestamp."""
    name: str
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)

# Event emitter class using closures
class EventEmitter:
    """
    A simple event emitter implementation using closures.
    
    This class allows objects to subscribe to named events and be notified when
    those events occur. It's a foundational pattern in event-driven programming.
    
    Features:
    - Register handlers for specific events
    - Emit events with associated data
    - Remove handlers when they're no longer needed
    - Support for multiple handlers per event
    
    Example:
        >>> emitter = EventEmitter()
        >>> def log_event(event, data):
        ...     print(f"{event}: {data}")
        >>> emitter.on('data')(log_event)
        >>> emitter.emit('data', {'value': 42})
    """
    
    def __init__(self) -> None:
        self._handlers: Dict[str, List[EventHandler]] = {}
    
    def on(self, event_name: str) -> Callable[[EventHandler], EventHandler]:
        """Decorator to register an event handler."""
        def decorator(handler: EventHandler) -> EventHandler:
            self.add_handler(event_name, handler)
            return handler
        return decorator
    
    def add_handler(self, event_name: str, handler: EventHandler) -> None:
        """Add an event handler for the specified event."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
    
    def remove_handler(self, event_name: str, handler: EventHandler) -> None:
        """Remove an event handler."""
        if event_name in self._handlers:
            self._handlers[event_name].remove(handler)
    
    def emit(self, event_name: str, data: Any = None) -> None:
        """Emit an event, calling all registered handlers."""
        event = Event(event_name, data)
        print(f"\n[Event] {event.timestamp}: {event.name}")
        if event_name in self._handlers:
            for handler in self._handlers[event_name]:
                handler(event.name, event.data)

# Example: UI Button with click events
def create_button(emitter: EventEmitter, label: str) -> None:
    """
    Simulate a button that emits click events.
    
    This function demonstrates how UI elements can use an event emitter
    to notify other parts of the application about user interactions.
    
    Args:
        emitter: The event emitter to use for click events
        label: The button's display text
        
    Example:
        >>> emitter = EventEmitter()
        >>> create_button(emitter, "Click me!")
        >>> # The button will emit 'button_click' events when clicked
    """
    def on_click() -> None:
        print(f"Button '{label}' clicked!")
        emitter.emit("button_click", {"button": label, "time": time.time()})
    
    # Simulate button click
    return on_click

# Example: Data loader with progress and completion events
def load_data(emitter: EventEmitter, data_id: str) -> None:
    """
    Simulate loading data with progress updates.
    
    This function demonstrates how to use events to report progress
    during a long-running operation. It emits 'progress' events during
    the operation and a 'complete' event when finished.
    
    Args:
        emitter: The event emitter to use for progress and completion events
        data_id: An identifier for the data being loaded
        
    Events Emitted:
        - 'progress': Contains the current progress percentage
        - 'complete': Emitted when loading is complete
    """
    def load() -> None:
        emitter.emit("load_start", {"id": data_id})
        
        total = 10
        for i in range(total + 1):
            time.sleep(0.2)  # Simulate work
            progress = i / total * 100
            emitter.emit("progress", {"id": data_id, "progress": progress})
        
        # Simulate success or failure
        if random.random() > 0.3:  # 70% success rate
            emitter.emit("load_complete", {"id": data_id, "result": f"Data {data_id} loaded successfully"})
        else:
            emitter.emit("error", {"id": data_id, "message": "Failed to load data"})
    
    return load

def demonstrate_callbacks() -> None:
    """
    Demonstrate various patterns for using closures with callbacks and events.
    
    This function shows:
    1. How to create and use an event emitter
    2. Registering event handlers using decorators
    3. Creating UI elements that emit events
    4. Simulating asynchronous operations with progress updates
    
    The examples progress from simple to more complex usage patterns,
    showing how closures help maintain state between event emissions.
    """
    # Create an event emitter
    emitter = EventEmitter()
    
    # Register event handlers using decorators
    @emitter.on("button_click")
    def handle_button_click(event: str, data: Any) -> None:
        print(f"Handling button click: {data['button']} at {data['time']}")
    
    # Register event handlers using method
    def handle_load_start(event: str, data: Any) -> None:
        print(f"Starting to load data: {data['id']}")
    
    def handle_progress(event: str, data: Any) -> None:
        print(f"Progress: {data['id']} - {data['progress']:.0f}%")
    
    def handle_complete(event: str, data: Any) -> None:
        print(f"Completed: {data['result']}")
    
    def handle_error(event: str, data: Any) -> None:
        print(f"Error: {data['message']}")
    
    emitter.add_handler("load_start", handle_load_start)
    emitter.add_handler("progress", handle_progress)
    emitter.add_handler("load_complete", handle_complete)
    emitter.add_handler("error", handle_error)
    
    # Create some buttons
    button1 = create_button(emitter, "Submit")
    button2 = create_button(emitter, "Cancel")
    
    # Simulate button clicks
    print("=== Simulating Button Clicks ===")
    button1()
    button2()
    
    # Simulate data loading
    print("\n=== Simulating Data Loading ===")
    load_data1 = load_data(emitter, "data1")
    load_data1()
    
    # Show multiple data loads
    print("\n=== Simulating Multiple Data Loads ===")
    for i in range(3):
        load_fn = load_data(emitter, f"data_{i+1}")
        load_fn()
        time.sleep(0.5)
    
    # Demonstrate removing a handler
    print("\n=== Removing a Handler ===")
    emitter.remove_handler("progress", handle_progress)
    print("Progress handler removed. Loading data again...")
    load_data(emitter, "data_final")()

if __name__ == "__main__":
    print("=== Callbacks and Event Handlers ===")
    demonstrate_callbacks()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures are commonly used for callbacks and event handlers")
    print("2. Event emitters use closures to maintain handler references")
    print("3. Handlers can be added and removed dynamically")
    print("4. The same event can have multiple handlers")
    print("5. This pattern is widely used in GUI frameworks and async programming")
