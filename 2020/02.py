import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]

S = 0
for l in F:
    a, b, c, d = util.scan("%d-%d %s: %s", l)
    n = 0
    for char in d:
        if char == c:
            n += 1

    if a <= n <= b:
        S += 1
print(S)

S = 0
for l in F:
    a, b, c, d = util.scan("%d-%d %s: %s", l)
    n = 0
    if d[a-1] == c:
        n += 1
    if d[b-1] == c:
        n += 1
    if n == 1: S+=1

print(S)
