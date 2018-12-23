import re

GEO_INDEX = {}
EROSION = {}
WORLD = {}
GLOBS = {'depth': 0}


def parse(lines):
    m = re.match(r'depth: (\d+)', lines[0])
    depth = int(m.group(1))
    m = re.match(r'target: (\d+),(\d+)', lines[1])
    target = (int(m.group(1)), int(m.group(2)))
    return depth, target


def calc_geo(pos):
    if pos in GEO_INDEX:
        return GEO_INDEX[pos]
    else:
        if pos[1] == 0:
            geo = pos[0] * 16807
        elif pos[0] == 0:
            geo = pos[1] * 48271
        else:
            geo = calc_erosion((pos[0]-1, pos[1])) * calc_erosion((pos[0], pos[1]-1))
        GEO_INDEX[pos] = geo
        return geo


def calc_erosion(pos):
    if pos in EROSION:
        return EROSION[pos]
    else:
        erosion = (calc_geo(pos) + GLOBS['depth']) % 20183
        EROSION[pos] = erosion
        return erosion


def fill_world(target):
    for x in range(target[0] + 1):
        for y in range(target[1] + 1):
            calc_erosion((x, y))


def scan(target):
    WORLD.clear()
    for x in range(target[0] + 1):
        for y in range(target[1] + 1):
            rest = calc_erosion((x, y)) % 3
            if rest == 0:
                WORLD[(x, y)] = '.'
            elif rest == 1:
                WORLD[(x, y)] = '='
            else:
                WORLD[(x, y)] = '|'


def pretty_print(target):
    print()
    for row in range(target[1] + 1):
        line = ''
        for col in range(target[0] + 1):
            line += WORLD[(col, row)]
        print(line)
    print()


def stats(target):
    rocky, wet, narrow = (0, 0, 0)
    for x in range(target[0] + 1):
        for y in range(target[1] + 1):
            if WORLD[(x, y)] == '.':
                rocky += 1
            elif WORLD[(x, y)] == '=':
                wet += 1
            elif WORLD[(x, y)] == '|':
                narrow += 1
            else:
                raise SyntaxError('Unexpected value !')
    return wet + 2 * narrow


def process(depth, target):
    GLOBS['depth'] = depth
    GEO_INDEX[(0, 0)] = 0
    GEO_INDEX[target] = 0
    fill_world(target)
    scan(target)
    pretty_print(target)
    return stats(target)


def compute(file_name):
    with open(file_name, "r") as file:
        depth, target = parse(file.readlines())
        return process(depth, target)


if __name__ == '__main__':
    print("Risk level  = ", compute("data.txt"))
