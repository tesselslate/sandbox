import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()
    if not F[-1].strip():
        del F[-1]

F = [l.strip() for l in F]

S = 0
V = set()

for l in F:
    x, y = l[:7], l[7:]
    a, b = list(range(128)), list(range(8))
    for i in x:
        if i == "F":
            a, _ = ul.halves(a)
        else:
            _, a = ul.halves(a)
    for i in y:
        if i == "R":
            _, b = ul.halves(b)
        else:
            b, _ = ul.halves(b)
    assert len(a) == len(b) == 1

    v = a[0] * 8 + b[0]
    if v > S:
        S = v
    V.add(v)
print(S)

for i in range(1024):
    if i not in V and i-1 in V and i+1 in V:
        print(i)
        break
