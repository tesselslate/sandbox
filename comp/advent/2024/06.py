import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

S = None
for (r,c) in ul.gridpoints(G):
    if G[r][c] == "^":
        S = (r,c)
        break
else: exit()

def search(O):
    V = defaultdict(list)
    P = S
    D = (-1, 0)
    while True:
        if D in V[P]: return V, True
        V[P].append(D)

        NP = (P[0] + D[0], P[1] + D[1])
        if not ul.gridcheck(G, *NP): return V, False
        if NP == O or G[NP[0]][NP[1]] == "#":
            D = ul.pcw(*D)
        else:
            P = NP

V = search(None)[0]
print(len(V))
print(sum(search(x)[1] for x in V if x != S))
