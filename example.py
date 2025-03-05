from pymatbridge import PyMatBridge


bridge = PyMatBridge()
bridge.load_python_module('numpy', 'np')
bridge.load_python_module('numpy.char', 'np.char') # todo: fixme
bridge.load_python_module('math')

print( f" sin(3.14) = {0:.2f} ".format( bridge.call("math.sin", 3.14)))
print(bridge.call("np.char.array", ['hello', 'world', 'numpy','array'])) 
