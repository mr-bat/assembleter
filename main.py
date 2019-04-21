import re


def calculate(command, a, b):
    if command == 'add' or command == 'addi':
        return a + b
    elif command == 'sub' or command == 'subi':
        return a - b
    elif command == 'and':
        return a & b
    elif command == 'or':
        return a | b
    elif command == 'xor':
        return a ^ b
    elif command == 'nor':
        return ~(a | b)
    elif command == 'sla' or command == 'sll':
        return a << b
    elif command == 'srl':
        return a >> b if a >= 0 else (a + 0x100000000) >> b
    elif command == 'sra':
        return a >> b
    else:
        raise NotImplementedError('ALU request is strange')


class Interpreter:
    RegSize = 26
    MemSize = 255000
    MemThreshold = 1024
    RegMax = 0x100000000

    def __init__(self, _instructions):
        self.instruction = _instructions
        self.pc = 0
        self.register = [0 for _ in xrange(self.RegSize)]
        self.mem = [0 for _ in xrange(self.MemSize)]

    def getVal(self, var):
        if var[0] == 'r':
            var = self.register[int(var[1:])]
        return int(var)

    def runOne(self):
        command = self.instruction[self.pc].lower()
        command = re.split('[ ,\n]', command)
        command = filter(None, command)
        self.pc += 1

        print(command)
        d_loc = int(command[1][1:])
        d = self.getVal(command[1]) if len(command) > 1 else None
        a = self.getVal(command[2]) if len(command) > 2 else None
        b = self.getVal(command[3]) if len(command) > 3 else None

        if command[0] == 'ld':
            print(d_loc, d, a, b)
            pos = (a + b - self.MemThreshold) / 4
            self.register[d_loc] = self.mem[pos]
        elif command[0] == 'st':
            pos = (a + b - self.MemThreshold) / 4
            self.mem[pos] = d
        elif command[0] == 'bez':
            if d == 0:
                self.pc += a
        elif command[0] == 'bne':
            if d != a:
                self.pc += b
        elif command[0] == 'jmp':
            self.pc += d
        else:
            self.register[d_loc] = calculate(command[0], a, b) % self.RegMax


if __name__ == '__main__':
    fileObject = open('parsedInstructions', 'r')
    instructions = fileObject.readlines()

    mips = Interpreter(instructions)

    for _ in xrange(600):
        mips.runOne()
