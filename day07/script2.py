CONFIG = {'elves': 0, 'prcessing_time': 0}


def parse(line):
    return line[5], line[36]


def no_dep(node, nodes, res):
    for dep in nodes[node]['depends_on']:
        if dep not in res:
            return False
    return True


def exec_time(letter):
    return CONFIG['processing_time'] + (ord(letter) - ord('A') + 1)


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
    ready = [node for (node, info) in graph.items() if len(info['depends_on']) == 0]
    res = ''
    elves = CONFIG['elves']
    time = 0
    countdown = {}
    while len(res) != len(graph):
        while elves > 0 and len(ready) > 0:
            elves -= 1
            first = ready.pop(0)
            countdown[first] = exec_time(first)
        for pending in countdown:
            countdown[pending] -= 1
            if countdown[pending] == 0:
                res += pending
                elves += 1
                for node in graph[pending]['depended_by']:
                    if no_dep(node, graph, res):
                        ready.append(node)
                        ready.sort()
        time += 1
    return time


def compute(file_name, elves, processing_time):
    CONFIG['elves'] = elves
    CONFIG['processing_time'] = processing_time
    with open(file_name, "r") as file:
        data = [parse(line) for line in file.readlines()]
        return process(data)


if __name__ == '__main__':
    print("Time = ", compute("data.txt", 5, 60))
