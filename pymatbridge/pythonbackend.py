from .genericbackendinterface import GenericBackendInterface  # Explicitly expose the class

import logging
from types import ModuleType, FunctionType
from typing import Literal, Optional

import importlib
import builtins

logger = logging.getLogger("PythonBackend")
logger.addHandler(logging.NullHandler())  # Prevents logging if the user doesn't configure it


class PythonBackend(GenericBackendInterface):
    """ Executes functions in Python dynamically. """

    loaded_python_module: dict[str, ModuleType] 

    def __init__(self):
        self.name = 'python'
        self.loaded_python_module = {} 

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
    
    def load_module(self, module_name:str, alias:str|None = None) -> GenericBackendInterface: 
        alias = module_name if alias is None else alias

        if alias in self.loaded_python_module : 
            logger.info(f' Module {alias} is already loaded')

        # Import module dynamically
        try:
            module = importlib.import_module(module_name)  
        except ( ModuleNotFoundError):
            logger.error(f"Unable to load {module_name} as {alias}. Module not found")
        
        self.loaded_python_module[alias] = module
        return self
    
    def load_function_from_module(self, module_name:str, functions: str | list[str] )  -> GenericBackendInterface:

        ''' Load one, or multiple function from a module
            Similar to 'import function from module'

            Example: 
                - import sin from math: bridge.load_function_from_module('math', 'sin')
                - import sin, cos from math: bridge.load_function_from_module('math', ('sin', 'cos') )
            
            Note: 
                - import * from math is not supported
        '''

        # Import module dynamically
        try:
            module = importlib.import_module(module_name)  
        except ( ModuleNotFoundError):
            logger.error(f"Unable to load {module}. Module not found")
        
        if isinstance(functions, str):
            functions = [functions]
        
        for function_name in functions: 
            logger.info(f' Loading  {function_name} from {module_name}')

            function = getattr(module, function_name, None)

            if function is None: 
                logger.error(f"Unable to load {function_name} from {module_name}")
                continue

            self.loaded_python_module[function_name] = function

        return self

    def load_function(self,func:FunctionType,  alias:Optional[str] = None ) -> GenericBackendInterface:

        if alias is None: 
            alias = func.__name__

        if not callable(func):
            logger.error(f'{alias} is not callable')

        if alias in self.loaded_python_module : 
            logger.info(f' Function {alias} is already loaded')
        
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

