import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, OrderedDict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()

F = [l.strip() for l in F]
while F[-1] == "":
    del F[-1]

G = ul.grid(F)
GG = defaultdict(list)

S = 0
for (r,c) in ul.gridpoints(G):
    if ul.gridcheck(G,r,c-1) and G[r][c].isdigit() and G[r][c-1].isdigit():
        continue

    acc = ""
    gears = set()
    sym = False
    while ul.gridcheck(G,r,c) and G[r][c].isdigit():
        for (rr,cc) in ul.padj8():
            rr += r
            cc += c
            if ul.gridcheck(G,rr,cc):
                if G[rr][cc] not in "1234567890.":
                    sym = True
                if G[rr][cc] == "*":
                    gears.add((rr,cc))
        acc += G[r][c]
        c += 1
    if sym:
        S += int(acc)
    for gear in gears:
        GG[gear].append(int(acc))
print(S)

S = 0
for gear in GG.values():
    if len(gear) == 2: S += math.prod(gear)
print(S)
