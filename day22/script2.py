import re
# import cProfile, pstats, io
# from pstats import SortKey


GEO_INDEX = {}
EROSION = {}
WORLD = {}
GLOBS = {'depth': 0, 'target': None, 'shortest': 100000}

REACHED = {}
TO_CRAWL = {}
TORCH = 'T'
GEAR = 'G'
NEITHER = 'N'
MARGIN = 200    # buffer size right and bottom we allow to go past the target


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
            calc_erosion((x,y))


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


def equipable(pos):
    if WORLD[pos] == '.':       # rocky
        return {TORCH, GEAR}
    elif WORLD[pos] == '=':     # wet
        return {GEAR, NEITHER}
    else:                       # narrow
        return {TORCH, NEITHER}


def crawl_cell(cell, status):
    if cell[0] >= 0 and cell[1] >= 0:
        x, y, equip, dist = status
        equipable_cell = equipable(cell)
        equipable_before = equipable((x, y))
        can_equip = equipable_cell.intersection(equipable_before)

        for new_equip in can_equip:  # 1 possible if different type of rock, 2 possible if same
            if equip != new_equip:
                next_dist = dist + 8  # change equipment
            else:
                next_dist = dist + 1  # keep current equipment

            if cell not in REACHED:
                REACHED[cell] = {}
            if new_equip not in REACHED[cell] or REACHED[cell][new_equip] > next_dist:
                REACHED[cell][new_equip] = next_dist
                if next_dist not in TO_CRAWL:
                    TO_CRAWL[next_dist] = []
                TO_CRAWL[next_dist].append((cell[0], cell[1], new_equip, next_dist))


def crawl(status):
    x, y, equip, dist = status
    if GLOBS['shortest'] and dist >= GLOBS['shortest']:
        return
    if y + 1  < GLOBS['target'][1] + MARGIN:
        crawl_cell((x, y+1), status)
    if x + 1  < GLOBS['target'][0] + MARGIN:
        crawl_cell((x+1, y), status)
    if x - 1 >= 0:
        crawl_cell((x-1, y), status)
    if y - 1 >= 0:
        crawl_cell((x, y - 1), status)


def process(depth, target):
    GLOBS['depth'] = depth
    GLOBS['target'] = target
    GEO_INDEX[(0, 0)] = 0
    GEO_INDEX[target] = 0

    # give some margin on both sides
    scope = (target[0] + MARGIN, target[1] + MARGIN)
    fill_world(scope)
    scan(scope)
    pretty_print(target)

    # now find the quickest way
    REACHED[(0, 0)] = {TORCH: 0, GEAR: 7}
    TO_CRAWL[0] = [(0, 0, TORCH, 0)]
    TO_CRAWL[7] = [(0, 0, GEAR, 7)]

    dist = 0
    while TO_CRAWL:
        if target in REACHED:
            min_dist = min([REACHED[target][reached] + (0 if reached == TORCH else 7) for reached in REACHED[target]])
            GLOBS['shortest'] = min_dist

        if dist > GLOBS['shortest']:
            return GLOBS['shortest']

        if dist not in TO_CRAWL:
            dist += 1
            continue
        elif not TO_CRAWL[dist]:
            del TO_CRAWL[dist]
            dist += 1
            continue
        else:
            crawl(TO_CRAWL[dist].pop(0))


def compute(file_name):
    # pr = cProfile.Profile()
    # pr.enable()
    with open(file_name, "r") as file:
        depth, target = parse(file.readlines())
        res = process(depth, target)
    # pr.disable()
    # s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())
    return res


if __name__ == '__main__':
    print("Quickest way  = ", compute("data.txt"))
