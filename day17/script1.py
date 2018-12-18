import re

# Solve both part 1 and part 2

GLOB = {'source': (0,0)}
WORLD = []


def parse(lines):
    coords = []
    for i in range(len(lines)):
        line = lines[i].strip('\n')
        m = re.match(r'x=(.*), y=(.*)\.\.(.*)', line)
        if m is not None:
            x, y1, y2 = m.groups()
            coords.append((int(x), int(x), int(y1), int(y2)))
        else:
            m = re.match(r'y=(.*), x=(.*)\.\.(.*)', line)
            y, x1, x2 = m.groups()
            coords.append((int(x1), int(x2), int(y), int(y)))
    xmin = min([coord[0] for coord in coords])
    xmax = max([coord[1] for coord in coords])
    ymin = min([coord[2] for coord in coords])
    ymax = max([coord[3] for coord in coords])

    # create the sand matrix
    for x in range(xmin - 1, xmax + 2):
        WORLD.append(['.'] * (ymax - ymin + 2))

    # add the glay in it
    for (x1, x2, y1, y2) in coords:
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                WORLD[x - xmin + 1][y - ymin + 1] = '#'

    # add the source
    WORLD[500 - xmin + 1][0] = '+'
    GLOB['source'] = (500 - xmin + 1, 0)


def pretty_print():
    for y in range(len(WORLD[0])):
        row = ''
        for x in range(len(WORLD)):
            row += WORLD[x][y]
        print(row)
    print()


def can_fall(x,y):
    return y < len(WORLD[0]) - 1 and WORLD[x][y+1] in '.|'


def fill_water(x0, x1, y, symbol):
    for x in range(x0, x1 + 1):
        WORLD[x][y] = symbol


def platform_limits(sx, sy):
    while WORLD[sx-1][sy] in '|.' and WORLD[sx-1][sy+1] in '#~' :  #scroll to right
        sx = sx - 1
    sx0 = sx
    while WORLD[sx+1][sy] in '|.' and WORLD[sx+1][sy+1] in '#~':
        sx = sx + 1
    return (sx0, sx)


def flow(sx, sy):
    # if the flow source is already water, nothing to do
    if WORLD[sx][sy] in '#~':
        return

    # mark the source
    if WORLD[sx][sy] == '.':
        WORLD[sx][sy] = '|'

    # fall as much as we can
    x, y = sx, sy
    while(can_fall(x, y)):
        y = y + 1
        if WORLD[x][y] == '.':
            WORLD[x][y] = '|'

    # we now reached the bottom or hit glay/water
    if y == len(WORLD[0]) - 1: # reached bottom
        return

    # reach a platform, need to know if bucket or plate
    x0, x1 = platform_limits(x, y)
    basket_left = WORLD[x0-1][y] in '#~'
    basket_right = WORLD[x1+1][y] in '#~'
    if basket_left and basket_right:
        fill_water(x0, x1, y, '~')
        # pretty_print()
        # we filled one level, reflow water from the same source
        return flow(sx, sy)
    else:
        fill_water(x0, x1, y, '|')
        if not basket_left:
            flow(x0 - 1, y)
        if not basket_right:
            flow(x1 + 1, y)

        # flow again from the source if it spills
        if WORLD[x][y] == '~':
            flow(sx, sy)


def count_water(symbols):
    total = 0
    for x in range(len(WORLD)):
        for y in range(len(WORLD[0])):
            if WORLD[x][y] in symbols:
                total += 1
    return total


def write():
    f = open("curr_water.txt", "w")
    for y in range(len(WORLD[0])):
        row = ''
        for x in range(len(WORLD)):
            row += WORLD[x][y]
        f.write(row + '\n')
    f.close()


def process():
    # pretty_print()
    s = GLOB['source']
    flow(s[0], s[1])
    water_reachable = count_water('~|')
    water_stored = count_water('~')
    write()
    # pretty_print()
    return water_reachable, water_stored


def compute(file_name):
    with open(file_name, "r") as file:
        parse(file.readlines())
        return process()


if __name__ == '__main__':
    print("water reachable / stored  = ", compute("sample.txt"))
