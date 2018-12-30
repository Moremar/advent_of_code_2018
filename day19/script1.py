import abc
import re


class Command:
    def __init__(self, op, a, b, c):
        self.op = op
        self.a = a
        self.b = b
        self.c = c


def valid_reg(reg_index):
    return reg_index in range(6)


class Instruction:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calc(self, a, b, c, regi):
        raise NotImplementedError('Should not call interface method')


class Addr(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] + regi[b]
        return rego


class Addi(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] + b
        return rego


class Mulr(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] * regi[b]
        return rego


class Muli(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] * b
        return rego


class Banr(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] & regi[b]
        return rego


class Bani(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] & b
        return rego


class Borr(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] | regi[b]
        return rego


class Bori(Instruction):
    def calc(self, a, b, c, regi):
        rego = list(regi)
        rego[c] = regi[a] | b
        return rego


class Setr(Instruction):
    def calc(self, a, b, c, regi):
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
        rego = list(regi)
        rego[c] = 1 if a > regi[b] else 0
        return rego


class Gtri(Instruction):
    def calc(self, a, b, c, regi):
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
    commands = []
    ip_line = re.match(r'#ip (\d+)', lines.pop(0).strip())
    ip = int(ip_line.group(1))
    while lines:
        (op, a, b, c) = lines.pop(0).strip().split(' ')
        commands.append(Command(op, int(a), int(b), int(c)))
    return commands, ip


def get_instr(name) -> Instruction:
    for instr in INSTRUCTIONS:
        if instr_name(instr).lower() == name:
            return instr
    raise LookupError('Did not find command with name : ', name)


def instr_name(instr):
    return instr.__class__.__name__


def process(commands: [Command], ip_reg):
    with open('output.log', 'w') as output :
        regi = [0, 0, 0, 0, 0, 0]
        ip = 0
        i = 0
        while 0 <= ip < len(commands):
            i += 1
            comm = commands[ip]
            regi[ip_reg] = ip
            # line = '[' + str(ip) + '] ' + str(comm.op) + ' ' + str(comm.a) + ' ' + str(comm.b) + ' ' + str(comm.c) + ' ' + str(regi)
            instr = get_instr(comm.op)
            regi = instr.calc(comm.a, comm.b, comm.c, regi)
            # line += '  ->  ' + str(regi) + '\n'
            # output.write(line)
            ip = regi[ip_reg] + 1
    return regi[0]


def compute(file_name):
    with open(file_name, "r") as file:
        commands, ip = parse(file.readlines())
        return process(commands, ip)


if __name__ == '__main__':
    print("Val of register 0 = ", compute("data.txt"))
