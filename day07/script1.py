def parse(line):
    return line[5], line[36]


def no_dep(node, nodes, res):
    for dep in nodes[node]['depends_on']:
        if dep not in res:
            return False
    return True


def build_graph(deps):
    graph = {}
    for dep in deps:
        for node in [dep[0], dep[1]]:
            if node not in graph:
                graph[node] = {'depends_on': set(), 'depended_by': set()}
        graph[dep[0]]['depended_by'].add(dep[1])
        graph[dep[1]]['depends_on'].add(dep[0])
    return graph


def process(deps):
    graph = build_graph(deps)

    # find root node
    ready = [node for (node, info) in graph.items() if len(info['depends_on']) == 0]

    res = ''
    while len(res) != len(graph):
        ready.sort()
        first = ready.pop(0)
        res += first
        for node in graph[first]['depended_by']:
            if no_dep(node, graph, res):
                ready.append(node)
    return res


def compute(file_name):
    with open(file_name, "r") as file:
        data = [parse(line) for line in file.readlines()]
        return process(data)


if __name__ == '__main__':
    print("Order = ", compute("data.txt"))
