import re
import numpy as np


class Fabric:
    def __init__(self, fabric_id, left, top, width, height):
        self.id = fabric_id
        self.left = left
        self.top = top
        self.width = width
        self.height = height


def parse(line):
    m = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    (fabric_id, left, top, width, height) = m.groups()
    return Fabric(int(fabric_id), int(left), int(top), int(width), int(height))


def overlap_matrix(fabrics):
    matrix = np.zeros((1000, 1000))
    for fabric in fabrics:
        for x in range(fabric.width):
            for y in range(fabric.height):
                x0 = fabric.left
                y0 = fabric.top
                matrix[x0 + x, y0 + y] += 1
    return matrix


def has_overlap(matrix, fabric):
    for x in range(fabric.width):
        for y in range(fabric.height):
            x0 = fabric.left
            y0 = fabric.top
            if matrix[x0 + x, y0 + y] > 1:
                return True
    return False


def process(fabrics):
    matrix = overlap_matrix(fabrics)
    for fabric in fabrics:
        if not has_overlap(matrix, fabric):
            return fabric.id


def compute(file_name):
    with open(file_name, "r") as file:
        data = [parse(line) for line in file.readlines()]
        return process(data)


if __name__ == '__main__':
    print("Fabric with no overlap = #", compute("data.txt"))
