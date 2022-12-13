import numpy as np
import time
from BaseEffect import BaseEffect


COLOR = (0.4, 0.4, 0.4)

INDEX = 81


class Effect(BaseEffect):

    def __init__(self, points):
        super().__init__(points)
        self.max_fps = 1
        print(self.points[INDEX])
        self.colors[INDEX] = COLOR[0]
        # self.colors[:, 0] = COLOR[0]
        # self.colors[:, 1] = COLOR[1]
        # self.colors[:, 2] = COLOR[2]

    def update(self):
        pass

