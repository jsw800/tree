import random
import time
from helpers import get_effect


EFFECTS = ['wheel', 'stripes', 'flicker', 'ripples']
TIME_TO_ROTATE = 120            # seconds


# rotate is a higher order effect which rotates between a few effects
class Effect:
    def __init__(self, points):
        self.points = points
        self.effects = [iter(get_effect(effect)(points)) for effect in EFFECTS]
        random.shuffle(self.effects)
        self.last_swap = time.time()
        self.effect_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def rotate(self):
        self.effect_index += 1
        self.effect_index %= len(self.effects)

    def render(self):
        now = time.time()
        if now - self.last_swap > TIME_TO_ROTATE:
            self.rotate()
            self.last_swap = now
        render_fn = next(self.effects[self.effect_index])
        return render_fn()
