def effect(points):
    import numpy as np
    import matplotlib
    import time
    def random_noise():
        hsv = np.random.random_sample(points.shape)
        return hsv
#        return matplotlib.colors.hsv_to_rgb(hsv)

    while True:
        yield random_noise
