import re


class Record:
    def __init__(self, min, action, guard) :
        self.min = min
        self.action = action
        self.guard = guard


def parse(line) :
    m = re.match(r'\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] (.*)', line)
    (min, text) = m.groups()
    if 'falls asleep' in text :
        return Record(int(min), "SLEEP", None)
    elif 'wakes up' in text :
        return Record(int(min), "WAKE", None)
    elif 'begins shift' in text :
        m2 = re.match(r'Guard #(\d+)', text)
        return Record(int(min), "BEGIN", int(m2.group(1)))
    else :
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


def most_sleepy_guard(history):
    most_sleepy = -1
    max_sleep = -1
    for guard in history:
        sleep = sum(history[guard])
        if sleep > max_sleep:
            most_sleepy = guard
            max_sleep = sleep
    return most_sleepy


def most_slept_min(guard, history):
    most_slept = -1
    max_slept = -1
    for min in range(60):
        slept = history[guard][min]
        if slept > max_slept:
            most_slept = min
            max_slept = slept
    return most_slept


def process(data):
    history = fill_table(data)
    sleeper = most_sleepy_guard(history)
    slept_min = most_slept_min(sleeper, history)
    return sleeper * slept_min


def compute(file_name):
    with open(file_name, "r") as file:
        data = [parse(line) for line in sorted(file.readlines())]
        return process(data)


if __name__ == '__main__':
    print("Guard * Mins = ", compute("data.txt"))
