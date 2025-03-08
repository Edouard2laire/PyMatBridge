from pymatbridge import PyMatBridge, GenericBackendInterface

bridge = PyMatBridge(backend=["python", "matlab"])
bridge.load_python_module('math')

print("Sin(3.14) \t= " , bridge.call("math.sin", 3.14) ) 

def sum_of_square(n:int):
    return sum( x*x for x in range(1,n+1) )

bridge.link_python_function('sum_of_square', sum_of_square)
print("Sum of square \t= ", bridge.call("sum_of_square", 20 )) 


print("randn(3) \t= " , bridge.call("randn", 3) ) 


test = GenericBackendInterface()
