from .genericbackendinterface import GenericBackendInterface  # Explicitly expose the class
import matlab.engine


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
        print('Starting matlab engine')
        self.eng = matlab.engine.start_matlab()

    def call(self, func_name:str, *args, **kwargs) -> any:
        if not self.is_running():
            self.start()

        matlab_args = [matlab.double(arg) if isinstance(arg, (list, tuple)) else arg for arg in args]
        return self.eng.feval(func_name, *matlab_args)

    def stop(self): 
        if self.is_running():
            print('Stopping matlab engine')
            self.eng.exit()
