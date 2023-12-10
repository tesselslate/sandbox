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
G3 = ul.grid(F)

S = 0
M = 0

sr, sc = 0, 0
D = defaultdict(dict)
valid = {
    (1,0): ["L", "J", "|", "S"],
    (-1,0): ["F", "7", "|", "S"],
    (0,1): ["-", "7", "J", "S"],
    (0,-1): ["-", "F", "L", "S"],
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
print(sr, sc)

M = 0
Q = deque([(sr, sc, 0)])
MIN = {}
VL = set()
while len(Q):
    E = Q.popleft()
    k = (E[0], E[1])
    assert G[E[0]][E[1]] != "."
    if k in MIN and MIN[k] < E[2]:
        continue
    MIN[k] = E[2]
    (r, c, dist) = E
    VL.add((r,c))
    if dist > M:
        M = dist
    for k2 in D[k].keys():
        Q.append((k2[0], k2[1], dist+1))
print(M)

G[sr][sc] = "L"
X = [[0 for _ in range(len(G) * 3)] for _ in range(len(G) * 3)]
for (r, c) in ul.gridpoints(G):
    xr = r * 3
    xc = c * 3
    match G[r][c]:
        case "|":
            X[xr][xc+1] = 1
            X[xr+1][xc+1] = 1
            X[xr+2][xc+1] = 1
        case "-":
            X[xr+1][xc] = 1
            X[xr+1][xc+1] = 1
            X[xr+1][xc+2] = 1
        case "7":
            X[xr+1][xc] = 1
            X[xr+1][xc+1] = 1
            X[xr+2][xc+1] = 1
        case "F":
            X[xr+1][xc+1] = 1
            X[xr+1][xc+2] = 1
            X[xr+2][xc+1] = 1
        case "L":
            X[xr][xc+1] = 1
            X[xr+1][xc+1] = 1
            X[xr+1][xc+2] = 1
        case "J":
            X[xr][xc+1] = 1
            X[xr+1][xc+1] = 1
            X[xr+1][xc] = 1
        case _: pass

for (r,c) in ul.gridpoints(X):
    if not (r == 0 or c == 0 or r == len(X) - 1 or c == len(X) - 1): continue
    Q = deque([(r,c)])
    while len(Q):
        (r,c) = Q.popleft()
        if X[r][c] != 0: continue
        X[r][c] = 2
        for (rr,cc) in ul.padj4():
            rr += r
            cc += c
            if ul.gridcheck(X,rr,cc):
                Q.append((rr,cc))
S = 0
for (r,c) in ul.gridpoints(G):
    if (r,c) in VL: continue
    s = set()
    for i in range(3):
        for j in range(3):
            s.add(X[r*3+i][c*3+j])
    if 2 not in s: S += 1

for r in range(len(X)):
    x = ""
    for c in range(len(X)):
        x += "$#."[X[r][c]]
    print(x)
print(S)
