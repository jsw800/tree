import math
import numpy as np
import colors as rgb
from BaseEffect import BaseEffect


THETA = 45
STRIPES_AT_ONCE = 1
DELTA = 0.015


class Effect(BaseEffect):

    def __init__(self, points):
        super().__init__(points)
        self.max_fps = 50
        theta_rad = math.radians(THETA)
        rotation_matrix = np.array([
            [math.cos(theta_rad), 0, math.sin(theta_rad)],
            [0, 1, 0],
            [-math.sin(theta_rad), 0, math.cos(theta_rad)],
        ])
        self.points = np.dot(points, rotation_matrix)
        self.zs = self.points[:, 2]
        # move and scale to between 0 and STRIPES_AT_ONCE
        self.zs -= np.min(self.zs)
        self.zs *= STRIPES_AT_ONCE * 2 / np.max(self.zs)
        self.transform = 0.0
        self.min = math.inf
        self.max = 0

    def update(self):
        transformed = (np.floor(self.zs + self.transform) / 2)
        for i, element in enumerate(transformed):
            if element.is_integer():
                self.colors[i] = rgb.RED
            else:
                self.colors[i] = rgb.GREEN
        self.transform += DELTA
        self.transform %= STRIPES_AT_ONCE * 2

