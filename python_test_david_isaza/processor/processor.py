import numpy as np
from baseProcessor import BaseProcessor, SizeImageException



class Lens(BaseProcessor):

    def __init__(self,height:int,width:int,enable:bool = False):
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


class Sensor(BaseProcessor):

    def __init__(self,gain: float,enable = False) -> None:
        self.gain = gain
        self.enable = enable

    def process(image: np.ndarray) -> np.ndarray:
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

