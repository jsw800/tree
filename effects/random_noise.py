def effect(points):
    import numpy as np
    import time

    def random_noise():
        rgb = np.random.random_sample(points.shape)
        return rgb

    while True:
        time.sleep(0.1)
        yield random_noise
