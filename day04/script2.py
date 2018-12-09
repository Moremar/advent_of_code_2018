import re


class Record:
    def __init__(self, minute, action, guard) :
        self.min = minute
        self.action = action
        self.guard = guard


def parse(line):
    m = re.match(r'\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] (.*)', line)
    (minute, text) = m.groups()
    if 'falls asleep' in text:
        return Record(int(minute), "SLEEP", None)
    elif 'wakes up' in text:
        return Record(int(minute), "WAKE", None)
    elif 'begins shift' in text:
        m2 = re.match(r'Guard #(\d+)', text)
        return Record(int(minute), "BEGIN", int(m2.group(1)))
    else:
        raise RuntimeError('Unknown action in ' + line)


def fill_table(records):
    guard = -1
    start_sleep = -1
    history = {}
    for record in records:
        if record.action == 'BEGIN':
            guard = record.guard
            if guard not in history:
                history[guard] = [0] * 60
        elif record.action == "SLEEP":
            start_sleep = record.min
        elif record.action == "WAKE":
            for i in range(start_sleep, record.min):
                history[guard][i] += 1
    return history


def most_asleep_at_same_min(history):
    max_slept_guard = -1
    max_slept_min = -1
    slept_nb = -1
    for guard in history:
        curr_max_slept = max(history[guard])
        curr_max_min = history[guard].index(curr_max_slept)
        if curr_max_slept > slept_nb:
            max_slept_guard = guard
            max_slept_min = curr_max_min
            slept_nb = curr_max_slept
    return max_slept_guard * max_slept_min


def process(data):
    history = fill_table(data)
    return most_asleep_at_same_min(history)


def compute(file_name):
    with open(file_name, "r") as file:
        data = [parse(line) for line in sorted(file.readlines())]
        return process(data)


if __name__ == '__main__':
    print("Guard * Mins = ", compute("data.txt"))
