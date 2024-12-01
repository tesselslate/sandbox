import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

a, b = [], []
for l in F:
    xs = ul.ints(l)
    a.append(xs[0])
    b.append(xs[1])

S = 0
for x, y in zip(sorted(a), sorted(b)):
    S += abs(x - y)
print(S)

D = defaultdict(int)
for x in b:
    D[x] += 1

S = 0
for x in a:
    S += x * D[x]

print(S)
