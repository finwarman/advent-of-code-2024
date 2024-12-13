#! /usr/bin/env python3

import re

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

# FILE = '''
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279
# '''.strip()

MACHINES = [] # A(x,y) B(x,y), P(x,y)

SECTIONS = FILE.split("\n\n")
for section in SECTIONS:
    lines = section.splitlines()
    if len(lines) != 3:
        continue  # Skip invalid sections
    a, b, p = lines

    # Extract numbers using regex
    a_vals = re.findall(r'X\+(\d+), Y\+(\d+)', a)
    b_vals = re.findall(r'X\+(\d+), Y\+(\d+)', b)
    p_vals = re.findall(r'X=(\d+), Y=(\d+)', p)

    if not a_vals or not b_vals or not p_vals:
        continue  # Skip if any part is missing

    ax, ay = map(int, a_vals[0])
    bx, by = map(int, b_vals[0])
    px, py = map(int, p_vals[0])

    MACHINES.append(
        [(ax, ay), (bx, by), (px, py)]
    )

def find_min_cost(a, b, prize):
    ax, ay = a
    bx, by = b
    px, py = prize

    min_cost = None

    # every possible number of presses for A
    max_a_presses = px // ax if ax != 0 else 0
    for nA in range(max_a_presses + 1):
        # remaining X and Y after pressing A nA times
        remaining_x = px - ax * nA
        remaining_y = py - ay * nA

        if remaining_x < 0 or remaining_y < 0:
            continue

        # Check if Button B can cover the remaining X and Y
        # We need to solve:
        # nB * bx = remaining_x
        # nB * by = remaining_y
        # for both to hold, 'remaining_x / bx' must equal 'remaining_y / by'

        if bx == 0 or by == 0 \
            or remaining_x % bx != 0 or remaining_y % by != 0:
            continue

        nB_x = remaining_x // bx
        nB_y = remaining_y // by
        if nB_x != nB_y or nB_x < 0:
            continue

        nB = nB_x

        # total cost
        total_cost = 3 * nA + 1 * nB

        # update min_cost if this is better
        if (min_cost is None) or (total_cost < min_cost):
            min_cost = total_cost

    return min_cost

total_min_cost = 0

for idx, machine in enumerate(MACHINES, 1):
    a, b, p = machine
    min_cost = find_min_cost(a, b, p)
    if min_cost is not None:
        total_min_cost += min_cost
    # otherwise, impossible

# part 1:
print(total_min_cost) # 32041
