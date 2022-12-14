from BaseEffect import BaseEffect, ColorMode

DELTA_HUE = 0.3


class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.HSV
        self.max_fps = 100
        self.colors[:, 1] = 0.8
        self.colors[:, 2] = 0.4
        self.index = 0
        self.hue = 0.0

    def update(self):
        self.colors[0:self.index, 0] = self.hue
        self.index += 1
        if self.index > self.points.shape[0]:
            self.index = 0
            self.hue += DELTA_HUE
            self.hue %= 1
