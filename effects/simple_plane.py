import numpy as np
import matplotlib.colors


AXIS = 2
ON_AMOUNT = 0.4
SPEED = 100.0


class Effect:
    def __init__(self, points):
        self.points = points
        self.axis_points = self.points[:, AXIS]
        self.max = np.max(self.axis_points)
        self.min = np.min(self.axis_points)
        self.size = self.max - self.min
        self.plane_location = self.max
        self.hue = 0.0
        self.down = True

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def _update(self):
        if self.down:
            self.plane_location -= (self.size / SPEED)
        else:
            self.plane_location += (self.size / SPEED)
        if self.plane_location <= self.min:
            self.down = False
        if self.plane_location >= self.max:
            self.down = True
        self.hue = (self.hue + 0.01) % 1

    def render(self):
        dist_from_plane = np.abs(self.axis_points - self.plane_location)
        max_dist_from_plane = ((self.max - self.min) * ON_AMOUNT / 2)
        brightness = (max_dist_from_plane - dist_from_plane) / max_dist_from_plane
        brightness = np.clip(brightness, 0, 1)
        hsv = np.zeros((brightness.shape[0], 3))
        hsv[:, 0] = self.hue
        hsv[:, 1] = 0.8
        hsv[:, 2] = brightness
        rgb = matplotlib.colors.hsv_to_rgb(hsv)
        self._update()
        return rgb
