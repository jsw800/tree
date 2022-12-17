"""
    Some colors I have tested on the tree that
    look pretty decent and aren't terrible on the eyes
"""
import numpy as np


def color(rgb255):
    return np.array(rgb255, dtype=np.float64) / 255


RED = color([214, 23, 2])
GREEN = color([40, 97, 20])
SEA_GREEN = color([13, 219, 75])
YELLOW = color([250, 218, 7])
PURPLE = color([104, 17, 130])
BLUE = color([20, 20, 250])
BRIGHT_WHITE = color([190, 190, 190])
LOW_WHITE = color([60, 60, 60])
CYAN = color([8, 207, 200])
DARK_CYAN = color([13, 99, 219])
