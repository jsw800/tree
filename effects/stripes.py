import math
import numpy as np
import colors as rgb


THETA = 45
STRIPES_AT_ONCE = 1
DELTA = 0.015


class Effect:
    def __init__(self, points):
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

    def _update_points(self):
        theta_rad = math.radians(THETA)
        rotation_matrix = np.array([
            [math.cos(theta_rad), 0, math.sin(theta_rad)],
            [0, 1, 0],
            [-math.sin(theta_rad), 0, math.cos(theta_rad)],
        ])
        self.points = np.dot(self.points, rotation_matrix)
        self.zs = self.points[:, 2]
        # move and scale to between 0 and STRIPES_AT_ONCE
        self.zs -= np.min(self.zs)
        self.zs *= STRIPES_AT_ONCE * 2 / np.max(self.zs)

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        colors = np.zeros((self.points.shape[0], 3))
        transformed = (np.floor(self.zs + self.transform) / 2)
        for i, element in enumerate(transformed):
            if element.is_integer():
                colors[i] = rgb.RED
            else:
                colors[i] = rgb.GREEN
        self.transform += DELTA
        self.transform %= STRIPES_AT_ONCE * 2
        return colors

