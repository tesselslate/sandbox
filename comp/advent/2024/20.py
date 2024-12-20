import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

start,end=None,None
for (r,c) in ul.gridpoints(G):
    if G[r][c]=="S":start=(r,c)
    if G[r][c]=="E":end=(r,c)

Q = deque([(start,0)])
V = defaultdict(lambda: math.inf)
V[start] = 0

mt = 0
while len(Q):
    pos,time = Q.popleft()

    if pos == end: mt = time; break

    r,c=pos
    for (rr,cc) in ul.padj4():
        nr,nc = r+rr,c+cc

        if G[nr][nc] != "#":
            if V[nr,nc] < math.inf: continue
            V[nr,nc]=time+1
            Q.append(((nr,nc),time+1))

adj = {}
Q = deque([((0,0),0)])
while len(Q):
    pos, time = Q.popleft()
    if time == 20: continue
    r,c=pos
    for (rr,cc) in ul.padj4():
        nr,nc=r+rr,c+cc
        if (nr,nc) in adj: continue
        adj[nr,nc] = time
        Q.append(((nr,nc),time+1))

print(len(adj))

S = 0
C = Counter()
for pos, time in V.items():
    r,c = pos
    for (rr,cc) in adj:
        nr,nc = r+rr,c+cc
        if not (nr,nc) in V: continue
        td = V[nr,nc] - time - adj[rr,cc]
        if td > 100: C[td] += 1

for k in sorted(C.keys()):
    print(k, C[k])
print(sum(C.values()))

#test:285
# not 1238075
