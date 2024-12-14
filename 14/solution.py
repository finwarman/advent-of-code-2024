#! /usr/bin/env python3

import re
from statistics import variance

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

def get_robots():
    robots = [] # [(x, y), (dx, dy)]
    for row in FILE.splitlines():
        matches = [m.group() for m in re.finditer(r'\-?\d+', row)]
        x, y, dx, dy = matches
        robots.append([(int(x), int(y)), (int(dx), int(dy))])
    return robots

WIDTH, HEIGHT = 101, 103

SECONDS = 100

robots = get_robots()
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

robots = get_robots()

# find the time t that minimizes variance (dir in {x, y})
def find_min_variance(robots, modulus, dir):
    if dir == 'x':
        return min(
            range(modulus),
            key=lambda t: variance((s + t * v) % modulus for ((s, _), (v, _)) in robots)
        )
    elif dir == 'y':
        return min(
            range(modulus),
            key=lambda t: variance((s + t * v) % modulus for ((_, s), (_, v)) in robots)
        )
    raise ValueError('unknown direction')


# tx, ty are timestamps that minimise variance on each axis
tx = find_min_variance(robots, modulus=WIDTH, dir='x')  # minimise variance for x-coords
ty = find_min_variance(robots, modulus=HEIGHT, dir='y') # minimise variance for y-coords

# apply Chinese Remainder Theorem (CRT) to find the global min t
inverse_W_mod_H = pow(WIDTH, -1, HEIGHT) # modular multiplicative inverse of WIDTH modulo HEIGHT
min_t = tx + ((inverse_W_mod_H * (ty - tx)) % HEIGHT) * WIDTH

print(min_t) # part 2: 8258

# simulate grid at min_t
# positions = [((sx + min_t * vx) % WIDTH, (sy + min_t * vy) % HEIGHT) for ((sx, sy), (vx, vy)) in robots]

# print grid:
# grid = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]
# for x, y in positions:
#     grid[y][x] = '#'
# for row in grid:
#     print("".join(row))
