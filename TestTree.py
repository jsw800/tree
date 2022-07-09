class TestTree(object):
    def __init__(self, points):
        import pptk
        import subprocess
        import numpy as np
        self.points = points
        self.viewer = pptk.viewer(self.points, np.zeros(self.points.shape))
        # hack to fix https://github.com/heremaps/pptk/issues/24
        self.viewer._process.stderr = subprocess.DEVNULL
        self.viewer.set(point_size=0.005)

    def off(self):
        self.viewer.close()

    def render_frame(self, frame):
        rgb = frame()
        self.viewer.attributes(rgb)
