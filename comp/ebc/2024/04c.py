import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
F = [int(l) for l in F]

mi, ma = min(F), max(F)

best = math.inf
for i in range(mi,ma):
    S = 0
    for nail in F:
        if nail > i: S += nail-i
        if nail < i: S += i-nail
    best = min(best,S)
print(best)
