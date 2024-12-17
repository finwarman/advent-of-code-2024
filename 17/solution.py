#! /usr/bin/env python3

with open('input.txt', 'r') as f:
    FILE = f.read()

# FILE = '''
# Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0
# '''

LINES = FILE.strip().splitlines()

# registers
A = int(LINES[0].split(' ')[-1])
B = int(LINES[1].split(' ')[-1])
C = int(LINES[2].split(' ')[-1])

PROGRAM = [int(x) for x in LINES[-1].split(' ')[-1].split(',')]

IPTR = 0 # instruction pointer

# 3 bit computer
# (8 instructions)

class ThreeBitComputer:
    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.iptr = 0
        self.program = program
        self.output = []

    def combo_operand(self, value):
        if 0 <= value <= 3:
            return value
        if value == 4:
            return self.a
        if value == 5:
            return self.b
        if value == 6:
            return self.c
        raise Exception(f"Bad combo operand: {value}")

    def step(self):
        if self.iptr + 1 >= len(self.program):
            return False

        i = self.program[self.iptr]
        o = self.program[self.iptr + 1]

        # print(f"IPTR: {self.iptr}, Opcode: {i}, Operand: {o}, Registers: A={self.a}, B={self.b}, C={self.c}")

        if i == 0:
            # adv: division -> a
            denom = 2 ** self.combo_operand(o)
            if denom == 0:
                raise Exception("Division by zero")
            self.a = self.a // denom
        elif i == 1:
            # bxl: B XOR o
            self.b = self.b ^ o
        elif i == 2:
            # bst: mod 8 (lowest 3 bits)
            self.b = self.combo_operand(o) % 8
        elif i == 3:
            # jnz: jump if A is not zero
            if self.a != 0:
                self.iptr = o
                return True  # do not increment iptr
        elif i == 4:
            # bxc: B XOR C
            self.b = self.b ^ self.c
            # Operand is read but ignored
        elif i == 5:
            # out: combo operand mod 8
            output_value = self.combo_operand(o) % 8
            self.output.append(output_value)
        elif i == 6:
            # bdv: division -> b
            denom = 2 ** self.combo_operand(o)
            if denom == 0:
                raise Exception("Division by zero")
            self.b = self.a // denom
        elif i == 7:
            # cdv: division -> c
            denom = 2 ** self.combo_operand(o)
            if denom == 0:
                raise Exception("Division by zero")
            self.c = self.a // denom
        else:
            raise Exception(f"Unknown opcode: {i}")

        self.iptr += 2
        return True

    def run(self):
        running = True
        while running:
            running = self.step()

        output_str = ",".join(map(str, self.output))
        return output_str

# part 1
computer = ThreeBitComputer(A, B, C, PROGRAM)
print(computer.run()) # 1,5,3,0,2,5,2,5,3
