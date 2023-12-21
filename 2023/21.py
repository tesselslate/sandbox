import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

sr, sc = 0,0
for (r,c) in ul.gridpoints(G):
    if G[r][c] == 'S': (sr,sc)=(r,c)
print(sr,sc)

N = 6 if len(G) < 20 else 64
Q = deque([(sr,sc,0)])
V = defaultdict(set)
V[0].add((sr,sc))
while len(Q):
    (r,c,d) = Q.popleft()
    for (rr, cc) in ul.padj4():
        rr, cc = rr+r, cc+c
        if not ul.gridcheck(G,rr,cc) or G[rr][cc] == "#": continue
        if (rr,cc) in V[d]: continue
        V[d].add((rr,cc))
        if d < N: Q.append((rr,cc,d+1))
print(len(V[N-1]))

N = 26501365
