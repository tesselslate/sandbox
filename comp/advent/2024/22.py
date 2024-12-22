import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

def shash(x):
    def pmix(x, y):
        return (x ^ y) % 16777216

    x = pmix(x << 6, x)
    x = pmix(x >> 5, x)
    x = pmix(x << 11, x)
    return x

prices, pdiffs = [], []
for l in F:
    n = int(l)

    p = []
    for i in range(2000):
        n = shash(n)
        p.append(n)

    pd = [(b%10) - (a%10) for a, b in itertools.pairwise(p)]
    prices.append(p)
    pdiffs.append(pd)

C = Counter()
for p, pd in zip(prices, pdiffs):
    seen = set()
    for i in range(len(pd)-4):
        diffset = tuple(pd[i:i+4])
        if diffset not in seen:
            C[diffset] += p[i+4] % 10
            seen.add(diffset)

print(sum(xs[-1] for xs in prices))
print(max(C.values()))
