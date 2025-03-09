from pymatbridge import PyMatBridge, PythonBackend, MatlabBackend, CBackend
import logging
import numpy as np

def sum_of_square(n:int):
    return sum( x*x for x in range(1,n+1) )

# User-defined logging setup
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.ERROR  # User can set DEBUG, INFO, WARNING, etc.
)


bridge = PyMatBridge()
bridge.add_backend(PythonBackend()) \
    .load_python_module('math')\
    .load_python_module('numpy', 'np')\
    .link_python_function('sum_of_square', sum_of_square)

# ✅ Works in Python

print("Sin(3.14) \t= " , bridge.call("math.sin", 3.14 )) 
print("Sum of square \t= ", bridge.call("sum_of_square", 20 )) 

# ✅ Works in Matlab

bridge.add_backend(MatlabBackend())
print("Sin(3.14) \t= " , bridge.call("sin", 3.14) ) 

# Error as the function does not exist
try:
    print("Sin(3.14) \t= " , bridge.call("FunctionThatDoesNotExist", 3.14) ) 
except RuntimeError as e:
    logging.error(str(e))

# Matlab: Create a 10x10 random matrix and then call SVD
A = bridge.call('randn', 10, 10)
(Ua, Sa, Va) = bridge.call('svd', A, 'vector', __nargout=3)


# Python: Call SVD on the matrix created by matlab
(Ub, Sb, Vb) = bridge.call('np.linalg.svd', A, full_matrices=True)

print('MATLAB: \n', np.matrix(Sa).transpose())
print('Python: \n', np.matrix(Sb))


# C: Calling C function

bridge = PyMatBridge()
bridge.add_backend(CBackend("libmathfuncs.so"))

print("Square of 5.5:", bridge.call("square", 5.5))

