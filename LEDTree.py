from time import sleep
import numpy as np

class LEDTree(object):
    def __init__(self, points, num_pixels):
        import board
        import neopixel
        self.points = points
        self.num_pixels = num_pixels
        self.neopixel = neopixel.NeoPixel(board.D18, num_pixels, auto_write=False, brightness=0.5, pixel_order=neopixel.RGB)
        self.off()
        sleep(2)


    def off(self):
        self.neopixel.fill((0, 0, 0))
        self.neopixel.show()

    def render_frame(self, render_fn):
        rgb = (render_fn() * 255).astype(np.uint8)
        self._set_rgb_pixels(rgb)
        sleep(0.01)

    def _set_rgb_pixels(self, pixels):
        for i, pixel in enumerate(pixels):
            if i >= self.num_pixels:
                break
            self.neopixel[i] = pixel
        self.neopixel.show()
