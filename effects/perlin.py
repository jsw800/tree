import time

import opensimplex
from BaseEffect import BaseEffect, ColorMode

SPEED = 0.05

class Effect(BaseEffect):

    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.HSV
        self.colors[:, 1] = 0.9
        self.colors[:, 2] = 0.4
        self.direction = 1
        self.offset = 0.0

    def update(self):
        for i, point in enumerate(self.points):
            self.colors[i, 0] = (self.noise([point[0], point[1], point[2], self.offset]) + 1) / 2
        self.colors[:, 0] += self.offset / 10
        self.colors[:, 0] %= 1
        self.offset += self.direction * SPEED
        if abs(self.offset) > 100:
            self.direction *= -1

    def noise(self, point):
        return opensimplex.noise4(point[0], point[1], point[2], point[3])
