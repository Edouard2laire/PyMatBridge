from pymatbridge import PyMatBridge, PythonBackend, MatlabBackend

def sum_of_square(n:int):
    return sum( x*x for x in range(1,n+1) )


bridge = PyMatBridge()
bridge.add_backend(PythonBackend()) \
    .load_python_module('math')\
    .link_python_function('sum_of_square', sum_of_square)

# ✅ Works in Python

print("Sin(3.14) \t= " , bridge.call("math.sin", 3.14) ) 
print("Sum of square \t= ", bridge.call("sum_of_square", 20 )) 

# ✅ Works in Matlab

bridge.add_backend(MatlabBackend())
print(bridge.call("sin", 3.14))  
print(bridge.call("magic", 3)) 
