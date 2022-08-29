from abc import ABC, abstractmethod
import numpy as np
from error_handler import SizeImageException

class Interface(type):



    def __init__(self, name, bases, namespace):
        for base in bases:
            must_implement = getattr(base, 'abstract_methods', [])
            class_methods = getattr(self, 'all_methods', [])
            for method in must_implement:
                if method not in class_methods:
                    err_str = """Can't create from abstract class {name}!
                    {name} must implement abstract method {method} of class {base_class}!""".format(name=name,
                        method=method,
                        base_class=base.__name__)
                    raise TypeError(err_str)

    def __new__(metaclass, name, bases, namespace):
        namespace['abstract_methods'] = Interface._get_abstract_methods(namespace)
        namespace['all_methods'] = Interface._get_all_methods(namespace)
        cls = super().__new__(metaclass, name, bases, namespace)
        return cls

    def _get_abstract_methods(namespace):
        return [name for name, val in namespace.items() if callable(val) and getattr(val, '__isabstract__', False)]

    def _get_all_methods(namespace):
        return [name for name, val in namespace.items() if callable(val)]

class BaseProcessor(ABC):
    """
    BaseProcessor class to create an processor Interface

    properties:
        enable : boolean

    """
    @abstractmethod
    def process(image: np.ndarray) -> np.ndarray:
        raise("not implement")

    @property
    def enable(self) -> bool:
        return self.__enable

    @enable.setter
    def enable(self,enable:bool):
        self.__enable = enable





class Lens(BaseProcessor):

    def __init__(self,height:int,width:int,enable:bool):
        self.enable = enable
        self.height = height
        self.width = width

    def process(image: np.ndarray) -> np.ndarray:

        try:
            if image is not None:
                if image.shape == (self.height,self.width):
                    return image
                else:
                    raise SizeImageException("The dimension of the np-image doesn't match with the accepted size")
            else:
                Exception("image is None")

        except Exception as e:
            print(f"Exception has raisen in proccess method: {e}" )


    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height:int):
        self.__height = height

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self,width:int):
        self.__width = width
