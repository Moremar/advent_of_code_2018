def opposite(l1, l2):
    return l1 != l2 and l1.upper() == l2.upper()


def reduce(polymer):
    reduced = ""
    for elem in polymer:
        if len(reduced) == 0:
            reduced = elem
        elif opposite(elem, reduced[-1]):
            reduced = reduced[:-1]
        else:
            reduced += elem
    return reduced


def process(polymer):
    shortest = len(polymer)
    for l in 'abcdefghijklmnopqrstuvwxyz':
        shorten = polymer.replace(l, '')
        shorten = shorten.replace(l.upper(), '')
        reduced = reduce(shorten)
        shortest = min(shortest, len(reduced))
    return shortest


def compute(file_name):
    with open(file_name, "r") as file:
        data = file.readline()
        return process(data)


if __name__ == '__main__':
    print("Polymer Size = ", compute("data.txt"))
