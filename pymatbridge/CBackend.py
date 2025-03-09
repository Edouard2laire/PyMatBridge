import logging
import ctypes
from typing import Any, Optional
from .genericbackendinterface import GenericBackendInterface

logger = logging.getLogger("CBackend")
logger.addHandler(logging.NullHandler())  # Prevents logging if the user doesn’t configure it

class CBackend(GenericBackendInterface):

    def __init__(self, lib_path: str):
        """
        Initialize the C backend by loading the shared library.

        :param lib_path: Path to the compiled C shared library (.so, .dll, .dylib)
        """
        self.name = "C"
        self.lib_path = lib_path
        self.lib = None

    def is_running(self) -> bool:
        """ Check if the shared library is loaded. """
        return self.lib is not None

    def start(self) -> bool:
        """ Load the shared library and prepare the backend. """
        logger.info(f"Loading C library from {self.lib_path}")
        try:
            self.lib = ctypes.CDLL(self.lib_path)
            return True
        except OSError as e:
            logger.error(f"Failed to load C library: {e}")
            self.lib = None
            return False

    def get_function(self, func_name: str) -> Optional[ctypes.CFUNCTYPE]:
        """ Get a function from the shared library. """
        if not self.is_running():
            logger.error("C library is not loaded")
            return None

        try:
            return getattr(self.lib, func_name)
        except AttributeError:
            logger.warning(f"Function '{func_name}' not found in the C library")
            return None

    def call(self, func_name: str, *args, **kwargs) -> Any:
        """ Call a function from the shared library. """
        if not self.is_running():
            raise RuntimeError("C library is not loaded")

        func = self.get_function(func_name)
        func.argtypes = [ctypes.c_double]  # Expecting a double input
        func.restype = ctypes.c_double     # Returning a double
        
        if func is None:
            raise NameError(f"Function '{func_name}' not found in C library")

        try:
            return func(*args)  # C functions don’t use keyword arguments
        except Exception as e:
            logger.error(f"Error calling '{func_name}': {e}")
            raise

    def stop(self):
        """ Unload the library (optional, depends on the OS). """
        logger.info("C backend does not require explicit stopping")
        self.lib = None