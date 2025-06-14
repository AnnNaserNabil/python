"""
8. Dispatch Tables with Higher-Order Functions

Demonstrates how to use dictionaries as dispatch tables to implement
command patterns, state machines, and rule-based systems using higher-order functions.
"""
from __future__ import annotations
from typing import (
    TypeVar, Callable, Any, Dict, List, Tuple, Optional, Union, 
    Protocol, cast
)
from enum import Enum, auto
from dataclasses import dataclass
import math
import random

T = TypeVar('T')

# 1. Basic Command Pattern with Dispatch Table

def handle_add(a: float, b: float) -> float:
    return a + b

def handle_subtract(a: float, b: float) -> float:
    return a - b

def handle_multiply(a: float, b: float) -> float:
    return a * b

def handle_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Dispatch table mapping operation names to functions
OPERATIONS: Dict[str, Callable[[float, float], float]] = {
    'add': handle_add,
    'subtract': handle_subtract,
    'multiply': handle_multiply,
    'divide': handle_divide,
}

def calculator(operation: str, a: float, b: float) -> float:
    """
    Perform a calculation using a dispatch table.
    
    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        a: First operand
        b: Second operand
        
    Returns:
        The result of the operation
        
    Raises:
        ValueError: If the operation is not supported or division by zero
    """
    if operation not in OPERATIONS:
        raise ValueError(f"Unknown operation: {operation}")
    
    return OPERATIONS[operation](a, b)

# 2. State Machine with Dispatch Table

class State(Enum):
    IDLE = auto()
    PROCESSING = auto()
    PAUSED = auto()
    STOPPED = auto()

class Event(Enum):
    START = auto()
    PAUSE = auto()
    RESUME = auto()
    COMPLETE = auto()
    ERROR = auto()
    STOP = auto()

# Type alias for state transition functions
StateTransition = Callable[[], State]

class StateMachine:
    """A simple state machine using a dispatch table for transitions."""
    
    def __init__(self):
        self.state = State.IDLE
        self._transitions: Dict[Tuple[State, Event], StateTransition] = {
            # From IDLE
            (State.IDLE, Event.START): self._start_processing,
            (State.IDLE, Event.STOP): self._stop,
            
            # From PROCESSING
            (State.PROCESSING, Event.PAUSE): self._pause,
            (State.PROCESSING, Event.COMPLETE): self._complete,
            (State.PROCESSING, Event.ERROR): self._error,
            (State.PROCESSING, Event.STOP): self._stop,
            
            # From PAUSED
            (State.PAUSED, Event.RESUME): self._resume,
            (State.PAUSED, Event.STOP): self._stop,
        }
    
    def dispatch(self, event: Event) -> None:
        """Process an event and transition to a new state if valid."""
        transition = self._transitions.get((self.state, event))
        if transition:
            self.state = transition()
            print(f"State changed to: {self.state.name}")
        else:
            print(f"Invalid transition: {self.state.name} -> {event.name}")
    
    # State transition handlers
    def _start_processing(self) -> State:
        print("Starting processing...")
        return State.PROCESSING
    
    def _pause(self) -> State:
        print("Pausing...")
        return State.PAUSED
    
    def _resume(self) -> State:
        print("Resuming...")
        return State.PROCESSING
    
    def _complete(self) -> State:
        print("Processing complete!")
        return State.IDLE
    
    def _error(self) -> State:
        print("An error occurred!")
        return State.IDLE
    
    def _stop(self) -> State:
        print("Stopping...")
        return State.STOPPED

# 3. Rule-Based Processing with Dispatch Tables

@dataclass
class Order:
    order_id: str
    customer_type: str  # 'regular', 'premium', 'vip'
    amount: float
    items: List[str]
    is_express: bool = False

# Type for order processing rules
OrderProcessor = Callable[[Order], Tuple[bool, str]]

def create_order_processor() -> Dict[str, OrderProcessor]:
    """Create a dispatch table of order processing rules."""
    def validate_order(order: Order) -> Tuple[bool, str]:
        if not order.order_id:
            return False, "Order ID is required"
        if order.amount <= 0:
            return False, "Order amount must be positive"
        if not order.items:
            return False, "Order must contain at least one item"
        return True, "Order is valid"
    
    def apply_discounts(order: Order) -> Tuple[bool, str]:
        discount = 0.0
        
        # Premium customers get 10% off
        if order.customer_type == 'premium':
            discount = 0.1
        # VIP customers get 20% off
        elif order.customer_type == 'vip':
            discount = 0.2
        
        if discount > 0:
            original = order.amount
            order.amount = order.amount * (1 - discount)
            return True, f"Applied {discount:.0%} discount (${original - order.amount:.2f})"
        
        return True, "No discounts applied"
    
    def apply_express_shipping(order: Order) -> Tuple[bool, str]:
        if order.is_express:
            # Add express shipping fee
            order.amount += 10.0
            return True, "Express shipping fee applied (+$10.00)"
        return True, "Standard shipping"
    
    def check_inventory(order: Order) -> Tuple[bool, str]:
        # In a real app, this would check inventory levels
        return True, "All items in stock"
    
    def process_payment(order: Order) -> Tuple[bool, str]:
        # In a real app, this would process the payment
        return True, f"Payment of ${order.amount:.2f} processed successfully"
    
    # Return the dispatch table of processing steps
    return {
        'validate': validate_order,
        'discounts': apply_discounts,
        'shipping': apply_express_shipping,
        'inventory': check_inventory,
        'payment': process_payment,
    }

