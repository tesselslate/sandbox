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
    PN = 0

    for (r, c) in P:
        visited_from = P[(r,c)]

        for entry_dir in visited_from:
            if (r, c, entry_dir) in PV: continue

            rr, cc = ul.pcw(*entry_dir)
            nr, nc = r, c

            PV.add((nr, nc, entry_dir))

            while (nr, nc) in P and entry_dir in P[(nr,nc)]:
                nr += rr
                nc += cc
                PV.add((nr, nc, entry_dir))

            nr -= rr
            nc -= cc

            while (nr, nc) in P and entry_dir in P[(nr,nc)]:
                nr -= rr
                nc -= cc
                PV.add((nr, nc, entry_dir))

            PN += 1

    S2 += len(V) * PN

print(S1)
print(S2)
