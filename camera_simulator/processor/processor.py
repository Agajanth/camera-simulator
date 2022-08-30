from typing import Callable
import numpy as np
from .baseProcessor import BaseProcessor, SizeImageException



class Lens(BaseProcessor):

    def __init__(self,height:int,width:int,enable:bool = False):
        self.enable = enable
        self.height = height
        self.width = width

    def process(self,image: np.ndarray) -> np.ndarray:

        if image is not None:
            if image.shape == (self.height,self.width):
                return image
            else:
                raise SizeImageException("The dimension of the np-image doesn't match with the accepted size")
        else:
            raise Exception("image is None")

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


    @property
    def funct(self) -> Callable:
        return self.__funct

    @funct.setter
    def funct(self, funct:Callable):
        self.__funct = funct



def lens():
    def decorator(funct:Callable):
        def wrapper(image,height,width):
            len_dec = Lens(height,width)
            a = len_dec.process(image)
            b = funct(image)
        return wrapper
    return decorator

class Sensor(BaseProcessor):

    def __init__(self,gain: float,enable = False) -> None:
        self.gain = gain
        self.enable = enable


    @lens()
    def process(image: np.ndarray, height:int = 0, width:int = 0) -> np.ndarray:
        try:
            if image is not None:
                return image*self.gain
        except ValueError as e:
            print(f"Array doesn't have info: {e}")


    @property
    def gain(self) -> float:
        return self.__gain

    @gain.setter
    def gain(self,gain:float):
        try:
            if gain > 0:
                self.__gain = gain
            else:
                raise ValueError("gain shloud be greater than 0")

        except ValueError as e:
            print(f"ValueError setting gain in Sensor: {e}")

