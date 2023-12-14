import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

S = 0
for l in F:
    a, b = ul.halves(l)
    x = "".join(set(a) & set(b))
    S += string.ascii_letters.index(x) + 1
print(S)

S = 0
for (x, y, z) in ul.batched(F, 3):
    x = "".join(set(x) & set(y) & set(z))
    S += string.ascii_letters.index(x) + 1
print(S)
