#! /usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().rstrip()

ROWS = DATA.strip().splitlines()
ROWS = [list(map(int, line.replace(':', '').split(' '))) for line in ROWS]

# evaluates left-to-right, checking each operator configuration
def eval_branch(target, current_sum, operands, idx, allow_concat=False):
    if current_sum > target:
        return 0
    if idx >= len(operands) - 1 and current_sum != target:
        return 0
    if idx == len(operands) - 1 and current_sum == target:
        return target

    if eval_branch(target, current_sum + operands[idx+1], operands, idx + 1, allow_concat):
        return target
    elif eval_branch(target, current_sum * operands[idx+1], operands, idx + 1, allow_concat):
        return target
    elif allow_concat and eval_branch(target, int(str(current_sum) + str(operands[idx+1])), operands, idx + 1, allow_concat):
        return target
    return 0

def get_total(allow_concat=False):
    total_valid = 0

    for equation in ROWS:
        total, operands = equation[0], equation[1:]
        total_valid += eval_branch(total, operands[0], operands, 0, allow_concat)

    return total_valid

print(get_total()) # 1708857123053

print(get_total(True)) # 189207836795655
