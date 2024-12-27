import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F, lambda x: 0)
G = {(r,c): 0 for (r,c) in ul.gridpoints(G) if F[r][c] == "#"}

S = 0
for i in range(1000):
    V = set()

    for (r,c) in G:
        for (rr,cc) in ul.padj4():
            if (r+rr,c+cc) not in G:
                if i != 0: break
                else: continue
            if G[r+rr,c+cc] != G[r,c]: break
        else:
            V.add((r,c))

    if not V: break
    for (r,c) in V: G[r,c] += 1
    S += len(V)
    print(i,len(V))
print(G)
print(S)
