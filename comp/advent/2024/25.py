import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.double_linefeed(ul.input())
G = [ul.grid(ll) for ll in F]

S = 0
for a, b in itertools.product(G, repeat=2):
    for (r, c) in ul.gridpoints(a):
        if a[r][c] == b[r][c] == "#": break
    else: S += 1
print(S // 2)
