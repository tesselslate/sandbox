import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)
dirs = [(-1,0),(0,-1),(1,0),(0,1)]

def pgrid():
    for r in G: print("".join(r))
    print("\n")

def find(g):
    v = []
    for (r,c) in ul.gridpoints(g):
        if g[r][c] == "O": v.append((r,c))
    return v

V = []
vv = set()
for j in range(10**9):
    v = set()
    for i, x in enumerate(dirs):
        (rr, cc) = x
        while True:
            n = 0
            for (r, c) in find(G):
                zr, zc = r, c
                r += rr
                c += cc
                it = False
                while ul.gridcheck(G,r,c) and G[r][c] == ".":
                    it = True
                    n += 1
                    r += rr
                    c += cc
                if it:
                    r -= rr
                    c -= cc
                    assert G[r][c] == "."
                    G[r][c] = "O"
                    G[zr][zc] = "."
            if n == 0: break
    v = frozenset(find(G))
    if v in vv:
        V.append(v)
        break
    vv.add(v)
    V.append(v)

def score(v):
    s = 0
    for (r,c) in v:
        s += len(G)-r
    return s

x = V.pop()
scores = [score(V[i]) for i in range(len(V))]
N = 10**9
l = len(scores)
print(scores)

cl = l - V.index(x)
print(cl)
N -= (l-cl)
print(score(V[(l-cl):][N%cl-1]))

# [87, 69, |69, 69, 65, 64, 65, 63, 68]
