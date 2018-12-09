TO_PROCESS = []


class Node:
    def __init__(self):
        self.children = []
        self.metas = []


def read_node():
    children_nb = TO_PROCESS.pop(0)
    metas_nb = TO_PROCESS.pop(0)
    node = Node()
    for i in range(children_nb):
        child = read_node()
        node.children.append(child)
    for i in range(metas_nb):
        meta = TO_PROCESS.pop(0)
        node.metas.append(meta)
    return node


def value(node: Node):
    if len(node.children) == 0:
        return sum(node.metas)
    total = 0
    for meta in node.metas:
        if meta == 0 or meta > len(node.children):
            continue
        total += value(node.children[meta-1])
    return total


def process(numbers):
    TO_PROCESS.extend(numbers)
    root = read_node()
    return value(root)


def compute(file_name):
    with open(file_name, "r") as file:
        data = file.readline().strip().split(' ')
        numbers = [int(number) for number in data]
        return process(numbers)


if __name__ == '__main__':
    print("Res = ", compute("data.txt"))
