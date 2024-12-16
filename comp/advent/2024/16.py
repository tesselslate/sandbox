import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

start = None
end = None
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "S":
        start = (r,c)
    elif G[r][c] == "E":
        end = (r,c)

def mkpath(pos):
    return [pos]

print(start,end)
import heapq
dir = (0, 1)
Q = [(0, start, dir, mkpath(dir))]
V = defaultdict(lambda: 10**9)
VV = list()
while len(Q):
    dist, pos, dir, path = heapq.heappop(Q)
    if V[(pos,dir)] < dist: continue
    V[(pos,dir)] = dist
    r, c = pos

    if pos == end:
        print(dist)
        VV.append(path)

    for (rr,cc) in ul.padj4():
        #if rr == -dir[0] or cc == -dir[1]: continue
        cost = 0 if (rr,cc) == dir else 1000
        nr, nc = r+rr, c+cc

        if G[nr][nc] == "." or G[nr][nc] == "E":
            heapq.heappush(Q, (dist+cost+1,(nr,nc),(rr,cc), path + mkpath((nr,nc))))

vs = set()
for path in VV:
    for (r,c) in path: vs.add((r,c))
print(len(vs))
