import numpy as np
import time
from BaseEffect import BaseEffect

"""
    Blink out the binary representation of each LED's index

    The use case here is to locate a specific light to debug and manually correct its coordinate.
    After the initial detection pass, use the simple_plane effect to locate lights that are not
    correctly detected and mark them somehow (like a sticky note). Then use this effect to get
    the binary of that light's index. Use the single effect to check that you have the right index,
    then manually correct the point in your coordinates file.
"""

COLOR = (0.4, 0.4, 0.4)

class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)
        num_leds = len(points)
        self.shift = len(bin(num_leds)[2:])
        self.started = False

    def update(self):
        if self.shift < 0:
            return
        if self.started:
            self.shift -= 1
            time.sleep(3)
        self.started = True
        onoff = (np.array(range(0, self.points.shape[0])) >> self.shift) & 1
        self.colors = np.array([COLOR if val else (0, 0, 0) for val in onoff])

