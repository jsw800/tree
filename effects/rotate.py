import random
import time
from helpers import get_effect
from BaseEffect import BaseEffect


EFFECTS = ['wheel', 'stripes', 'flicker', 'ripples']
TIME_TO_ROTATE = 120            # seconds


# rotate is a higher order effect which rotates between a few effects
class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)
        self.points = points
        self.effects = [get_effect(effect)(points) for effect in EFFECTS]
        random.shuffle(self.effects)
        self.last_swap = time.time()
        self.effect_index = 0
        self.max_fps = self.effects[0].max_fps

    def rotate(self):
        self.effect_index += 1
        self.effect_index %= len(self.effects)
        self.max_fps = self.effects[self.effect_index].max_fps
        self.color_mode = self.effects[self.effect_index].color_mode

    def update(self):
        now = time.time()
        if now - self.last_swap > TIME_TO_ROTATE:
            self.rotate()
            self.last_swap = now
        self.colors = next(self.effects[self.effect_index])
