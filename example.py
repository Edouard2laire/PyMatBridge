from pymatbridge import PyMatBridge
import matlab.engine

import matlab.engine
print(matlab.engine.find_matlab()) 

#bridge = PyMatBridge()
#bridge.call("math.sin", 3.14)  # Calls Python function
#bridge.call("sin", 3.14)       # Calls MATLAB function