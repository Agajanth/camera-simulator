import re
from typing import Callable
import numpy as np
from .baseProcessor import BaseProcessor, SizeImageException
import functools
import concurrent.futures as cf

class Lens(BaseProcessor):

    def __init__(self,height:int,width:int,enable:bool = True):
        self.enable = enable
        self.height = height
        self.width = width

    def process(self,image: np.ndarray) -> np.ndarray:
        if self.enable:
            if image is not None:
                if image.shape == (self.height,self.width):
                    return image
                else:
                    raise SizeImageException("The dimension of the np-image doesn't match with the accepted size")
            else:
                raise Exception("image is None")
        else:
            return "The lens class is not enable"

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height:int):
        if isinstance(height,int) :
            if height >=0:
                self.__height = height
            else:
                raise ValueError("Height must be a positive integer")

        else:
            raise ValueError("Height must be a positive integer")

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self,width:int):
        if isinstance(width,int):
            if width >=0 :
                self.__width = width
            else:
                 raise ValueError("Width must be positive integer")
        else:
            raise ValueError("Width must be positive integer")



def lens(orig_func):
    functools.wraps(orig_func)
    def wrapper(*args,**kwds):
        lens=Lens(args[2],args[3],args[4])
        if lens.enable:
            a = lens.process(args[1])
        result = orig_func(*args,**kwds)
        return result
    return wrapper


class Sensor(BaseProcessor):

    def __init__(self,gain: float,enable = True) -> None:
        self.gain = gain
        self.enable = enable


    @lens
    def process(self,image: np.ndarray, height:int = 0, width:int = 0, enable:bool = False) -> np.ndarray:
        if image is not None and image.size >0:
            if isinstance(image,np.ndarray):
                return image*self.gain
            else:
                raise ValueError("Array doesn't have info")
        else:
            raise ValueError("Array doesn't have info")



    @property
    def gain(self) -> float:
        return self.__gain

    @gain.setter
    def gain(self,gain:float):
        if isinstance(gain,float):
            if gain >=0 :
                self.__gain = gain
            else:
                raise ValueError("Gain must be positive float")
        else:
            raise ValueError("Gain must be positive float")

def mymean():
    random_image = np.random.random((100,100))
    sensor = Sensor(1.0)
    result = np.mean(sensor.process(random_image,100,100,True))
    print(result)
    return result

def con():
    worker = cf.ProcessPoolExecutor(max_workers=5)
    for i in range(100):
        print(f"iteration {i}, result = {worker.submit(mymean)}")
