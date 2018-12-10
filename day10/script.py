import re
import numpy as np


class Star:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


def parse(line):
    m = re.match(r'position=<(.*), (.*)> velocity=<(.*), (.*)>', line)
    (x, y, dx, dy) = m.groups()
    return Star(int(x), int(y), int(dx), int(dy))


def draw(stars):
    (minx, miny, maxx, maxy) = rect(stars)
    m = np.zeros((maxx - minx + 2, maxy - miny + 2))
    for star in stars:
        m[star.x - minx + 1, star.y - miny + 1] = 1
    for y in range(maxy - miny + 2):
        line = ''
        for x in range(maxx - minx + 2):
            line += '@' if m[x, y] == 1 else '_'
        print(line)


def rect(stars: [Star]):
    minx = min([star.x for star in stars])
    miny = min([star.y for star in stars])
    maxx = max([star.x for star in stars])
    maxy = max([star.y for star in stars])
    return minx, miny, maxx, maxy


def rect_area(stars: [Star]):
    (minx, miny, maxx, maxy) = rect(stars)
    return (maxx - minx) * (maxy - miny)


def translate(stars):
    return [Star(star.x + star.dx, star.y + star.dy, star.dx, star.dy) for star in stars]


def process(stars, max_step):
    min_step = 0
    min_area = rect_area(stars)
    min_stars = stars
    for i in range(1, max_step):
        stars = translate(stars)
        area = rect_area(stars)
        if area < min_area:
            min_step = i
            min_area = area
            min_stars = stars
    draw(min_stars)
    return min_step


def compute(file_name, max_step):
    with open(file_name, "r") as file:
        stars = [parse(line) for line in file.readlines()]
        return process(stars, max_step)


if __name__ == '__main__':
    print("Steps = ", compute("data.txt", 12000))
