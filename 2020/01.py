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
F = [int(l) for l in F]

for p in itertools.combinations(F, 2):
    if p[0] + p[1] == 2020:
        print(p[0] * p[1])
        break

for p in itertools.combinations(F, 3):
    if p[0] + p[1] + p[2] == 2020:
        print(p[0] * p[1] * p[2])
        break
