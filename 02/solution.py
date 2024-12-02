#! /usr/bin/env python3

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from util import get_input_data

# ==== INPUT ====

data = get_input_data()
rows = [[int(x) for x in row.split()] for row in data.split('\n')[:-1] if row]

# ==== SOLUTION ====

# part 1:

# report is safe only if:
# - all levels are all increasing or decreasing
# - adjacentlvels differ by at least one and at most three

safe_count = 0
for report in rows:
    safe = True
    last_sign = None
    for i in range(len(report) - 1):
        x, y = report[i], report[i+1]
        diff = abs(x - y)
        sign = 1 if (x - y >= 0) else -1

        if (diff < 1 or diff > 3) or (last_sign and last_sign != sign):
            safe = False
            break
        last_sign = sign

    if safe:
        safe_count += 1

print("part 1:", safe_count) # 356


# part 2:

# tolerate a single bad level

def generate_report_variations(report):
    yield report
    for i in range(len(report)):
        yield report[:i] + report[i+1:] # 1 char removed

safe_count = 0
for report in rows:
    for report in generate_report_variations(report):
        safe = True
        last_sign = None
        for i in range(len(report) - 1):
            x, y = report[i], report[i+1]
            diff = abs(x - y)
            sign = 1 if (x - y >= 0) else -1

            if (diff < 1 or diff > 3) or (last_sign and last_sign != sign):
                safe = False
                break
            last_sign = sign

        if safe:
            safe_count += 1
            break

print("part 2:", safe_count) # 413
