import abc
import re


class Command:
    def __init__(self, op, a, b, c):
        self.op = op
        self.a = a
        self.b = b
        self.c = c


class Sample:
    def __init__(self, regi, comm, rego):
        self.regi = regi
        self.comm = comm
        self.rego = rego


def valid_reg(reg_index):
    return reg_index in [0, 1, 2, 3]

class Instruction:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calc(self, A, B, C, regi):
        raise NotImplementedError('Should not call interface method')


class Addr(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a) or not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = regi[a] + regi[b]
        return rego


class Addi(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a):
            return None
        rego = list(regi)
        rego[c] = regi[a] + b
        return rego


class Mulr(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a) or not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = regi[a] * regi[b]
        return rego


class Muli(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a):
            return None
        rego = list(regi)
        rego[c] = regi[a] * b
        return rego


class Banr(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a) or not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = regi[a] & regi[b]
        return rego


class Bani(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a):
            return None
        rego = list(regi)
        rego[c] = regi[a] & b
        return rego


class Borr(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a) or not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = regi[a] | regi[b]
        return rego


class Bori(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a):
            return None
        rego = list(regi)
        rego[c] = regi[a] | b
        return rego


class Setr(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a):
            return None
        rego = list(regi)
        rego[c] = regi[a]
        return rego


class Seti(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = a
        return rego


class Gtir(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = 1 if a > regi[b] else 0
        return rego


class Gtri(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a):
            return None
        rego = list(regi)
        rego[c] = 1 if regi[a] > b else 0
        return rego


class Gtrr(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a) or not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = 1 if regi[a] > regi[b] else 0
        return rego


class Eqir(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = 1 if a == regi[b] else 0
        return rego


class Eqri(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a):
            return None
        rego = list(regi)
        rego[c] = 1 if regi[a] == b else 0
        return rego


class Eqrr(Instruction):
    def calc(self, a, b, c, regi):
        if not valid_reg(a) or not valid_reg(b):
            return None
        rego = list(regi)
        rego[c] = 1 if regi[a] == regi[b] else 0
        return rego


INSTRUCTIONS: [Instruction] = [Addr(), Addi(), Mulr(), Muli(), Banr(), Bani(), Borr(), Bori(),
                               Setr(), Seti(), Gtir(), Gtri(), Gtrr(), Eqir(), Eqri(), Eqrr()]


def parse(lines):
    samples = []
    commands = []
    while len(lines):
        line = lines.pop(0).strip()
        if len(line) == 0:
            continue
        # samples parsing (1st part of the data)
        elif 'Before' in line:
            m = re.match(r'Before: \[(.*)\]', line)
            regi = [int(i) for i in m.group(1).split(', ')]
            instr = [int(i) for i in lines.pop(0).strip().split(' ')]
            line = lines.pop(0).strip()
            m = re.match(r'After: {2}\[(.*)\]', line)
            rego = [int(i) for i in m.group(1).split(', ')]
            samples.append(Sample(regi, Command(instr[0], instr[1], instr[2], instr[3]), rego))
        # command sequence parsing (2nd part of the data)
        else:
            comm = [int(i) for i in line.strip().split(' ')]
            commands.append(Command(comm[0], comm[1], comm[2], comm[3]))

    return samples, commands


def instr_name(instr):
    return instr.__class__.__name__


def get_instr(name) -> Instruction:
    for instr in INSTRUCTIONS:
        if instr_name(instr) == name:
            return instr
    raise LookupError('Did not find command with name : ', name)


def create_instr_map(samples: [Sample]):
    maybe_instr_tab = [set([instr_name(instr) for instr in INSTRUCTIONS])] * 16
    # parse all samples and find the possible optypes for each index
    for sample in samples:
        possible_instr = []
        for instr in INSTRUCTIONS:
            res_calc = instr.calc(sample.comm.a, sample.comm.b, sample.comm.c, sample.regi)
            if res_calc == sample.rego:
                possible_instr.append(instr_name(instr))
        maybe_instr_tab[sample.comm.op] = maybe_instr_tab[sample.comm.op].intersection(set(possible_instr))

    # from the above result, infer the optype for each index
    instr_tab = [-1] * 16
    to_compute = set(range(16))
    while len(to_compute):
        for i in to_compute:
            if len(maybe_instr_tab[i]) == 1:
                instr = maybe_instr_tab[i].pop()
                instr_tab[i] = instr
                for k,v in enumerate(maybe_instr_tab):
                    v.discard(instr)
                to_compute.remove(i)
                break
    return instr_tab


def apply_commands(commands, instr_tab):
    regi = [0, 0, 0, 0]
    for comm in commands:
        instr = get_instr(instr_tab[comm.op])
        regi = instr.calc(comm.a, comm.b, comm.c, regi)
    return regi[0]


def process(samples, commands):
    instr_tab = create_instr_map(samples)
    return apply_commands(commands, instr_tab)


def compute(file_name):
    with open(file_name, "r") as file:
        samples, commands = parse(file.readlines())
        return process(samples, commands)


if __name__ == '__main__':
    print("Register [0] after commands = ", compute("data.txt"))
