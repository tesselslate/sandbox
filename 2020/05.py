import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
a = [i for i in range(128)]
b = [i for i in range(8)]

S = set()
M = 0
for l in F:
    x = l[:7]
    y = l[7:]

    z = a
    for c in x:
        if c == "F":
            z = z[:(len(z)//2)]
        else:
            z = z[len(z)//2:]

    assert len(z) == 1
    i = z[0]

    z = b
    for c in y:
        if c == "L":
            z = z[:(len(z)//2)]
        else:
            z = z[len(z)//2:]

    assert len(z) == 1
    j = z[0]

    v = (i * 8 + j)
    if v > M:
        M = v
    S.add(v)
print(M)

for i in range(1024):
    if i not in S:
        print(i)
