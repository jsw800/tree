import numpy as np
import os
import sys
import csv
from PIL import Image, ImageDraw
from scipy import signal

"""
    This file will read the images taken by camera.py, determine the x/y
    coordinates of each light, and output them to the coords file supplied as the first arg
    
    We're assuming here that the number of and filenames of images in the x and y dirs is equal,
    if this is not the case, something is wrong.
"""

DO_ANNOTATIONS = False


# make a gaussian kernel,
# see http://scipy-lectures.org/intro/scipy/auto_examples/solutions/plot_image_blur.html
t = np.linspace(-10, 10, 30)
bump = np.exp(-0.1*t**2)
bump /= np.trapz(bump)
gaussian_kernel = bump[:, np.newaxis] * bump[np.newaxis, :]

def get_coord(file, average_img):
    with Image.open(file) as im:
        # to grayscale and subtract average image
        gray = np.asarray(im).mean(2)
        minus_avg = gray - average_img
        img = (gray + minus_avg) / 2
        # gaussian blur the image to reduce the probability of tiny hot spots being detected
        # generally the LEDs are a larger portion of the image than a tiny hotspot
        # they also look somewhat like a gaussian so it is a good kernel for this use case
        img = signal.fftconvolve(img, gaussian_kernel, mode='same')
    coord = np.unravel_index(np.argmax(img, axis=None), img.shape)

    confidence = img[coord] / 255

    if DO_ANNOTATIONS:
        annotation_file = file.replace('images', 'images_annotated')
        with Image.open(annotation_file) as im:
            draw = ImageDraw.Draw(im)
            draw.ellipse([coord[1] - 20, coord[0] - 20, coord[1] + 20, coord[0] + 20])
            im.save(annotation_file)

    return coord, confidence


# we can use use the avg images to subtract any constant light sources out of the scene
def get_avg_image(files):
    avg = None
    for file in files:
        with Image.open(file) as im:
            if avg is None:
                avg = np.asarray(im).mean(2) / len(files)
            else:
                avg += np.asarray(im).mean(2) / len(files)
    return avg


def main(out_path):
    if DO_ANNOTATIONS:
        os.system('rm -r images_annotated')
        os.system('cp -r images images_annotated')
    with Image.open('images/x/0.png') as test_im:
        test_image = np.asarray(test_im)
        width = test_image.shape[1]
        height = test_image.shape[0]
    files = os.listdir('images/x')
    # sort by image number
    files = sorted(files, key=lambda x: int(x.split('.')[0]))
    x_files = ['images/x/' + f for f in files]
    x_reverse_files = ['images/x_reverse/' + f for f in files]
    y_files = ['images/y/' + f for f in files]
    y_reverse_files = ['images/y_reverse/' + f for f in files]

    x_avg = get_avg_image(x_files)
    x_reverse_avg = get_avg_image(x_reverse_files)
    y_avg = get_avg_image(y_files)
    y_reverse_avg = get_avg_image(y_reverse_files)

    x1_coords = []
    x1_confidences = []
    x2_coords = []
    x2_confidences = []
    y1_coords = []
    y1_confidences = []
    y2_coords = []
    y2_confidences = []
    for i, file in enumerate(x_files):
        print(i)
        coord, confidence = get_coord(file, x_avg)
        x1_coords.append(coord)
        x1_confidences.append(confidence)

    for i, file in enumerate(x_reverse_files):
        print(i)
        coord, confidence = get_coord(file, x_reverse_avg)
        x2_coords.append((coord[0], width - coord[1]))
        x2_confidences.append(confidence)

    for i, file in enumerate(y_files):
        print(i)
        coord, confidence = get_coord(file, y_avg)
        y1_coords.append(coord)
        y1_confidences.append(confidence)

    for i, file in enumerate(y_reverse_files):
        print(i)
        coord, confidence = get_coord(file, y_reverse_avg)
        y2_coords.append((coord[0], width - coord[1]))
        y2_confidences.append(confidence)

    x1_coords, x2_coords, y1_coords, y2_coords = (np.array(c) for c in [x1_coords, x2_coords, y1_coords, y2_coords])

    # move x/y points of second set coordinates into the frame of reference of the first set
    x_medians = np.median(x1_coords - x2_coords, axis=0).astype(np.int64)
    x2_coords[:, 0] += x_medians[0]
    x2_coords[:, 1] += x_medians[1]
    y_medians = np.median(y1_coords - y2_coords, axis=0).astype(np.int64)
    y2_coords[:, 0] += y_medians[0]
    y2_coords[:, 1] += y_medians[1]

    # move all the z points into the frame of reference of x1_coords
    for to_change_z in [x2_coords, y1_coords, y2_coords]:
        z_median = np.median(x1_coords[:, 1] - to_change_z[:, 1]).astype(np.int64)
        to_change_z[:, 1] += z_median

    CONFIDENCE_THRESHOLD = 0.7
    out_coords = []
    for i in range(len(x1_coords)):
        x1 = {'coord': x1_coords[i], 'confidence': x1_confidences[i]}
        x2 = {'coord': x2_coords[i], 'confidence': x2_confidences[i]}
        y1 = {'coord': y1_coords[i], 'confidence': y1_confidences[i]}
        y2 = {'coord': y2_coords[i], 'confidence': y2_confidences[i]}

        # get z coord
        points = [x1, x2, y1, y2]
        points_to_use = [p for p in points if p['confidence'] > CONFIDENCE_THRESHOLD]
        if len(points_to_use) == 0:
            points_to_use = points
        z_coords = [p['coord'][0] for p in points_to_use]
        z = sum(z_coords) // len(z_coords)

        # get x coord
        points = [x1, x2]
        points_to_use = [p for p in points if p['confidence'] > CONFIDENCE_THRESHOLD]
        if len(points_to_use) == 0:
            points_to_use = points
        x_coords = [p['coord'][1] for p in points_to_use]
        x = sum(x_coords) // len(x_coords)

        # get y coord
        points = [y1, y2]
        points_to_use = [p for p in points if p['confidence'] > CONFIDENCE_THRESHOLD]
        if len(points_to_use) == 0:
            points_to_use = points
        y_coords = [p['coord'][1] for p in points_to_use]
        y = sum(y_coords) // len(y_coords)

        out_coords.append([x, y, z])

    with open(out_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for out_coord in out_coords:
            csv_writer.writerow(out_coord)


if __name__ == '__main__':
    main(sys.argv[1])
