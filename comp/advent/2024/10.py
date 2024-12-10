import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F, int)

S = 0
for (r,c) in ul.gridpoints(G):
    if G[r][c] != 0: continue
    Q = deque([(r,c)])
    V = {(r,c)}
    while len(Q):
        r, c = Q.popleft()
        if G[r][c] == 9: S += 1; continue
        for (rr,cc) in ul.padj4():
            np = (r+rr, c+cc)
            if ul.gridcheck(G, r+rr, c+cc) and G[r+rr][c+cc] == G[r][c] + 1 and np not in V:
                Q.append(np)
                V.add(np)

print(S)

S = 0
for (r,c) in ul.gridpoints(G):
    if G[r][c] != 0: continue
    Q = deque([(r,c,0)])
    while len(Q):
        r, c, d = Q.popleft()
        if d > 9: continue
        if G[r][c] == 9: S += 1; continue
        for (rr,cc) in ul.padj4():
            np = (r+rr, c+cc, d+1)
            if ul.gridcheck(G, r+rr, c+cc) and G[r+rr][c+cc] == G[r][c] + 1:
                Q.append(np)
print(S)
