
class GenericBackendInterface:

    name:str = ''
    
    def __init__(self):
        pass
    
    def is_running(self) -> bool:
        raise NotImplementedError()

    def start(self): 
        raise NotImplementedError()

    def call(self, func_name:str, *args, **kwargs) -> any:
        raise NotImplementedError()

    def stop(self): 
        raise NotImplementedError()