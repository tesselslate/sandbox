import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

S = 0
S2 = 0
for l in F:
    a, b = l.split()
    a = "ABC".index(a)
    b = "XYZ".index(b)

    v = 3
    if (a + 1) % 3 == b: v = 6
    if (a - 1) % 3 == b: v = 0
    S += v + b + 1

    match b:
        case 0: S2 += ((a - 1) % 3) + 1
        case 1: S2 += a + 1 + 3
        case 2: S2 += ((a + 1) % 3) + 1 + 6
print(S)
print(S2)
