def compute(file_name):
    with open(file_name, "r") as file:
        return sum([int(line) for line in file.readlines()])


if __name__ == '__main__':
    print("Total = ", compute("data.txt"))
