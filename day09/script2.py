SCORES = {}


class Marble:
    def __init__(self, val, prev, next):
        self.val = val
        self.prev = prev
        self.next = next

    def remove_seven_before(self):
        seven_before = self
        for i in range(7):
            seven_before = seven_before.prev
        seven_before.prev.next = seven_before.next
        seven_before.next.prev = seven_before.prev
        return seven_before

    def insert_after_next(self, val):
        new_marble = Marble(val, self.next, self.next.next)
        self.next.next.prev = new_marble
        self.next.next = new_marble
        return new_marble


def play(marble_id, player, current_marble):
    if marble_id % 23 != 0:
        return current_marble.insert_after_next(marble_id)
    else:
        removed = current_marble.remove_seven_before()
        SCORES[player] += marble_id + removed.val
        return removed.next


def process(players, max_marble):
    for player in range(players):
        SCORES[player] = 0

    # init the circle
    marble0 = Marble(0, None, None)
    marble0.prev = marble0
    marble0.next = marble0

    current_marble = marble0
    for j in range(1, max_marble + 1):
        current_marble = play(j, (j-1) % players, current_marble)
    return max(SCORES.values())


def compute(file_name):
    with open(file_name, "r") as file:
        data = file.readline().strip().split(' ')
        players, max_marble = (int(data[0]), int(data[6]) * 100)
        return process(players, max_marble)


if __name__ == '__main__':
    print("Max score = ", compute("data.txt"))
