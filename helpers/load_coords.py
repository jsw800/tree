import numpy as np
import csv


def load_coords(filename):
    with open(filename, mode='r', encoding='utf-8-sig') as f:
        # janky csv reader
        coords = np.array([
            [float(elem) for elem in coord.split(',')]
            for coord in f.read().split('\n')
            if coord != ''
        ])
    return coords


def write_coords(filename, coords):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for out_coord in coords:
            csv_writer.writerow(out_coord)
