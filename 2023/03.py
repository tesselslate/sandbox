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

S = 0
for r, c in ul.gridpoints(G):
    if ul.gridcheck(G,r,c-1) and G[r][c-1].isdigit():
        continue
    if G[r][c].isdigit():
        x = list(itertools.takewhile(lambda x: x.isdigit(), G[r][c:]))
        num = int("".join(x))
        def check():
            for C in range(c, c+len(x)):
                for i, j in ul.padj8():
                    if ul.gridcheck(G,r+i,C+j) and G[r+i][C+j] not in "1234567890.":
                        return True
        if check(): S += num
print(S)

S = 0
for a, b in ul.gridpoints(G):
    if G[a][b] != "*": continue
    ns = set()
    for x, y in ul.padj8():
        r,c = a+x, b+y
        if ul.gridcheck(G,r,c) and G[r][c].isdigit():
            while c >= 0 and G[r][c].isdigit():
                c -= 1
            c += 1
            x = list(itertools.takewhile(lambda x: x.isdigit(), G[r][c:]))
            ns.add(int("".join(x)))
    if len(ns) == 2:
        S += math.prod(ns)
print(S)
