#! /usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

# FILE = '''
# ##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########

# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
# '''

# FILE='''
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^'''

map, moves = FILE.strip().split('\n\n')

MOVES = moves.replace('\n', '')

MAP = [list(row) for row in map.strip().splitlines()]
WIDTH, HEIGHT = len(MAP[0]), len(MAP) # square

idx = map.replace('\n', '').index('@')
x, y = start_pos = (idx % WIDTH, idx // WIDTH)

# for row in MAP:
#     print(''.join(row))

# def is_within_bounds(x, y):
#     return 0 <= x < WIDTH and 0 <= y < HEIGHT

def can_push_group(pos, dx, dy):
    """recursively check if a group of boxes can be pushed."""
    x, y = pos
    nx, ny = x + dx, y + dy

    if MAP[ny][nx] == '#':
        return False  # blocked by a wall / out of bounds

    if MAP[ny][nx] == '.':
        return True # found empty spot to push into

    if MAP[ny][nx] == 'O':
        # check if the next box in the line can be pushed
        return can_push_group((nx, ny), dx, dy)

    return False # blocked by other objects

def push_group(pos, dx, dy):
    """push a group of boxes, if possible."""
    x, y = pos
    nx, ny = x + dx, y + dy

    if MAP[ny][nx] == 'O':
        push_group((nx, ny), dx, dy) # recursively push the next box

    # Move this box to the next position
    MAP[ny][nx] = 'O'
    MAP[y][x] = '.'

MAP[y][x] = '.'

pos = start_pos
for move in MOVES:
    x, y = pos

    MAP[y][x] = '.'

    dx, dy = 0, 0
    if move == '<':
        dx, dy = -1, 0
    elif move == '>':
        dx, dy = 1, 0
    elif move == '^':
        dx, dy = 0, -1
    elif move == 'v':
        dx, dy = 0, 1

    nx, ny = x + dx, y + dy
    next_char = MAP[ny][nx]

    if next_char == '#':
        pos = x, y
    elif next_char == '.':
        pos = nx, ny
    elif next_char == 'O':
        if can_push_group((nx, ny), dx, dy):
            push_group((nx, ny), dx, dy) # push all boxes in the group
            pos = nx, ny

    MAP[pos[1]][pos[0]] = '@'

    # print(move)
    # for row in MAP:
    #     print(''.join(row))
    # print()

gps_sum = 0
for y, row in enumerate(MAP):
    for x, char in enumerate(row):
        if char == 'O':
            gps_sum += 100 * y + x

# debug: Print the final map
for row in MAP:
    print(''.join(row))

print("part 1:", gps_sum) # 1463512
