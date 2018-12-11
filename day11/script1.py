import numpy as np

SIZE = 300          # fuel matrix size


def power(x, y, serial):
    rack_id = x + 10
    p = rack_id * y
    p += serial
    p *= rack_id
    p = int((p / 100) % 10)
    p -= 5
    return p


def power_mx(serial):
    mx = np.zeros((SIZE, SIZE))
    for x in range(SIZE):
        for y in range(SIZE):
            mx[x, y] = power(x+1, y+1, serial)  # +1 because cells are from 1 to 300
    return mx


def square_power(mx, x, y):
    p = 0
    for dx in range(3):
        for dy in range(3):
            p += mx[x + dx, y + dy]
    return p


def power_mx_square(mx):
    size2 = SIZE - 2    # size of the matrix of square power
    mx_3x3 = np.zeros((size2, size2))
    for x in range(size2):
        for y in range(size2):
            mx_3x3[x, y] = square_power(mx, x, y)
    return mx_3x3


def find_max(mx_square):
    max_power = np.max(mx_square)
    (max_x, max_y) = tuple(np.argwhere(mx_square == max_power)[0])
    return max_x + 1, max_y + 1


def process(serial):
    mx = power_mx(serial)
    mx_square = power_mx_square(mx)
    return find_max(mx_square)


def compute(file_name):
    with open(file_name, "r") as file:
        serial = int(file.readline())
        return process(serial)


if __name__ == '__main__':
    print("Max power 3x3 cell  = ", compute("sample.txt"))
