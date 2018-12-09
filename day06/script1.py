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


def closest_point(p, coords):
    closest_coord = 0
    closest_dist = manhattan(p, coords[0])
    equal_dist = False      # if 2 coords are at the same dist
    for coord in range(1, len(coords)):
        dist = manhattan(p, coords[coord])
        if dist < closest_dist:
            closest_dist = dist
            closest_coord = coord
            equal_dist = False
        elif dist == closest_dist:
            equal_dist = True
    if equal_dist:
        return -1
    else:
        return closest_coord


def control_matrix(coords, xmax, ymax):
    matrix = np.zeros((xmax, ymax))
    for x in range(xmax):
        for y in range(ymax):
            matrix[x, y] = closest_point(Point(x, y), coords)
    return matrix


def process(coords):
    (xmax, ymax) = limits(coords)
    matrix = control_matrix(coords, xmax, ymax)
    areas = {}
    for i in range(len(coords)):
        areas[i] = 0

    for x in range(xmax):
        for y in range(ymax):
            controller = matrix[x, y]
            if controller != -1 and controller in areas:    # if it was not removed
                if x == 0 or y == 0 or x == xmax-1 or y == ymax-1:
                    del areas[controller]    # it is on the edge, so infinite
                else:
                    areas[controller] += 1
    return max(areas.values())


def compute(file_name):
    with open(file_name, "r") as file:
        coords = [parse(line.strip()) for line in file.readlines()]
        return process(coords)


if __name__ == '__main__':
    print("Largest Area = ", compute("data.txt"))
