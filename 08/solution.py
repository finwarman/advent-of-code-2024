#! /usr/bin/env python3

from collections import defaultdict
from itertools import combinations

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

GRID = [list(line) for line in DATA.splitlines()]
WIDTH, HEIGHT = len(GRID[0]), len(GRID)

FREQS = defaultdict(list)

for y in range(HEIGHT):
    for x in range(WIDTH):
        f = GRID[y][x]
        if f != '.':
            FREQS[f].append((x, y)) # in order

def generate_antinodes(all_harmonics=False):
    antinodes = set()
    for antennas in FREQS.values():
        # for each pair of antennas
        for pos_a, pos_b in combinations(antennas, 2):
            dx, dy = (pos_b[0] - pos_a[0]), (pos_b[1] - pos_a[1])

            if all_harmonics:
                limit = min(WIDTH // abs(dx), HEIGHT // abs(dy))

                for mult in range(limit):
                    x, y = node = ((pos_a[0] - (mult*dx)), (pos_a[1] - (mult*dy)))

                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        antinodes.add(node)
                    else:
                        break

                for mult in range(limit):
                    x, y = node = ((pos_b[0] + (mult*dx)), (pos_b[1] + (mult*dy)))

                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        antinodes.add(node)
                    else:
                        break
            else:
                nodes =[
                    ((pos_a[0] - dx), (pos_a[1] - dy)),
                    ((pos_b[0] + dx), (pos_b[1] + dy)),
                ]

                for node in nodes:
                    x, y = node
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        antinodes.add(node)

    return len(antinodes)

# part 1

print(generate_antinodes()) # 280

# part 2

print(generate_antinodes(all_harmonics=True)) # 958
