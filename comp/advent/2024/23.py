import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
U = defaultdict(set)

for l in F:
    a, b = l.split("-")

    U[a].add(b)
    U[b].add(a)

S = 0
for a, b, c in itertools.combinations(U.keys(), 3):
    if a in U[b] & U[c] and b in U[a] & U[c]:
        if a[0] == "t" or b[0] == "t" or c[0] == "t": S += 1
print(S)

def check(points):
    for p in points:
        for p2 in points:
            if p != p2 and p not in U[p2]: return False
    return True

lengths = len(U[next(iter(U.keys()))])

for i in range(lengths - 1, -1, -1):
    for k in U:
        for points in itertools.combinations(U[k], i):
            if check(points):
                print(",".join(sorted([k] + list(points))))
                exit()
