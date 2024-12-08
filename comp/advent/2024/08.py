import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

D = defaultdict(list)

for (r,c) in ul.gridpoints(G):
    if G[r][c] != ".": D[G[r][c]].append((r,c))

def run(n1, n2):
    S = set()
    for P in D.values():
        for (a,b) in itertools.permutations(P, 2):
            dx = a[0] - b[0]
            dy = a[1] - b[1]

            for i in range(n1, n2):
                n = (a[0] + dx * i, a[1] + dy * i)
                if ul.gridcheck(G, *n): S.add(n)

    return len(S)

print(run(1, 2))
print(run(0, 100))
