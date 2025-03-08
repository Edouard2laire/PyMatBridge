import builtins
import importlib
from types import ModuleType, FunctionType
from typing import Literal, Optional

import matlab.engine

class PyMatBridge:

    loaded_python_module: dict[str, ModuleType] 
    eng: matlab.engine.MatlabEngine | None
    backend: list[str]

    
    def __init__(self, backend: Optional[ Literal["python", "matlab"] | list[Literal["python", "matlab"]]] = None ):

        self.backend = []
        self.set_backend(backend)

        self.eng = None
        self.loaded_python_module = {} 

    def set_backend(self, backends: Optional[ Literal["python", "matlab"] | list[Literal["python", "matlab"]]]):

        if backends is None:
            self.backend = []
            return
        
        if isinstance(backends, str):
            backends = [backends]
        
        for backend in backends:
            match backend:
                case 'python' | 'matlab': 
                    self.backend.append(backend)
                case _:
                    raise NotImplementedError(f"'{backend}' is not a supported backed. ")


    def call(self, func_name:str, *args, **kwargs) -> any:
        """ 
            Call the function  func_name using the defined backend 
        """

        if self.backend is None or len(self.backend) == 0 :
              raise ValueError(f"No backend available.")

        for iBackend, backend_name in enumerate(self.backend, start = 1):
            
            # print(f"Backend {iBackend} : calling {backend_name}")

            match backend_name:
                case "python":
                    try:
                        return self.call_python(func_name, *args, **kwargs)
                    
                    except (NameError,ValueError) as e:
                        pass
                case "matlab": 

                    if not self.is_matlab_started():
                        self.start_matlab()

                    try:
                        return self.call_matlab(func_name, *args, **kwargs)
                    except NameError as e:
                        pass  
                case _:          
                    raise NotImplementedError(f"'{backend_name}' is not a supported backed. ")

        raise ValueError(f"Function '{func_name}' not found.")

    # All functions related to Matlab 

    def start_matlab(self):
        print('Starting matlab engine')
        self.eng = matlab.engine.start_matlab()

    def is_matlab_started(self):
        if self.eng is None:
            return False
        
        return self.eng._check_matlab()
    def call_matlab(self, func_name:str, *args, **kwargs) -> any:
        if not self.is_matlab_started():
            self.start_matlab()

        matlab_args = [matlab.double(arg) if isinstance(arg, (list, tuple)) else arg for arg in args]
        return self.eng.feval(func_name, *matlab_args)


    def stop_matlab(self):
        if self.is_matlab_started():
            print('Stopping matlab engine')
            self.eng.exit()


    # All functions related to Python 
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
    
    def link_python_function(self, alias:str, func:FunctionType) -> bool:
        if not callable(func):
            print(f'{alias} is not callable')
            return False
        if alias in self.loaded_python_module : 
            print(f' Function {alias} is already loaded')
            return True
        
        self.loaded_python_module[alias] = func
        return True


    def get_loaded_python_module(self)  -> list: 
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
        return getattr(module, sub_module, None)


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
            