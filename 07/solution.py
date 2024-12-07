#! /usr/bin/env python3

from multiprocessing import Pool

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

ROWS = [list(map(int, line.replace(':', '').split(' '))) for line in DATA.splitlines()]
ROWS = [(line[0], line[1:]) for line in ROWS] # (total, operands)

# evaluates left-to-right, checking each operator configuration
def process_equation(target, current_sum, operands, idx, allow_concat=False):
    if current_sum > target:
        return 0
    if idx >= len(operands) - 1:
        return target if current_sum == target else 0

    result = 0
    if process_equation(target, current_sum + operands[idx+1], operands, idx + 1, allow_concat):
        result = target
    elif process_equation(target, current_sum * operands[idx+1], operands, idx + 1, allow_concat):
        result = target
    elif allow_concat:
        concat_value = int(str(current_sum) + str(operands[idx+1]))
        result = process_equation(target, concat_value, operands, idx + 1, allow_concat)

    return result

def get_total(allow_concat=False):
    with Pool() as pool:
        return sum(pool.starmap(process_equation, [
            (total, operands[0], operands, 0, allow_concat)
            for total, operands in ROWS
        ]))

# entry point, to allow multiprocessing
if __name__ == "__main__":
    print(get_total())       # 1708857123053
    print(get_total(True))   # 189207836795655
