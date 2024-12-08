conda activate aoc
Use .env or set PYTHONPATH=. to import util in scripts.

## Benchmarks

| Day   | Filename        | `time python3 "$filename"`    | sub `0.5s` |
| ----- | --------------- | ----------------------------- | -------- |
| -     | -               | `user` `system` `cpu` `total` | - |
| 01    | 01/solution.py  | `0.04s` `0.02s` `85%` `0.063` | ✔️ |
| 02    | 02/solution.py  | `0.05s` `0.01s` `87%` `0.068` | ✔️ |
| 03    | 03/solution.py  | `0.03s` `0.01s` `87%` `0.043` | ✔️ |
| 04    | 04/solution.py  | `0.09s` `0.01s` `95%` `0.103` | ✔️ |
| 05    | 05/solution.py  | `0.04s` `0.01s` `76%` `0.069` | ✔️ |
| 06    | ~~06/solution.py~~  | `18.82s` `0.74s` `1346%` `1.453` | ❌ |
|  ->   | 06/solution_opt.py | `0.32s` `0.01s` `98%` `0.334` | ✔️ |
| 07    | 07/solution.py  | `5.88s` `1.18s` `1031%` `0.684` | ❌ |
| 08    | 08/solution.py  | `0.02s` `0.01s` `85%` `0.032` | ✔️ |
| 01    | 09/solution.py  ||
| 02    | 10/solution.py  ||
| 03    | 11/solution.py  ||

#### Specs
```
2.3 GHz 8-Core Intel Core i9
16 GB 2667 MHz DDR4
MacOS
Python 3.13
```
