from pymatbridge import PyMatBridge


bridge = PyMatBridge()
bridge.load_python_module('math')

def square(x):
    return x*x

def sum_of_square(n):
    return sum( square(x) for x in range(1,n) )


print( f"Sin(3.14) = {0:.2f} ".format( bridge.call("math.sin", 3.14)))

bridge.link_python_function('sum_of_square', sum_of_square)
print("Sum of square: ", bridge.call("sum_of_square", 10 )) 

