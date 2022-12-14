import numpy as np
import random
from BaseEffect import BaseEffect, ColorMode


VELOCITY_MIN = -0.002
VELOCITY_MAX = 0.002

VELOCITY_Z_MIN = -0.03
VELOCITY_Z_MAX = -0.08

RADIUS_MIN = 0.35
RADIUS_MAX = 0.5

NUM_SPHERES = 10

"""
self.spheres = [
    [x, y, z, r, x_vel, y_vel, z_vel],
    ...
]    
"""


class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.HSV
        self.max_z = np.max(self.points[:, 2])
        self.hue = 0.0
        self.top_center = np.array([
            (np.max(self.points[:, 0]) + np.min(self.points[:, 0])) / 2,
            (np.max(self.points[:, 1]) + np.min(self.points[:, 1])) / 2,
            np.max(self.points[:, 2]) + 1
        ], dtype=np.float64)
        self.spheres = np.zeros((NUM_SPHERES, 7), dtype=np.float64)
        for i in range(NUM_SPHERES):
            self.spheres[i] = self._gen_random_sphere()

    def _gen_random_sphere(self):
        return np.array([
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            self.max_z * 5 / 4,
            random.uniform(RADIUS_MIN, RADIUS_MAX),
            random.uniform(VELOCITY_MIN, VELOCITY_MAX),
            random.uniform(VELOCITY_MIN, VELOCITY_MAX),
            random.uniform(VELOCITY_Z_MIN, VELOCITY_Z_MAX),
        ], dtype=np.float64)

    def update(self):
        # update spheres
        self.spheres[:, 0] += self.spheres[:, 4]
        self.spheres[:, 1] += self.spheres[:, 5]
        self.spheres[:, 2] += self.spheres[:, 6]

        for i, sphere in enumerate(self.spheres):
            if sphere[2] < -1:
                self.spheres[i] = self._gen_random_sphere()

        # render out the colors
        self._reset_colors()
        for sphere in self.spheres:
            for i, point in enumerate(self.points):
                dist = np.linalg.norm(sphere[:3] - point)
                if dist < sphere[3]:
                    self.colors[i, 2] += (sphere[3] - dist) / sphere[3]
        self.colors[:, 2] = np.clip(self.colors[:, 2], 0, 0.4)

    def _reset_colors(self):
        self.colors[:, :] = 0.0
