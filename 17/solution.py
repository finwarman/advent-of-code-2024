#! /usr/bin/env python3

from time import sleep

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

print(A)
print(B)
print(C)

print(PROGRAM)

def combo_operand(value):
    if 0 <= value <= 3:
        return value
    if value == 4:
        return A
    if value == 5:
        return B
    if value == 6:
        return C
    raise Exception(f"Bad combo operand: {value}")

def step():
    global IPTR, A, B, C, PROGRAM

    if IPTR+1 >= len(PROGRAM):
        return False

    i = PROGRAM[IPTR]
    o = PROGRAM[IPTR+1]

    if i == 0:
        # adv: division -> a
        denom = 2 ** combo_operand(o)
        A = A // denom
    elif i == 1:
        # bxl: B XOR o
        B = B ^ o
    elif i == 2:
        # bst: mod 8 (lowest 3 bits)
        B = combo_operand(o) % 8
    elif i == 3:
        # jnz: jump if A is not zero
        if A != 0:
            IPTR = o
            return True
    elif i == 4:
        # bxc: B XOR C
        B = B ^ C
        # ignores operand, but reads it
    elif i == 5:
        # out: combo mod 8
        print(f"{combo_operand(o) % 8}", end=",")
    elif i == 6:
        # bdv: division -> b
        denom = 2 ** combo_operand(o)
        B = A // denom
    elif i == 7:
        # cdv: division -> c
        denom = 2 ** combo_operand(o)
        C = A // denom

    IPTR += 2
    return True

running = True
while running:
    running = step()

# backspace and newline
print('\b ', end="", flush=True)
print()

# part 1: 1,5,3,0,2,5,2,5,3
