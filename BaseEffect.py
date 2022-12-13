from abc import ABC, abstractmethod
from enum import Enum
import numpy as np


class ColorMode(Enum):
    RGB = 0
    HSV = 1


# TODO
class BaseEffect(ABC):

    def __init__(self, points):
        self.points = points
        self.colors = np.zeros((self.points.shape[0], 3))
        self.__started = False
        self.color_mode = ColorMode.RGB
        self.max_fps = 60

    def __iter__(self):
        return self

    def __next__(self):
        if self.__started:
            self.update()
        self.__started = True
        return self.colors

    @abstractmethod
    def update(self):
        pass
