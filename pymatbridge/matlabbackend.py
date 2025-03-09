from .genericbackendinterface import GenericBackendInterface  # Explicitly expose the class

import logging
import matlab.engine

logger = logging.getLogger("MatlabBackend")
logger.addHandler(logging.NullHandler())  # Prevents logging if the user doesn't configure it


class MatlabBackend(GenericBackendInterface):

    eng: matlab.engine.MatlabEngine | None

    def __init__(self):
        self.name = 'matlab'
        self.eng = None
    
    def is_running(self) -> bool:
        if self.eng is None:
            return False
        
        return self.eng._check_matlab()

    def start(self): 
        logger.info('Starting matlab engine')
        self.eng = matlab.engine.start_matlab()

    def call(self, func_name:str, *args, **kwargs) -> any:
        if not self.is_running():
            self.start()

        matlab_args = [matlab.double(arg) if isinstance(arg, (list, tuple)) else arg for arg in args]
        return self.eng.feval(func_name, *matlab_args)

    def stop(self): 
        if self.is_running():
            logger.info('Stopping matlab engine')
            self.eng.exit()
