import collections

WORLD = {}
GLOBS = {'path': collections.deque(), 'size': 0, 'popped': 0}
NEXT = []


def letter():
    c = GLOBS['path'].popleft()
    GLOBS['popped'] += 1
    if GLOBS['popped'] % 250 == 0:
        print('Popped ', GLOBS['popped'], ' letters (', round(GLOBS['popped'] * 100 / GLOBS['size'], 2), '%)')
    return c


def finished():
    return not GLOBS['path']


def parse(path_str):
    GLOBS['path'] = collections.deque(path_str)
    GLOBS['size'] = len(path_str)
    positions = set()
    positions.add((0, 0))
    parse_block(positions)


def move_in_direction(positions, direction):
    new_pos = set()
    while len(positions):
        pos = positions.pop()
        if direction == 'N':
            door_pos = (pos[0], pos[1] + 1)
            room_pos = (pos[0], pos[1] + 2)
        elif direction == 'W':
            door_pos = (pos[0] - 1, pos[1])
            room_pos = (pos[0] - 2, pos[1])
        elif direction == 'E':
            door_pos = (pos[0] + 1, pos[1])
            room_pos = (pos[0] + 2, pos[1])
        else:
            door_pos = (pos[0], pos[1] - 1)
            room_pos = (pos[0], pos[1] - 2)
        WORLD[door_pos] = '-'
        new_pos.add(room_pos)
    return new_pos


def parse_block(positions: set):
    # process letters one by one, and perform the move from each position in parameter
    while not finished():
        c = letter()
        if c in 'NWES':
            positions = move_in_direction(positions, c)
        elif c == '|':
            return positions, False
        elif c == ')':
            return positions, True
        elif c == '(':
            # will get the positions after taking each of the possible branches
            last = False
            new_pos = set()
            # get final position for every possible next block, then
            # continue processing the path string for each of those positions
            while not last:
                option_pos, last = parse_block(set(positions))
                new_pos = new_pos.union(option_pos)
            positions = new_pos
        else:
            raise SyntaxError('Unknown symbol : ' + c)


def find_furthest_room():
    min_dist_map = {(0, 0): 0}
    to_process = [(0, 0, 0)]
    while len(to_process):
        (x, y, d) = to_process.pop(0)
        # if the next cell is in WORLD then it is a door
        if (x-1, y) in WORLD and (x-2, y) not in min_dist_map:
            min_dist_map[(x-2, y)] = d + 1
            to_process.append((x-2, y, d + 1))
        if (x+1, y) in WORLD and (x+2, y) not in min_dist_map:
            min_dist_map[(x+2, y)] = d + 1
            to_process.append((x+2, y, d + 1))
        if (x, y-1) in WORLD and (x, y-2) not in min_dist_map:
            min_dist_map[(x, y-2)] = d + 1
            to_process.append((x, y-2, d + 1))
        if (x, y+1) in WORLD and (x, y+2) not in min_dist_map:
            min_dist_map[(x, y+2)] = d + 1
            to_process.append((x, y+2, d + 1))
    return max(min_dist_map.values())


def is_room(pos):
    if WORLD.get((pos[0]-1, pos[1])) == '|' or WORLD.get((pos[0]+1, pos[1])) == '|' \
           or WORLD.get((pos[0], pos[1]-1)) == '-' or WORLD.get((pos[0], pos[1]+1)) == '-':
        return '.'
    return '#'


def pretty_print():
    min_x = min([x for (x, y) in WORLD])
    min_y = min([y for (x, y) in WORLD])
    max_x = max([x for (x, y) in WORLD])
    max_y = max([y for (x, y) in WORLD])
    print()
    for row in range(max_y + 2, min_y - 3, -1):
        to_print = ''
        for col in range(min_x - 2, max_x + 3):
            to_print += WORLD[(col, row)] if (col, row) in WORLD else is_room((col, row))
        print(to_print)
    print()


def process(path_str):
    WORLD.clear()
    WORLD[(0, 0)] = 'X'
    parse(path_str)
    pretty_print()
    return find_furthest_room()


def compute(file_name):
    with open(file_name, "r") as file:
        path_str = file.readline().strip()[1:-1]
        return process(path_str)


if __name__ == '__main__':
    print("#doors to furthest room  = ", compute("data.txt"))
