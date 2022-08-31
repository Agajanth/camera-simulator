from abc import ABC, abstractmethod
import numpy as np


class BaseProcessor(ABC):
    """BaseProcessor class to create an processor Interface

    properties:
        enable : boolean to enable functionalities in the child class

    methods:
        process:  method for implementing a processing process

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


class SizeImageException(ValueError):
    pass
