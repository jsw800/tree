import numpy as np

def load_coords(filename):
    with open(filename, mode='r', encoding='utf-8-sig') as f:
        # janky csv reader
        coords = np.array([
            [float(elem) for elem in coord.split(',')]
            for coord in f.read().split('\n')
            if coord != ''
        ])
    return coords
