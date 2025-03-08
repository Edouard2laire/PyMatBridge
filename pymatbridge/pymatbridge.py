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

