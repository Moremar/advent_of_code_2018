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
        state = state + [False * 10]        # increase on the right if needed

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
        if state[i] == 1:
            total += i - SHIFT
    return total


def calculate_positions(state):
    pos_absolute = []
    for i in range(len(state)):
        if state[i]:
            pos_absolute += [i]
    return [pos - pos_absolute[0] for pos in pos_absolute]


def process(init, rules, generations):
    last_state = [False] * SHIFT + init + [False] * SHIFT
    history = [last_state]
    position_founds = [calculate_positions(last_state)]
    for i in range(generations):
        last_state = calculate_next_state(last_state, rules)
        history += [last_state]
        new_pos = calculate_positions(last_state)
        if new_pos == position_founds[-1]:
            # we found a pattern that shifts itself from a step to the next
            # we do not need to process all steps, just to find the final shift
            curr_sum = sum_plants(last_state)
            prev_sum = sum_plants(history[-2])
            diff = curr_sum - prev_sum
            return curr_sum + diff * (generations - (i + 1))
        position_founds += [new_pos]

    # this will not be reached for a big generations value
    # we rely on the fact that we will find a pattern shifting iteself
    return sum_plants(last_state)


def compute(file_name):
    with open(file_name, "r") as file:
        init = parse_init(file.readline())
        file.readline()                         # skip empty line
        rules = parse_rules(file.readlines())
        return process(init, rules, 50000000000)


if __name__ == '__main__':
    print("Sum of plants positions  = ", compute("data.txt"))
