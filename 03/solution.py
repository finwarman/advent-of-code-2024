#! /usr/bin/env python3

import re

with open('input.txt', 'r') as file:
    input = file.read().rstrip()

# part 1
# input = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
matches = [m.group() for m in re.finditer(r'mul\(\d{1,3}\,\d{1,3}\)', input)]

total = 0
for match in matches:
    x, y = re.sub(r'[a-z()]', '', match).split(',')
    x, y = int(x), int(y)

    total += x * y

print(total) # 173731097

# part 2
# input = 'xmul(2,4)&mul[3,7]!^don\'t()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'
matches = [m.group() for m in re.finditer(r"do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\)", input)]

do = True
total = 0
for match in matches:
    if match == 'do()':
        do = True
        continue
    if match == 'don\'t()':
        do = False
        continue

    if do:
        x, y = re.sub(r'[a-z()]', '', match).split(',')
        total += int(x) * int(y)

print(total) # 93729253
