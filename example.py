from pymatbridge import PyMatBridge, PythonBackend, MatlabBackend
import logging

def sum_of_square(n:int):
    return sum( x*x for x in range(1,n+1) )

# User-defined logging setup
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO  # User can set DEBUG, INFO, WARNING, etc.
)


bridge = PyMatBridge()
bridge.add_backend(PythonBackend()) \
    .load_python_module('math')\
    .link_python_function('sum_of_square', sum_of_square)

# ✅ Works in Python

print("Sin(3.14) \t= " , bridge.call("math.sin", 3.14) ) 
print("Sum of square \t= ", bridge.call("sum_of_square", 20 )) 

# ✅ Works in Matlab

bridge.add_backend(MatlabBackend())
print("Sin(3.14) \t= " , bridge.call("sin", 3.14) ) 


