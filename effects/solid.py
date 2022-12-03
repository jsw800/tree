import time

import numpy as np
import time


COLOR = (0.4, 0.4, 0.4)


class Effect:
    def __init__(self, points):
        self.points = points
        self.colors = np.zeros((self.points.shape[0], 3))
        self.colors[:, 0] = COLOR[0]
        self.colors[:, 1] = COLOR[1]
        self.colors[:, 2] = COLOR[2]

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        time.sleep(5)
        return self.colors

