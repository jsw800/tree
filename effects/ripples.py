import matplotlib.colors
import numpy as np
import math
import random

NUM_SPHERES = 1
MIN_VELOCITY = 0.025
MAX_VELOCITY = 0.05

"""
    [x, y, z, r, r_velocity, hue]
"""

class Effect:
    def __init__(self, points):
        self.points = points
        self.xmin = np.min(points[:, 0])
        self.xmax = np.max(points[:, 0])
        self.ymin = np.min(points[:, 1])
        self.ymax = np.max(points[:, 1])
        self.zmin = np.min(points[:, 2])
        self.zmax = np.max(points[:, 2])
        self.max_r = math.sqrt(
            (self.xmax - self.xmin) ** 2 +
            (self.ymax - self.ymin) ** 2 +
            (self.zmax - self.zmin) ** 2
        )
        self.sphere = self._gen_random_sphere()
        self.colors = np.zeros((self.points.shape[0], 3))
        self.colors[:, 1] = 0.9
        self.colors[:, 2] = 0.4

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def _gen_random_sphere(self):
        return np.array([
                random.uniform(self.xmin, self.xmax),
                random.uniform(self.ymin, self.ymax),
                random.uniform(self.zmin, self.zmax),
                0,
                random.uniform(MIN_VELOCITY, MAX_VELOCITY),
                random.uniform(0, 1),
        ], dtype=np.float64)

    def _update(self):
        self.sphere[3] += self.sphere[4]
        if self.sphere[3] > self.max_r or self.sphere[4] == 0:
            self.sphere = self._gen_random_sphere()
        dists = np.linalg.norm(self.points - self.sphere[:3], axis=1)
        to_show = dists < self.sphere[3]
        for j, show in enumerate(to_show):
            if show:
                self.colors[j, 0] = self.sphere[5]

    def render(self):
        self._update()
        return matplotlib.colors.hsv_to_rgb(self.colors)

