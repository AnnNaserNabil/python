# Functional Programming Examples in Python

This repository contains practical examples of functional programming concepts implemented in Python. The examples are designed to be educational, well-documented, and demonstrate how to write pure functions and leverage functional programming patterns.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Pure Functions](#pure-functions)
  - [Higher-Order Functions](#higher-order-functions)
  - [Lazy Evaluation](#lazy-evaluation)
  - [Advanced Functional Patterns](#advanced-functional-patterns)
- [Contributing](#contributing)
- [License](#license)

## Features

- Pure function implementations
- Immutable data structures
- Function composition and currying
- Lazy evaluation with generators
- Advanced patterns like monads and lenses
- Comprehensive documentation with examples
- Type hints for better code clarity

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/functional_programming_examples.git
   cd functional_programming_examples
   ```

2. Ensure you have Python 3.8+ installed.

3. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage

Each Python file in the `pure_functions` directory demonstrates different functional programming concepts. You can run them directly:

```bash
python pure_functions/01_pure_functions.py
python pure_functions/08_higher_order_functions.py
python pure_functions/09_lazy_evaluation.py
python pure_functions/10_advanced_functional_patterns.py
```

## Examples

### Pure Functions

Basic examples of pure functions that have no side effects and always produce the same output for the same inputs.

### Higher-Order Functions

Functions that take other functions as arguments or return them as results, including decorators and function composition.

### Lazy Evaluation

Implementation of lazy evaluation patterns using Python generators and the `itertools` module.

### Advanced Functional Patterns

Advanced concepts including:

- **Maybe Monad**: For handling optional values
- **Either Monad**: For error handling
- **Function Currying**: For partial function application
- **Immutable Data Structures**: With structural sharing
- **Lenses**: For working with nested immutable data structures

## Example: Advanced Functional Patterns

```python
# Using the Maybe monad
def safe_divide(x: float, y: float) -> Maybe[float]:
    if y == 0:
        return Nothing()
    return Just(x / y)

# Safe division that handles division by zero
result = safe_divide(10, 2).bind(lambda x: Just(x * 3))  # Just(15.0)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by functional programming concepts from Haskell, Scala, and other functional languages
- Thanks to the Python community for excellent functional programming support
