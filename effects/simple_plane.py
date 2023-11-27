import numpy as np
from BaseEffect import BaseEffect, ColorMode

"""
    This effect slides a plane of lights back and forth along the axis defines in the AXIS variable.

    The use case for this is to quickly locate lights that are not correctly detected and mark them
    for manual correction. You should change AXIS to each axis to check for bad coordinates in each
    direction (0 = X, 1 = Y, 2 = Z).
"""


AXIS = 2
ON_AMOUNT = 0.4
SPEED = 100.0
DELTA_HUE = 0.002

BOUNCE = True


class Effect(BaseEffect):

    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.HSV
        self.axis_points = self.points[:, AXIS]
        self.max = np.max(self.axis_points)
        self.min = np.min(self.axis_points)
        self.size = self.max - self.min
        self.plane_location = self.max
        self.hue = 0.0
        self.down = True

    def update(self):
        if self.down:
            self.plane_location -= (self.size / SPEED)
        else:
            self.plane_location += (self.size / SPEED)
        if BOUNCE:
            if self.plane_location <= self.min:
                self.down = False
            if self.plane_location >= self.max:
                self.down = True
        else:
            if self.plane_location <= self.min:
                self.plane_location = self.max
        self.hue = (self.hue + DELTA_HUE) % 1
        dist_from_plane = np.abs(self.axis_points - self.plane_location)
        max_dist_from_plane = ((self.max - self.min) * ON_AMOUNT / 2)
        brightness = ((max_dist_from_plane - dist_from_plane) / max_dist_from_plane) * 0.7
        brightness = np.clip(brightness, 0, 1)
        self.colors[:, 0] = self.hue
        self.colors[:, 1] = 0.8
        self.colors[:, 2] = brightness

