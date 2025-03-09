from pymatbridge import PyMatBridge, PythonBackend, MatlabBackend
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
    .load_module('math')\
    .load_function_from_module('math','cos')\
    .load_module('numpy', 'np')\
    .load_function(sum_of_square)

# ✅ Works in Python

print("Sin(3.14) \t= " , bridge.call("math.sin", 3.14 )) 
print("Cos(3.14) \t= " , bridge.call("cos", 3.14 )) 
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
