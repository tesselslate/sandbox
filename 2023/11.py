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

RR = set()
CC = set()

for r in range(len(G)):
    x = set(G[r])
    if x == {"."}:
        RR.add(r)
for c in range(len(G)):
    s = set()
    for r in range(len(G)):
        s.add(G[r][c])
    if s == {"."}:
        CC.add(c)

galaxies = []
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "#": galaxies.append((r,c))

def find(mult):
    S = 0
    for g in galaxies:
        Q = deque([(*g, 0)])
        V = {}
        vv = set()
        while len(Q):
            E = Q.popleft()
            (r, c, dist) = E
            if (r,c) in vv: continue
            vv.add((r,c))
            if G[r][c] == "#": V[(r,c)] = dist
            for rr, cc in ul.padj4():
                rr += r
                cc += c
                if ul.gridcheck(G,rr,cc):
                    d = dist
                    if rr in RR and rr != r: d += mult - 1
                    if cc in CC and cc != c: d += mult - 1
                    Q.append((rr,cc,d+1))
        S += sum(V.values())
    return S // 2
print(find(2))
print(find(1000000))
