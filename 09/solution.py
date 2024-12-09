#! /usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()
DATA = list(map(int, FILE.strip()))

# === part 1 === #

# create memory layout, files (by ID) with free space as None
def init_memory(data):
    memory = []
    is_file = True
    file_id = 0
    for size in data:
        if is_file:
            memory.extend([file_id] * size)
            file_id += 1
        else:
            memory.extend([None] * size)
        is_file = not is_file
    return memory

# compact memory to move all files to the start, free spaces to the end
# return checksum
def compact_memory(memory):
    free_ptr = 0
    end_ptr = len(memory) - 1

    while free_ptr < end_ptr:
        # move free_ptr to the first free block
        while free_ptr < len(memory) and memory[free_ptr] is not None:
            free_ptr += 1

        # move end_ptr to the last data block
        while end_ptr >= 0 and memory[end_ptr] is None:
            end_ptr -= 1

        # swap free space with data block
        if free_ptr < end_ptr:
            memory[free_ptr], memory[end_ptr] = memory[end_ptr], memory[free_ptr]

    checksum = sum(i * (block or 0) for i, block in enumerate(memory))
    return checksum

# ============== #

# === part 2 === #

# create file and free block structure,
# alternates between data and free spaces
def parse_filesystem(data):
    data_blocks, free_blocks = [], []

    file_id = 0
    for i in range(0, len(data), 2):
        data_size = data[i]
        free_size = data[i+1] if (i+1 < len(data)) else 0

        data_blocks.append([file_id] * data_size)
        free_blocks.append([[], free_size])
        file_id += 1

    return data_blocks, free_blocks

# mov files into suitable free blocks
def compact_filesystem(data_blocks, free_blocks):
    candidate_id = len(data_blocks)

    while candidate_id > 1:
        candidate_id -= 1
        candidate_data = data_blocks[candidate_id]
        candidate_len = len(candidate_data)

        # find a free block with enough space
        for i in range(candidate_id):
            if free_blocks[i][1] >= candidate_len:
                # move candidate data into the free block
                free_blocks[i][0].extend(candidate_data)
                free_blocks[i][1] -= candidate_len

                # free the original data block
                data_blocks[candidate_id] = [None] * candidate_len
                break


    # calculate checksum
    checksum, position = 0, 0

    for i in range(len(data_blocks)):
        for block in data_blocks[i]:
            checksum += (block or 0) * position
            position += 1

        for block in free_blocks[i][0]:
            checksum += block * position
            position += 1

        position += free_blocks[i][1]

    return checksum

# ============== #

# part 1
memory = init_memory(DATA)
part1_checksum = compact_memory(memory)
print(part1_checksum) # 6398252054886

# part 2
data_blocks, free_blocks = parse_filesystem(DATA)
part2_checksum = compact_filesystem(data_blocks, free_blocks)
print(part2_checksum) # 6415666220005
