#! /usr/bin/env python3

from collections import defaultdict

def count_stones(data, iterations):
    # initialise frequencies of stones
    stone_freq = defaultdict(int)
    for stone in data:
        stone_freq[stone] += 1

    # process stones by tracking unique states + counts
    for _ in range(iterations):
        new_freq = defaultdict(int)
        for stone, count in stone_freq.items():
            if stone == 0:
                # replace 0 with 1
                new_freq[1] += count
            else:
                # calculate number of digits
                num_digits = len(str(stone))
                if num_digits % 2 == 0:
                    # split into two stones
                    half = num_digits // 2
                    left = stone // (10 ** half)
                    right = stone % (10 ** half)
                    new_freq[left] += count
                    new_freq[right] += count
                else:
                    # multiply by 2024
                    new_freq[stone * 2024] += count
        stone_freq = new_freq

    return sum(stone_freq.values())

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

data = list(map(int, FILE.split()))

# part 1: 25 iterations
print(count_stones(data, 25)) # 197157

# part 2: 75 iterations
print(count_stones(data, 75)) # 234430066982597
