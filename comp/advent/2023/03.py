import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()
G = ul.grid(F)

symbols = {}
for (r, c) in ul.gridpoints(G):
    ch = G[r][c]
    if not ch.isdigit() and ch != '.':
        symbols[(r,c)] = ch

gears = {(r, c): [] for (r, c) in symbols if symbols[(r, c)] == '*'}

S = 0
for (r, c) in ul.gridpoints(G):
    if ul.gridcheck(G, r, c-1) and G[r][c-1].isdigit(): continue
    if not G[r][c].isdigit(): continue

    acc = ""
    sym = False
    gear = None

    while ul.gridcheck(G, r, c) and G[r][c].isdigit():
        acc += G[r][c]
        for (rr, cc) in ul.padj8():
            if ul.gridcheck(G, r+rr, c+cc) and (r+rr, c+cc) in symbols:
                if G[r+rr][c+cc] == '*':
                    gear = gears[(r+rr, c+cc)]
                sym = True
        c += 1

    if sym:
        S += int(acc)
    if gear is not None:
        gear.append(int(acc))

print(S)
print(sum(math.prod(gear) for gear in gears.values() if len(gear) > 1))
