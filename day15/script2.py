GLOB = {'last_id': -1}


class Warrior:
    def __init__(self, race, i, j, atk):
        GLOB['last_id'] += 1
        self.id = GLOB['last_id']
        self.race = race
        self.i = i
        self.j = j
        self.hp = 200
        self.atk = atk

    def desc(self):
        return self.race + '(' + str(self.id) + ',' + str(self.i) + ',' + str(self.j) + ',' + str(self.hp) + ')'


WORLD = []
WARRIORS: [Warrior] = []


def parse(lines, elf_atk):
    for i in range(len(lines)):
        world_line = []
        line = lines[i].strip('\n')
        for j in range(len(line)):
            c = line[j]
            if c == '#':
                world_line += [False]
                continue
            elif c == 'G':
                WARRIORS.append(Warrior('G', i, j, 3))
            elif c == 'E':
                WARRIORS.append(Warrior('E', i, j, elf_atk))
            world_line += [True]
        WORLD.append(world_line)


def get_char_for_cell(i, j):
    if not WORLD[i][j]:
        return '#'
    for warrior in WARRIORS:
        if warrior.i == i and warrior.j == j:
            return warrior.race
    return '.'


def pretty_print():
    for i in range(len(WORLD)):
        line = WORLD[i]
        chars = ''
        for j in range(len(line)):
            chars += get_char_for_cell(i, j)
        print(str(i//10), str(i % 10), '  ', chars)


def get_w(w_id):
    return [w for w in WARRIORS if w.id == w_id][0]


def get_w_from_coord(i, j):
    return [w for w in WARRIORS if w.i == i and w.j == j][0]


def other_race(w):
    return 'E' if w.race == 'G' else 'G'


def find_squares_in_range(race):
    squares = []
    for w in WARRIORS:
        if w.race == race:
            squares.extend(find_adjacent('.', w.i, w.j))
    return squares


def find_adjacent(symbol, i, j):
    squares = []
    # return adjacent squares in reading order
    for square in [(i-1, j), (i, j-1), (i, j+1), (i+1, j)]:
        if get_char_for_cell(square[0], square[1]) == symbol:
            squares.append(square)
    return squares


def find_next_move(w, squares_in_range):
    reach_map = {(w.i, w.j): 0}
    path_map = {(w.i, w.j): []}
    to_process = [(w.i, w.j)]
    dist_max = 1000     # above this dist, useless to check
    while len(to_process):
        processing = to_process.pop(0)
        if reach_map[processing] >= dist_max:
            break   # further exploration is useless, all path will be longer
        adj_empty_squares = find_adjacent('.', processing[0], processing[1])
        for square in adj_empty_squares:
            if square not in reach_map:
                reach_map[square] = reach_map[processing] + 1
                path_map[square] = path_map[processing] + [square]
                to_process.append(square)
                if square in squares_in_range:
                    dist_max = reach_map[square]   # we found a way to a square in range

    possible_moves = [square for square in reach_map if square in squares_in_range]
    if len(possible_moves) == 0:
        return None     # No possible move to get closer to an ennemy
    target_square = possible_moves[0]
    if len(possible_moves) == 1:
        return path_map[target_square][0]
    else:
        for square in possible_moves[1:]:
            if square[0] < target_square[0] or (square[0] == target_square[0] and square[1] < target_square[1]):
                target_square = square
        return path_map[target_square][0]


def move(w):
    squares_in_range = find_squares_in_range(other_race(w))
    next_move = find_next_move(w, squares_in_range)
    if next_move is None:
        # print('No reachable ennemy for ', w.desc(), ', EOT')
        return False

    # actually move
    w.i = next_move[0]
    w.j = next_move[1]
    return True


def attack_target(adj_ennemy_cells):
    adj_ennemies = [get_w_from_coord(coord[0], coord[1]) for coord in adj_ennemy_cells]
    min_hp = min([w.hp for w in adj_ennemies])
    min_adj_ennemies = [w for w in adj_ennemies if w.hp == min_hp]
    if len(min_adj_ennemies) == 1:
        return min_adj_ennemies[0].id
    else:
        target = min_adj_ennemies[0]
        for w in min_adj_ennemies[1:]:
            if w.i < target.i or (w.i == target.i and w.j < target.j):
                target = w
        return target.id


def attack(w: Warrior):
    adjacent_ennemy_cells = find_adjacent(other_race(w), w.i, w.j)
    if len(adjacent_ennemy_cells) == 0:
        # print(w.desc(), ' cannot attack, EOT')
        return  # has moved and cannot attack
    target_id = attack_target(adjacent_ennemy_cells)
    target = get_w(target_id)
    # print(w.desc(), ' attack ', target.desc(), ', EOT')
    target.hp -= w.atk
    if target.hp <= 0:
        # print(w.desc(), 'killed ', target.desc())
        WARRIORS.remove(target)


def play_warrior(w_id):
    w = get_w(w_id)
    if len(find_adjacent(other_race(w), w.i, w.j)) == 0:
        if not move(w):
            return          # no one adjacent and cannot move, end of turn
    attack(w)


def still_alive(w_id):
    return w_id in [w.id for w in WARRIORS]


def battle_end():
    return len(set([w.race for w in WARRIORS])) == 1


def next_round():
    WARRIORS.sort(key=lambda w: w.i * 1000 + w.j)
    w_ids = [w.id for w in WARRIORS]
    for w_id in w_ids:
        if still_alive(w_id):
            if battle_end():
                return True    # the battle ended before a warrior could play
            play_warrior(w_id)
    return False


def process():
    elves_nb = len([w for w in WARRIORS if w.race == 'E'])
    pretty_print()
    curr_round = 0
    over = False
    while not over:
        curr_round += 1
        over = next_round()
    pretty_print()
    print('Full rounds =', curr_round - 1)
    remaining_hp = sum([w.hp for w in WARRIORS])
    print('Remaining HP = ', remaining_hp)
    remaining_elves = len([w for w in WARRIORS if w.race == 'E'])
    if remaining_elves < elves_nb:
        print(str(remaining_elves), '/', str(elves_nb), ' survived...')
        return -1
    print('All elves survived !')
    return (curr_round - 1) * remaining_hp


def compute(file_name, elf_atk):
    WORLD.clear()
    WARRIORS.clear()
    with open(file_name, "r") as file:
        parse(file.readlines(), elf_atk)
        return process()


def wrapper(file_name):
    atk_elf = 3
    score = -1
    while score < 0:
        atk_elf += 1
        print('Try with elf attack = ', str(atk_elf))
        score = compute(file_name, atk_elf)
    print('Elf attack = ', str(atk_elf))
    return score


if __name__ == '__main__':
    print("Res  = ", wrapper("data.txt"))
