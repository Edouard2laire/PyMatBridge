
class GenericBackendInterface:

    name:str = ''

    def __init__(self):
        pass
    
    def is_running(self) -> bool:
        return True

    def start(self): 
        raise NotImplementedError()

    def call(self, func_name:str, *args, **kwargs) -> any:
        raise NotImplementedError()

    def set_nargout(self, nargout: int | None):
        pass    
        
    def stop(self): 
        pass