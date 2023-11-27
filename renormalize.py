import csv
import sys

"""
    The purpose of this script is to renormalize the points to be in the range [-1, 1]
    in the X/Y directions after correcting bad points. The use case here is that after manually
    correcting points that were not detected correctly, the points may no longer be in the range
    [-1, 1] in the X/Y directions. This happens because misidentified points are often on the fringes
    of the image. If the points are not renormalized, the effects will not be centered on the tree.
"""

def read_from_csv(csv_file):
    points = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            points.append([float(row[0]), float(row[1]), float(row[2])])
    return points

def write_to_csv(normalized_points, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(normalized_points)

def normalize_points(points):
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_y = max(point[1] for point in points)

    normalized_points = []
    for point in points:
        x = (2 * (point[0] - min_x) / (max_x - min_x)) - 1
        y = (2 * (point[1] - min_y) / (max_y - min_y)) - 1
        z = point[2] * (max_x - min_x) / (max_y - min_y)
        normalized_points.append([x, y, z])

    return normalized_points

# Usage example
csv_file = sys.argv[1]
points = read_from_csv(csv_file)
normalized_points = normalize_points(points)

# Usage example
output_file = sys.argv[2]
write_to_csv(normalized_points, output_file)
