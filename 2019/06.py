import collections, itertools, math, string, util
from dataclasses import dataclass
from functools import cache
from sys import argv

F = [l.strip() for l in open(argv[1])]
G = dict()
R = dict()

for l in F:
    a, b = l.split(')')
    if a not in G:
        G[a] = dict()
    G[a][b] = True

    if b not in R:
        R[b] = dict()
    R[b][a] = True

N = 0
def recurse(d, depth):
    global N
    for k, v in d.items():
        if k in G:
            recurse(G[k], depth+1)
        N += 1

for k in G.keys():
    recurse(G[k], 0)
print(N)

V = {}
S = {"YOU"}
Q = collections.deque([("YOU", -1)])
while len(Q) > 0:
    E = Q.popleft()
    V[E[0]] = E[1]
    if E[0] in R:
        for c in R[E[0]]:
            if c not in S:
                S.add(c)
                Q.append((c, E[1]+1))
    if E[0] in G:
        for c in G[E[0]]:
            if c not in S:
                S.add(c)
                Q.append((c, E[1]+1))
print(V["SAN"]-1)
