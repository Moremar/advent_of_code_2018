def calc_freqs(word):
    freqs = {}
    for l in word:
        freqs[l] = freqs.get(l, 0) + 1
    return freqs


def process(words):
    x2, x3 = (0, 0)
    for word in words:
        f = calc_freqs(word)
        if 2 in f.values():
            x2 += 1
        if 3 in f.values():
            x3 += 1
    return x2 * x3


def compute(file_name):
    with open(file_name, "r") as file:
        return process([line.strip() for line in file.readlines()])


if __name__ == '__main__':
    print("Checksum = ", compute("data.txt"))
