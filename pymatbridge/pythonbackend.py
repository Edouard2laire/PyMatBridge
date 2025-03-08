from .genericbackendinterface import GenericBackendInterface  # Explicitly expose the class

from types import ModuleType, FunctionType
from typing import Literal, Optional

import importlib
import builtins

class PythonBackend(GenericBackendInterface):
    """ Executes functions in Python dynamically. """


    loaded_python_module: dict[str, ModuleType] 

    def __init__(self):
        self.name = 'python'
        self.loaded_python_module = {} 

    def is_running(self) -> bool:
        return True

    def start(self): 
        pass

    def call(self, func_name:str, *args, **kwargs) -> any:
        
        # Check in the loaded functions 
        func = self.get_python_module(func_name)
        if callable(func):
            return func(*args, **kwargs)

        # Check in builtins functions 
        func = getattr(builtins, func_name, None)
        if callable(func) :
            return func(*args, **kwargs)
        
        raise NameError(f"Function '{func_name}' not found")
    
    def stop(self): 
        pass

    # All functions related to Python 
    def load_python_module(self, module_name:str, alias:str|None = None) -> GenericBackendInterface: 
        alias = module_name if alias is None else alias

        if alias in self.loaded_python_module : 
            print(f' Module {alias} is already loaded')

        # Import module dynamically
        try:
            module = importlib.import_module(module_name)  
        except ( ModuleNotFoundError):
            print(f"Unable to load {module_name} as {alias}. Module not found")
        
        self.loaded_python_module[alias] = module
        return self

    def link_python_function(self, alias:str, func:FunctionType) -> GenericBackendInterface:
        if not callable(func):
            print(f'{alias} is not callable')

        if alias in self.loaded_python_module : 
            print(f' Function {alias} is already loaded')
        
        self.loaded_python_module[alias] = func
        return self
    
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

