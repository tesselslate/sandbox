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

S = 0

for i in range(25, len(F)):
    xs = F[i-25:i]
    assert len(xs) == 25
    found = False
    for ps in itertools.combinations(xs, 2):
        if ps[0] + ps[1] == F[i]:
            found = True
            break
    if not found:
        print(F[i])
        break

inv = 3199139634
for i in range(2, len(F)):
    for j in range(0, len(F) - i):
        if sum(F[j:j+i]) == inv:
            x = F[j:j+i]
            print(x, min(x), max(x), min(x) + max(x))
            exit()
