import numpy as np
import time
from BaseEffect import BaseEffect


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

