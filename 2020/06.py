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
F = ul.double_linefeed(F)

S = 0
S2 = 0

for l in F:
    s = set()
    xs = []
    for x in l:
        s = s | set(x)
        xs += [set(x)]
    S += len(s)
    S2 += len(set.intersection(*xs))
print(S)
print(S2)
