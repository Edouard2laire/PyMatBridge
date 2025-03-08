
from .genericbackendinterface import GenericBackendInterface  # Explicitly expose the class
from typing import Optional


class PyMatBridge:

    backend: list[GenericBackendInterface]
 
    def __init__(self ):

        self.backend = []


    def add_backend(self, backend: GenericBackendInterface ) -> GenericBackendInterface: 

            if isinstance(backend, GenericBackendInterface):
                self.backend.append(backend)
            else:
                raise NotImplementedError(" Unsuported backend ")

            return backend

    def call(self, func_name:str, *args, **kwargs) -> any:
        """ 
            Call the function  func_name using the defined backend 
        """

        if self.backend is None or len(self.backend) == 0 :
              raise ValueError(f"No backend available.")

        for iBackend, backend in enumerate(self.backend, start = 1):
            
            print(f"Backend {iBackend} : calling {backend.name}")
            
            try:
                if not backend.is_running():
                    backend.start()
            
                return backend.call(func_name, *args, **kwargs)
            
            except (NameError,ValueError) as e:
                pass

        raise ValueError(f"Function '{func_name}' not found.")
