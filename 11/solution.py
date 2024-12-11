#! /usr/bin/env python3

import llist
from llist import sllist,sllistnode

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

# FILE = '125 17'

DATA = list(map(int, FILE.strip().split()))

stones = sllist(DATA)

# print(stones)

# if stone is 0, it is replaced by a stone engraved with the number 1.
# if the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
#  - the left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone.
#  - (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# if none of the other rules apply, the stone is replaced by a new stone;
#  - the old stone's number multiplied by 2024 is engraved on the new stone.


def process_stones(iterations):
    sstones = sllist(DATA)

    for _ in range(iterations):
        node = stones.first
        while node is not None:
            current = node.value
            # print(current, end=" ")

            if current == 0:
                # Replace 0 with 1
                node.value = 1
                node = node.next  # Move to the next node

            elif len(str(current)) % 2 == 0:
                # Split the number with even digits
                digits = str(current)
                mid = len(digits) // 2

                # Calculate left and right halves
                left_half = int(digits[:mid])
                right_half = int(digits[mid:])

                # Replace current node's value with left_half
                node.value = left_half

                # Insert the right_half after the current node
                right_node = stones.insertafter(right_half, node)

                # Move to the right node (newly inserted)
                node = right_node.next

            else:
                # Multiply the stone's number by 2024
                node.value = current * 2024
                node = node.next  # Move to the next node

    return len(stones)

# for current in stones:
#     print(current, end=" ")
# print()

# part 1
print(process_stones(25)) # 197157

# part 2
print(process_stones(75))
