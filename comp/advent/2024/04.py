import functools, math, re, string, itertools, ul
from dataclasses import dataclass
from collections import Counter, defaultdict, deque

F = ul.input()

def check(G):
    S = 0
    for (r,c) in ul.gridpoints(G):
        for (rr,cc) in ul.padj8():
            for (i, ch) in enumerate("XMAS"):
                R = r + (rr*i)
                C = c + (cc*i)
                if not ul.gridcheck(G, R, C) or G[R][C] != ch: break
            else:
                S += 1
    return S

def check2(G):
    S = defaultdict(int)
    for (r,c) in ul.gridpoints(G):
        for (rr,cc) in [(-1,-1),(1,-1),(1,1),(-1,1)]:
            for (i, ch) in enumerate("MAS"):
                R = r + (rr*i)
                C = c + (cc*i)
                if not ul.gridcheck(G, R, C) or G[R][C] != ch: break
            else:
                S[(r+rr,c+cc)] += 1
    return sum(1 for v in S.values() if v == 2)

print(check(F))
print(check2(F))
