# Parses files from a drawing instead of a coord list
# Much easier to test different scenarios

GLOB = {'source': (0,0)}
WORLD = []


def parse_map(lines):
    size_x = len(lines[0])
    size_y = len(lines)
    for x in range(size_x):
        WORLD.append(['.'] * size_y)
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(lines[0])):
            WORLD[x][y] = line[x]
    GLOB['source'] = (10, 0)


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
    pretty_print()
    s = GLOB['source']
    flow(s[0], s[1])
    water_reachable = count_water('~|')
    water_stored = count_water('~')
    write()
    pretty_print()
    return water_reachable, water_stored


def compute(file_name):
    with open(file_name, "r") as file:
        parse_map([line.strip() for line in file.readlines()])
        return process()


if __name__ == '__main__':
    print("water reachable / stored  = ", compute("sample_map.txt"))
