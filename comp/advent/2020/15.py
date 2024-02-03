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

F = [int(x) for x in F[0].split(',')]
S = 0

V = defaultdict(list)
l = 0
for i in range(30000000):
    if i < len(F):
        l = F[i]
    else:
        if len(V[l]) < 2:
            l = 0
        else:
            l = V[l][1] - V[l][0]
    V[l].append(i)
    if len(V[l]) > 2:
        del V[l][0]
        assert len(V[l]) == 2
    if i == 2019:
        print(l)
print(l)
