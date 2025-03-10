.. PyMatBridge documentation master file, created by
   sphinx-quickstart on Sun Mar  9 19:57:54 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyMatBridge documentation
=========================

# PyMatBridge

PyMatBridge is a Python package that provides a seamless interface for calling functions from either Python or MATLAB. It enables users to dynamically execute functions in Python when available and fall back to MATLAB when necessary.

## Features

- **Hybrid Execution:** Automatically calls a Python function if available; otherwise, it executes the MATLAB equivalent.
- **Modular Backend Design:** Supports multiple language backends via an extensible architecture.
- **Dynamic Function Registration:** Load Python modules and link custom functions.
- **Logging Support:** Uses Python's logging module for better debugging and output control.

## Installation

Ensure you have the required dependencies before using PyMatBridge.

### Prerequisites

- Python 3.8+
- MATLAB installed with the MATLAB Engine API for Python

### Installation Steps

```sh
# Clone the repository
git clone https://github.com/yourusername/PyMatBridge.git

# Navigate to the project directory
cd PyMatBridge

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
import logging
from pymatbridge import PyMatBridge, PythonBackend

def sum_of_square(n: int):
    return sum(x * x for x in range(1, n + 1))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize PyMatBridge and add backends
bridge = PyMatBridge()
bridge.add_backend(PythonBackend()) \
      .load_python_module('math') \
      .link_python_function('sum_of_square', sum_of_square)

# Call functions dynamically
print("Sin(3.14) =", bridge.call("math.sin", 3.14))
print("Sum of squares up to 20 =", bridge.call("sum_of_square", 20))
```

### Calling MATLAB Functions

```python
# Call a MATLAB function if it's not available in Python
print("MATLAB sqrt(16) =", bridge.call("sqrt", 16))

# Stop MATLAB engine when done
bridge.stop_matlab()
```

## Logging

Users can configure logging to control output verbosity.

```python
import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("pymatbridge.log"),  # Save logs to file
        logging.StreamHandler()  # Print logs to console
    ]
)
```

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes and push to your fork.
4. Submit a pull request.

## License

MIT License. See `LICENSE` for details.

## Contact

For any issues, please open an issue on GitHub or contact `your.email@example.com`.




.. toctree::
   :maxdepth: 2
   :caption: Contents:

