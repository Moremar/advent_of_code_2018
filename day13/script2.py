RIGHT = 'RIGHT'
LEFT = 'LEFT'
STRAIGHT = 'STRAIGHT'

DIR_LINE = {'>': '-', 'v': '|', '<': '-', '^': '|'}
GLOB = {'last_id': -1}
CLEANED_ID = []


class Cart:
    def __init__(self, i, j, direction):
        GLOB['last_id'] += 1
        self.id = GLOB['last_id']
        self.i = i
        self.j = j
        self.dir = direction
        self.last_turn = RIGHT

    def next_turn(self):
        if self.last_turn == RIGHT:
            turn = LEFT
        elif self.last_turn == LEFT:
            turn = STRAIGHT
        else:
            turn = RIGHT
        self.last_turn = turn
        return turn

    def move(self, cell):
        if cell == '-':
            self.j += 1 if self.dir == '>' else -1
        elif cell == '|':
            self.i += 1 if self.dir == 'v' else -1
        elif cell == '/' and self.dir == '^':
            self.j += 1;    self.dir = '>'
        elif cell == '/' and self.dir == '<':
            self.i += 1;    self.dir = 'v'
        elif cell == '/' and self.dir == 'v':
            self.j -= 1;    self.dir = '<'
        elif cell == '/' and self.dir == '>':
            self.i -= 1;    self.dir = '^'
        elif cell == '\\' and self.dir == '^':
            self.j -= 1;    self.dir = '<'
        elif cell == '\\' and self.dir == '<':
            self.i -= 1;    self.dir = '^'
        elif cell == '\\' and self.dir == 'v':
            self.j += 1;    self.dir = '>'
        elif cell == '\\' and self.dir == '>':
            self.i += 1;    self.dir = 'v'
        elif cell == '+':
            turn = self.next_turn()
            if turn == LEFT:
                if self.dir == '^':
                    self.j -= 1;    self.dir = '<'
                elif self.dir == '<':
                    self.i += 1;    self.dir = 'v'
                elif self.dir == 'v':
                    self.j += 1;    self.dir = '>'
                elif self.dir == '>':
                    self.i -= 1;    self.dir = '^'
            elif turn == STRAIGHT:
                if self.dir == '^':
                    self.i -= 1
                elif self.dir == '<':
                    self.j -= 1
                elif self.dir == 'v':
                    self.i += 1
                elif self.dir == '>':
                    self.j += 1
            elif turn == RIGHT:
                if self.dir == '^':
                    self.j += 1;    self.dir = '>'
                elif self.dir == '<':
                    self.i -= 1;    self.dir = '^'
                elif self.dir == 'v':
                    self.j -= 1;    self.dir = '<'
                elif self.dir == '>':
                    self.i += 1;    self.dir = 'v'


WORLD = []
CARTS: [Cart] = []


def get_cart(i, j):
    for cart in CARTS:
        if cart.i == i and cart.j == j:
            return cart
    return None


def parse(lines):
    for i in range(len(lines)):
        world_line = []
        line = lines[i].strip('\n')
        for j in range(len(line)):
            c = line[j]
            if c in 'v<^>':
                CARTS.append(Cart(i, j, c))
                world_line += [DIR_LINE[c]]
            else:
                world_line += [c]
        WORLD.append(world_line)


def pretty_print():
    for i in range(len(WORLD)):
        line = WORLD[i]
        chars = ''
        for j in range(len(line)):
            cart: Cart = get_cart(i, j)
            chars += cart.dir if cart else line[j]
        print(chars)


def clean_if_crash(i, j):
    count = 0
    for cart in CARTS:
        if cart.i == i and cart.j == j and cart.id not in CLEANED_ID:
            count += 1
    if count > 1:
        for cart in CARTS:
            if cart.i == i and cart.j == j and cart.id not in CLEANED_ID:
                CLEANED_ID.append(cart.id)


def next_move():
    CARTS.sort(key=lambda c: c.i * 1000 + c.j)
    for cart in CARTS:
        if cart.id not in CLEANED_ID:
            cart.move(WORLD[cart.i][cart.j])
            clean_if_crash(cart.i, cart.j)
    remaining = [cart for cart in CARTS if cart.id not in CLEANED_ID]
    if len(remaining) == 1:
        return remaining[0]
    return None


def process():
    remaining: Cart = None
    # pretty_print()
    while not remaining:
        remaining = next_move()
        # pretty_print()
    return remaining.j, remaining.i


def compute(file_name):
    with open(file_name, "r") as file:
        parse(file.readlines())
        return process()


if __name__ == '__main__':
    print("Last cart = ", compute("data.txt"))
