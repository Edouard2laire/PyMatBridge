import importlib
import matlab.engine

class PyMatBridge:
    def __init__(self):
        self.eng = matlab.engine.start_matlab()

    def call(self, func_name, *args, **kwargs):
        """ Try calling a Python function first, then fall back to MATLAB. """
        try:
            # Handle module-scoped functions like math.sin
            if "." in func_name:
                module_name, func_name = func_name.rsplit(".", 1)
                module = importlib.import_module(module_name)
                func = getattr(module, func_name)
            else:
                func = eval(func_name)  # For built-in or global functions

            return func(*args, **kwargs)
        except (NameError, AttributeError, ModuleNotFoundError):
            pass  # If function not found, try MATLAB
        
        try:
            print("Calling matlab function")
            matlab_args = [matlab.double(arg) if isinstance(arg, (list, tuple)) else arg for arg in args]
            return self.eng.feval(func_name, *matlab_args)
        except matlab.engine.MatlabExecutionError:
            raise ValueError(f"Function '{func_name}' not found in Python or MATLAB.")

    def stop_matlab(self):
        self.eng.quit()