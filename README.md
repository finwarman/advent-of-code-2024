conda activate aoc

Use .env or set PYTHONPATH=. to import util in scripts.

## Benchmarks

| Day   | Filename        | `time python3 "$filename"`    | total  | sub `0.5s` |
| ----- | --------------- | ----------------------------- | ------ | -------- |
| -     | -               | `user` `system` `cpu` `total` | -      | - |
| 01    | 01/solution.py  | `0.04s` `0.02s` `85%` `0.063` | 0.06s  | ✔️ |
| 02    | 02/solution.py  | `0.05s` `0.01s` `87%` `0.068` | 0.07s  | ✔️ |
| 03    | 03/solution.py  | `0.03s` `0.01s` `87%` `0.043` | 0.04s  | ✔️ |
| 04    | 04/solution.py  | `0.09s` `0.01s` `95%` `0.103` | 0.10s  | ✔️ |
| 05    | 05/solution.py  | `0.04s` `0.01s` `76%` `0.069` | 0.07s  | ✔️ |
| 06   | 06/solution.py | `0.32s` `0.01s` `98%` `0.334` | 0.33s  | ✔️ |
| 07    | 07/solution.py  | `0.04s` `0.01s` `87%` `0.054` | 0.05s  | ✔️ |
| 08    | 08/solution.py  | `0.02s` `0.01s` `85%` `0.032` |  0.03s  | ✔️ |
| 01    | 09/solution.py  | `8.51s` `0.04s` `99%` `8.570` | 8.57s  | ❌ |
| 02    | 10/solution.py  ||
| 03    | 11/solution.py  ||

#### Specs
```
2.3 GHz 8-Core Intel Core i9
16 GB 2667 MHz DDR4
MacOS
Python 3.13
```
