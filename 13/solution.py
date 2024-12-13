#! /usr/bin/env python3

import re

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

MACHINES = [] # (A(x,y) B(x,y), P(x,y))

SECTIONS = FILE.split("\n\n")
for section in SECTIONS:
    lines = section.splitlines()
    a, b, p = lines

    a_vals = re.findall(r'X\+(\d+), Y\+(\d+)', a)
    b_vals = re.findall(r'X\+(\d+), Y\+(\d+)', b)
    p_vals = re.findall(r'X=(\d+), Y=(\d+)', p)

    MACHINES.append((
        tuple(map(int, a_vals[0])),
        tuple(map(int, b_vals[0])),
        tuple(map(int, p_vals[0]))
    ))

# solve for min cost, returns None if there is no non-negative integer solution
def find_min_cost(a, b, prize):
    ax, ay = a
    bx, by = b
    px, py = prize

    det = (ax * by) - (ay * bx)
    if det == 0:
        return None # no unique solution

    # get nA and nB (Cramer's Rule)
    nA_num = (px * by) - (py * bx)
    nB_num = (ax * py) - (ay * px)

    # adjust signs if determinant is negative
    if det < 0:
        det = -det
        nA_num = -nA_num
        nB_num = -nB_num

    # ensure nA and nB are integers (i.e. int solution exists)
    if nA_num % det != 0 or nB_num % det != 0:
        return None

    nA = nA_num // det
    nB = nB_num // det

    # negative presses are invalid
    if nA < 0 or nB < 0:
        return None

    total_cost = 3 * nA + 1 * nB
    return total_cost

# part 1 and 2:
for adj in [0, 10000000000000]:
    total_min_cost = 0
    for idx, machine in enumerate(MACHINES, 1):
        a, b, p = machine
        p_adj = (p[0] + adj, p[1] + adj)
        min_cost = find_min_cost(a, b, p_adj)
        if min_cost is not None:
            total_min_cost += min_cost

    print(total_min_cost)
    # part 1: 32041
    # part 2: 95843948914827
