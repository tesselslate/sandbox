import math, ul
from collections import defaultdict

F = ul.input()
G = ul.grid(F, int)

dirs = ul.dirs_rc("NESW")

def mincost(mi, ma):
    Q = ul.pq([(0, 0, 0, d, 0) for d in ((0,1),(1,0))])
    V = set()
    M = defaultdict(lambda: math.inf)

    while len(Q):
        (cost, r, c, dir, n) = Q.pop()
        if (r, c, dir, n) in V: continue
        V.add((r, c, dir, n))
        if (r, c) == (len(G)-1, len(G[0])-1) and n >= mi:
            return cost

        di = dirs.index(dir)
        dd = [dir] if n < ma else []
        if n >= mi: dd += [dirs[di-1], dirs[(di+1)%4]]
        for d in dd:
            rr, cc = r + d[0], c + d[1]
            if not ul.gridcheck(G, rr, cc): continue
            nc = cost + G[rr][cc]
            nd = n+1 if d == dir else 1
            if nc < M[rr, cc, d, nd]:
                M[rr, cc, d, nd] = nc
                Q.push((nc, rr, cc, d, nd))
print(mincost(1,3))
print(mincost(4,10))
