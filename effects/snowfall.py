import time

import numpy as np
import random

BASE_COLOR = np.array([0, 0, 0], dtype=np.float64) / 255
SNOW_COLOR = np.array([150, 150, 150], dtype=np.float64) / 255

VELOCITY_MIN = -7
VELOCITY_MAX = 7

VELOCITY_Z_MIN = 5
VELOCITY_Z_MAX = 15

RADIUS_MIN = 50
RADIUS_MAX = 70

NUM_SPHERES = 8


class Sphere:
    def __init__(self, x, y, z):
        self.initial = (x, y, z)
        self.reset()

    def reset(self):
        self.x = self.initial[0]
        self.y = self.initial[1]
        self.z = self.initial[2]
        self.velx = random.randint(VELOCITY_MIN, VELOCITY_MAX)
        self.vely = random.randint(VELOCITY_MIN, VELOCITY_MAX)
        self.velz = random.randint(VELOCITY_Z_MIN, VELOCITY_Z_MAX)
        self.radius = random.randint(RADIUS_MIN, RADIUS_MAX)

    def update(self):
        self.x += self.velx
        self.y += self.vely
        self.z += self.velz

    def point_in_sphere(self, xyz):
        return self.dist(xyz) < self.radius

    def dist(self, xyz):
        return np.linalg.norm(np.array((self.x, self.y, self.z)) - xyz)


class Effect:
    def __init__(self, points):
        self.points = points
        self.colors = np.zeros((self.points.shape[0], 3))
        self.min_z = np.max(self.points[:, 2])
        top_center = (
            (np.max(self.points[:, 0]) + np.min(self.points[:, 0])) / 2,
            (np.max(self.points[:, 1]) + np.min(self.points[:, 1])) / 2,
            np.min(self.points[:, 2])
        )
        self.spheres = [Sphere(top_center[0], top_center[1], top_center[2]) for _ in range(NUM_SPHERES)]

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        self._update()
        return self.colors

    def _update(self):
        # update spheres
        for sphere in self.spheres:
            sphere.update()
            if sphere.z > self.min_z:
                sphere.reset()

        # render out the colors
        self._reset_colors()
        for sphere in self.spheres:
            for i, point in enumerate(self.points):
                if sphere.point_in_sphere(point):
                    self.colors[i] = SNOW_COLOR * (sphere.dist(point) / sphere.radius)

    def _reset_colors(self):
        self.colors[:, 0] = BASE_COLOR[0]
        self.colors[:, 1] = BASE_COLOR[1]
        self.colors[:, 2] = BASE_COLOR[2]
