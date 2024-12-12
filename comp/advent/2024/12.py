import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

S1, S2 = 0, 0
VV = set()

for (r,c) in ul.gridpoints(G):
    if (r,c) in VV: continue

    V = set([(r,c)])
    Q = deque([(r,c)])
    P = defaultdict(set)
    ID = G[r][c]

    while len(Q):
        r, c = Q.popleft()
        for (rr,cc) in ul.padj4():
            nr = r + rr
            nc = c + cc

            # perimeter
            if not ul.gridcheck(G, nr, nc) or G[nr][nc] != ID:
                P[(nr,nc)].add((rr,cc))

            # fill
            if ul.gridcheck(G, nr, nc) and G[nr][nc] == ID:
                if (nr, nc) not in V:
                    V.add((nr,nc))
                    Q.append((nr,nc))

    VV = VV.union(V)
    S1 += len(V) * sum(len(x) for x in P.values())

    PV = set()
    P2 = 0

    for (dr, dc) in ul.padj4():
        for (r, c) in P:
            if (r, c, dr, dc) in PV: continue
            if (dr, dc) not in P[(r,c)]: continue

            Q = deque([(r,c)])
            PV.add((r, c, dr, dc))
            while len(Q):
                r, c = Q.popleft()
                for (rr, cc) in ul.padj4():
                    nr, nc = r + rr, c + cc
                    if (nr, nc) in P and (dr, dc) in P[(nr, nc)] and (nr, nc, dr, dc) not in PV:
                        PV.add((nr, nc, dr, dc))
                        Q.append((nr, nc))
            P2 += 1

    S2 += len(V) * P2

print(S1)
print(S2)
