#! /usr/bin/env python3

from collections import defaultdict
from itertools import combinations

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

GRID = [list(line) for line in DATA.splitlines()]
WIDTH, HEIGHT = len(GRID[0]), len(GRID) # square

FREQS = defaultdict(list)

for y in range(HEIGHT):
    for x in range(WIDTH):
        freq = GRID[y][x]
        if freq != '.':
            FREQS[freq].append((x, y)) # in order

def generate_antinodes(all_harmonics=False):
    antinodes = set()
    for antennas in FREQS.values():
        # for each pair of antennas
        for pos_a, pos_b in combinations(antennas, 2):
            dx, dy = (pos_b[0] - pos_a[0]), (pos_b[1] - pos_a[1])

            start, limit = 1, 1 # first only
            if all_harmonics:
                start, limit = 0, (WIDTH // abs(dx))

            for mult in range(start, limit+1):
                node = ((pos_a[0] - (mult*dx)), (pos_a[1] - (mult*dy)))
                if 0 <= node[0] < WIDTH and 0 <= node[1] < HEIGHT:
                    antinodes.add(node)
                else:
                    break

            for mult in range(start, limit+1):
                node = ((pos_b[0] + (mult*dx)), (pos_b[1] + (mult*dy)))
                if 0 <= node[0] < WIDTH and 0 <= node[1] < HEIGHT:
                    antinodes.add(node)
                else:
                    break
    return len(antinodes)

# part 1

print(generate_antinodes()) # 280

# part 2

print(generate_antinodes(all_harmonics=True)) # 958
