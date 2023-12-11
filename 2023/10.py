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
G = ul.grid(F)

sr, sc = 0, 0
D = defaultdict(dict)
valid = {
    (1,0): "LJ|S",
    (-1,0): "F7|S",
    (0,1): "-7JS",
    (0,-1): "-FLS",
}
adj = {
    "-": [(0,1),(0,-1)],
    "|": [(1,0),(-1,0)],
    "F": [(1,0),(0,1)],
    "J": [(-1,0),(0,-1)],
    "7": [(1,0),(0,-1)],
    "L": [(-1,0),(0,1)],
    "S": [],
}
for (r, c) in ul.gridpoints(G):
    if G[r][c] == "S":
        sr = r
        sc = c
    if G[r][c] == ".": continue
    for (rr, cc) in adj[G[r][c]]:
        xr, xc = rr, cc
        rr += r
        cc += c
        if not ul.gridcheck(G,rr,cc):
            continue
        if G[rr][cc] in valid[(xr,xc)]:
            D[(r,c)][(rr,cc)] = True
        if G[rr][cc] == "S":
            D[(rr,cc)][(r,c)] = True
for k, v in adj.items():
    v1 = list([(k[0]-sr,k[1]-sc) for k in D[(sr,sc)].keys()])
    v1.sort()
    v2 = list(v)
    v2.sort()
    if v1 == v2:
        G[sr][sc] = k

M = 0
Q = deque([(sr, sc, 0)])
V = {}
while len(Q):
    E = Q.popleft()
    k = (E[0], E[1])
    if k in V and V[k] < E[2]:
        continue
    V[k] = E[2]
    (r, c, dist) = E
    if dist > M:
        M = dist
    for k in D[k].keys():
        Q.append((*k, dist+1))
print(M)

S = 0
for (r, c) in ul.gridpoints(G):
    if (r,c) in V:
        continue
    s = len([x for (i, x) in enumerate(G[r][:c]) if (r,i) in V and x in "|LJ"])
    if s % 2 == 1: S += 1
print(S)
