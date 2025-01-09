#! /usr/bin/env python3

PRUNE = 16777216

def prng(secret):
    secret = ((secret * 64) ^ secret) % PRUNE
    secret = ((secret // 32) ^ secret) % PRUNE
    secret = ((secret * 2048) ^ secret) % PRUNE
    return secret

def main(input):
    # initial 'secrets'
    secrets = [int(x) for x in input.strip().splitlines()]

    total = 0
    for secret in secrets:
        for _ in range(2000):
            secret = prng(secret)
        total += secret

    print(total) # part 1: 20506453102

if __name__ == '__main__':
    with open('input.txt', 'r', encoding='ascii') as f:
        file = f.read()

    main(file)
