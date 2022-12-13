import numpy as np
import math
from BaseEffect import BaseEffect, ColorMode


DELTA_THETA = 2.0
DELTA_HUE = 0.0015
CONSTANT_AXIS = 1


class Effect(BaseEffect):

    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.HSV
        self.theta = 0.0
        # translate the points so they are centered around 0, this makes it easier to do the calculations
        center_point = (np.max(self.points, axis=0) - np.min(self.points, axis=0)) / 2
        self.points -= np.min(self.points, axis=0)
        self.points -= center_point
        self.hue_1 = 0.0
        self.hue_2 = 0.5
        # these never change
        self.colors[:, 1] = 0.8
        self.colors[:, 2] = 0.5

    def update(self):
        self.theta += DELTA_THETA
        self.theta %= 360
        self.hue_1 += DELTA_HUE
        self.hue_1 %= 1
        self.hue_2 += DELTA_HUE
        self.hue_2 %= 1

        axes = [a for a in [0, 1, 2] if a != CONSTANT_AXIS]
        which = math.tan(math.radians(self.theta)) * self.points[:, axes[0]] <= self.points[:, axes[1]]
        if 90 < self.theta <= 270:
            which = np.invert(which)
        for i, value in enumerate(which):
            if value:
                self.colors[i, 0] = self.hue_1
            else:
                self.colors[i, 0] = self.hue_2
