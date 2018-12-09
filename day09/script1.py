# solution with a global array of marbles
# sufficient for part 1, but not not very efficient
# solution for part 2 with a linked list of marbles is much quicker

MARBLES = []
SCORES = {}


def play(marble_id, player, current_marble_index):
    if marble_id % 23 != 0:
        marble_index = (current_marble_index + 2) % len(MARBLES)
        MARBLES.insert(marble_index, marble_id)
        return marble_index
    else:
        SCORES[player] += marble_id
        back_marble_index = (current_marble_index - 7) % len(MARBLES)
        SCORES[player] += MARBLES.pop(back_marble_index)
        return back_marble_index % len(MARBLES)  # if we removed the last marble, must return 0


def process(players, max_marble):
    for player in range(players):
        SCORES[player] = 0
    MARBLES.append(0)
    MARBLES.append(1)
    current_marble_index = 1
    for j in range(2, max_marble + 1):
        current_marble_index = play(j, (j-1) % players, current_marble_index)
    return max(SCORES.values())


def compute(file_name):
    with open(file_name, "r") as file:
        data = file.readline().strip().split(' ')
        players, max_marble = (int(data[0]), int(data[6]))
        return process(players, max_marble)


if __name__ == '__main__':
    print("Max score = ", compute("data.txt"))
