import re
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def parse(line):
    m = re.match(r'(\d+), (\d+)', line)
    return Point(int(m.group(1)), int(m.group(2)))


def limits(coords):
    (xmax, ymax) = (0, 0)
    for coord in coords:
        xmax = max(xmax, coord.x)
        ymax = max(ymax, coord.y)
    return xmax+1, ymax+1


def manhattan(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def is_agglo(p, coords, threshold):
    sum_dist = sum([manhattan(p, coords[i]) for i in range(len(coords))])
    return sum_dist < threshold


def agglo_matrix(coords, threshold):
    (xmax, ymax) = limits(coords)
    matrix = np.zeros((xmax, ymax))
    for x in range(xmax):
        for y in range(ymax):
            matrix[x, y] = is_agglo(Point(x, y), coords, threshold)
    return matrix


def process(coords, threshold):
    return np.sum(agglo_matrix(coords, threshold))


def compute(file_name, threshold):
    with open(file_name, "r") as file:
        coords = [parse(line.strip()) for line in file.readlines()]
        return process(coords, threshold)


if __name__ == '__main__':
    print("Agglo = ", compute("data.txt", 10000))
