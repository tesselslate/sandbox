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
for l in F:
    a, b, c, d = ul.scan("%d-%d %s: %s", l)
    n = 0
    for ch in d:
        if ch == c:
            n += 1
    if a <= n <= b:
        S += 1
print(S)

S = 0
for l in F:
    a, b, c, d = ul.scan("%d-%d %s: %s", l)
    n = 0
    if d[a-1] == c: n += 1
    if d[b-1] == c: n += 1
    if n == 1:
        S += 1
print(S)
