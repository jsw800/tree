import matplotlib.colors
import numpy as np
import math


DELTA = 1.0
CONSTANT_AXIS = 2


class Effect:
    def __init__(self, points):
        self.points = points
        self.theta = 0.0
        self.center_point = (np.max(self.points, axis=0) - np.min(self.points, axis=0)) / 2
        self.points -= np.min(self.points, axis=0)
        self.points -= self.center_point
        self.hue_1 = 0.0
        self.hue_2 = 0.5

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        which = math.tan(math.radians(self.theta)) * self.points[:, 1] <= self.points[:, 2]
        hsv = np.zeros((self.points.shape[0], 3))
        if 90 < self.theta <= 270:
            which = np.invert(which)
        for i, value in enumerate(which):
            if value:
                hsv[i, 0] = self.hue_1
            else:
                hsv[i, 0] = self.hue_2
        hsv[:, 1] = 0.8
        hsv[:, 2] = 0.9
        rgb = matplotlib.colors.hsv_to_rgb(hsv)
        self._update()
        return rgb

    def _update(self):
        self.theta += DELTA
        self.theta = self.theta % 360
