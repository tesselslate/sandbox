import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()[0]
F = [int(x) for x in F.split()]

def blink(stones):
    new = Counter()

    for k, v in stones.items():
        if k == 0:
            new[1] += v
        elif len(str(k)) % 2 == 0:
            a, b = ul.halves(str(k))
            a, b = int(a), int(b)
            new[a] += v
            new[b] += v
        else:
            new[k * 2024] += v

    return new

F = Counter(F)
for i in range(75):
    F = blink(F)

    if i == 24 or i == 74:
        print(sum(F.values()))
