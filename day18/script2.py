FOREST = []
PREVS = []


def parse(lines):
    for line in lines:
        forest_line = []
        for j in range(len(line)):
            forest_line.append(line[j])
        FOREST.append(forest_line)


def pretty_print():
    for line in FOREST:
        print(''.join(line))
    print()


def adjacent(x, y, ref):
    adjs = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
    adjs = [(a, b) for (a, b) in adjs if 0 <= a < len(ref) and 0 <= b < len(ref[0])]
    return ''.join([ref[a][b] for (a, b) in adjs])


def next_gen(x, y, ref):
    adjs = adjacent(x, y, ref)
    if ref[x][y] == '.' and adjs.count('|') >= 3:
        return '|'
    elif ref[x][y] == '|' and adjs.count('#') >= 3:
        return '#'
    elif ref[x][y] == '#' and (adjs.count('#') < 1 or adjs.count('|') < 1):
        return '.'
    return ref[x][y]


def snap():
    snapped = []
    for line in FOREST:
        snapped.append(list(line))
    return snapped


def mutate():
    forest_snap = snap()
    for x in range(len(FOREST)):
        for y in range(len(FOREST[0])):
            FOREST[x][y] = next_gen(x, y, forest_snap)


def calc():
    trees = 0
    lumber = 0
    for x in range(len(FOREST)):
        for y in range(len(FOREST[0])):
            if FOREST[x][y] == '|':
                trees += 1
            elif FOREST[x][y] == '#':
                lumber += 1
    return trees * lumber


def find_loop_size():
    for i in range(10000):
        PREVS.append(snap())
        mutate()
        if FOREST in PREVS :
            found = PREVS.index(FOREST)
            return i - found + 1


def reset(snap):
    for x in range(len(snap)):
        for y in range(len(snap[0])):
            FOREST[x][y] = snap[x][y]


def process():
    init = snap()
    pretty_print()
    # we can see a loop after 500 iterations so we find the size of the loop
    # and stop at the step that will have the same pattern as the target nb of iterations
    loop_size = find_loop_size()
    print('Found loop of size ', loop_size)

    reset(init)
    for i in range(500 + (1_000_000_000 - 500) % loop_size):
        mutate()

    pretty_print()
    return calc()

def compute(file_name):
    with open(file_name, "r") as file:
        parse([line.strip() for line in file.readlines()])
        return process()


if __name__ == '__main__':
    print("#trees * #lumberyards  = ", compute("data.txt"))
