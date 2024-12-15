#! /usr/bin/env python3

from collections import defaultdict

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

### PART 2

map, moves = FILE.strip().split('\n\n')

MOVES = moves.replace('\n', '')

MAP = [list(row) for row in map.strip().splitlines()]
WIDTH, HEIGHT = len(MAP[0]), len(MAP) # square

idx = map.replace('\n', '').index('@')
x, y = start_pos = (idx % WIDTH, idx // WIDTH)

# double map

NEW_MAP = [['.' for _ in range(WIDTH * 2)] for _ in range(HEIGHT)]

for y, row in enumerate(MAP):
    for x, char in enumerate(row):
        j = x * 2
        if char == '#':
            NEW_MAP[y][j] = '#'
            NEW_MAP[y][j+1] = '#'
        elif char == 'O':
            NEW_MAP[y][j] = '['
            NEW_MAP[y][j+1] = ']'

MAP = NEW_MAP
WIDTH = WIDTH * 2

x, y = start_pos = (start_pos[0] * 2, start_pos[1])

MAP[y][x] = '.'

def handle_push(grid, robot, direction, walls, boxes, box_to_squares):
    """Handle the robot push logic with BFS to resolve connected boxes."""
    dx, dy = direction
    moved_boxes = set()
    should_move = True
    q = [robot]
    seen = set()

    # collect all affected boxes
    while q:
        current = q.pop()
        current = (current[0] + dx, current[1] + dy)
        if current in seen:
            continue
        seen.add(current)
        if current in walls:
            should_move = False
            break
        elif current in boxes:
            squares = box_to_squares[current]
            moved_boxes.update(squares)
            q.extend(squares)

    if not should_move:
        return robot, boxes, box_to_squares # no movement

    # update box positions
    removed = set()
    added = set()
    new_box_to_squares = {}
    for box in moved_boxes:
        squares = box_to_squares[box]
        removed.update(squares)
        new_squares = {(b[0] + dx, b[1] + dy) for b in squares}
        added.update(new_squares)
        for new_square in new_squares:
            new_box_to_squares[new_square] = new_squares

    for b in removed:
        boxes.remove(b)
        del box_to_squares[b]
    for b in added:
        boxes.add(b)
        box_to_squares[b] = new_box_to_squares[b]

    # Move the robot
    robot = (robot[0] + dx, robot[1] + dy)
    return robot, boxes, box_to_squares

def solve(grid, instructions):
    robot = start_pos
    boxes = set()
    box_to_squares = defaultdict(set)
    walls = set()

    # Parse the grid
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            # if c == "@":
            #     robot = (x, y)
            if c == "[":
                boxes.add((x, y))
                boxes.add((x + 1, y))
                squares = {(x, y), (x + 1, y)}
                box_to_squares[(x, y)] = squares
                box_to_squares[(x + 1, y)] = squares
            elif c == "#":
                walls.add((x, y))

    instruction_to_d = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}

    for instruction in instructions:
        direction = instruction_to_d[instruction]
        robot, boxes, box_to_squares = handle_push(grid, robot, direction, walls, boxes, box_to_squares)

    top_lefts = set()
    for squares in box_to_squares.values():
        top_left = sorted(squares)[0]
        top_lefts.add(top_left)
    return sum(b[0] + b[1] * 100 for b in top_lefts)

print(solve(MAP, MOVES)) # 1486520
