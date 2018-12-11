import numpy as np

# TODO : this works but takes forever
# TODO : Would be smarter to calculate all blocks starting at a given position
# TODO : to re-use the previous calculation each time

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


def square_power(mx, x, y, square_size):
    p = 0
    for dx in range(square_size):
        for dy in range(square_size):
            p += mx[x + dx, y + dy]
    return p


def power_mx_square(mx, s):
    mx_size = SIZE - s + 1
    mx_square = np.zeros((mx_size, mx_size))
    for x in range(mx_size):
        for y in range(mx_size):
            mx_square[x, y] = square_power(mx, x, y, s)
    return mx_square


def process(serial):
    mx = power_mx(serial)
    max_s = 0
    max_power = -100000
    max_coords = (0, 0)
    for s in range(1, SIZE+1):
        mx_square = power_mx_square(mx, s)
        curr_max_power = np.max(mx_square)
        if curr_max_power > max_power:
            max_power = curr_max_power
            max_s = s
            (max_x, max_y) = tuple(np.argwhere(mx_square == curr_max_power)[0])
            max_coords = (max_x + 1, max_y + 1)
        print('Step ', s, 'local mx = ', curr_max_power, ', max so far = ',
              list(max_coords) + [max_s], ' (max = ', max_power, ')')
    return list(max_coords) + [max_s]


def compute(file_name):
    with open(file_name, "r") as file:
        serial = int(file.readline())
        return process(serial)


if __name__ == '__main__':
    print("Max power 3x3 cell  = ", compute("data.txt"))
