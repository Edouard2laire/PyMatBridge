
from .genericbackendinterface import GenericBackendInterface  # Explicitly expose the class
import logging

# Create a logger for the library
logger = logging.getLogger("PyMatBridge")
logger.addHandler(logging.NullHandler())  # Prevents logging if the user doesn't configure it

class PyMatBridge:

    backend: list[GenericBackendInterface]
 
    def __init__(self ):

        self.backend = []

    def add_backend(self, backend: GenericBackendInterface ) -> GenericBackendInterface: 

        if not isinstance(backend, GenericBackendInterface):
            raise RuntimeError("Unsuported backend")
        
        self.backend.append(backend)
        return backend
    
    def call(self, func_name:str, *args, **kwargs) -> any:
        """ 
            Call the function  func_name using the defined backend 
        """

        if self.backend is None or len(self.backend) == 0 :
              raise RuntimeError(f"No backend available.")

        for iBackend, backend in enumerate(self.backend, start = 1):
            logger.info(f"Backend {iBackend} : calling {backend.name}")
            
            try:
                if not backend.is_running():
                    logger.info(f"Backend {iBackend} is not running. Starting {backend.name}... ")
                    backend.start()

                return backend.call(func_name, *args, **kwargs)
            
            except (NameError,ValueError) as e:
                logger.warning(f"Unable to call '{func_name}' using {backend.name}")
                pass

        raise RuntimeError(f"Function '{func_name}' not found.")
