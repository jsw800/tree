import numpy as np
import random
import colors as rgb


BASE_COLOR = rgb.GREEN
FLICKER_COLOR = rgb.RED
NUM_FLICKERING = 45


class Effect:
    def __init__(self, points):
        self.points = points
        self.iteration = 0
        self.colors = np.zeros((points.shape[0], 3), dtype=np.float64)
        self._reset_colors()
        self.indices = [random.randint(0, len(self.points) - 1) for _ in range(NUM_FLICKERING)]

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        self._update()
        return self.colors

    def _reset_colors(self):
        self.colors[:, 0] = BASE_COLOR[0]
        self.colors[:, 1] = BASE_COLOR[1]
        self.colors[:, 2] = BASE_COLOR[2]

    def _update(self):
        self.iteration += 1
        self.iteration %= NUM_FLICKERING
        for i in range(NUM_FLICKERING):
            if self.iteration == i:
                self.indices[i] = random.randint(0, len(self.points) - 1)
        self._reset_colors()
        for index in self.indices:
            self.colors[index] = FLICKER_COLOR
