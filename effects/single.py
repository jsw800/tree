from BaseEffect import BaseEffect, ColorMode

"""
    Turn on a single light at the given index

    The use case for this effect is to be a helper when locating a specific light
    to debug and manually correct its coordinate. Once you think you have the light's index,
    you can use this effect to turn on the light at that index to verify that you have the
    right one. If you do, you can then manually correct the point in your coordinates file.
"""

LIGHT_INDEX = 53

class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.RGB
        self.colors[LIGHT_INDEX] = [1.0, 1.0, 1.0]
        

    def update(self):
        pass
