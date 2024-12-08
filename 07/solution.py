#! /usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

ROWS = [list(map(int, line.replace(':', '').split(' '))) for line in DATA.splitlines()]
ROWS = [(line[0], line[1:]) for line in ROWS] # (total, operands)

# check if target value can be obtained by reversing operations from operand list
# works from right-to-left (since everything is applied left-to-right)
def reverse_operations(target, operands, allow_concat=False):
    if not operands:
        return target == 0 # valid if we reached 0 after reversing all operations

    current_operand, remaining_operands = operands[-1], operands[:-1]

    # undo add
    if target >= current_operand: # ensure non-negative after substraction
        if reverse_operations(target - current_operand, remaining_operands, allow_concat):
            return True

    # undo multiply
    if current_operand != 0 and \
        target % current_operand == 0: # ensure integer & no remainder after division ()
        if reverse_operations(target // current_operand, remaining_operands, allow_concat):
            return True

    # undo concatenation (if allowed):
    # check if concat of current operand with preceding number could have formed the target.
    if allow_concat:
        power = 10 ** len(str(current_operand)) # check if target ends with current_operand (modulo)
        if target % power == current_operand:
            new_target = target // power # remove the concatenated part (integer division)
            if reverse_operations(new_target, remaining_operands, allow_concat):
                return True

    # no valid operations can undo the target, return False.
    return False


def get_total_opt(allow_concat=False):
    return sum(
        (total if reverse_operations(total, operands, allow_concat) else 0)
        for total, operands in ROWS
    )

if __name__ == "__main__":
    print(get_total_opt())     # 1708857123053
    print(get_total_opt(True)) # 189207836795655
