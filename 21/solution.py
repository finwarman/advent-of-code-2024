#! /usr/bin/env python3

from functools import cache

with open('input.txt', 'r') as f:
    FILE = f.read()

FILE = '''
029A
980A
179A
456A
379A'''

CODES = [x.strip() for x in FILE.strip().splitlines()]

'''
  0   1   2   (<x, y)
+---+---+---+
| 7 | 8 | 9 |  0
+---+---+---+
| 4 | 5 | 6 |  1
+---+---+---+
| 1 | 2 | 3 |  2
+---+---+---+
    | 0 | A |  3
    +---+---+

  0   1   2
    +---+---+
    | ^ | A |  0
+---+---+---+
| < | v | > |  1
+---+---+---+
'''

# KEYPAD #
KEYPAD_TO_POS = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
                 '0': (1, 3), 'A': (2, 3),
}
KEYPAD_VALID_POS = set(KEYPAD_TO_POS.values())
KEYPAD_GAP = (0, 3) # x, y
##########

# ARROWPAD #
ARROWPAD_TO_POS = {
                 '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1),
}
ARROWPAD_VALID_POS = set(ARROWPAD_TO_POS.values())
ARROWPAD_GAP = (0, 0) # x, y
############

def shortest_keypad_path(start, end, gap, valid_positions):
    if start == end:
        return ''

    x, y = start
    gx, gy = end

    dx = 1 if gx - x > 0 else (-1 if gx - x < 0 else 0)
    dy = 1 if gy - y > 0 else (-1 if gy - y < 0 else 0)

    seq = ''

    horizontal_first = True
    if (y == gap[1] and dy < 0) or (x == gap[0] and dx < 0):
        horizontal_first = False

    if horizontal_first:
        while (x, y) != (gx, gy):
            if x != gx:
                x += dx
                seq += ('>' if dx > 0 else '<')
            elif y != gy:
                y += dy
                seq += ('v' if dy > 0 else '^')
    else:
        while (x, y) != (gx, gy):
            if y != gy:
                y += dy
                seq += ('v' if dy > 0 else '^')
            elif x != gx:
                x += dx
                seq += ('>' if dx > 0 else '<')
    return seq


def keypad_seq(start, code, pos_map, gap, valid_positions):
    final_seq = ''
    current_position = start
    for c in code:
        end_position = pos_map[c]
        moves = shortest_keypad_path(current_position, end_position, gap, valid_positions)
        final_seq += moves + 'A'
        current_position = end_position
    return final_seq


total = 0
for code in CODES:
    # keypad sequence to type the numeric code
    numpad_seq = keypad_seq(
        start=KEYPAD_TO_POS['A'],
        code=code,
        pos_map=KEYPAD_TO_POS,
        gap=KEYPAD_GAP,
        valid_positions=KEYPAD_VALID_POS
    )

    # first robot's keypad sequence to type the numpad sequence
    robot1_seq = keypad_seq(
        start=ARROWPAD_TO_POS['A'],
        code=numpad_seq,
        pos_map=ARROWPAD_TO_POS,
        gap=ARROWPAD_GAP,
        valid_positions=ARROWPAD_VALID_POS
    )

    # second robot's keypad sequence to type the robot1 sequence
    robot2_seq = keypad_seq(
        start=ARROWPAD_TO_POS['A'],
        code=robot1_seq,
        pos_map=ARROWPAD_TO_POS,
        gap=ARROWPAD_GAP,
        valid_positions=ARROWPAD_VALID_POS
    )

    print(code)
    print(robot2_seq) # final robot sequence
    print(robot1_seq) # middle robot sequence
    print(numpad_seq) # our input to middle robot

    # Calculate complexity
    numeric = int(''.join(c for c in code if c.isdigit()))
    complexity = len(robot2_seq) * numeric

    print(f"{len(robot2_seq)} * {numeric} = {complexity}\n")
    total += complexity

print("Total complexity:", total)


# 261392 - too high
