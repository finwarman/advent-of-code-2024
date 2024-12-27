#! /usr/bin/env python3

with open('input.txt', 'r') as f:
    FILE = f.read()

def main():
    gates_str, wires_str = FILE.strip().split('\n\n')

    gates = {gate[:-1]: int(state) for line in gates_str.splitlines() for gate, state in [line.split(' ')]}

    skipped = True
    while skipped:
        skipped = False
        for wire_str in wires_str.splitlines():
            l, op, r, _, out = wire_str.split(' ')

            # there are no loops!
            if out in gates:
                continue # skip
            if l not in gates or r not in gates:
                # retry next loop
                skipped = True
                continue

            lv, rv = gates[l], gates[r]
            res = None
            if op == 'AND':
                res = lv & rv
            elif op == 'XOR':
                res = lv ^ rv
            elif op == 'OR':
                res = lv | rv
            else:
                raise ValueError(f"Invalid op: {op}")

            gates[out] = res

    # todo: resolve references
    # waiting for values on all wires starting with z
    # the wires in this system have the following values

    out_binary = ''
    for gate in sorted(gates.keys(), reverse=True):
        if gate[0] != 'z':
            continue
        out_binary += str(gates[gate])

    output = int(out_binary, 2)

    print(out_binary)
    print(output) # part 1: 57270694330992


if __name__ == '__main__':
    main()
