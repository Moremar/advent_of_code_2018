import re
import numpy as np


class Fabric:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height


def parse(line):
    m = re.match(r'#\d+ @ (\d+),(\d+): (\d+)x(\d+)', line)
    (left, top, width, height) = m.groups()
    return Fabric(int(left), int(top), int(width), int(height))


def overlap_matrix(fabrics):
    matrix = np.zeros((1000, 1000))
    for fabric in fabrics:
        for x in range(fabric.width):
            for y in range(fabric.height):
                x0 = fabric.left
                y0 = fabric.top
                matrix[x0 + x, y0 + y] += 1
    return matrix


def process(data):
    matrix = overlap_matrix(data)
    count = 0
    for elem in np.nditer(matrix):
        if elem > 1:
            count += 1
    return count


def compute(file_name):
    with open(file_name, "r") as file:
        data = [parse(line) for line in file.readlines()]
        return process(data)


if __name__ == '__main__':
    print("Inches in collisions = ", compute("data.txt"))
