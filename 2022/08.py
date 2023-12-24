import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F, int)

S = 0
M = 0
for (r,c) in ul.gridpoints(G):
    good = False
    dist = []
    for dir in ul.padj4():
        rr = r
        cc = c
        for i in itertools.count():
            rr += dir[0]
            cc += dir[1]
            if not ul.gridcheck(G,rr,cc):
                good = True
                dist.append(i)
                break
            if G[rr][cc] >= G[r][c]:
                dist.append(i+1)
                break
    if good:
        S += 1
    v = math.prod(dist)
    if v > M: M = v
print(S)
print(M)
