import numpy as np
import matplotlib

# how much of the z space should be lit at a time (0-1)?
ON_RATIO = 0.35
SPEED = 0.05

# an effect is a generator function (or iterable) that yields a
# Callable mapping a points (np array of x, y, z) to a colors (np array of r, g, b)
def effect(points):
    started = False
    down = True
    max_z = 0.0
    min_z = 0.0
    plane_z = 1.0
    hue = 0.0
    points_z = points[:, 2]

    def plane():
        dist_from_plane = np.abs(points_z - plane_z)
        brightness = ((dist_from_plane * (ON_RATIO ** -1)) * -1) + 1
        brightness = np.clip(brightness, 0, 1)
        hsv = np.zeros((brightness.shape[0], 3))
        hsv[:, 0] = hue
        hsv[:, 1] = 0.8
        hsv[:, 2] = brightness
        rgb = matplotlib.colors.hsv_to_rgb(hsv)
        return rgb


    while True:
        if not started:
            max_z = np.max(points_z)
            min_z = np.min(points_z)
            plane_z = max_z
            started = True
        yield plane
        if down:
            plane_z -= SPEED
        else:
            plane_z += SPEED
        if plane_z <= min_z:
            down = False
        if plane_z >= max_z:
            down = True
        hue = (hue + 0.01) % 1
        
