from time import sleep
import numpy as np


class LEDTree(object):
    def __init__(self, points):
        import board
        import neopixel
        self.points = points
        self.num_pixels = len(points)
        self.neopixel = neopixel.NeoPixel(board.D18, self.num_pixels, auto_write=False, brightness=0.5, pixel_order=neopixel.RGB)
        self.off()
        sleep(1)


    def off(self):
        self.neopixel.fill((0, 0, 0))
        self.neopixel.show()

    def render_frame(self, colors):
        rgb = (colors * 255).astype(np.uint8)
        self._set_rgb_pixels(rgb)

    def _set_rgb_pixels(self, pixels):
        for i, pixel in enumerate(pixels):
            if i >= self.num_pixels:
                break
            self.neopixel[i] = pixel
        self.neopixel.show()
