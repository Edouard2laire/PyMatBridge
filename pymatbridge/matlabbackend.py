from .genericbackendinterface import GenericBackendInterface  # Explicitly expose the class

import logging
import matlab.engine
from typing import Any, Callable, Optional

logger = logging.getLogger("MatlabBackend")
logger.addHandler(logging.NullHandler())  # Prevents logging if the user doesn't configure it


class MatlabBackend(GenericBackendInterface):

    eng: matlab.engine.MatlabEngine | None
    nargout: int = 1
    path: list[ tuple[str, int]] | None = None

    def __init__(self):
        self.name = 'matlab'
        self.eng = None
        self.path = []

    def is_running(self) -> bool:
        if self.eng is None:
            return False
        
        return self.eng._check_matlab()

    def addpath(self, folder:str, add_subfolder: Optional[bool] = False) -> GenericBackendInterface : 

        self.path.append( (folder,add_subfolder ) )

        if self.is_running():
            self.__run_addpath( [self.path[-1]])

        return self
    
    def __run_addpath(self, new_paths: list[ tuple[str, int]]): 
        ''' Run the addpath function from matlab
            Assume that matlab is started
        '''

        for (folder, add_subfolder) in new_paths: 

            if add_subfolder:
                folder = self.eng.genpath(folder , nargout = 1)

            self.eng.addpath(folder , nargout = 0)

    def start(self) -> bool: 

        logger.info('Starting matlab engine')

        try:
            self.eng = matlab.engine.start_matlab()
        except matlab.engine.EngineError as e:
            logger.error(f"Failed to start MATLAB engine: {str(e)}")
            self.eng = None
            return False
        
        self.__run_addpath(self.path)
        return True
    
    def get_function(self, func_name:str) -> Callable[..., Any] | None:  
        if not self.is_running(): 
            logger.debug('[get_function] MATLAB is not started')
            return None
        
        return getattr(self.eng, func_name, None)

    def set_nargout(self, nargout: int | None):
        """ Set nargout for the next MATLAB function call. """

        if nargout is None: 
            nargout = 1

        self.nargout = nargout

    def call(self, func_name:str, *args, **kwargs) -> any:

        func = self.get_function(func_name)

        if func is None:
            logger.error(f"MATLAB is not started")
            raise RuntimeError(f"MATLAB is not started")

        matlab_args = [matlab.double(arg) if isinstance(arg, (list, tuple)) else arg for arg in args]
            
        try:
            return func(*matlab_args,**kwargs, nargout=self.nargout)
        
        except matlab.engine.MatlabExecutionError as e:
            if str(e).find('Unrecognized function or variable'): 
                raise NameError(f"Function '{func_name}' not found")
            
            logger.error(f"MATLAB execution error for '{func_name}': {e}")
            raise

    def stop(self): 
        if self.is_running():
            logger.info('Stopping matlab engine')
            self.eng.exit()

        self.eng = None 