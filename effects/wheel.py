import matplotlib.colors
import numpy as np
import math


DELTA_THETA = 1.0
DELTA_HUE = 0.0015
CONSTANT_AXIS = 2


class Effect:
    def __init__(self, points):
        self.points = points
        self.theta = 0.0
        # translate the points so they are centered around 0, this makes it easier to do the calculations
        center_point = (np.max(self.points, axis=0) - np.min(self.points, axis=0)) / 2
        self.points -= np.min(self.points, axis=0)
        self.points -= center_point
        self.hue_1 = 0.0
        self.hue_2 = 0.5

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        axes = [a for a in [0, 1, 2] if a != CONSTANT_AXIS]
        which = math.tan(math.radians(self.theta)) * self.points[:, axes[0]] <= self.points[:, axes[1]]
        hsv = np.zeros((self.points.shape[0], 3))
        if 90 < self.theta <= 270:
            which = np.invert(which)
        for i, value in enumerate(which):
            if value:
                hsv[i, 0] = self.hue_1
            else:
                hsv[i, 0] = self.hue_2
        hsv[:, 1] = 0.8
        hsv[:, 2] = 0.5
        rgb = matplotlib.colors.hsv_to_rgb(hsv)
        self._update()
        return rgb

    def _update(self):
        self.theta += DELTA_THETA
        self.theta %= 360
        self.hue_1 += DELTA_HUE
        self.hue_1 %= 1
        self.hue_2 += DELTA_HUE
        self.hue_2 %= 1
