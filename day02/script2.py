def one_char_diff(word1, word2):
    diff = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            diff += 1
        if diff > 1:
            return False
    return diff == 1


def common(word1, word2):
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            return word1[:i] + word1[i+1:]
    raise RuntimeError('String are equals')


def process(words):
    for i in range(len(words)-1):
        for j in range(i+1, len(words)):
            if one_char_diff(words[i], words[j]):
                return common(words[i], words[j])
    raise RuntimeError('Could not find similar words')


def compute(file_name):
    with open(file_name, "r") as file:
        return process([line.strip() for line in file.readlines()])


if __name__ == '__main__':
    print("Common part = ", compute("data.txt"))
