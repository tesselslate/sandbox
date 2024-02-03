import ul
from collections import deque

F = ul.input()
G = ul.grid(F)

sr, sc = 0, 1
er, ec = len(G)-1,len(G[0])-2

# calculate "points of interest" (intersections, exits) accessible from a given point
# do not cross any intersections
def poi(sr, sc, climb):
    P = {}
    Q = deque([(sr,sc,0)])
    V = set((sr,sc))
    while len(Q):
        (r,c,d) = Q.popleft()
        n, nq = 0, []

        for rr, cc in ul.padj4():
            xr, xc = rr, cc
            rr, cc = r+rr, c+cc
            if not ul.gridcheck(G,rr,cc):
                P[r,c] = d # exit
                continue
            if G[rr][cc] != "#":
                n += 1
                if (rr,cc) not in V:
                    if climb or G[rr][cc] == ".":
                        nq.append((rr,cc))
                    else:
                        match G[rr][cc]:
                            case "<" if xc == -1: nq.append((rr, cc))
                            case ">" if xc == 1: nq.append((rr, cc))
                            case "v" if xr == 1: nq.append((rr, cc))
                            case "^" if xr == -1: nq.append((rr, cc))
        if n > 2: P[r,c] = d
        if n <= 2 or (r,c) == (sr,sc):
            Q.extend((*p, d+1) for p in nq)
            V |= {p for p in nq}
    return P

# recursively calculate all POI for each intersection
def poi_all(sr, sc, climb):
    P = {}
    Q = deque([(sr,sc)])
    while len(Q):
        (xr, xc) = Q.popleft()
        P[xr,xc] = poi(xr, xc, climb)
        for next in P[xr,xc]:
            if next not in P:
                P[next] = {}
                Q.append(next)
    return P

def dfs(p, d, V):
    M = 0
    if p == (er, ec): return d
    for (r,c) in P[p]:
        if (r,c) not in V:
            M = max(M, dfs((r,c), d+P[p][r,c], V|{(r,c)}))
    return M

for climb in [False, True]:
    P = poi_all(sr, sc, climb)
    print(dfs((sr, sc), 0, {(sr, sc)}))
