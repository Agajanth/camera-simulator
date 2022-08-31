import re
from typing import Callable
import numpy as np
from .baseProcessor import BaseProcessor, SizeImageException
import functools
import concurrent.futures as cf

class Lens(BaseProcessor):
    """Lens class for processing images

    The lens class will implement a method called process
    just to procees and evaluate the shape of an image

    Attributes:
        height: int with the height of the image
        width: int with the width of the image
        enable: boolean to enable process method functionality

    """

    def __init__(self,height:int,width:int,enable:bool = True):
        """Constructor for Lens class

        Args:
            height: int with the height of the image
            width: int with the width of the image
            enable: boolean to enable process method functionality


        """
        self.enable = enable
        self.height = height
        self.width = width

    def process(self,image: np.ndarray) -> np.ndarray:
        """ Process an image evaluating the shape
        Args:
            image: A numpy ndarray 2D object

        Returns:
            Processed image

        Rasises:
            SizeImageException: If the image doesn't have a valid shape|size
            Exception: If the image is None
        """
        if self.enable:
            if image is not None and isinstance(image,np.ndarray):
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
        """height property

        int for save the height of the image

        setter:
            Args:
                height:int for save height of the image
            raise:
                ValueError: if the height is not a positive integer
        """
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
        """width property

        int for save the Width of the image

        setter:
        Args:
            height:int for save Width of the image
        raise:
            ValueError: if the Width is not a positive integer
        """
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
    """Sensor class for processing an image

    This class gonna implement an method call process to
    apply gains to an image

    Attributes:
        gain: float wich will be apply in process method
        enable: boolean to enable the process method (not implemented yet)


    """
    def __init__(self,gain: float,enable = True) -> None:
        """Constructor for the Sensor class

        Args:
            gain: float wich will be apply in process method
            enable: boolean to enable the process method


        """
        self.gain = gain
        self.enable = enable


    @lens
    def process(self,image: np.ndarray, height:int = 0, width:int = 0, enable:bool = False) -> np.ndarray:
        """Process an image multiplying by a gain, and it has a decorator that gets enable by the arguments

        Args:
            image: an numpy ndarray 2D object
            height: int for using lens decorator to do lens.process before sensor.process
            width: int for using lens decorator to do lens.process before sensor.process
            enable: boolean object to enable lens decorator (if is False doesn't call lens.process)

        Returns:
            Processed image

        Raises:
            ValueError: When the image is none, void or is not an instance of np.ndarray
        """
        if image is not None and image.size >0:
            if isinstance(image,np.ndarray):
                return image*self.gain
            else:
                raise ValueError("Array doesn't have info")
        else:
            raise ValueError("Array doesn't have info")



    @property
    def gain(self) -> float:
        """gain property

        float for save the gain wich will be apply to the image

        setter:
            Args:
                gain:float for save the gain wich will be apply to the image
            raise:
                ValueError: if the gain is not a positive float
        """
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
    """My mean function to take the mean of an image

    this function generates a random image and pass it  through
    a sensor function, and return the mean of the image
    """
    random_image = np.random.random((100,100))
    sensor = Sensor(1.0)
    result = np.mean(sensor.process(random_image,100,100,True))
    print(result)
    return result

def con():
    """con function to generate pool of process

    this functions generates an pool of 5 worker, to execute 100 time my mean function
    """
    worker = cf.ProcessPoolExecutor(max_workers=5)
    for i in range(100):
        print(f"iteration {i}, result = {worker.submit(mymean)}")
