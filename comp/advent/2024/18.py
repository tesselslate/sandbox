import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

OF = ul.input()
S = 0

F = OF[:1024]

P = set()
start = (0,0)
end = (70,70)

for l in F:
    x, y = ul.ints(l)
    P.add((x,y))

def path(P):
    Q = deque([(start, 0)])
    V = set()
    while len(Q):
        pos, cost = Q.popleft()
        x,y = pos

        if pos == end:
            return cost

        for (dx, dy) in ul.padj4():
            nx, ny = x+dx, y+dy

            if (nx,ny) not in P and (nx,ny) not in V and 0 <= nx <= 70 and 0 <= ny <= 70:
                V.add((nx,ny))
                Q.append(((nx,ny),cost+1))

for l in OF[1024:]:
    r,c = ul.ints(l)
    if (r,c) in P: continue
    P.add((r,c))
    if path(P) == None: print((r,c)); exit()
