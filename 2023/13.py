import functools, math, re, string, sys, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

if len(sys.argv) > 1:
    F = open(sys.argv[1])
else:
    F = sys.stdin.readlines()

F = [l.strip() for l in F]
while F[-1] == "":
    del F[-1]
F = ul.double_linefeed(F)
G = [ul.grid(g) for g in F]

S = 0

def check(g, r):
    n = min(r, len(g)-r)
    a = g[r-n:r]
    b = g[r:r+n]
    assert len(a) == len(b)
    assert len(a[0]) == len(b[0])
    b.reverse()
    return a == b

V = []
for g in G:
    for i in range(1,len(g)):
        if check(g, i):
            S += i * 100
            V.append((i,"v"))
            break
    else:
        for i in range(1,len(g[0])):
            if check(ul.transpose(g), i):
                S += i
                V.append((i,"h"))
                break
        else:
            assert False
print(S)

S = 0
for (g, valid) in zip(G, V):
    for (r,c) in ul.gridpoints(g):
        g[r][c] = "." if g[r][c] == "#" else "#"
        v = []
        for i in range(1, len(g)):
            if check(g, i):
                v.append((i,"v"))
        for i in range(1,len(g[0])):
            if check(ul.transpose(g), i):
                v.append((i,"h"))
        go = False
        g[r][c] = "." if g[r][c] == "#" else "#"
        if len(v):
            v = [x for x in v if x != valid]
            if len(v) == 1:
                v = v[0]
                S += v[0] * (1 if v[1] == "h" else 100)
                go = True
        if go: break
    else: assert False
print(S)
