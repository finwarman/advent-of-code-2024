#! /usr/bin/env python3

PRUNE = 16777216

def prng(secret):
    secret = ((secret * 64) ^ secret) % PRUNE
    secret = ((secret // 32) ^ secret) % PRUNE
    secret = ((secret * 2048) ^ secret) % PRUNE
    return secret

def main(input, iters=2000):
    # initial 'secrets'
    secrets = [int(x) for x in input.strip().splitlines()]

    sequences_starters = {
        # (0, -1, 2, 3): set(0, 1, 2)
    }
    starter_seq_prices = {
        # (seq, start): price
    }

    total = 0
    for s, secret in enumerate(secrets):
        diffs = []
        price = secret % 10 # last digit
        for i in range(iters):
            secret = prng(secret)
            new_price = secret % 10
            diff = new_price - price
            diffs.append(diff)
            if i > 3:
                seq = tuple(diffs[i-4:i])

                if seq not in sequences_starters:
                    sequences_starters[seq] = set()
                sequences_starters[seq].add(s)

                if (seq, s) not in starter_seq_prices:
                    starter_seq_prices[(seq, s)] = price # first only


            # print(secret, new_price, diff)
            price = new_price
        # print()
        total += secret
        # print()

    # print(starter_sequences)
    # print(price_sequences)

    best_total = 0
    best_seq = None
    for seq in sequences_starters:
        # print(seq)
        total = 0
        for s, secret in enumerate(secrets):
            if (seq, s) in starter_seq_prices:
                p = starter_seq_prices[(seq, s)]
                # print(s, secrets[s], seq, p)
                total += p

        if total > best_total:
            # print(seq)
            # print(total)
            best_total = total
            best_seq = seq

    print(f"{best_seq}: total = {best_total}")

    # print(starter_seq_prices)

    # part 2: 2423

if __name__ == '__main__':
    with open('input.txt', 'r', encoding='ascii') as f:
        file = f.read()

#     file = '''
# 1
# 2
# 3
# 2024
#     '''

    # file = '''
    # 123'''

    # main(file, iters=10)
    main(file, iters=2000)
