from abc import ABC, abstractmethod
from enum import Enum
import inspect
import numpy as np


class ColorMode(Enum):
    RGB = 0
    HSV = 1


class BaseEffect(ABC):

    def __init__(self, points):
        self.points = points
        self.colors = np.zeros((self.points.shape[0], 3))
        self.__started = False
        self.color_mode = ColorMode.RGB
        self.max_fps = 60

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.__started:
            if inspect.iscoroutinefunction(self.update):
                await self.update()
            else:
                self.update()
        self.__started = True
        return self.colors

    # this coroutine function allows effects to tie into the
    # event loop to watch for any async stuff they might need
    # by default does nothing, but can override in child classes
    async def coroutine(self):
        pass

    @abstractmethod
    def update(self):
        pass
