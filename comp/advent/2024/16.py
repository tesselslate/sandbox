import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

dir = (0, 1)
start, end = None, None
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "S": start = (r,c)
    if G[r][c] == "E": end = (r,c)

P = set()
Q = ul.pq([(0, start, dir, [start])])
V = defaultdict(lambda: math.inf)
while len(Q):
    dist, pos, dir, path = Q.pop()

    if V[(pos, dir)] < dist: continue
    V[(pos, dir)] = dist

    r, c = pos
    if pos == end:
        V[pos] = dist
        P |= set(path)
        continue

    for (rr, cc) in ul.padj4():
        cost = 1 if (rr, cc) == dir else 1001
        nr, nc = r+rr, c+cc

        if G[nr][nc] != "#":
            Q.push((dist + cost, (nr,nc), (rr,cc), path + [(nr, nc)]))

print(V[end])
print(len(P))
