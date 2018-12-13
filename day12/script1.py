SHIFT = 10


def parse_init(line):
    return [c == '#' for c in line[15:].strip()]


def parse_rules(lines):
    rules = []
    for line in lines:
        if line[9] == '#':
            rules.append([c == '#' for c in line[:5]])
    return rules


def calculate_next_state(state, rules):
    # experimentally we never need to increase the size
    # of the array on the left, which makes it easier
    if sum(state[-5:]):
        state = state + [False * 10]    # increase on the right if needed
    next_state = []
    for i in range(len(state)):
        if i < 2 or i > len(state) - 3:
            next_state += [False]
        else:
            next_state += [state[i-2:i+3] in rules]
    return next_state


def sum_plants(state):
    total = 0
    for i in range(len(state)):
        if state[i]:
            total += i - SHIFT
    return total


def process(init, rules, generations):
    # add 10 empty pots before and after
    last_state = [0] * SHIFT + init + [0] * SHIFT
    for i in range(generations):
        last_state = calculate_next_state(last_state, rules)
        # print('step ', i, 'res = ', sum_plants(last_state))
    return sum_plants(last_state)


def compute(file_name):
    with open(file_name, "r") as file:
        init = parse_init(file.readline())
        file.readline()                         # skip empty line
        rules = parse_rules(file.readlines())
        return process(init, rules, 20)


if __name__ == '__main__':
    print("Sum of plants positions  = ", compute("data.txt"))
