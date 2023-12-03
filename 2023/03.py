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
G = ul.grid(F)

S = 0

GUID = 0
v = dict()
for r in range(len(G)):
    acc = ""
    adj = False
    s = set()
    for c in range(len(G[0])):
        if G[r][c].isdigit():
            for slot in ul.padj8():
                r2, c2 = slot
                r2 += r
                c2 += c
                if r2 >= 0 and r2 < len(G) and c2 >= 0 and c2 < len(G[0]):
                    if G[r2][c2] not in "1234567890.":
                        adj = True
            acc += G[r][c]
            s.add((r,c))
        else:
            if len(acc) > 0 and adj:
                S += int(acc)
                for el in s:
                    assert el not in v
                    v[el] = (int(acc), GUID)
                s.clear()
            adj = False
            acc = ""
            GUID += 1
    if len(acc) > 0 and adj:
        S += int(acc)
        for el in s:
            assert el not in v
            v[el] = (int(acc), GUID)
        s.clear()
    adj = False
    acc = ""
print(S)

S = 0
for r in range(len(G)):
    for c in range(len(G[0])):
        if G[r][c] == "*":
            e = []
            s = set()
            for slot in ul.padj8():
                r2, c2 = slot
                x = (r + r2, c + c2)
                if x[0] >= 0 and x[0] < len(G) and x[1] >= 0 and x[1] < len(G[0]):
                    if x in v and v[x][1] not in s:
                        e.append(v[x][0])
                        s.add(v[x][1])
            if len(e) == 2:
                S += e[0] * e[1]
print(S)
