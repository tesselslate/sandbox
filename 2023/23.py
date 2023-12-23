import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

sr, sc = 0, 1
er, ec = len(G)-1,len(G[0])-2

X = defaultdict(dict)
def intersections(xr,xc):
    V = set((xr,xc))
    Q = deque([(xr,xc,0)])
    while len(Q):
        (r,c,d) = Q.popleft()
        n = 0
        nq = []
        for rr, cc in ul.padj4():
            rr, cc = rr+r, cc+c
            if not ul.gridcheck(G,rr,cc): X[xr,xc][r,c] = d; continue
            if G[rr][cc] != "#":
                n += 1
                if (rr,cc) in V: continue
                nq.append((rr,cc,d+1))
        if n > 2: X[xr,xc][r,c] = d
        if n <= 2 or (r,c) == (xr,xc):
            Q.extend(nq)
            V |= set(x[:2] for x in nq)
    if (xr,xc) in X[xr,xc]: del X[xr,xc][xr,xc]

I = set()
QQ = deque([(0,1)])

while len(QQ):
    (r,c) = QQ.popleft()
    if (r,c) in I: continue
    I.add((r,c))
    intersections(r,c)
    for (r,c) in X[r,c]: QQ.append((r,c))
print(X)

N = []
def recurse(r,c,d,V):
    if (r,c) == (er,ec): print(d); N.append(d)
    for (rr, cc) in X[r,c]:
        if (rr,cc) not in V:
            recurse(rr,cc,d+X[r,c][rr,cc],V|{(rr,cc)})
recurse(sr,sc,0,set((sr,sc)))
print("sol:",max(N))
