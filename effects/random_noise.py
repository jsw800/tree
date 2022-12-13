import numpy as np
from BaseEffect import BaseEffect


class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)

    def update(self):
        self.colors = np.random.random_sample(self.colors.shape)
