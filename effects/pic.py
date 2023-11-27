import numpy as np
import cv2
from BaseEffect import BaseEffect, ColorMode
from helpers import process_image

IMAGE_NAME = 'pics/pic.jpg'

class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.RGB
        self.colors = process_image(self.points, cv2.imread(IMAGE_NAME)) / 2.0

    def update(self):
        pass
