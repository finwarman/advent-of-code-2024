#! /usr/bin/env python3

from collections import defaultdict

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

GRID = [list(line) for line in DATA.splitlines()]
WIDTH, HEIGHT = len(GRID[0]), len(GRID)

freqs = defaultdict(list)

for y in range(HEIGHT):
    for x in range(WIDTH):
        f = GRID[y][x]
        if f != '.':
            freqs[f].append((x, y))

# part 1

antinodes = set()

for freq in freqs:
    antennas = list(freqs[freq])

    # for each pair of antennas
    for i, ant in enumerate(antennas):
        for j in range(i+1, len(antennas)):
            pos_a, pos_b = antennas[i], antennas[j]

            dx, dy = (pos_b[0] - pos_a[0]), (pos_b[1] - pos_a[1])
            nodes =[
                ((pos_a[0] - dx), (pos_a[1] - dy)),
                ((pos_b[0] + dx), (pos_b[1] + dy)),
            ]

            for node in nodes:
                x, y = node
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    antinodes.add(node)

print(len(antinodes)) # 280

# part 2

antinodes = set()

for freq in freqs:
    antennas = list(freqs[freq])

    # for each pair of antennas
    for i, ant in enumerate(antennas):
        for j in range(i+1, len(antennas)):
            pos_a, pos_b = antennas[i], antennas[j]

            dx, dy = (pos_b[0] - pos_a[0]), (pos_b[1] - pos_a[1])
            nodes =[
                ((pos_a[0] - dx), (pos_a[1] - dy)),
                ((pos_b[0] + dx), (pos_b[1] + dy)),
            ]

            for node in nodes:
                x, y = node
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    antinodes.add(node)


            dx, dy = (pos_b[0] - pos_a[0]), (pos_b[1] - pos_a[1])

            for mult in range(100):
                x, y = node = ((pos_a[0] - (mult*dx)), (pos_a[1] - (mult*dy)))

                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    antinodes.add(node)
                else:
                    break

            for mult in range(100):
                x, y = node = ((pos_b[0] + (mult*dx)), (pos_b[1] + (mult*dy)))

                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    antinodes.add(node)
                else:
                    break

# for node in antinodes:
#     x, y = node
#     GRID[y][x] = '#'

# for row in GRID:
#     print(''.join(row))

print(len(antinodes)) # 958
