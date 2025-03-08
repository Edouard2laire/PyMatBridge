
class GenericBackendInterface:

    def __init__(self):
        pass
    
    def is_running(self) -> bool:
        pass

    def start(self): 
        pass

    def call(self, func_name:str, *args, **kwargs) -> any:
        pass

    def stop(self): 
        pass