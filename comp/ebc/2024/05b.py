import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)
G = [deque([int(x+y) for x, y in zip(ul.gcol(G, i), ul.gcol(G,i+1))]) for i in [0,2,4,6]]

print(G)
def do_round(col):
    x = G[col].popleft()
    ncol = (col+1)%4

    if x > len(G[ncol]):
        G[ncol].insert(len(G[ncol])-(x%len(G[ncol])),x)
    else:
        G[ncol].insert(x-1,x)

    return int("".join(str(c[0]) for c in G))

C = Counter()
for i in range(10000000):
    n = do_round(i%4)
    C[n] += 1
    if C[n] == 2024: print(n, i, n*(i+1)); exit()
