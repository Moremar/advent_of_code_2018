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
    def calc(self, a, b, c, regi):
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
    while lines and 'Before' in lines[0]:
        line = lines.pop(0).strip()
        m = re.match(r'Before: \[(.*)\]', line)
        regi = [int(i) for i in m.group(1).split(', ')]
        instr = [int(i) for i in lines.pop(0).strip().split(' ')]
        line = lines.pop(0).strip()
        m = re.match(r'After: {2}\[(.*)\]', line)
        rego = [int(i) for i in m.group(1).split(', ')]
        if len(lines) > 0:
            lines.pop(0)    # empty line
        samples.append(Sample(regi, Command(instr[0], instr[1], instr[2], instr[3]), rego))
    return samples


def instr_name(instr):
    return instr.__class__.__name__


def process(samples):
    count = 0
    for sample in samples:
        possible_instr = []
        for instr in INSTRUCTIONS:
            res_calc = instr.calc(sample.comm.a, sample.comm.b, sample.comm.c, sample.regi)
            if res_calc == sample.rego:
                possible_instr.append(instr_name(instr))
        if len(possible_instr) >= 3:
            count += 1
    return count


def compute(file_name):
    with open(file_name, "r") as file:
        samples = parse(file.readlines())
        return process(samples)


if __name__ == '__main__':
    print("Samples with 3+ possibles instr = ", compute("data.txt"))
