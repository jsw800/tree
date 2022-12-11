import numpy as np
import time


COLOR = (0.4, 0.4, 0.4)


class Effect:
    def __init__(self, points):
        self.points = points
        self.shift = 0
        self.started = False

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        if self.started:
            self.shift += 1
            time.sleep(3)
        self.started = True
        onoff = (np.array(range(0, self.points.shape[0])) >> self.shift) & 1
        print(np.array(range(0, self.points.shape[0])) >> self.shift)
        colors = np.array([COLOR if val else (0, 0, 0) for val in onoff])
        return colors

