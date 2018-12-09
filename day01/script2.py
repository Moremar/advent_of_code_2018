def process(values):
    total = 0
    seen = {0}
    while True:
        for value in values:
            total += value
            if total in seen:
                return total
            else:
                seen.add(total)


def compute(file_name):
    with open(file_name, "r") as file:
        return process([int(line) for line in file.readlines()])


if __name__ == '__main__':
    print("First item to repeat = ", compute("data.txt"))