def process_order(order: Order) -> Dict[str, Any]:
    """Process an order using the rule-based dispatch table."""
    processor = create_order_processor()
    results: Dict[str, Any] = {
        'order_id': order.order_id,
        'steps': [],
        'success': True,
        'messages': []
    }
    
    # Define the order of processing steps
    steps = ['validate', 'discounts', 'shipping', 'inventory', 'payment']
    
    for step in steps:
        success, message = processor[step](order)
        results['steps'].append({
            'step': step,
            'success': success,
            'message': message,
            'amount': order.amount
        })
        
        if not success:
            results['success'] = False
            results['error'] = f"Failed at step '{step}': {message}"
            break
    
    results['final_amount'] = order.amount
    return results

# 4. Strategy Pattern with Dispatch Table

def strategy_add(a: float, b: float) -> float:
    return a + b

def strategy_subtract(a: float, b: float) -> float:
    return a - b

def strategy_multiply(a: float, b: float) -> float:
    return a * b

def strategy_divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Dispatch table mapping operation names to strategy functions
STRATEGIES: Dict[str, Callable[[float, float], float]] = {
    'add': strategy_add,
    'subtract': strategy_subtract,
    'multiply': strategy_multiply,
    'divide': strategy_divide,
}

class Calculator:
    """A calculator that uses different strategies for different operations."""
    
    def __init__(self):
        self._strategies = STRATEGIES
    
    def calculate(self, operation: str, a: float, b: float) -> float:
        """
        Perform a calculation using the appropriate strategy.
        
        Args:
            operation: The operation to perform (add, subtract, multiply, divide)
            a: First operand
            b: Second operand
            
        Returns:
            The result of the operation
            
        Raises:
            ValueError: If the operation is not supported or division by zero
        """
        if operation not in self._strategies:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return self._strategies[operation](a, b)
    
    def add_strategy(self, name: str, strategy: Callable[[float, float], float]) -> None:
        """Add a new strategy to the calculator."""
        self._strategies[name] = strategy

def demonstrate_dispatch_tables() -> None:
    print("=== Dispatch Tables with Higher-Order Functions ===\n")
    
    # 1. Basic Command Pattern
    print("1. Basic Calculator with Dispatch Table:")
    try:
        print(f"2 + 3 = {calculator('add', 2, 3)}")
        print(f"10 - 4 = {calculator('subtract', 10, 4)}")
        print(f"7 * 5 = {calculator('multiply', 7, 5)}")
        print(f"15 / 3 = {calculator('divide', 15, 3)}")
        # This will raise an error
        # print(calculator('power', 2, 3))  # Uncomment to see the error
    except ValueError as e:
        print(f"Error: {e}")
    
    # 2. State Machine
    print("\n2. State Machine with Dispatch Table:")
    sm = StateMachine()
    
    # Valid transitions
    sm.dispatch(Event.START)    # IDLE -> PROCESSING
    sm.dispatch(Event.PAUSE)    # PROCESSING -> PAUSED
    sm.dispatch(Event.RESUME)   # PAUSED -> PROCESSING
    sm.dispatch(Event.COMPLETE) # PROCESSING -> IDLE
    sm.dispatch(Event.START)    # IDLE -> PROCESSING
    sm.dispatch(Event.STOP)     # PROCESSING -> STOPPED
    
    # Invalid transition
    sm.dispatch(Event.RESUME)   # Invalid from STOPPED
    
    # 3. Rule-Based Order Processing
    print("\n3. Rule-Based Order Processing:")
    
    # Create some test orders
    orders = [
        Order("ORD001", "regular", 100.0, ["Item1", "Item2"]),
        Order("ORD002", "premium", 200.0, ["Item3"], is_express=True),
        Order("ORD003", "vip", 500.0, ["Item4", "Item5", "Item6"]),
    ]
    
    for order in orders:
        print(f"\nProcessing order {order.order_id} (${order.amount:.2f}):")
        result = process_order(order)
        
        if result['success']:
            print(f"  Success! Final amount: ${result['final_amount']:.2f}")
        else:
            print(f"  Failed: {result.get('error', 'Unknown error')}")
        
        print("  Steps:")
        for step in result['steps']:
            print(f"    {step['step']}: {step['message']} (${step['amount']:.2f})")
    
    # 4. Strategy Pattern
    print("\n4. Strategy Pattern with Dispatch Table:")
    calc = Calculator()
    
    # Use built-in strategies
    print(f"8 + 4 = {calc.calculate('add', 8, 4)}")
    print(f"8 - 4 = {calc.calculate('subtract', 8, 4)}")
    
    # Add a custom strategy (power)
    calc.add_strategy('power', lambda x, y: x ** y)
    print(f"2 ^ 8 = {calc.calculate('power', 2, 8)}")

if __name__ == "__main__":
    demonstrate_dispatch_tables()
    
    print("\n=== Key Takeaways ===")
    print("1. Dispatch tables replace complex conditionals with dictionary lookups")
    print("2. They make it easy to add/remove behaviors at runtime")
    print("3. Useful for implementing state machines, command patterns, and rule engines")
    print("4. Improve readability by separating behavior definition from selection")
