#! /usr/bin/env python3

import re

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

robots = [] # [(x, y), (dx, dy)]
for row in FILE.splitlines():
    matches = [m.group() for m in re.finditer(r'\-?\d+', row)]
    x, y, dx, dy = matches
    robots.append([(int(x), int(y)), (int(dx), int(dy))])

WIDTH, HEIGHT = 101, 103
SECONDS = 100

for _ in range(SECONDS):
    for robot in robots:
        pos, vel = robot
        nx = (pos[0] + vel[0]) % WIDTH
        ny = (pos[1] + vel[1]) % HEIGHT
        robot[0] = (nx, ny)

quadrants = [0, 0, 0, 0]

for robot in robots:
    pos, _ = robot
    x, y = pos

    if x < WIDTH // 2 and y < HEIGHT // 2:
        quadrants[0] += 1  # Top-left
    elif x >= (WIDTH // 2) + 1 and y < HEIGHT // 2:
        quadrants[1] += 1  # Top-right
    elif x < WIDTH // 2 and y >= (HEIGHT // 2) + 1:
        quadrants[2] += 1  # Bottom-left
    elif x >= (WIDTH // 2) + 1 and y >= (HEIGHT // 2) + 1:
        quadrants[3] += 1  # Bottom-right

total = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

print(total) # part 1: 228410028
