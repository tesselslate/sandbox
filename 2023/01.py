import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()

F = [l.strip() for l in F]
while F[-1] == "":
    del F[-1]

S = 0
for l in F:
    v = [int(c) for c in l if c.isdigit()]
    S += v[0] * 10 + v[-1]
print(S)

nums = "one two three four five six seven eight nine".split()
S = 0
for l in F:
    v = []
    for i, c in enumerate(l):
        if c.isdigit(): v.append(int(c))
        for j, nw in enumerate(nums):
            if l[i:].startswith(nw): v.append(j+1)
    S += v[0] * 10 + v[-1]
print(S)
