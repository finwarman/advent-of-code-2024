#! /usr/bin/env python3

import re
from statistics import variance

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

ROBOTS = [] # [(x, y), (dx, dy)]
for row in FILE.splitlines():
    matches = [m.group() for m in re.finditer(r'\-?\d+', row)]
    x, y, dx, dy = matches
    ROBOTS.append([(int(x), int(y)), (int(dx), int(dy))])

WIDTH, HEIGHT = 101, 103
SECONDS = 100

# simulate grid at t = 100
positions = [((sx + SECONDS * vx) % WIDTH, (sy + SECONDS * vy) % HEIGHT)
             for ((sx, sy), (vx, vy)) in ROBOTS]

quadrants = [0, 0, 0, 0]

for x, y in positions:
    if x < WIDTH // 2 and y < HEIGHT // 2:
        quadrants[0] += 1  # top-left
    elif x >= (WIDTH // 2) + 1 and y < HEIGHT // 2:
        quadrants[1] += 1  # top-right
    elif x < WIDTH // 2 and y >= (HEIGHT // 2) + 1:
        quadrants[2] += 1  # bottom-left
    elif x >= (WIDTH // 2) + 1 and y >= (HEIGHT // 2) + 1:
        quadrants[3] += 1  # bottom-right

total = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
print(total) # part 1: 228410028

# find the time t that minimizes variance (dir in {x, y})
def find_min_variance(robots, modulus, dir):
    axis = [(p, v) for ((p, _), (v, _)) in robots] if dir == 'x' else \
           [(p, v) for ((_, p), (_, v)) in robots]

    return min(
        range(modulus),
        key=lambda t: variance((p + t * v) % modulus for (p, v) in axis)
    )

# tx, ty are timestamps that minimise variance on each axis
tx = find_min_variance(ROBOTS, modulus=WIDTH, dir='x')  # minimise variance for x-coords
ty = find_min_variance(ROBOTS, modulus=HEIGHT, dir='y') # minimise variance for y-coords

# apply chinese remainder theorem (CRT) to find the global min t
inverse_W_mod_H = pow(WIDTH, -1, HEIGHT) # modular multiplicative inverse of WIDTH modulo HEIGHT
min_t = tx + ((inverse_W_mod_H * (ty - tx)) % HEIGHT) * WIDTH

print(min_t) # part 2: 8258

# ...................................
# ..###############################..
# ..#.............................#..
# ..#.............................#.#
# ..#.............................#..
# ..#.............................#..
# #.#..............#..............#..
# ..#.............###.............#..
# ..#............#####............#..
# ..#...........#######...........#..
# ..#..........#########..........#..
# ..#............#####............#..
# ..#...........#######...........#..
# ..#..........#########..........#..
# ..#.........###########.........#..
# ..#........#############........#..
# ..#..........#########..........#..
# ..#.........###########.........#..
# ..#........#############........#..
# ..#.......###############.......#.#
# ..#......#################......#..
# ..#........#############........#..
# ..#.......###############.......#..
# ..#......#################......#..
# ..#.....###################.....#..
# ..#....#####################....#..
# ..#.............###.............#..
# ..#.............###.............#..
# ..#.............###.............#..
# ..#.............................#..
# ..#.............................#..
# ..#.............................#..
# ..#.............................#..
# ..###############################..
# ...................................
