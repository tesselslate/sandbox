import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

S = 0
for l in F:
    i = int(l)
    S += (i // 3) - 2
print(S)

S = 0
for l in F:
    i = int(l)
    v = (i // 3) - 2
    while v > 0:
        S += v
        v = (v // 3) - 2
print(S)
