#! /usr/bin/env python3

from itertools import chain


with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

EMPTY = -1
DATA = list(DATA.strip())

filesystem = []

total_data = 0

free_spaces = []
data_spaces = []

is_data = True
id = 0
end_ptr = 0
for x in DATA:
    x = int(x)

    if is_data:
        for i in range(x):
            filesystem.append(id)
            data_spaces.append(end_ptr)
            end_ptr += 1
        id += 1
        total_data += x
    else:
        for i in range(x):
            filesystem.append(EMPTY)
            free_spaces.append(end_ptr)
            end_ptr += 1

    is_data = not is_data

free_ptr = int(DATA[0])


# swap full spaces into empty ones
while len(free_spaces) > 1:
    if free_spaces:
        free_ptr = free_spaces.pop(0)
    end_ptr = data_spaces.pop()

    if end_ptr < total_data:
        break

    filesystem[free_ptr] = filesystem[end_ptr]
    filesystem[end_ptr] = EMPTY

# calculate checksum
checksum = 0

for i in range(total_data):
    data = filesystem[i]
    assert data != EMPTY

    checksum += i*data

# part 1

print(checksum) # 6398252054886

# part 2

# disk: [0, 1, 2]
# [file_id, data_blocks, free_blocks]

def parse_filesystem(data):
    numbers = [int(x) for x in data]
    disks = []
    for i in range(0, len(numbers), 2):
        data_blocks = numbers[i]
        free_blocks = numbers[i + 1] if i + 1 < len(numbers) else 0
        disks.append([i // 2, data_blocks, free_blocks])
    return disks

def compact_filesystem(disks):
    ptr = len(disks) - 1

    while ptr > 0:
        current_idx = ptr

        # find free spaces with enough capacity for current file
        suitable_free_spaces = [
            idx for idx, disk in enumerate(disks[:current_idx]) if disk[2] >= disks[current_idx][1]
        ]

        if not suitable_free_spaces:
            ptr -= 1
            continue

        # remove the current file and reallocate its blocks
        current_disk = disks.pop(current_idx)

        # add unused space to the previous disk
        disks[current_idx - 1][2] += current_disk[1] + current_disk[2]

        # allocate file into the first suitable free space
        target_idx = suitable_free_spaces[0]
        blocks_to_move = current_disk[1]
        disks.insert(
            target_idx + 1,
            [current_disk[0], blocks_to_move, disks[target_idx][2] - blocks_to_move]
        )

        # mark free space as used
        disks[target_idx][2] = 0

    return disks

def calculate_checksum(disks):
    # flatten files into a block list
    block_list = list(chain.from_iterable(
        [disk[0]] * disk[1] + [0] * disk[2] for disk in disks
    ))
    return sum(index * block for index, block in enumerate(block_list))


# Input parsing
# DATA = '2333133121414131402'  # Example input

# Initialize filesystem and compact
disks = parse_filesystem(DATA)
disks = compact_filesystem(disks)

# calculate checksum - part 2
print(calculate_checksum(disks)) # 6415666220005
