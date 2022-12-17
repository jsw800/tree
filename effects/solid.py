import colors as rgb
from BaseEffect import BaseEffect


"""
    loop through the colors in the colors array
"""


COLORS = [rgb.GREEN, rgb.BLUE]
FRAMES_PER_COLOR = 150


class Effect(BaseEffect):

    def __init__(self, points):
        super().__init__(points)
        self.color_index = 0
        self.i = 0

    def set_color(self, color):
        for i in range(len(self.colors)):
            self.colors[i] = color

    def update(self):
        if self.i % FRAMES_PER_COLOR == 0:
            self.color_index += 1
            self.color_index %= len(COLORS)
            self.i = 0
            self.set_color(COLORS[self.color_index])
        self.i += 1

