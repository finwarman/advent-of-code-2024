#! /usr/bin/env python3

from itertools import chain


with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

# DATA = '12345'
# DATA = '2333133121414131402'

# input = disk map
# layout of files and free space on disk

# checksum = sum of index * file id

EMPTY = '.'

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

# print(free_ptr)
# print(end_ptr)
# print(total_data)
# print(filesystem)
# print()

while len(free_spaces) > 1:
    # print(''.join(str(x) for x in filesystem))

    if free_spaces:
        free_ptr = free_spaces.pop(0)
    end_ptr = data_spaces.pop()

    if end_ptr < total_data:
        break

    filesystem[free_ptr] = filesystem[end_ptr]
    filesystem[end_ptr] = EMPTY

# print()
# print(end_ptr)
# print(free_ptr)
# print(total_data)
# print()
# print(''.join(str(x) for x in filesystem))


checksum = 0

for i in range(total_data):
    data = filesystem[i]
    assert data != EMPTY

    checksum += i*data

# part 1

print(checksum) # 6398252054886

# TODO: keep track of spans
# part 2


class Disk:
    def __init__(self, file_id, data_blocks, free_blocks):
        self.file_id = file_id
        self.data_blocks = data_blocks
        self.free_blocks = free_blocks

def parse_filesystem(data):
    numbers = [int(x) for x in data]
    disks = []
    for i in range(0, len(numbers), 2):
        data_blocks = numbers[i]
        free_blocks = numbers[i + 1] if i + 1 < len(numbers) else 0
        disks.append(Disk(i // 2, data_blocks, free_blocks))
    return disks

def compact_filesystem(disks):
    ptr = len(disks) - 1

    while ptr > 0:
        current_idx = ptr

        # find free spaces with enough capacity for current file
        suitable_free_spaces = [
            idx for idx, disk in enumerate(disks[:current_idx]) if disk.free_blocks >= disks[current_idx].data_blocks
        ]

        if not suitable_free_spaces:
            ptr -= 1
            continue

        # remove the current file and reallocate its blocks
        current_disk = disks.pop(current_idx)

        # add unused space to the previous disk
        disks[current_idx - 1].free_blocks += current_disk.data_blocks + current_disk.free_blocks

        # allocate file into the first suitable free space
        target_idx = suitable_free_spaces[0]
        blocks_to_move = current_disk.data_blocks
        disks.insert(
            target_idx + 1,
            Disk(current_disk.file_id, blocks_to_move, disks[target_idx].free_blocks - blocks_to_move)
        )

        # mark free space as used
        disks[target_idx].free_blocks = 0

    return disks

def calculate_checksum(disks):
    # flatten files into a block list
    block_list = list(chain.from_iterable(
        [disk.file_id] * disk.data_blocks + [0] * disk.free_blocks for disk in disks
    ))
    return sum(index * block for index, block in enumerate(block_list))


# Input parsing
# DATA = '2333133121414131402'  # Example input

# Initialize filesystem and compact
disks = parse_filesystem(DATA)
disks = compact_filesystem(disks)

# calculate checksum - part 2
print(calculate_checksum(disks)) # 6415666220005
