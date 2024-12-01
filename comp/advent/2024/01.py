import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

a, b = [], []
for l in F:
    xs = ul.ints(l)
    a.append(xs[0])
    b.append(xs[1])

C = Counter()
for x in b:
    C[x] += 1

print(sum([abs(a-b) for (a, b) in zip(sorted(a), sorted(b))]))
print(sum([x * C[x] for x in a]))
