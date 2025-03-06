import builtins
import importlib
from types import ModuleType, FunctionType
import matlab.engine

class PyMatBridge:

    loaded_python_module: dict[str, ModuleType] 
    eng: matlab.engine.MatlabEngine | None

    def __init__(self):

        self.eng = None
        self.loaded_python_module = {} 

    def start_matlab(self):
        print('Starting matlab engine')
        self.eng = matlab.engine.start_matlab()

    def load_python_module(self, module_name:str, alias:str|None = None) -> bool: 
        alias = module_name if alias is None else alias

        if alias in self.loaded_python_module : 
            print(f' Module {alias} is already loaded')
            return True

        # Import module dynamically
        try:
            module = importlib.import_module(module_name)  
        except ( ModuleNotFoundError):
            print(f"Unable to load {module_name} as {alias}. Module not found")
            return False
        
        self.loaded_python_module[alias] = module
        return True
    def link_python_function(self, alias:str, func):
        if alias in self.loaded_python_module : 
            print(f' Function {alias} is already loaded')
            return True
        
        self.loaded_python_module[alias] = func



    def get_loaded_python_module(self): 
        return list(self.loaded_python_module.keys())

    def get_python_module(self,  module_name:str) -> ModuleType | FunctionType | None:
        ''' Return the module module_name '''

        if module_name in self.loaded_python_module:
            return self.loaded_python_module[module_name]

        if "." not in module_name:
            return None
        
        parent_module, sub_module = module_name.rsplit(".", 1)

        # We check if the parent module is loaded
        module = self.get_python_module(parent_module)
        return getattr(module, sub_module)

    def call(self, func_name, *args, **kwargs):

        """ Try calling a Python function first, then fall back to MATLAB. """
        try:
            return self.call_python(func_name, *args, **kwargs)
        except NameError as e:
            print(str(e))
            pass

        print("Calling matlab function")
        if self.eng is None:
            self.start_matlab()

        try:

            matlab_args = [matlab.double(arg) if isinstance(arg, (list, tuple)) else arg for arg in args]
            return self.eng.feval(func_name, *matlab_args)
        
        except matlab.engine.MatlabExecutionError:
            raise ValueError(f"Function '{func_name}' not found in Python or MATLAB.")


    def call_python(self, func_name:str, *args, **kwargs) -> any:
        
        # Check in the loaded functions 
        func = self.get_python_module(func_name)
        if callable(func):
            return func(*args, **kwargs)

        # Check in builtins functions 
        func = getattr(builtins, func_name, None)
        if callable(func) :
            return func(*args, **kwargs)
        
        raise NameError(f"Function '{func_name}' not found")
            

    def stop_matlab(self):
        self.eng.exit()